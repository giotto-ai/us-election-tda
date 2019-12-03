import networkx as nx
import numpy as np
import plotly.figure_factory as ff


def nx_plot_mapper(mapper, node_color=None, cmap='autumn',
                   node_size=None, pos=None, with_labels=False,
                   labels=None):
    nx.draw(mapper.complex._graph,
            node_color=node_color,
            cmap=cmap, vmin=np.min(node_color), vmax=np.max(node_color),
            node_size=node_size, pos=pos, with_labels=with_labels,
            labels=labels)


def county_plot(fips, values, colorscale=["#0000ff", "#ff0000"],
                legend_title='Republican/Democrat'):
    # https://plot.ly/python/county-choropleth/

    fig = ff.create_choropleth(fips=fips, values=values,
                               colorscale=colorscale,
                               show_state_data=False,
                               show_hover=True, centroid_marker={'opacity': 0},
                               asp=2.9, title='Election Outcome',
                               legend_title=legend_title)
    fig.layout.template = None
    fig.show()
