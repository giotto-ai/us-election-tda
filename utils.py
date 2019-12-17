import numpy as np

from sklearn.preprocessing import StandardScaler


def get_node_size(node_elements):
    return list(map(len, node_elements))


def get_node_summary(node_elements, data, summary_stat=np.mean):
    return list(map(lambda x: summary_stat(data[x]),
                    node_elements))


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
