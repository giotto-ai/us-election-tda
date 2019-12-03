import pandas as pd
import numpy as np
import matplotlib.colors

import sys
sys.path.append('..')
import lmapper as lm
from lmapper.cover import UniformCover
from lmapper.cluster import Linkage


def get_node_size(mapper, offset=50):
    return list(map(lambda x: len(x._labels) + offset,
                    list(dict(mapper._nodes.items()).values())))


def get_mean_node(mapper, df, col):
    return list(map(lambda x: df.iloc[x._labels][col].mean(),
                    list(dict(mapper._nodes.items()).values())))


def get_mapper(filtr, nintervals, overlap, method,
               metric, cutoff, data):
    cover = UniformCover(nintervals=nintervals,
                         overlap=overlap)
    cluster = Linkage(method=method, metric=metric,
                      cutoff=cutoff)
    mapper = lm.Mapper(data=data,
                       filter=filtr,
                       cover=cover, cluster=cluster)
    return mapper


def get_county_plot_data(data, mapper, df, col, cmap):
    map_col = (pd.DataFrame(np.zeros((data.shape[0],
                                      2)),
                            columns=['color_sum', 'n_counties'])
               .astype({'n_counties': 'int'}))

    for rows, val in zip(list(map(lambda x: x._labels.tolist(),
                                  dict(mapper._nodes.items()).values())),
                         get_mean_node(mapper, df=df,
                                       col=col)):
        map_col.loc[rows] = map_col.loc[rows] + [val, 1]

    colors = list(map(lambda x: matplotlib.colors.rgb2hex(x),
                      cmap((map_col['color_sum'] /
                            map_col['n_counties']).unique().tolist())[:, :3]))

    return ((map_col['color_sum'] / map_col['n_counties']).tolist(),
            colors)
