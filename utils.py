import pandas as pd
import numpy as np
import matplotlib.colors

from functools import reduce
import operator
import networkx as nx

from plotting import mapper_plotly_plot

import sys
sys.path.append('..')
import lmapper as lm
from lmapper.cover import UniformCover
from lmapper.cluster import Linkage


def get_node_size(mapper, offset=50):
    return list(map(lambda x: len(x._labels) + offset,
                    dict(mapper._nodes.items()).values()))


def get_mean_node(mapper, df, col):
    return list(map(lambda x: df.iloc[x._labels][col].mean(),
                    dict(mapper._nodes.items()).values()))


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


def get_unique_cluster_vals(mapper, cluster):
    '''
        return indices belonging only to a cluster
    '''
    return list(set(list(dict(mapper._nodes.items()).values())[cluster]
                    ._labels)
                .difference(set(reduce(operator.iconcat,
                                       list(map(lambda x: list(x._labels),
                                                list(dict(mapper._nodes
                                                          .items())
                                                     .values())[0:cluster] +
                                                list(dict(mapper._nodes
                                                          .items())
                                                     .values())[cluster + 1:])
                                            ), []))))


def get_weighted_electors_plot(mapper, df, seed=0):
    col = 'winner'
    pos = nx.spring_layout(mapper.complex._graph, seed=seed)
    size = list(map(lambda x: 12 + x / min(get_node_size(mapper)),
                    get_node_size(mapper)))

    node_color = list(map(lambda x, y: x / y,
                          get_mean_node(mapper,
                                        df=pd.DataFrame(df['winner'] *
                                                        df['n_electors'],
                                                        columns=['weighted_' +
                                                                 'winner']),
                                        col='weighted_winner'),
                          get_mean_node(mapper, df=df, col='n_electors')))

    node_text = []
    for node, pct, weighted_electors in zip(list(dict(mapper._nodes.items())
                                                 .values()),
                                            get_mean_node(mapper, df=df,
                                                          col=col),
                                            node_color):
        node_text.append(f'# of counties: {len(node._labels)}<br>' +
                         f'Percentage voted for republican:' +
                         f' {round(100 * pct, 2)}<br>' +
                         f'Mean weighted number of electors:' +
                         f'{weighted_electors}')

    cmin = np.min(node_color)
    cmax = np.max(node_color)
    mapper_plotly_plot(mapper, df, pos, size, node_color, node_text, cmin=cmin,
                       cmax=cmax, colorscale='RdBu',
                       title='Percentage voted for republican')
