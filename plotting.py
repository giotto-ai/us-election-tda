import plotly.figure_factory as ff


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
