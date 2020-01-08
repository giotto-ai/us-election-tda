import plotly.figure_factory as ff
import utils
import itertools
import collections
from giotto.mapper import visualization
import numpy as np


def get_region_plot(graph, data, layout, columns_to_color, node_elements,
                    colorscale):
    regions = utils.get_regions()

    # set node color:
    # 1. assign to each node of a region its color (zip())
    # 2. convert zip elements to list (map())
    # 3. flatten list (itertools.chain())
    # 4. sort values by keys
    # 5. convert to ordered dictionary
    # 6. extract values and convert to list
    node_color = list(
        collections.OrderedDict(
            sorted(itertools.chain(
                *map(list,
                     [zip(regions[region],
                          itertools.repeat(colorscale[region]))
                      for region in range(len(regions))])))).values())

    # set plotly arguments:
    # 1. set uniform node size
    # 2. hide scale of marker color
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

    # set node color to percentage of number of electors won by republicans
    node_color = [
        100 * (df[df['year'] == year]['winner'].values *
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
        'Percentage of Electors Won by Republicans')

    plotly_kwargs = {
        'node_trace_marker_colorscale': 'RdBu',
        'node_trace_marker_reversescale': True,
        'node_trace_marker_cmin': 0,
        'node_trace_marker_cmax': 100,
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


def get_county_plot(fips, values, colorscale=["#0000ff", "#ff0000"], title='',
                    show_state_data=False, legend_title='', showlegend=False):
    # https://plot.ly/python/county-choropleth/

    fig = ff.create_choropleth(fips=fips, values=values,
                               colorscale=colorscale,
                               show_state_data=show_state_data,
                               show_hover=True, centroid_marker={'opacity': 0},
                               asp=2.9, title=title,
                               legend_title=legend_title)
    fig.layout.template = None
    fig.update_layout(showlegend=showlegend)
    return fig


def get_county_plot_by_region(data, colorscale, node_elements, fips):
    # convert colorscale from hex format to rgb
    colorscale = dict(zip(map(str, range(len(colorscale))),
                          utils.hex2rgb(colorscale.values())))
    # define color of counties belonging to two regions as their mean rgb value
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

    # assign each county its color
    county_color = np.zeros(data.shape[0], dtype='int')
    # region 0
    county_color[list(elements_per_region[0])] = 0
    # region 1 and not 3
    county_color[list(elements_per_region[1]
                      .difference(elements_per_region[3]))] = 1
    # region 2 and not 3
    county_color[list(elements_per_region[2]
                      .difference(elements_per_region[3]))] = 2
    # region 3 and neither 1 nor 2
    county_color[list(elements_per_region[3]
                      .difference(elements_per_region[1])
                      .difference(elements_per_region[2]))] = 3
    # region 4 but not 3
    county_color[list(elements_per_region[4]
                      .difference(elements_per_region[3]))] = 4
    # region 5 but not 4
    county_color[list(elements_per_region[5]
                      .difference(elements_per_region[4]))] = 5

    # region 1 and 3
    county_color[list(elements_per_region[1]
                      .intersection(elements_per_region[3]))] = 6
    # region 2 and 3
    county_color[list(elements_per_region[2]
                      .intersection(elements_per_region[3]))] = 7
    # region 3 and 4
    county_color[list(elements_per_region[3]
                      .intersection(elements_per_region[4]))] = 8
    # region 4 and 5
    county_color[list(elements_per_region[4]
                      .intersection(elements_per_region[5]))] = 9

    county_color = county_color.tolist()

    return get_county_plot(
        fips=fips, values=county_color,
        colorscale=[f'rgb{rgb}' for rgb in list(colorscale.values())])
