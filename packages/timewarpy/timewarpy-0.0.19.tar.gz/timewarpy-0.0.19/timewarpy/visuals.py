from matplotlib import pyplot as plt
import numpy as np
from timewarpy import preprocess, datasets

plt.rcParams.update({'font.size': 14})

# ------------------------------ Single Example ------------------------------ #

# retrive data and preprocess
df = datasets.load_energy_data()
train_horizon = 100
pred_horizon = 10
column = 'Appliances'
X, y = preprocess.create_univariate_windows(
    df, train_horizon, pred_horizon, column
)

# plot example time series
fig, ax = plt.subplots(figsize=(10, 4))
y_plot = X[0][:].T[0]
x_plot = np.arange(y_plot.shape[0])
y_plot_pred = y[0]
x_plot_pred = np.arange(y_plot_pred.shape[0]) + max(x_plot) + 1
ax.plot(x_plot, y_plot, 'k--', label='training vector')
ax.plot(x_plot_pred, y_plot_pred, 'r', label='prediction vector')
ax.legend()
ax.set_title('Example Univariate Time Series Manipulation')
ax.set_ylabel('Energy Consumption (Wh)')
ax.set_xlabel('Time (10 min)')
fig.tight_layout()
fig.savefig('../docs/img/examples/univariate_single.png', dpi=200)

# ------------------------------ Multiple Example ------------------------------ #

# initialize
windows = 7
full_time_series = X[0][:].T[0]

# make plot and add to it
fig, ax = plt.subplots(windows + 1, 1, figsize=(10, windows*1.8), sharex=True)

# roll windows
for w in range(windows):

    # get data points
    y_plot = X[w][:].T[0]
    x_plot = np.arange(y_plot.shape[0]) + w
    y_plot_pred = y[w]
    x_plot_pred = np.arange(y_plot_pred.shape[0]) + max(x_plot) + 1

    # append to main time series
    full_time_series = np.append(full_time_series, [y_plot_pred[0]])
    if w+1 == windows:
        full_time_series = np.append(full_time_series, y_plot_pred)

    # plot individual values
    ax[w].plot(x_plot, y_plot, 'k--', label=f'training vector {w+1}')
    ax[w].plot(x_plot_pred, y_plot_pred, 'r', label=f'prediction vector {w+1}')
    ax[w].set_xlim([0, 120])
    ax[w].set_ylim([0, 610])
    ax[w].set_ylabel(f'Roll #{w+1}')

# plot full time series
ax[-1].plot(full_time_series, 'k--')
ax[-1].set_title('Full Time Series')
fig.tight_layout()
fig.savefig('../docs/img/examples/univariate_multiple.png', dpi=200)
