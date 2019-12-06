import pandas as pd
import numpy as np
import matplotlib.colors

from functools import reduce
import operator
import networkx as nx

from plotting import mapper_plotly_plot

from sklearn.preprocessing import StandardScaler

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


def get_sum_node(mapper, df, col):
    return list(map(lambda x: df.iloc[x._labels][col].sum(),
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


def get_county_plot_data(mapper, df, col, cmap):
    map_col = (pd.DataFrame(np.zeros((df.shape[0],
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


def get_weighted_electors_plot(mapper, df, seed=0, size_offset=12):
    col = 'winner'
    pos = nx.spring_layout(mapper.complex._graph, seed=seed)
    size = list(map(lambda x: size_offset + x / min(get_node_size(mapper)),
                    get_node_size(mapper)))

    node_color = list(map(lambda x, y: x / y,
                          get_sum_node(mapper,
                                       df=pd.DataFrame(df['winner'] *
                                                       df['n_electors'],
                                                       columns=['weighted_' +
                                                                'winner']),
                                       col='weighted_winner'),
                          get_sum_node(mapper, df=df, col='n_electors')))

    node_text = []
    for node, pct, weighted_electors, n_electors \
        in zip(list(dict(mapper._nodes.items()).values()),
               get_mean_node(mapper, df=df, col=col),
               node_color, get_sum_node(mapper, df, 'n_electors')):
        node_text.append(f'# of counties: {len(node._labels)}<br>' +
                         f'Percentage voted for republican:' +
                         f' {round(100 * pct, 2)}<br>' +
                         f'Total (weighted) number of electors:'
                         f'{round(n_electors, 2)}<br>' +
                         f'Percentage of weighted, republican electors:' +
                         f'{round(100 * weighted_electors, 2)}')

    cmin = np.min(node_color)
    cmax = np.max(node_color)
    mapper_plotly_plot(
        mapper, pos, size, node_color, node_text, cmin=cmin, cmax=cmax,
        colorscale='RdBu',
        legend_title='Percentage of Weighted Republican Electors')


def get_cols_by_type():
    num_cols = ['Personal income (thousands of dollars)',
                'Net earnings by place of residence',
                'Personal current transfer receipts',
                'Income maintenance benefits 1/',
                'Unemployment insurance compensation',
                'Retirement and other',
                'Dividends, interest, and rent 2/',
                'Population (persons) 3/',
                'Per capita personal income 4/',
                'Per capita net earnings 4/',
                'Per capita personal current transfer receipts 4/',
                'Per capita income maintenance benefits 4/',
                'Per capita unemployment insurance compensation 4/',
                'Per capita retirement and other 4/',
                'Per capita dividends, interest, and rent 4/',
                'Earnings by place of work',
                'Wages and salaries',
                'Supplements to wages and salaries',
                'Employer contributions for employee pension and ' +
                'insurance funds 5/',
                'Employer contributions for government social insurance',
                "Proprietors' income",
                "Farm proprietors' income",
                "Nonfarm proprietors' income",
                'Total employment (number of jobs)',
                'Wage and salary employment',
                'Proprietors employment',
                'Farm proprietors employment 6/',
                'Nonfarm proprietors employment',
                'Average earnings per job (dollars)',
                'Average wages and salaries',
                "Average nonfarm proprietors' income"]

    info_cols = ['year', 'state', 'county', 'fips', 'pres']

    elec_cols = ['republican', 'democrat', 'total_votes', 'n_electors',
                 'winner']

    return num_cols, info_cols, elec_cols


def get_data(df):
    num_cols, _, _ = get_cols_by_type()

    # perform a log transformation on the data
    df[num_cols] = (df[num_cols] +
                    abs(df[num_cols].min().min()) + 1).apply(np.log)

    # columns to use for the mapper were found by comparing the distribution
    # of each column between the different election years
    # The ones differing throughout the years are selected (selection was made
    # by eye)
    cols2use = ['Personal income (thousands of dollars)',
                'Net earnings by place of residence',
                'Income maintenance benefits 1/',
                'Unemployment insurance compensation',
                'Per capita personal income 4/',
                'Per capita net earnings 4/',
                'Per capita personal current transfer receipts 4/',
                'Per capita income maintenance benefits 4/',
                'Per capita unemployment insurance compensation 4/',
                'Per capita retirement and other 4/',
                'Per capita dividends, interest, and rent 4/',
                'Earnings by place of work',
                "Proprietors' income",
                "Nonfarm proprietors' income",
                'Total employment (number of jobs)',
                'Proprietors employment',
                'Farm proprietors employment 6/',
                'Nonfarm proprietors employment',
                'Average earnings per job (dollars)',
                'Average wages and salaries',
                "Average nonfarm proprietors' income"]

    # scale data to have zero mean and a standard deviation of one
    scaler = StandardScaler()
    df[num_cols] = scaler.fit_transform(df[num_cols])

    return df[cols2use].values


def split_data_by_year(data, df):
    return dict(zip(['2000', '2004', '2008', '2012', '2016'],
                map(lambda x: data[x, :],
                    map(lambda x: df[df['year'] == x].index,
                        df['year'].unique()))))


def get_colored_mapper_plot(mapper, df, col, seed=0, size_offset=12):
    pos = nx.spring_layout(mapper.complex._graph, seed=seed)

    node_size = list(map(lambda x: size_offset + x /
                         min(get_node_size(mapper)),
                     get_node_size(mapper)))
    node_text = []
    for node_id, node, pct in zip(range(len(dict(mapper._nodes.items())
                                            .values())),
                                  dict(mapper._nodes.items()).values(),
                                  get_mean_node(mapper, df=df, col=col)):
        node_text.append(f'Node id: {node_id}<br>' +
                         f'Number of counties: {len(node._labels)}<br>' +
                         f'Mean {col}: {round(pct, 2)}')
    node_color = get_mean_node(mapper, df=df, col=col)

    cmin = np.min(node_color)
    cmax = np.max(node_color)
    mapper_plotly_plot(mapper=mapper, pos=pos, size=node_size,
                       node_color=node_color,
                       cmin=cmin, cmax=cmax, node_text=node_text,
                       colorscale='RdBu', legend_title=col)
