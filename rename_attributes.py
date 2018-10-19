# -*- coding: utf-8 -*-

import datetime
import click
import fiona
import os
from collections import OrderedDict

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

    with fiona.drivers():

        # Open a file for reading. We'll call this the "source."

        with fiona.open('{filename}/{filename}.shp'.format(filename=filename)) as source:
            # Copy the source schema, change the properties
            sink_schema = source.schema.copy()
            props = source.schema['properties']
            # Make all properties title case
            sink_schema['properties'] = OrderedDict((k.title(), v) for k, v in props.viewitems())
            # Add a property for date updated, with type date
            sink_schema['properties']['date_props_updated'] = 'date'

            # Create a sink for processed features with the same format and
            # coordinate reference system as the source.
            with fiona.open(
                '{dest_path}/{dest_path}.shp'.format(dest_path=dest_path),
                'w',
                crs=source.crs,
                driver=source.driver,
                schema=sink_schema,
                ) as sink:

                for i, rec in enumerate(source):
                    # update the properties to match the new schema
                    new_props = OrderedDict((k.title(), v) for k, v in props.viewitems())
                    rec['properties'] = new_props
                    rec['properties'].update(
                        date_props_updated=datetime.datetime.now().isoformat()
                    )

                    if i < 1000:  # write only the first 1000
                        sink.write(rec)
                # The sink file is written to disk and closed when its block ends.


if __name__ == '__main__':
    read_file()
