import streamlit as st
from tqdm import tqdm
from sklearn.neighbors import KernelDensity
from arch import arch_model
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
from math import sqrt
import pandas as pd
import numpy as np
import warnings
from stqdm import stqdm

# we want to not print any warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


class DataTreatment:
    def __init__(self, data_retriever, model, n, currency, start_date, end_date):

        # DataRetriever object
        self.data = data_retriever

        # Variables for model and simulation
        self.model = model
        self.n = n

        # Needed variables for DataRetriever class
        self.currency = currency
        self.start_date = start_date
        self.end_date = end_date

        # Get historical returns data using our DataRetriever class
        self.returns = self.data.get_market_data(
            currency, start_date, end_date)

    def create_model(self):

        if self.model == 'GARCH':
            model = arch_model(self.returns, p=1, o=0, q=1,
                               vol='GARCH', dist="t", rescale=False)
        elif self.model == 'ARCH':
            model = arch_model(self.returns, mean='Zero', vol='ARCH', p=15)
        elif self.model == 'HARCH':
            model = arch_model(self.returns, mean='AR', lags=2,
                               vol='HARCH', p=[1, 5, 22])

        return model

    def find_volatility(self):

        model = self.create_model()

        volatility_result = model.fit(update_freq=1, disp='off')

        return volatility_result

    def create_forecast(self):

        volatility_result = self.find_volatility()
        forecast = volatility_result.forecast(horizon=1)

        return forecast

    def set_variables(self):

        forecast = self.create_forecast()

        self.sigma = sqrt(forecast.variance["h.1"].iloc[-1] / 10000)
        self.mu = forecast.mean["h.1"].iloc[-1]
        self.return_list = self.returns.to_numpy()

    def get_variables(self):
        return self.sigma, self.mu, self.return_list

    def monte_carlo_simulation(self):

        sigma, mu, return_list = self.get_variables()
        monthly_return_list = []

        for i in stqdm(range(self.n), desc="Running simulation... Please do not refresh the window"):

            # open the list to append all the values from one iteration
            states = []

            for j in range(30):  # we need to forecast 30 days with crypto

                # one day innovation
                epsilon = np.random.normal(0, 1)  # random number

                # Determine States 1-30
                # time varying sigma multiplied with innvoation for state
                state = np.exp(mu + epsilon*sigma)
                states.append(state)  # pack elements into states list
                state_return = (state-1) * 100  # upscale to plug it back in
                return_list = np.append(
                    return_list, np.array([state_return]), axis=0)

                # apply the GARCH again, this simulates the next sigma based on all the past returns including the one estimated above

                gm = self.create_model()

                gjrgm_result = gm.fit(
                    update_freq=1, disp='off', show_warning=False)
                gjr_forecast = gjrgm_result.forecast(horizon=1)
                sigma_ = sqrt(
                    gjr_forecast.variance["h.1"].iloc[-1] / 10000)  # rescale

            monthly_return = states[-1] / states[0]-1  # compute monthly return
            # append to our final list of returns
            monthly_return_list.append(monthly_return)

        monte_carlo_dataframe = np.asarray(
            monthly_return_list)  # turn list into array
        # remove inf and nan, should not happen though
        monte_carlo_dataframe = monte_carlo_dataframe[np.isfinite(
            monte_carlo_dataframe)]
        average_percent = str(round(100 * np.mean(monte_carlo_dataframe), 2))

        return monte_carlo_dataframe, average_percent
