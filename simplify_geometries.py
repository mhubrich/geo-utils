"""
This script
* converts all multi-geometries into single-geometries
    * MultiPoint -> [Point]
    * MultiLineString -> [LineString]
    * MultiPolygon -> [Polygon]
* simplifies LineStrings and Polygons based on a given error margin
* rounds all coordinates to a specified floating point digit

Run:
python simplify_geometries.py -i "path_in" -o "path_out"
"""
import json
import argparse
import numpy as np
import geopandas as gpd
from shapely import wkt


def to_single_geometries(df):
    """
    Converts all multi-geometries to single-geometries.
    Params:
        df - GeoDataFrame.
    Returns:
        df - GeoDataFrame.
    """
    assert isinstance(df, gpd.GeoDataFrame)
    assert not df.geometry.isna().any()
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


def simplify(df, thres=0.000005):
    """
    Simplifies the the shape of LineStrings and Polygons.
    Params:
        df - GeoDataFrame.
        thres - Float. Error margin for simplifying shapes.
    Returns:
        df - GeoDataFrame.
    """
    assert isinstance(df, gpd.GeoDataFrame)
    assert isinstance(thres, float)
    assert thres >= 0
    for i, row in df[df.geom_type.isin(['LineString', 'Polygon'])].iterrows():
        df.loc[i, 'geometry'] = row['geometry'].simplify(thres)
    return df


def _round(geo, ndigits):
    """
    Rounds all coordinates to a specified number of floating point digits.
    Params:
        geo - Geometry.
        ndigits - Integer. Number of floating point digits.
    Returns:
        geo - Geometry.
    """
    return wkt.loads(wkt.dumps(geo, rounding_precision=ndigits))


def round_coordinates(df, ndigits=6):
    """
    Rounds coordinates of all geometries to a specified number of floating point digits.
    Params:
        df - GeoDataFrame.
        ndigits - Integer. Number of floating point digits.
    Returns:
        df - GeoDataFrame.
    """
    assert isinstance(df, gpd.GeoDataFrame)
    assert isinstance(ndigits, int)
    assert ndigits > 0
    df.geometry = df.geometry.apply(lambda x: _round(x, ndigits))
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', required=True, type=str,
                        help='path to the input file')
    parser.add_argument('--output', '-o', required=True, type=str,
                        help='path to the output file')
    parser.add_argument('--simplify', '-S', required=False, type=float,
                        default=0.000005,
                        help='error margin for simplifying shapes')
    parser.add_argument('--digits', '-D', required=False, type=int,
                        default=6,
                        help='number of floating point digits')
    args = parser.parse_args()
    df = gpd.read_file(args.input)
    df = to_single_geometries(df)
    df = simplify(df, args.simplify)
    df = round_coordinates(df, args.digits)
    json.dump(json.loads(df.to_json()), open(args.output, 'w'))
