pyHaversine
==============

[![PyPI](https://github.com/luk-f/pyhaversine/actions/workflows/pip.yml/badge.svg)](https://github.com/luk-f/pyhaversine/actions/workflows/pip.yml)

An simple project built with [pybind11](https://github.com/pybind/pybind11).
This requires Python 3.6+; for older versions of Python, check the commit
history.

Installation
------------

 - Use `pip install pyhaversine` directly

Or, manually:

 - clone this repository
 - `pip install ./pyhaversine`

License
-------

pybind11 is provided under a BSD-style license that can be found in the LICENSE
file. By using, distributing, or contributing to this project, you agree to the
terms and conditions of this license.

Test call
---------

```python
import pyhaversine
pyhaversine.haversine((1.0, 2.0), (3.0, 4.0))
```
