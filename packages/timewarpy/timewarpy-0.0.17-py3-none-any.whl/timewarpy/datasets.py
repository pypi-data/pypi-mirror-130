import pandas as pd


def load_energy_data():
    """Loads a multi-variate time series dataset from the timewarpy library
    for energy usage forecasting.

    More information can be found [here](https://archive.ics.uci.edu/ml/datasets/Appliances+energy+prediction)

    Returns:
        pandas.DataFrame: time series dataset
    """
    return pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/00374/energydata_complete.csv')
