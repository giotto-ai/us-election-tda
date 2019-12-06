import networkx as nx
import numpy as np
import plotly.figure_factory as ff

import plotly.graph_objects as go
from functools import reduce
import operator


def mapper_nx_plot(mapper, node_color=None, cmap='autumn',
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


def mapper_plotly_plot(graph, pos, size, node_color, node_text,
                       colorscale='RdBu', cmin=0, cmax=1, legend_title=''):
    edge_x = list(reduce(operator.iconcat,
                  map(lambda x: [pos[x[0]][0],
                                 pos[x[1]][0], None],
                      graph.edges()), []))
    edge_y = list(reduce(operator.iconcat,
                  map(lambda x: [pos[x[0]][1],
                                 pos[x[1]][1], None],
                      graph.edges()), []))

    edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

    node_x = list(map(lambda x: pos[x][0], range(len(pos))))
    node_y = list(map(lambda x: pos[x][1], range(len(pos))))

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale=colorscale,
            reversescale=True,
            line=dict(width=.5, color='#888'),
            color=node_color,
            size=size,
            cmin=cmin,
            cmax=cmax,
            colorbar=dict(
                thickness=15,
                title=legend_title,
                xanchor='left',
                titleside='right'
            ),
            line_width=2),
        text=node_text)

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(showlegend=False,
                                     hovermode='closest',
                                     margin={'b': 20, 'l': 5, 'r': 5, 't': 40},
                                     xaxis=dict(showgrid=False, zeroline=False,
                                                showticklabels=False, ticks="",
                                                showline=False),
                                     yaxis=dict(showgrid=False, zeroline=False,
                                                showticklabels=False, ticks="",
                                                showline=False),
                                     xaxis_title="",
                                     yaxis_title=""))
    fig.update_layout(template='simple_white')
    fig.show()


def mapper_plotly_3dplot(graph, pos, size, node_color, node_text,
                         colorscale='RdBu', cmin=0, cmax=1,
                         legend_title=''):

    edge_x = list(reduce(operator.iconcat,
                  map(lambda x: [pos[x[0]][0],
                                 pos[x[1]][0], None],
                      graph.edges()), []))
    edge_y = list(reduce(operator.iconcat,
                  map(lambda x: [pos[x[0]][1],
                                 pos[x[1]][1], None],
                      graph.edges()), []))

    edge_z = list(reduce(operator.iconcat,
                  map(lambda x: [pos[x[0]][2],
                                 pos[x[1]][2], None],
                      graph.edges()), []))

    edge_trace = go.Scatter3d(x=edge_x,
                              y=edge_y,
                              z=edge_z,
                              mode='lines',
                              line=dict(color='rgb(125,125,125)',
                                        width=1),
                              hoverinfo='none')

    node_x = list(map(lambda x: pos[x][0], range(len(pos))))
    node_y = list(map(lambda x: pos[x][1], range(len(pos))))
    node_z = list(map(lambda x: pos[x][2], range(len(pos))))

    node_trace = go.Scatter3d(
        x=node_x,
        y=node_y,
        z=node_z,
        mode='markers',
        marker=dict(
            showscale=True,
            colorscale=colorscale,
            reversescale=True,
            line=dict(width=.5, color='#888'),
            color=node_color,
            size=size,
            cmin=cmin,
            cmax=cmax,
            colorbar=dict(
                thickness=15,
                title=legend_title,
                xanchor='left',
                titleside='right'
            ),
            line_width=2),
        text=node_text,
        hoverinfo='text')

    axis = dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title='')

    layout = go.Layout(
        title="",
        width=1000,
        height=1000,
        showlegend=False,
        scene=dict(xaxis=dict(axis),
                   yaxis=dict(axis),
                   zaxis=dict(axis)),
        margin=dict(
            t=100
        ),
        hovermode='closest',
        annotations=[])

    data = [edge_trace, node_trace]
    fig = go.Figure(data=data, layout=layout)

    fig.show()
