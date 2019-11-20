"""
This module takes the data and generates different graphs and reports
"""

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy


class Visualisation():

    def load_data(self, gaz_list):

        self.x = list()
        self.y = list()

        for datum in gaz_list:
            self.x.append(datum.get_date())
            self.y.append(datum.get_money_spent())

    def generate_plot(self):

        plt.plot_date(self.x, self.y, ".b")
        plt.show(block=False)
