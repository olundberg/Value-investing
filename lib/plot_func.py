"""Return plot object for various things."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_function(df, plot_type='Yield'):
    """Return plot object of relevant plot_type."""
    if plot_type == 'Price':
        # Plot prices
        plt.figure()
        plt.plot(20, 20)
        plt.title('x')
        plt.xlabel('x')
        plt.ylabel('y')
    elif plot_type == 'test':
        # Plot yield
        plt.figure()
        plt.plot(2, 2)
        plt.title('x')
        plt.xlabel('x')
        plt.ylabel('y')
    elif plot_type == 'test':
        plt.figure()
        plt.plot(2, 2)
        plt.title('x')
        plt.xlabel('x')
        plt.ylabel('y')
    return plt


if __name__ == '__main__':
    asdf = plot_function(1, plot_type='test')
    asdf.show()
