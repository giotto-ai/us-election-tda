import utils
import numpy as np
from giotto.mapper import visualize


def get_graph_plot_colored_by_winner(graph, year, df, pos=None):
    node_elements = graph['node_metadata']['node_elements']

    if pos is None:
        pos = graph.layout('kamada_kawai')

    node_color = utils.get_node_summary(node_elements,
                                        df[df['year'] == year]['winner']
                                        .values,
                                        summary_stat=np.mean)

    node_text = utils.get_node_text(
        dict(zip(range(len(node_elements)),
                 node_elements)),
        utils.get_n_electors(node_elements,
                             df[df['year'] == year]['n_electors']
                             .reset_index(drop=True)),
        node_color,
        'Number of Counties Won by Republicans')

    custom_plot_options = {
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

    return visualize.create_network_2d(graph, pos, node_color,
                                       custom_plot_options=custom_plot_options)
