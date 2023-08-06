# Tracklet Extraction Engine
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This package provides a function to retrieve _tracklets_ from a list of _vertices_ in a three-dimensional space. The function find a set of linearly aligned vertices in the list and derive a line segment (tracklet) to approximate the vertex distribution.


## Overview

The module provides a class `Tracklet` and a function `extract`. The `extract` function receives a list of vertices as `numpy.ndarray`. The array shape should be `(n,6)`, where _n_ is the number of vertices. Then, a list of `Tracklets` instances are returned. Some tutorials are available in [notebook][notebook].

[notebook]: https://bitbucket.org/ryou_ohsawa/tracee/src/master/notebook/


## Requiremnts
The package `tracee` depends on the following packages. Both packages are available in [PyPi][pypi]. Installation on Ubuntu 18.04 was confirmed. If you have any troubles in installation, please contact to the developer.

- [fdlsgm>=0.5.5][fdlsgm]
- [minimalKNN>=0.5][minimalKNN]


[pypi]: https://pypi.org/
[fdlsgm]: https://pypi.org/project/fdlsgm/
[minimalKNN]: https://pypi.org/project/minimalKNN/
