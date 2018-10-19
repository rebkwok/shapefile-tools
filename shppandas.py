import click
import geopandas
import os

@click.command()
@click.argument('filename')
@click.argument('dest_path')
@click.option('--overwrite', '-o', is_flag=True,
              help='Overwrite existing destination folder')
def read_file(filename, dest_path, overwrite):
    # Register format drivers with a context manager

    if os.path.exists(dest_path):
        if not overwrite:
            print(
                'Destination folder already exists, please specify a different '
                'name or -o to overwrite'
            )
            return
    else:
        os.makedirs(dest_path)

    source = geopandas.GeoDataFrame.from_file(
        '{filename}/{filename}.shp'.format(filename=filename)
    )

    reprojected = source.to_crs(epsg=3857)
    reprojected.to_file(
        filename='{dest_path}/{dest_path}.shp'.format(dest_path=dest_path),
        driver="ESRI Shapefile"
    )
    print('New file written to {dest_path}/{dest_path}.shp'.format(dest_path=dest_path))


if __name__ == '__main__':
    read_file()
