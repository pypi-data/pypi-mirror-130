import numpy as np


def create_univariate_windows(df, train_horizon, pred_horizon, column=None):
    """Given a dataframe or raw data sequence, this will create deep learning friendly
    matrices (X, y) with a given training and prediction length.

    Args:
        df (array_like): raw data potentially with column names if a full dataframe
        train_horizon (int): number of data points in each training observation of the X matrix
        pred_horizon (int): number of data points in each prediction observation of the y matrix
        column (str, optional): column to use if df is a pandas dataframe. Defaults to None.
    """
    # number of windows
    num_windows = df.shape[0] - train_horizon - pred_horizon + 1

    # allocate memory to numpy
    X = np.zeros([num_windows, train_horizon, 1])
    y = np.zeros([num_windows, pred_horizon])

    # create numpy object
    if column is not None:
        raw_data = df[[column]].to_numpy()
    else:
        raw_data = np.array(df)

    # loop through the windows
    for i in range(num_windows):

        # store X and Y information
        X[i] = raw_data[i: i + train_horizon]
        y[i] = raw_data[i + train_horizon: i + train_horizon + pred_horizon].reshape(1, -1)[0]

    return X, y


def create_multivariate_windows(df, train_horizon, pred_horizon, train_columns=None, pred_columns=None):
    """Given a dataframe or raw data sequence with more than one dimension in time,
     this will create deep learning friendly matrices (X, y) with a given training
     and prediction length. If not columns are provided, the whole matrix will be used
     as the training and prediction set.

    Args:
        df (array_like): raw data potentially with column names if a full dataframe (>1d in time)
        train_horizon (int): number of data points in each training observation of the X matrix
        pred_horizon (int): number of data points in each prediction observation of the y matrix
        train_columns (list, optional): list of columns to use from dataframe for training matrices.
            Defaults to None.
        pred_columns (list, optional): list of columns to use from dataframe for prediction matrices.
            Defaults to None.
    """
    # number of windows
    num_windows = df.shape[0] - train_horizon - pred_horizon + 1

    # create numpy object
    if train_columns is not None:
        raw_X_data = df[train_columns].to_numpy()
        raw_y_data = df[pred_columns].to_numpy()
    else:
        raw_X_data = np.array(df)
        raw_y_data = np.array(df)

    # allocate memory to numpy
    X = np.zeros([num_windows, train_horizon, raw_X_data.shape[1]])
    y = np.zeros([num_windows, pred_horizon, raw_y_data.shape[1]])

    # loop through the windows
    for i in range(num_windows):

        # store X and Y information
        X[i] = raw_X_data[i: i + train_horizon]
        y[i] = raw_y_data[i + train_horizon: i + train_horizon + pred_horizon]

    return X, y
