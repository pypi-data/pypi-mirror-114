# Dask
from dask.distributed import Client, progress
import dask

# PDAL and Entwine
from pyproj import CRS, Transformer
from ept.ept import EPT
import pdal

# Scipy
from scipy import stats as sci_stats

# Standard imports
import io
import logging
import argparse
import sys
from pathlib import Path
import numpy as np
import math
import random
from PIL import Image

import subprocess
import json

# Rasterio
import rasterio
import rasterio.features
from rasterio.io import MemoryFile

# Shapely
from shapely.geometry import mapping, Polygon, MultiPolygon, Point
from shapely.wkt import loads
from shapely.ops import transform


# Set up logger for stdout
logger = logging.getLogger(__file__)

formatter = logging.Formatter('[%(levelname)s] %(message)s')
#
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)


logger.addHandler(handler)


class Datasource(EPT):
    def __init__(self, args):
        self.args = args
        super(Datasource, self).__init__(self.args.ept_url)

        self.transformation = Transformer.from_crs(self.info.srs, 4326, always_xy=True)
        self.raster = rasterio.open(self.args.raster_url)

        dtype = np.dtype([('points_std', 'f4'),
                          ('points_med','f4'),
                          ('dem_std', 'f4'),
                          ('dem_med','f4'),
                          ('ks_stat','f4'),
                          ('ks_pvalue','f4')])

        self.stats = np.zeros(self.args.sample_count, dtype = dtype)

    def do(self):

        client = Client(threads_per_worker = self.args.threads,
                        n_workers = self.args.workers)

        self.poly = self.boundary()

        samples = self.samples()

        images = []
        data = []
        count = 0
        sample_data = []
        for sample in samples:
            logger.debug(f'{sample.x},{sample.y}')
            d = dask.delayed((self.get_data)(sample, sample_data))
            data.append(d)


        data = dask.persist(*data)
        count = 0
        for d in data:
            d.compute()
            dem, points = sample_data[count][0], sample_data[count][1]
            if points.size == 0:
                continue
            self.get_stats(dem, points, self.stats[count])

            if self.args.plot:
                img = self.plot(dem, points, self.stats[count])
                images.append(img)
            count = count + 1

        points_med = np.mean(self.stats['points_med'])
        points_std = np.mean(self.stats['points_std'])
        dem_med = np.mean(self.stats['dem_med'])
        dem_std = np.mean(self.stats['dem_std'])
        ks_pvalue = np.mean(self.stats['ks_pvalue'])
        ks_stat = np.mean(self.stats['ks_stat'])
        upper = points_med + self.args.threshold * points_std
        lower = points_med - self.args.threshold * points_std

        didPass = bool( lower <= dem_med <= upper)
        out_stats = {'upper': f'{upper}', 'lower': f'{lower}',
                'didPass': didPass, 'points_med': f'{points_med}',
                'points_std': f'{points_std}', 'dem_med': f'{dem_med}',
                'dem_std': f'{dem_std}', 'ks_pvalue': f'{ks_pvalue}', 'ks_stat' : f'{ks_stat}',
                'n':len(self.stats['dem_med'])}
        sys.stdout.write(json.dumps(out_stats))


        if self.args.plot:
            im = Image.open(images[0]).convert('RGB')
            pils = [Image.open(image).convert('RGB') for image in images[1:]]
            im.save(self.args.plot, "PDF" ,resolution=100.0, save_all=True, append_images=pils)
        return out_stats

    def boundary(self):
        """Compute a PDAL hexbin boundary at a coarse resolution"""
        cargs = ['pdal','info','--all',
                '--driver','readers.ept',
                f'--readers.ept.resolution={self.args.boundary_resolution}',
                f'--readers.ept.threads=6',
                f'--filters.hexbin.edge_size={self.args.edge_size}',
                f'--filters.hexbin.threshold=1',
                self.root_url+'/ept.json']
        logger.debug(" ".join(cargs))
        p = subprocess.Popen(cargs, stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    encoding='utf8')
        ret = p.communicate()
        if p.returncode != 0:
            error = ret[1]
            logger.error(cargs)
            logger.error(error)
            error = {"args":cargs, "error": error}
            raise AttributeError(error)
        self.point_stats = json.loads(ret[0])

        self.wkt = self.point_stats['boundary']['boundary']

        try:
            self.poly = loads(self.wkt)
            if self.poly.type == 'Polygon':
                self.poly = MultiPolygon([self.poly])
        except Exception as E:
            self.error = {"error": str(E)}
            raise (f"failed to convert WKT for {self.key}")

        return self.poly


    def samples(self):
        """Compute sample points within the EPT boundary. If a sample point
        outside the boundary, toss it out"""

        left = self.args.sample_count
        output = []
        while left > 0:
            x, y = random.uniform(self.poly.bounds[0], self.poly.bounds[2]), \
                   random.uniform(self.poly.bounds[1], self.poly.bounds[3])
            p = Point(x, y)
            if self.poly.contains(p):
                output.append(p)
                left = left - 1
        return output


    def get_data(self, point, sample_data):
        """Fetch sample DEM and EPT point data for a sample point"""

        point_buf = point.buffer(self.args.point_buffer)
        lon, lat = self.transformation.transform(point.x, point.y)
        point_dd = transform(self.transformation.transform, point)
        buffer_dd = transform(self.transformation.transform, point_buf)

        bounds = rasterio.features.geometry_window(self.raster, [buffer_dd])
        dem = self.raster.read(window = bounds)

        pipeline = [{
              "type": "readers.ept",
              "filename": self.root_url+'/ept.json',
              "resolution":self.args.ept_resolution,
              "bounds": f"([{point_buf.bounds[0]}, {point_buf.bounds[2]}], [{point_buf.bounds[1]}, {point_buf.bounds[3]}])"

              },{"type":"filters.range","limits":"Classification![7:7]"}]

        logger.debug(f'{pipeline} ')
        p = pdal.Pipeline(json.dumps(pipeline))
        num_points = p.execute()
        logger.debug(f'Fetched {num_points} from EPT')
        if not num_points:
            points = np.array([])
        else:
            points = p.arrays[0]


        sample_data.append((dem, points,))
        return True

    def get_stats(self, dem, points, stats):
        """Compute our moments for DEM and points arrays"""

        points = points['Z']
        dem_std = np.std(dem); dem_med = np.median(dem)

        points_std = np.std(points); points_med = np.median(points)
        stats['points_std'] = points_std
        stats['points_med'] = points_med
        stats['dem_std'] = dem_std
        stats['dem_med'] = dem_med
        ks = sci_stats.kstest(dem.flatten(), points)
        stats['ks_stat'] = ks.statistic
        stats['ks_pvalue'] = ks.pvalue



    def plot(self, dem, points, stats):
        """Make pretty pictures"""

        import matplotlib
        import matplotlib.pyplot as plt
        from matplotlib.colors import ListedColormap, LinearSegmentedColormap
        rng = np.random.default_rng()


        n_bins = 100
        dem_2d = dem[0]

        dem = dem[0].flatten()

        points_sub = points #rng.choice(points, size=len(dem))

        points_x = points['X']
        points_y = points['Y']
        points_z = points['Z']
        points = points['Z']

        fig, axes = plt.subplots(ncols=3, figsize=(11, 8.5), dpi=100)
        ax = axes[0]
        raster_ax = axes[1]
        points_ax = axes[2]
        img_pl = raster_ax.imshow(dem_2d)
        raster_ax.set_yticklabels([])
        raster_ax.set_xticklabels([])

        # https://stackoverflow.com/questions/17682216/scatter-plot-and-color-mapping-in-python
        normalize = matplotlib.colors.Normalize(vmin=np.min(dem), vmax=np.max(dem))
        sc = points_ax.scatter(points_sub['X'], points_sub['Y'], c=points_sub['Z'], norm=normalize, cmap=img_pl.get_cmap(), edgecolors='face', s=0.5)
        points_ax.set_yticklabels([])
        points_ax.set_xticklabels([])
        fig.colorbar(sc, ax=points_ax)


        threshold = 8.0
        n, bins, patches = ax.hist(points, bins=n_bins, range=(np.median(points) - threshold*np.std(points), np.median(points) + threshold*np.std(points)), density=True, histtype='step', cumulative=True, label='Point')
        ax.hist(dem, n_bins, range=(np.median(dem) - threshold*np.std(dem), np.median(dem) + threshold*np.std(dem)), density=True, histtype='step', cumulative=True, facecolor='g', label='NASADEM')


        textstr = '\n'.join((
                r'$\mathrm{median_{points}}=%.2f$' % (stats['points_med'], ),
                r'$\sigma_{points}=%.2f$' % (stats['points_std'], ),
                r'$\mathrm{median_{dem}}=%.2f$' % (stats['dem_med'], ),
                r'$\sigma_{dem}=%.2f$' % (stats['dem_std'], ),
                r'$D_n=%.2f$ p=%.2f' % (stats['ks_stat'], stats['ks_pvalue'] )))

        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

        # place a text box in upper left in axes coords
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
                 verticalalignment='top', bbox=props)
        # tidy up the figure
