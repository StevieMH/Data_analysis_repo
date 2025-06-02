import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import os


def draw_plot():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'epa-sea-level.csv')

    # Read data from file
    df = pd.read_csv(csv_path)

    # Create scatter plot
    fig, ax = plt.subplots(figsize=(16, 6))

    ax.scatter(df['Year'], df['CSIRO Adjusted Sea Level'])

    # Create first line of best fit
    slope1, intercept1, * \
        _ = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    x_all = pd.Series(range(1880, 2051))
    y_all = slope1 * x_all + intercept1
    ax.plot(x_all, y_all, 'r', label='Best Fit Line (All Data)')

    # Create second line of best fit
    df_2000 = df[df['Year'] >= 2000]
    slope2, intercept2, * \
        _ = linregress(df_2000['Year'], df_2000['CSIRO Adjusted Sea Level'])
    x_2000 = pd.Series(range(2000, 2051))
    y_2000 = slope2 * x_2000 + intercept2
    ax.plot(x_2000, y_2000, 'g', label='Best Fit Line (2000–2022)')

    # Add labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('Sea Level (inches)')
    ax.set_title('Rise in Sea Level')
    ax.legend()
    ax.grid(True)

    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()
