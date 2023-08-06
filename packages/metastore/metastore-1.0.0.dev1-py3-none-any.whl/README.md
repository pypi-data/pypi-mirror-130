# Metastore

Metastore Python SDK.

## Prerequisites

* [Python (>=3.6.0)](https://www.python.org)

## Installation

### Production

Install package:

```
pip install metastore
```

### Development

Install package:

```
pip install -e .[development]
```

> **Note** Use the `-e, --editable` flag to install the package in development mode.

Format source code:

```
autopep8 --recursive --in-place metastore
```

Lint source code:

```
pylint metastore
```

Test package:

```
pytest
```

Build package:

```
python setup.py bdist_wheel
```

Publish package:

```
twine upload dist/*
```

## Changelog

[Changelog](CHANGELOG.md) contains information about new features, improvements, known issues, and bug fixes in each release.

## Copyright and license

Copyright (c) 2022, Metastore Developers. All rights reserved.

Project developed under a [BSD-3-Clause License](LICENSE.md).
