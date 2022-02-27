import matplotlib.pyplot as plt
# from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
# from plotly import graph_objs as go
import pandas as pd
import numpy as np
# init_notebook_mode(connected=True)


def simple_graph(list_par, x_line=range(10)):
    for par in list_par:
        plt.plot(x_line, par)
    plt.grid()
    plt.show()


# def plotly_df(df, title=''):
#     data = []
#
#     for column in df.columns:
#         trace = go.Scatter(
#             x = df.index,
#             y = df[column],
#             mode = 'lines',
#             name = column
#         )
#         data.append(trace)
#
#     layout = dict(title = title)
#     fig = dict(data = data, layout = layout)
#     iplot(fig, show_link=False)
