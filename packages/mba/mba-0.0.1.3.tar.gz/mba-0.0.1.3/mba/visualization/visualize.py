import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

from mba.config.core import config
from mba.processing.data_management import read_data_csv


class TransactionPlot(object):
    def __init__(self):
        self.df_transaction = read_data_csv(config.data_config.data_filename)

    def transactions_per_day_plot(self, show=False):
        """number of transactions per day graph plot"""

        dow_freq = self.df_transaction[
            config.data_config.day_of_week].value_counts()
        dow_freq = dict(dow_freq)

        dow = list(dow_freq.keys())
        count = list(dow_freq.values())

        data = go.Bar(x=dow,
                      y=count,
                      name='Order Count by Day of Week',
                      marker_color=dow,
                      text=count,
                      textposition='outside')

        layout = go.Layout(title="Transactions per day",
                           title_x=0.5,
                           xaxis=dict(title_text='Day of Week',
                                      showgrid=False),
                           yaxis=dict(title_text='Count', showgrid=False))

        fig = go.Figure(data=data, layout=layout)
        if show:
            fig.show()

        return fig

    def transactions_per_hour_plot(self, show=False):
        """number of transactions per hour graph plot"""
        fig = go.Figure()
        if show:
            fig.show()
        return fig


if __name__ == '__main__':
    pass