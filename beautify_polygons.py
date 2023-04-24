"""
This script
* converts all MultiPolygons into single Polygons,
* removes holes which are smaller than a specified value (in sq. meters),
* removes polygons smaller than a specified size (in sq. meters)
* simplifies polygons based on a given error margin
* removes floating point digits

Run:
python beautify_polygons.py -i "path_in" -o "path_out"
"""
import json
import pyproj
import argparse
import numpy as np
import geopandas as gpd
from functools import partial
from shapely import wkt
from shapely.geometry import Polygon
from shapely.ops import transform


PROJ = partial(pyproj.transform, pyproj.Proj(init='epsg:4326'),  pyproj.Proj(init='epsg:2154'))


def convert_to_single(df):
    rows = []
    for i, row in df.iterrows():
        if row['geometry'].geom_type in ('MultiPoint', 'MultiLineString', 'MultiPolygon'):
            for g in row['geometry']:
                r = row.copy()
                r['geometry'] = g
                rows.append(r)
        else:
            rows.append(row)
    return gpd.GeoDataFrame(rows, index=np.arange(len(rows)))


def remove_null_geometries(df):
    return df.drop(df.index[df.geometry.isna()], axis=0)


def _area(geom):
    return transform(PROJ, geom).area


def _remove_holes(poly, hole):
    interiors = filter(lambda x: _area(Polygon(x)) > hole, list(poly.interiors))
    return Polygon(poly.exterior, interiors)


def remove_holes(df, hole=60):
    for i, row in df[df.geom_type == 'Polygon'].iterrows():
        df.loc[i, 'geometry'] = _remove_holes(row['geometry'], hole)
    return df


def remove_small_polygons(df, thres=10):
    if (df.geom_type == 'Polygon').any():
        polys = df[df.geom_type == 'Polygon']
        drop = polys.index[polys.geometry.apply(lambda x: _area(x)) < thres]
        return df.drop(drop, axis=0)
    else:
        return df


def simplify_polygons(df, thres=0.000005):
    for i, row in df[df.geom_type == 'Polygon'].iterrows():
        df.loc[i, 'geometry'] = row['geometry'].simplify(thres)
    return df


def _round(geo, ndigits):
    return wkt.loads(wkt.dumps(geo, rounding_precision=ndigits))


def compress(df, ndigits=6):
    df.geometry = df.geometry.apply(lambda x: _round(x, ndigits))
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', required=True, type=str,
                        help='path to the input file')
    parser.add_argument('--output', '-o', required=True, type=str,
                        help='path to the output file')
    parser.add_argument('--hole', '-H', required=False, type=float,
                        default=60.,
                        help='threshold for holes to remove')
    parser.add_argument('--area', '-A', required=False, type=float,
                        default=10.,
                        help='threshold for area of polygons to remove')
    parser.add_argument('--simplify', '-S', required=False, type=float,
                        default=0.000005,
                        help='error margin for simplifying polygons')
    parser.add_argument('--digits', '-D', required=False, type=int,
                        default=6,
                        help='number of floating point digits')
    args = parser.parse_args()
    df = gpd.read_file(args.input)
    df = convert_to_single(df)
    df = remove_null_geometries(df)
    df = remove_holes(df, args.hole)
    df = remove_small_polygons(df, args.area)
    df = simplify_polygons(df, args.simplify)
    df = compress(df, args.digits)
    json.dump(json.loads(df.to_json()), open(args.output, 'w'))
