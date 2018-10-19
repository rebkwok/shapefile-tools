# -*- coding: utf-8 -*-

import click
import fiona
import os
from tabulate import tabulate


@click.command(help="Print information on a provided shapefile")
@click.argument('filepath')
@click.option('--geometry-index', '-g', type=int, help='index of a geometry to print')
def read_file(filepath, geometry_index):
    # Register format drivers with a context manager

    with fiona.drivers():

        print("SHAPEFILE {}".format(os.path.split(filepath)[-1]))
        print("=======================")

        # Open a file for reading. We'll call this the "source."
        with fiona.open(filepath) as source:
            # The file we'll write to, the "sink", must be initialized
            # with a coordinate system, a format driver name, and
            # a record schema.  We can get initial values from the open
            # collection's ``meta`` property and then modify them as
            # desired.
            meta = source.meta
            # Open an output file, using the same format driver and
            # coordinate reference system as the source. The ``meta``
            # mapping fills in the keyword parameters of fiona.open().
            print("Number of features in shapefile: {}".format(len(source)))
            print("CRS: {}".format(meta['crs']))
            print("CRS WKT: {}".format(meta['crs_wkt']))
            print("Driver: {}".format(meta['driver']))
            print("Schema: {}".format(meta['schema']))

            feature_values = []
            holes = 0
            non_polys = 0
            for i, feature in enumerate(source):
                has_hole = 'N'
                if i == 0:
                    headers = list(feature['properties'].keys())
                    headers.append('Geometry Type')
                    headers.append('Has holes(s)')

                feature_row = list(feature['properties'].values())
                feature_row.append(feature['geometry']['type'])

                if feature['geometry']['type'] == 'Polygon':
                    if len(feature['geometry']['coordinates']) > 1:
                        holes += 1
                        has_hole = 'Y'
                elif feature['geometry']['type'] == 'MultiPolygon':
                    for geometry in feature['geometry']['coordinates']:
                        if len(geometry) > 1:
                            holes += 1
                            has_hole = 'Y'
                else:
                    non_polys += 1
                    has_hole = 'N/A'
                feature_row.append(has_hole)
                feature_values.append(feature_row)

            print(tabulate(feature_values, headers=headers, showindex='always'))
            print('Total holey polygons/multipolygons:: {}'.format(str(holes)))
            print('Total non poly/multipoly geometry types: {}'.format(str(non_polys)))

            if geometry_index:
                requested_feature = source[geometry_index]
                if requested_feature is None:
                    print('No feature at index {}'.format(geometry_index))
                else:
                    print("=======================")
                    print("Geometry for feature {}".format(geometry_index))
                    print("=======================")
                    print(requested_feature['geometry']['coordinates'])


if __name__ == '__main__':
    read_file()
