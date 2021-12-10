import matplotlib.pyplot as plt

from sklearn.neighbors import KernelDensity
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st
from math import factorial, sqrt


class GraphCreator:

    def __init__(self, data_treatment, currency, start_date, end_date):
        self.data_treatment = data_treatment
        self.currency = currency
        self.start_date = start_date
        self.end_date = end_date

        # Reading values for graphs
        self.volatility_results = self.data_treatment.find_volatility()
        self.dataframe, self.avg_return = self.data_treatment.monte_carlo_simulation()

    def volatility_plot(self):
        vol = sqrt(250) * self.volatility_results.conditional_volatility
        fig, ax = plt.subplots(figsize=(15, 5))

        # Plot estimated volatility, setting colors, labels and title
        ax.plot(vol, color='#00B7C2',
                label=self.data_treatment.model + ' Volatility')
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())

        ax.set_xlabel('Date', color="white")
        ax.set_ylabel(self.currency + ' Return Volatility',
                      color='white')
        ax.set_title(self.data_treatment.model + " model from " +
                     self.start_date + " until " + self.end_date)

        ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.25))

        fig.set_facecolor("#1B262C")
        ax.set_facecolor("#1B262C")
        ax.title.set_color("white")
        ax.tick_params(colors="white")
        ax.spines['bottom'].set_color("white")
        ax.spines['left'].set_color("white")
        ax.spines['right'].set_color("#1B262C")
        ax.spines['top'].set_color("#1B262C")

        # Show the plot using Streamlit
        st.pyplot(fig)

    def density_plot(self):
        # Reshape the results of a Monte Carlo simulation into a 2D array
        returns = self.dataframe.reshape(-1, 1)

        x_plot = np.linspace(-.2, .2, 1000)[:, np.newaxis]
        bins = np.linspace(-.2, .2, 50)

        std = np.std(returns)

        # get the bandwidth #n is defined on top and is the nr of repetitions
        bandwidth = 0.9 * self.data_treatment.n**(-1/5) * std

        kde = KernelDensity(kernel='gaussian', bandwidth=bandwidth).fit(
            returns)  # fit the kernel
        kde_score_samples = kde.score_samples(x_plot)

        fig, ax = plt.subplots(1, 2, figsize=(
            15, 5), sharex=True, sharey=False)
        fig.subplots_adjust(hspace=0.1, wspace=0.1)

        ax[0].hist(returns[:, 0], bins=bins, color="#00B7C2",
                   label="return distribution")
        ax[1].plot(x_plot[:, 0], np.exp(kde_score_samples),
                   color="#00B7C2", label="smoothed distribution")

        # Setting labels and title
        ax[0].set_xlabel(self.currency + " next period return", color="white")
        ax[0].set_ylabel('Returns per Bin', color="white")
        ax[0].set_title("Return Density Historgram")

        # Setting labels and title for the density plot
        ax[1].set_xlabel(self.currency + " next period return", color="white")
        ax[1].set_ylabel('Probability Density', color="white")
        ax[1].set_title("Return Density Function")

        # Setting legends for each plot
        ax[0].legend(loc="lower center", bbox_to_anchor=(0.5, -0.3))
        ax[1].legend(loc="lower center", bbox_to_anchor=(0.5, -0.3))

        # Changing styling of the figure
        fig.set_facecolor("#1B262C")

        # Changing styling of the histogram
        ax[0].set_facecolor("#1B262C")
        ax[0].title.set_color("white")
        ax[0].tick_params(colors="white")
        ax[0].spines['bottom'].set_color("white")
        ax[0].spines['left'].set_color("white")
        ax[0].spines['right'].set_color("#1B262C")
        ax[0].spines['top'].set_color("#1B262C")

        # Changing styling of the density function plot
        ax[1].set_facecolor("#1B262C")
        ax[1].title.set_color("white")
        ax[1].tick_params(colors="white")
        ax[1].spines['bottom'].set_color("white")
        ax[1].spines['left'].set_color("white")
        ax[1].spines['right'].set_color("#1B262C")
        ax[1].spines['top'].set_color("#1B262C")

        # Show the plot using Streamlit
        st.pyplot(fig)

    def show_forecasted_return(self):
        # Show the forecasted average return using Streamlit
        st.metric("Forecasted Average Return", self.avg_return)
