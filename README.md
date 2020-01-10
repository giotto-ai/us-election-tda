<img src="https://www.giotto.ai/static/vector/logo.svg" alt="logo" width="850"/>

# us-election-tda

Want to dive right in? Go directly to the [Getting started](#getting-started) section!

## What it is

A guide on how to gain insight in socio-economic and election data of U.S. counties using the Mapper algorithm implemented in [Giotto-learn](https://github.com/giotto-ai/giotto-learn).

## Data

The socio-economic data has been taken from the [U.S. Bureau of Economic Analysis](https://www.bea.gov) (BEA). The voting data is provided by the [MIT Election Data and Science Lab](https://electionlab.mit.edu/data) (MEDSL).

## Results

Our study shows that we can divide the counties into five main regions based on economic indicators:

1. High net worth
2. High net worth per inhabitant
3. High per capita retirement
4. Elevated and average net worth
5. Low net worth

When combined with election results, we find that in 2016, the high per capita retirement, and low net worth regions are strongholds for the Republicans. The remaining three regions vote predominantly Democrat with an exception for some clusters of elevated and medium net worth counties.

## Getting started

__1. Linux / MacOS__

If you have `pip` installed, it suffices to run the following commands in a terminal:

```console
virtualenv -p python3.7 env
source PATH_TO_ENV/bin/activate
pip install -r requirements.txt
pip install python-igraph
```

__2. Windows__

You first have to download from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-igraph) the binary wheel corresponding to your Python version and architecture. Then, you need to run the following commands in a terminal:

```console
virtualenv -p python3.7 env
PATH_TO_ENV\Scripts\activate
pip install -r requirements.txt
pip install python_igraph‑0.7.1.post6‑cp{YOUR_PYTHON_VERSION}‑cp{YOUR_PYTHON_VERSION}‑win_amd64.whl
```
