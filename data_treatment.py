import streamlit as st
from tqdm import tqdm
from sklearn.neighbors import KernelDensity
from arch import arch_model
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
from pandas_datareader import data as web
from math import sqrt
import pandas as pd
import numpy as np
import warnings
# we want to not print any warnings
# warnings.simplefilter(action='ignore', category=FutureWarning)


def garch(returns):
    # feed in data until date
    gjr_gm = arch_model(returns, p=1, q=1, o=1,
                        vol='GARCH', dist='t', rescale=False)

    # Fit the model
    gjrgm_result = gjr_gm.fit(update_freq=1, disp='off')

    # Forecast volatilities 1-20 for Working days (1 month)
    gjr_forecast = gjrgm_result.forecast(horizon=1)

    # these are the initial inputs for every simulation cycle
    # rescale with 10000, that's the factor for std to return
    sigma = sqrt(gjr_forecast.variance["h.1"].iloc[-1] / 10000)
    mu = gjr_forecast.mean["h.1"].iloc[-1]

    return_list = returns.to_numpy()  # turn the pd column into an array

    return sigma, mu, gjrgm_result, return_list


def garch_volatility(result, currency, start_date, end_date):
    # PLOT GARCH VOL
    ###############

    # annualized list of vols to plot
    vol = sqrt(250)*result.conditional_volatility

    fig, ax = plt.subplots(figsize=(15, 5))

    # Plot GJR-GARCH estimated volatility | only cosmetics for plit
    ax.plot(vol, color='black', label='GJR-GARCH Volatility')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())

    ax.set_xlabel('Date')
    ax.set_ylabel(currency + ' Return Volatility')
    ax.set_title("Asymmetric GARCH model from " +
                 start_date + " until " + end_date)

    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.25))

    st.pyplot(fig)

# Return Monte Carlo Simulation
#############################


def monte_carlo_simulation(return_list, mu, sigma, n, currency):
    monthly_return_list = []

    for i in tqdm(range(n)):

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
            gjr_gm = arch_model(return_list, p=1, q=1, o=1,
                                vol='GARCH', dist='t', rescale=False)
            gjrgm_result = gjr_gm.fit(
                update_freq=1, disp='off', show_warning=False)
            gjr_forecast = gjrgm_result.forecast(horizon=1)
            sigma_ = sqrt(
                gjr_forecast.variance["h.1"].iloc[-1] / 10000)  # rescale

        monthly_return = states[-1]/states[0]-1  # compute monthly return
        # append to our final list of returns
        monthly_return_list.append(monthly_return)

    df = np.asarray(monthly_return_list)  # turn list into array
    df = df[np.isfinite(df)]  # remove inf and nan, should not happen though
    average_percent = str(round(100 * np.mean(df), 2))

    print("The on average forecasted return of " + currency +
          " over the next month is " + average_percent + "%")
    return df

# We now plot our returns applying a kernel density | It's up to us how we do that
##################################################


def density_plot(df, n, currency):

    # we need to turn the list into a 2D array to plot them
    returns = df.reshape(-1, 1)

    X_plot = np.linspace(-.2, .2, 1000)[:, np.newaxis]
    bins = np.linspace(-.2, .2, 50)

    std = np.std(returns)

    # get the bandwidth #n is defined on top and is the nr of repetitions
    bandwidth = 0.9 * n**(-1/5) * std

    kde = KernelDensity(kernel='gaussian', bandwidth=bandwidth).fit(
        returns)  # fit the kernel
    kde_score_samples = kde.score_samples(X_plot)

    fig, ax = plt.subplots(1, 2, figsize=(15, 5), sharex=True, sharey=False)
    fig.subplots_adjust(hspace=0.1, wspace=0.1)

    ax[0].hist(returns[:, 0], bins=bins, color="black",
               label="return distribution")
    ax[1].plot(X_plot[:, 0], np.exp(kde_score_samples),
               color="black", label="smoothed distribution")

    ax[0].set_xlabel(currency + " next period return")
    ax[0].set_ylabel('Returns per Bin')
    ax[0].set_title("Return Density Historgram")

    ax[1].set_xlabel(currency + " next period return")
    ax[1].set_ylabel('Probability Density')
    ax[1].set_title("Return Density Function")

    ax[0].legend(loc="lower center", bbox_to_anchor=(0.5, -0.3))
    ax[1].legend(loc="lower center", bbox_to_anchor=(0.5, -0.3))

    st.pyplot(fig)
