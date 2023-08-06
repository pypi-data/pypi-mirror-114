# <p align="center"> <a href="https://predict-idlab.github.io/tsflex"><img alt="tsflex" src="https://raw.githubusercontent.com/predict-idlab/tsflex/main/docs/_static/logo.png" height="100"></a></p>

[![PyPI Latest Release](https://img.shields.io/pypi/v/tsflex.svg)](https://pypi.org/project/tsflex/)
[![Conda Latest Release](https://img.shields.io/conda/vn/conda-forge/tsflex?label=conda)](https://anaconda.org/conda-forge/tsflex)
[![support-version](https://img.shields.io/pypi/pyversions/tsflex)](https://img.shields.io/pypi/pyversions/tsflex)
[![codecov](https://img.shields.io/codecov/c/github/predict-idlab/tsflex?logo=codecov)](https://codecov.io/gh/predict-idlab/tsflex)
[![Code quality](https://img.shields.io/lgtm/grade/python/github/predict-idlab/tsflex?label=code%20quality&logo=lgtm)](https://lgtm.com/projects/g/predict-idlab/tsflex/context:python)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?color=black)
[![Downloads](https://pepy.tech/badge/tsflex)](https://pepy.tech/project/tsflex)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?)](http://makeapullrequest.com) 
[![Documentation](https://github.com/predict-idlab/tsflex/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/predict-idlab/tsflex/actions/workflows/deploy-docs.yml)
[![Testing](https://github.com/predict-idlab/tsflex/actions/workflows/test.yml/badge.svg)](https://github.com/predict-idlab/tsflex/actions/workflows/test.yml)

<!-- ![Downloads](https://img.shields.io/conda/dn/conda-forge/tsflex?logo=anaconda) -->

*tsflex* is a toolkit for _**flex**ible **t**ime **s**eries_ **[processing](https://predict-idlab.github.io/tsflex/processing) & [feature extraction](https://predict-idlab.github.io/tsflex/features)**, making few assumptions about input data. 

#### Useful links

- [Documentation](https://predict-idlab.github.io/tsflex/)
- [Example notebooks](https://github.com/predict-idlab/tsflex/tree/main/examples)

## Installation

If you are using [**pip**](https://pypi.org/project/tsflex/), just execute the following command:

```sh
pip install tsflex
```

Or, if you are using [**conda**](https://anaconda.org/conda-forge/tsflex), then execute this command:

```sh
conda install -c conda-forge tsflex
```

## Why tsflex? ✨

* flexible;
    * handles multivariate time series
    * versatile function support  
      => **integrates natively** with many packages for processing (e.g., [scipy.signal](https://docs.scipy.org/doc/scipy/reference/tutorial/signal.html), [statsmodels.tsa](https://www.statsmodels.org/stable/tsa.html#time-series-filters)) & feature extraction (e.g., [numpy](https://numpy.org/doc/stable/reference/routines.html), [scipy.stats](https://docs.scipy.org/doc/scipy/reference/tutorial/stats.html))
    * feature-extraction handles **multiple strides & window sizes**
* efficient view-based operations  
  => extremely **low memory peak & fast execution times** ([see benchmarks](https://github.com/predict-idlab/tsflex-benchmarking))
    <!-- * faster than any existing library (single- & multi-core)
    * lower memory peak than any existing library (single- & multi-core) -->
* maintains the **time-index** of the data
* makes **little to no assumptions** about the time series data

## Usage

_tsflex_ is built to be intuitive, so we encourage you to copy-paste this code and toy with some parameters!

### <a href="https://predict-idlab.github.io/tsflex/features/#getting-started">Feature extraction</a>

```python
import pandas as pd; import scipy.stats as ssig; import numpy as np
from tsflex.features import FeatureDescriptor, FeatureCollection, FuncWrapper

# 1. -------- Get your time-indexed data --------
# Data contains 1 column; ["TMP"]
url = "https://github.com/predict-idlab/tsflex/raw/main/examples/data/empatica/tmp.parquet"
data = pd.read_parquet(url).set_index("timestamp")

# 2 -------- Construct your feature collection --------
fc = FeatureCollection(
    feature_descriptors=[
        FeatureDescriptor(
            function=FuncWrapper(func=ssig.skew, output_names="skew"),
            series_name="TMP", 
            window="5min",  # Use 5 minutes 
            stride="2.5min",  # With steps of 2.5 minutes
        )
    ]
)
# -- 2.1. Add features to your feature collection
fc.add(FeatureDescriptor(np.min, "TMP", '2.5min', '2.5min'))

# 3 -------- Calculate features --------
fc.calculate(data=data)
```

### More examples

For processing [look here](https://predict-idlab.github.io/tsflex/processing/index.html#working-example)    
Other examples can be found [here](https://github.com/predict-idlab/tsflex/tree/main/examples)

## Future work 🔨

* scikit-learn integration for both processing and feature extraction<br>
  **note**: is actively developed upon [sklearn integration](https://github.com/predict-idlab/tsflex/tree/sklearn_integration) branch.
* support for multi-indexed dataframes
* random-strided rolling for data-augmention purposes.

## Referencing our package

If you use `tsflex` in a scientific publication, we would highly appreciate citing us as:

```bibtex
@article{vanderdonckt2021tsflex,
    author = {Van Der Donckt, Jonas and Van Der Donckt, Jeroen and Deprost, Emiel and Van Hoecke, Sofie},
    title = {tsflex: flexible time series processing \& feature extraction},
    journal = {SoftwareX},
    year = {2021},
    url = {https://github.com/predict-idlab/tsflex},
    publisher={Elsevier}
}
```

---

<p align="center">
👤 <i>Jonas Van Der Donckt, Jeroen Van Der Donckt, Emiel Deprost</i>
</p>
