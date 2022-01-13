import matplotlib


def set_plot_settings():
    font = {
        'family': 'sans-serif',
        'weight': 'normal',
        'size': 10,
    }
    matplotlib.rc('font', **font)

    axes = {
        'titlesize': 10,
    }
    matplotlib.rc('axes', **axes)