#        ax.grid(True)
        ax.legend(loc='right')
        ax.set_title(f'NASADEM vs 3DEP \n something')
        ax.set_xlabel('Elevation (m)')
        ax.set_ylabel('Likelihood of occurrence')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf



def get_parser(args):

    import argparse

    parser = argparse.ArgumentParser(description='Accept or reject EPT data as matching against a known benchmark DEM')
    parser.add_argument('raster_url',
                        help='GDAL-readable raster datasource ')
    parser.add_argument('ept_url',
                        help='EPT endpoint')
    parser.add_argument('--sample_count', type=int, default=20,
                        help='Number of samples to check')
    parser.add_argument('--edge_size', type=int, default=1000,
                        help='filters.hexbin edge_size')
    parser.add_argument('--threads', type=int, default=8,
                        help='Dask threads')
    parser.add_argument('--workers', type=int, default=2,
                        help='Dask workers')
    parser.add_argument('--point_buffer', type=float, default=1000.0,
                        help='Sample point buffer')
    parser.add_argument('--threshold', type=float, default=2.0,
                        help='stddev threshold')
    parser.add_argument('--boundary_resolution', type=float, default=150,
                        help='filters.hexbin resolution')
    parser.add_argument('--ept_resolution', type=float, default=25.0,
                        help='filters.hexbin resolution')
    parser.add_argument('--debug',
                        action='store_true',
                        help='print debug messages to stderr')

    parser.add_argument('--plot', default = '',
                                  help='Plot PDF of sample illustrations')

    args = parser.parse_args(args)
    return args
#
def main():
    args = get_parser(sys.argv[1:])
    if args.debug:
        handler.setLevel(logging.DEBUG)
    ds = Datasource(args)
    passed = ds.do()

    if not passed:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())


