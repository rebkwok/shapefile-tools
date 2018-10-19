Some (very) basic shapefile utilities.  Currently requires
shapefiles to be unzipped and located in the same repo as the scripts.

# read_shp.py

```
python read_shp.py <source-dir> -g <index of feature to display>
```

Reads a shapefile and prints information about its CRS, number of features etc,
and a table of properties.

source-dir: an unzipped shapefile folder; assumes that all files in the folder
have the same name as the folder.

-g / --geometry-index: Optional index of a specific feature in the shapefile; prints
the feature's coordinates


# rename_atttibutes.py
```
python rename_attributes.py <source-dir> <destination-dir>
```
Reads a shapefile, makes all the property names title case, adds a new property for
the updated date and writes out the first 1000 features to a new shapefile.

source-dir: an unzipped shapefile folder; assumes that all files in the folder
have the same name as the folder.

destination-dir: directory to write the new shapefile to.


# shppandas.py
```
python shppandas.py <source-dir> <destination-dir>
```
Just an example of how to write a shapefile with geopandas instead of fiona; reads
a shapefile, reprojects it to epsg=3857, writes out to a new shapefile.

