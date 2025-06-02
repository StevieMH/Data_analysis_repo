import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import os

register_matplotlib_converters()


script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'fcc-forum-pageviews.csv')

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv(csv_path, parse_dates=['date'], index_col='date')

# Clean data
df = df[(df['value'] > df['value'].quantile(0.025)) &
        (df['value'] < df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(18, 6))
    ax.plot(df.index, df['value'], color='red',  linestyle='-')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.grid(False)
    plt.xticks(rotation=0)
    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig(os.path.join(script_dir, 'line_plot.png'))
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    # Draw bar plot
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    df_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']

    df_grouped = df_grouped[month_order]

    fig, ax = plt.subplots(figsize=(14, 7))

    df_grouped.plot(kind='bar', ax=ax)

    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months', loc='upper left')
    ax.set_title('Average Daily Page Views for Each Month Grouped by Year')
    plt.xticks(rotation=0)
    plt.tight_layout()
    # Save image and return fig (don't change this part)
    fig.savefig(os.path.join(script_dir, 'bar_plot.png'))
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots using matplotlib (avoids seaborn/numpy compatibility issue)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Year-wise Box Plot (Trend)
    years = sorted(df_box['year'].unique())
    year_data = [df_box[df_box['year'] == year]
                 ['value'].values for year in years]

    box1 = axes[0].boxplot(year_data, labels=years, patch_artist=True)
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Color the year boxes (optional, for better appearance)
    colors = ['lightblue', 'lightgreen',
              'lightcoral', 'lightyellow', 'lightpink']
    for patch, color in zip(box1['boxes'], colors[:len(box1['boxes'])]):
        patch.set_facecolor(color)

    # Month-wise Box Plot (Seasonality)
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Get data for each month in order (only for months that exist in data)
    month_data = []
    month_labels = []
    for month in month_order:
        if month in df_box['month'].values:
            month_data.append(df_box[df_box['month'] == month]['value'].values)
            month_labels.append(month)

    box2 = axes[1].boxplot(month_data, labels=month_labels, patch_artist=True)
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Color the month boxes (optional, for better appearance)
    month_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b',
                    '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#aec7e8', '#ffbb78']
    for patch, color in zip(box2['boxes'], month_colors[:len(box2['boxes'])]):
        patch.set_facecolor(color)

    # Adjust layout to prevent overlapping
    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig(os.path.join(script_dir, 'box_plot.png'))
    return fig
