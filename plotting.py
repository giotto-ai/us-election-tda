import utils
from giotto.mapper import visualize


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

    return visualize.create_network_2d(graph, data, layout, node_color,
                                       columns_to_color=columns_to_color,
                                       plotly_kwargs=plotly_kwargs)
