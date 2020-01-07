import plotly.figure_factory as ff
import utils
import itertools
import collections
from giotto.mapper import visualization
import numpy as np


def get_region_plot(graph, data, layout, columns_to_color, node_elements,
                    colorscale):
    regions = utils.get_regions()

    node_color = list(
        collections.OrderedDict(
            sorted(itertools.chain(
                *map(list,
                     [zip(regions[region],
                          itertools.repeat(colorscale[region]))
                      for region in range(len(regions))])))).values())

    plotly_kwargs = {
        'node_trace_marker_size': [1] * len(node_elements),
        'node_trace_marker_showscale': False}

    return visualization.create_network_2d(graph, data, layout, node_color,
                                           columns_to_color=columns_to_color,
                                           plotly_kwargs=plotly_kwargs)

def get_graph_plot_colored_by_election_results(graph, year, df, data,
                                               layout=None):
    node_elements = graph['node_metadata']['node_elements']

    if layout is None:
        layout = graph.layout('kk', dim=2)

    node_color = [(df[df['year'] == year]['winner'].values *
                   df[df['year'] == year]['n_electors'].values)[x].sum() /
                  df[df['year'] == year]['n_electors'].values[x].sum()
                  for x in node_elements]

    data_cols = utils.get_cols_for_mapper()
    columns_to_color = dict(zip(data_cols, range(len(data_cols))))

    node_text = utils.get_node_text(
        dict(zip(range(len(node_elements)),
                 node_elements)),
        utils.get_n_electors(node_elements,
                             df[df['year'] == year]['n_electors']
                             .reset_index(drop=True)),
        node_color,
        'Percentage of Electors')

    plotly_kwargs = {
        'node_trace_marker_colorscale': 'RdBu',
        'node_trace_marker_reversescale': True,
        'node_trace_text': node_text,
        'node_trace_marker_size':
        utils.get_n_electors(node_elements,
                             df[df['year'] == year]['n_electors']
                             .reset_index(drop=True)),
        'node_trace_marker_sizeref':
        .5 / max(utils.get_n_electors(node_elements,
                                      df[df['year'] == year]['n_electors']
                                      .reset_index(drop=True)))}

    return visualization.create_network_2d(graph, data, layout, node_color,
                                           columns_to_color=columns_to_color,
                                           plotly_kwargs=plotly_kwargs)


def get_county_plot(fips, values, colorscale=["#0000ff", "#ff0000"],
                    legend_title='', showlegend=False):
    # https://plot.ly/python/county-choropleth/

    fig = ff.create_choropleth(fips=fips, values=values,
                               colorscale=colorscale,
                               show_state_data=False,
                               show_hover=True, centroid_marker={'opacity': 0},
                               asp=2.9, title='Election Outcome',
                               legend_title=legend_title)
    fig.layout.template = None
    fig.update_layout(showlegend=showlegend)
    return fig


def get_county_plot_by_region(data, colorscale, node_elements, fips):
    colorscale = dict(zip(map(str, range(len(colorscale))),
                          utils.hex2rgb(colorscale.values())))
    colorscale['1-3'] = utils.mean_rgb([colorscale['1'],
                                        colorscale['3']])
    colorscale['2-3'] = utils.mean_rgb([colorscale['2'],
                                        colorscale['3']])
    colorscale['3-4'] = utils.mean_rgb([colorscale['3'],
                                        colorscale['4']])
    colorscale['4-5'] = utils.mean_rgb([colorscale['4'],
                                        colorscale['5']])

    elements_per_region = utils.get_data_per_region(utils.get_regions(),
                                                    node_elements)

    county_color = np.zeros(data.shape[0], dtype='int')
    county_color[list(elements_per_region[0])] = 0
    county_color[list(elements_per_region[1]
                      .difference(elements_per_region[3]))] = 1
    county_color[list(elements_per_region[2]
                      .difference(elements_per_region[3]))] = 2
    county_color[list(elements_per_region[3]
                      .difference(elements_per_region[1])
                      .difference(elements_per_region[2]))] = 3
    county_color[list(elements_per_region[4]
                      .difference(elements_per_region[3]))] = 4
    county_color[list(elements_per_region[5]
                      .difference(elements_per_region[4]))] = 5

    county_color[list(elements_per_region[1]
                      .intersection(elements_per_region[3]))] = 6
    county_color[list(elements_per_region[2]
                      .intersection(elements_per_region[3]))] = 7
    county_color[list(elements_per_region[3]
                      .intersection(elements_per_region[4]))] = 8
    county_color[list(elements_per_region[4]
                      .intersection(elements_per_region[5]))] = 9
    county_color = county_color.tolist()

    return get_county_plot(
        fips=fips, values=county_color,
        colorscale=[f'rgb{rgb}' for rgb in list(colorscale.values())])
