import matplotlib.pyplot as plt

from sklearn.neighbors import KernelDensity
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st
from math import sqrt


class GraphCreator:
    def __init__(self, data_treatment, currency, start_date, end_date):
        self.data_treatment = data_treatment
        self.currency = currency
        self.start_date = start_date
        self.end_date = end_date

    def volatility_plot(self):
        volatility_results = self.data_treatment.find_volatility()

        vol = sqrt(250) * volatility_results.conditional_volatility

        fig, ax = plt.subplots(figsize=(15, 5))
        # Plot GJR-GARCH estimated volatility | only cosmetics for plit
        ax.plot(vol, color='black',
                label=self.data_treatment.model + ' Volatility')
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())

        ax.set_xlabel('Date')
        ax.set_ylabel(self.currency + ' Return Volatility')
        ax.set_title(self.data_treatment.model + " model from " +
                     self.start_date + " until " + self.end_date)

        ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.25))

        st.pyplot(fig)

    def density_plot(self):

        # Fetch the results of Monte Carlo simulation
        dataframe, avg_return = self.data_treatment.monte_carlo_simulation()

        # Reshape the results of a Monte Carlo simulation into a 2D array
        returns = dataframe.reshape(-1, 1)

        X_plot = np.linspace(-.2, .2, 1000)[:, np.newaxis]
        bins = np.linspace(-.2, .2, 50)

        std = np.std(returns)

        # get the bandwidth #n is defined on top and is the nr of repetitions
        bandwidth = 0.9 * self.data_treatment.n**(-1/5) * std

        kde = KernelDensity(kernel='gaussian', bandwidth=bandwidth).fit(
            returns)  # fit the kernel
        kde_score_samples = kde.score_samples(X_plot)

        fig, ax = plt.subplots(1, 2, figsize=(
            15, 5), sharex=True, sharey=False)
        fig.subplots_adjust(hspace=0.1, wspace=0.1)

        ax[0].hist(returns[:, 0], bins=bins, color="black",
                   label="return distribution")
        ax[1].plot(X_plot[:, 0], np.exp(kde_score_samples),
                   color="black", label="smoothed distribution")

        ax[0].set_xlabel(self.currency + " next period return")
        ax[0].set_ylabel('Returns per Bin')
        ax[0].set_title("Return Density Historgram")

        ax[1].set_xlabel(self.currency + " next period return")
        ax[1].set_ylabel('Probability Density')
        ax[1].set_title("Return Density Function")

        ax[0].legend(loc="lower center", bbox_to_anchor=(0.5, -0.3))
        ax[1].legend(loc="lower center", bbox_to_anchor=(0.5, -0.3))

        st.pyplot(fig)
