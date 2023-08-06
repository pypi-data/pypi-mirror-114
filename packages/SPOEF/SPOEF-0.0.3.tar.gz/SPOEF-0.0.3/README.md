[![PyPi Version](https://img.shields.io/pypi/pyversions/SPOEF)](#)
[![PyPI](https://img.shields.io/pypi/v/SPOEF)](#)

# SPOEF

## Overview

**SPOEF** is a Python package that lets you easily generate features with signal processing methods from transaction data.

## Example Usage - Generating Features

```python
transaction_features_quarterly = feature_generation(
    data=data[["name", "date", "transaction"]],
    grouper="name",
    combine_fill_method="transaction",
    time_window='quarter',
    list_featuretypes=["FourierComplete", "WaveletComplete"],
    observation_length=1
)
```

- [Minimal Working Example](https://janbargeman.github.io/SPOEF/tutorials/minimal_working_example.html)

## Installation

```bash
pip install SPOEF
```

## Documentation

The documentation can [be found here.](https://janbargeman.github.io/SPOEF/)

