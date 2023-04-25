<div align="center">
  <a href="https://github.com/mhubrich/geo-utils">
    <img src="https://esri.github.io/geometry-api-java/doc/Images/Intersection/Intersection3.jpg" alt="Logo">
  </a>

  <h3 align="center">Geo Utils</h3>

  <p align="center">
    A collection of geospatial utility functions in Python
  </p>
</div>
<br />

## About the Project
There are a number of geospatial functions I frequently use in coding projects. These functions all operate on geometries (points, lines, polygons) loaded from GeoJSON files. I decided to centralize these utility functions so I can reference them faster, but also to share them with other geospatial data enthusiasts.

## Functions
- [`load_file`](https://github.com/mhubrich/geo-utils/blob/abb4111965f3c8f9dec45f347004c2640940f56f/utils.py#L18-L20) and [`save_file`](https://github.com/mhubrich/geo-utils/blob/abb4111965f3c8f9dec45f347004c2640940f56f/utils.py#L23-L25): Loads and saves GeoJSON files
- [`shift`](https://github.com/mhubrich/geo-utils/blob/abb4111965f3c8f9dec45f347004c2640940f56f/utils.py#L39-L41): Shifts points by given distance and angle
- [`translate`](https://github.com/mhubrich/geo-utils/blob/abb4111965f3c8f9dec45f347004c2640940f56f/utils.py#L102-L104): Translates geometries by given offset
- [`split`](https://github.com/mhubrich/geo-utils/blob/abb4111965f3c8f9dec45f347004c2640940f56f/utils.py#L107-L109): Splits geometries by given geometry
- [`distance`](https://github.com/mhubrich/geo-utils/blob/abb4111965f3c8f9dec45f347004c2640940f56f/utils.py#L44-L48): Computes distance between points
- [`line_length`](https://github.com/mhubrich/geo-utils/blob/abb4111965f3c8f9dec45f347004c2640940f56f/utils.py#L51-L53): Computes length of a linestring
- [`substring`](https://github.com/mhubrich/geo-utils/blob/abb4111965f3c8f9dec45f347004c2640940f56f/utils.py#L97-L99): Returns a substring with specific length of a linestring
- [`side`](https://github.com/mhubrich/geo-utils/blob/abb4111965f3c8f9dec45f347004c2640940f56f/utils.py#L56-L60): Determines which side of a line a given point falls on
- [`closest_segment`](https://github.com/mhubrich/geo-utils/blob/349150a3ba3c90718918f782f1df2a78ba294154/utils.py#L82-L94): Finds the segment of a line which is closest to a given point
- [`to_circle`](https://github.com/mhubrich/geo-utils/blob/abb4111965f3c8f9dec45f347004c2640940f56f/utils.py#L63-L65): Creates a circle from a given point and radius
- [`to_single_geometry`](https://github.com/mhubrich/geo-utils/blob/abb4111965f3c8f9dec45f347004c2640940f56f/utils.py#L68-L79): Converts multi-geometries to single-geometries
- [`remove_holes`](https://github.com/mhubrich/geo-utils/blob/abb4111965f3c8f9dec45f347004c2640940f56f/beautify_polygons.py#L52-L55): Removes holes in polygons
- [`remove_small_polygons`](https://github.com/mhubrich/geo-utils/blob/abb4111965f3c8f9dec45f347004c2640940f56f/beautify_polygons.py#L58-L64): Removes tiny geometries (artifacts)
- [`simplify`](https://github.com/mhubrich/geo-utils/blob/abb4111965f3c8f9dec45f347004c2640940f56f/simplify_geometries.py#L42-L56): Simplifies geometries (reduces amount of nodes)
- [`compress`](https://github.com/mhubrich/geo-utils/blob/abb4111965f3c8f9dec45f347004c2640940f56f/simplify_geometries.py#L71-L84): Compresses geometries (reduces amount of floating point digits of nodes)

## Dependencies

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.
