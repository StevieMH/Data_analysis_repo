import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'medical_examination.csv')

# 1
df = pd.read_csv(csv_path)

# 2
df['overweight'] = (
    (df['weight'] / (df['height'] / 100) ** 2) > 25).astype(int)

# 3
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)


# 4

def draw_cat_plot():
    # 5
    df_cat = pd.melt(df, id_vars=['id'], value_vars=['cholesterol', 'gluc', 'smoke',
                     'alco', 'active', 'overweight'], var_name='variable', value_name='value')

    # 6
    df_cat = df_cat.merge(df[['id', 'cardio']], on='id')
    df_grouped = df_cat.groupby(
        ['cardio', 'variable', 'value']).size().reset_index(name='total')

    # 7
    g = sns.catplot(
        data=df_grouped,
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        kind='bar',
        height=4,
        aspect=1
    )

    g.set_titles("Cardio = {col_name}")
    g.set_axis_labels("variable", "total")
    # g.set_xticklabels(rotation=45)
    plt.tight_layout()

    # 8
    fig = g.fig

    # 9
    fig.savefig(os.path.join(script_dir, 'catplot.png'))
    return fig


# 10
def draw_heat_map():
    # 11
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 12
    corr = df_heat.corr()

    # 13
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14
    fig, ax = plt.subplots(figsize=(12, 10))

    # 15
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt='.1f',
        center=0,
        cmap='coolwarm',
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.5},
        ax=ax
    )

    # 16
    fig.savefig(os.path.join(script_dir, 'heatmap.png'))
    return fig
