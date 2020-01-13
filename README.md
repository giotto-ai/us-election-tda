<img src="https://www.giotto.ai/static/vector/logo.svg" alt="logo" width="850"/>

# Discovering hidden socio-economic voting patterns in the US thanks to Giotto-Mapper

The accompanying blog post can be found [here](https://towardsdatascience.com/the-shape-of-the-united-states-presidential-elections-c336d80e4ddf) .

Want to dive right in? Find the accompanying blog post Go directly to the [Getting started](#getting-started) section!

## What it is

A guide on how to gain insight in socio-economic and election data of U.S. counties using the Mapper algorithm implemented in [Giotto-learn](https://github.com/giotto-ai/giotto-learn).
See the accompanying [blog post](https://towardsdatascience.com/the-shape-of-the-united-states-presidential-elections-c336d80e4ddf) for further details.

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

If you have `pip` and [anaconda](https://anaconda.org) installed, it suffices to run the following commands in a terminal:

```console
conda create --name mapper python=3.7 && conda activate mapper
conda install jupyter -y
pip install -r requirements.txt
pip install python-igraph
```

__2. Windows__

You first have to download from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-igraph) the wheel corresponding to your Python version and architecture. Then, you need to run the following commands in a terminal:

```console
conda create --name mapper python=3.7 && conda activate mapper
conda install jupyter -y
pip install -r requirements.txt
pip install python_igraph‑0.7.1.post6‑cp{YOUR_PYTHON_VERSION}‑cp{YOUR_PYTHON_VERSION}‑win_amd64.whl
```

## JupyterLab setup

To see the Plotly graphs in JupyterLab, some [extra steps](https://github.com/plotly/plotly.py) are required:

__1. Linux / MacOS__

```bash
# Avoid "JavaScript heap out of memory" errors during extension installation
export NODE_OPTIONS=--max-old-space-size=4096
# Jupyter widgets extension
jupyter labextension install @jupyter-widgets/jupyterlab-manager@1.1 --no-build
# FigureWidget support
jupyter labextension install plotlywidget@1.4.0 --no-build
# and jupyterlab renderer support
jupyter labextension install jupyterlab-plotly@1.4.0 --no-build
# Build extensions (must be done to activate extensions since --no-build is used above)
jupyter lab build
# Unset NODE_OPTIONS environment variable
unset NODE_OPTIONS
```

__2. Windows__

```bash
# Avoid "JavaScript heap out of memory" errors during extension installation
set NODE_OPTIONS=--max-old-space-size=4096
# Jupyter widgets extension
jupyter labextension install @jupyter-widgets/jupyterlab-manager@1.1 --no-build
# FigureWidget support
jupyter labextension install plotlywidget@1.4.0 --no-build
# and jupyterlab renderer support
jupyter labextension install jupyterlab-plotly@1.4.0 --no-build
# Build extensions (must be done to activate extensions since --no-build is used above)
jupyter lab build
# Unset NODE_OPTIONS environment variable
set NODE_OPTIONS=
```

After running these steps, deactivate and reactivate your conda environment before spinning up JupyterLab.
