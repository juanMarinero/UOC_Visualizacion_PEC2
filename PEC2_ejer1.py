#!/usr/bin/env python3

#  vim: set foldmethod=indent foldcolumn=4 :

import seaborn as sns
import matplotlib.pyplot as plt

def get_df():
    return sns.load_dataset('iris')

def plot_PairGrid(df, figsize=(15, 15)):

    g = sns.PairGrid(df,
                     hue = "species",
                     palette="Set2",
                     height=3,
                     aspect=2)

    g.map_upper(sns.scatterplot, s=5)
    g.map_lower(sns.kdeplot, levels=3, common_norm=False, alpha=.8, warn_singular=False)
    g.map_diag(sns.histplot)

    g.fig.set_size_inches(figsize)
    g.add_legend();
    plt.show()

def main():

    df = get_df()
    plot_PairGrid(df)


if __name__ == "__main__":
    main()
