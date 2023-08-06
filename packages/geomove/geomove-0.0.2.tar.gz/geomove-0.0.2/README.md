# geomove

[![pypi_version](https://img.shields.io/pypi/v/geomove?label=pypi)](https://pypi.org/project/geomove)[![build](https://github.com/merschformann/geomove/actions/workflows/build.yml/badge.svg)](https://github.com/merschformann/geomove/actions/workflows/build.yml)

Moves points on earth's surface towards a given bearing by a given distance.

## Introductory example

These points were created by moving a reference point (R) by 10 km in all base directions of a compass rose:

![compass_rose](material/compass_rose.png)

## Installation

```bash
pip install geomove
```

## Usage

Move a `(lat, lon)` point west by 10 km:

```python
from geomove import move, Bearing

# Define point
point = (51.9624, 7.6256)

# Move 
moved_point = move(point, Bearing.WEST, 10)
```

Move a point towards 357° by 5 km:

```python
from geomove import move

# Define point
point = (51.9624, 7.6256)

# Move
moved_point = move(point, 357, 5)
```
