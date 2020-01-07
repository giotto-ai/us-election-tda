import numpy as np

from sklearn.preprocessing import StandardScaler

import matplotlib.colors
import pandas as pd


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


def get_cols_for_mapper():
    # columns to use for the mapper were found by comparing the distribution
    # of each column between the different election years
    # The ones differing throughout the years are selected (selection was made
    # by eye)
    return ['Personal income (thousands of dollars)',
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


def get_data(df):
    data_cols = get_cols_for_mapper()

    # perform a log transformation on the data
    df[data_cols] = (df[data_cols] +
                     abs(df[data_cols].min().min()) + 1).apply(np.log)

    # scale data to have zero mean and a standard deviation of one
    scaler = StandardScaler()
    df[data_cols] = scaler.fit_transform(df[data_cols])

    return df[data_cols].values


def split_data_by_year(data, df):
    return dict(zip(['2000', '2004', '2008', '2012', '2016'],
                map(lambda x: data[x, :],
                    map(lambda x: df[df['year'] == x].index,
                        df['year'].unique()))))


def filter_2d_trafo(x):
    x[:, 0] = np.log(x[:, 0] - min(x[:, 0]) + 1)
    x[:, 1] = np.log(np.abs(x[:, 1]) + 1)
    return x


# for plotting
def get_node_size(node_elements):
    return list(map(len, node_elements))


def get_node_summary(node_elements, data, summary_stat=np.mean):
    return list(map(lambda x: summary_stat(data[x]),
                    node_elements))


def get_n_electors(node_elements, n_electors):
    return [100 * n_electors.iloc[x].sum() / n_electors.sum()
            for x in node_elements]


def get_node_text(node_elements, n_electors, node_color, label):
    return [f'Node Id: {x[0]}<br>' +
            f'Node size: {len(x[1])}<br>' +
            f'Percentage of Electors: {round(y, 2)}<br>' +
            f'Percentage of Electors per County: '
            f'{round(y / len(n_electors), 3)}<br>' +
            f'Mean {label}: {z}'
            for x, y, z in zip(node_elements.items(), n_electors, node_color)]


def get_subgraph(graph, vertices_to_remove):
    subgraph = graph.copy()
    subgraph.delete_vertices(vertices_to_remove)

    return subgraph


def get_county_plot_data(graph, df, col, cmap):
    map_col = (pd.DataFrame(np.zeros((df.shape[0],
                                      2)),
                            columns=['color_sum', 'n_counties'])
               .astype({'n_counties': 'int'}))

    for rows, val in zip(graph['node_metadata']['node_elements'],
                         get_node_summary(graph['node_metadata']
                                          ['node_elements'],
                                          df[col])):
        map_col.loc[rows] = map_col.loc[rows] + [val, 1]

    colors = list(map(matplotlib.colors.rgb2hex,
                      cmap((map_col['color_sum'] /
                            map_col['n_counties']).sort_values().unique()
                           .tolist())[:, :3]))

    return ((map_col['color_sum'] / map_col['n_counties']).tolist(),
            colors)


def get_regions():
    return {
        0: {45, 18, 1, 7, 52, 55, 50, 49, 46, 51, 47, 30, 2, 44,
            37, 54, 53, 9, 48, 13, 24},
        1: {41, 42, 43},
        2: {38, 39, 40},
        3: {25, 26, 27, 28, 29, 31, 32, 33, 34, 35, 36},
        4: {14, 15, 16, 17, 19, 20, 21, 22, 23},
        5: {0, 3, 4, 5, 6, 8, 10, 11, 12}
    }


def get_data_per_region(regions, node_elements):
    # return dictionary with regions as key and corresponding data points as
    # values
    return dict((region_id, set.union(*[set(node_elements[node])
                                        for node in regions[region_id]]))
                for region_id in regions.keys())


def hex2rgb(hex_colors):
    # convert #xxyyzz hex color format to (r, g, b)
    rgb_colors = [color.lstrip('#') for color in hex_colors]
    return [tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
            for color in rgb_colors]


def mean_rgb(rgb_vals):
    # calculate mean of list of rbg values
    return tuple(map(int, np.mean(rgb_vals, axis=0)))
