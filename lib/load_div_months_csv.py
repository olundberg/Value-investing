"""Load dividend months from csv file."""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.collections


def load_div_months_csv(filename):
    """Load dividend months."""
    df = pd.read_csv(filename)
    # Strip spaces
    df.columns = [col_name.strip() for col_name in df.columns]

    columns = list(df.columns)
    print(columns)
    df_return = pd.DataFrame(columns=['stock', 'month', 'div'])
    for idx, df_row in df.iterrows():
        stock = df_row[columns[0]]
        for idx in range(1, 13):
            month = columns[idx]
            div = df_row.values[idx]
            row = {'stock': stock,
                   'month': month,
                   'div': div}
            df_return = df_return.append(row, ignore_index=True)

    return df_return

def load_div_months_plot(df):
    """Return plot object."""
    rows, cols = 4, 3
    # Plot
    sns.set_style('darkgrid')
    g = sns.catplot(x="stock", y="div", col="month",
                    data=df, kind="bar", col_wrap=cols, sharex=False,
                    legend_out=False, margin_titles=True)
    g.set_xticklabels(rotation=45)
    # Remove 0 dividends
    n_stocks = len(df["stock"].unique())
    for idx, ax in enumerate(g.axes):
        # print("Ax: {}".format(idx))

        remove_idx = []
        for st_idx in range(n_stocks):
            bar = ax.containers[0][st_idx]
            div = bar.get_height()
            # print(div)
            if div == 0.0:
                remove_idx.append(st_idx)

        for r_idx in remove_idx:
            ax.containers[0][r_idx].remove()  # Remove bar
            ax.autoscale()  # Autoscale

        x_ticks = ax.get_xticks()  # Remove ticks
        x_ticks = [idx for idx in x_ticks if idx not in remove_idx]
        x_labels = []
        for i in x_ticks:
            x_labels.append(ax.get_xticklabels()[i].get_text())

        ax.set_xticks(x_ticks)  # Set new ticks
        ax.set_xticklabels(x_labels)
        plt.subplots_adjust(hspace=0.6)

    return plt


def load_div_months_csv_2(filename):
    """Load dividend months."""
    df = pd.read_csv(filename)

    # Strip spaces
    df.columns = [col_name.strip() for col_name in df.columns]

    return df

def load_div_months_plot_2(df):
    """New function to present monthly dividends."""
    sns.set_style('darkgrid')
    rows, cols = 3, 4
    months = ['jan', 'feb', 'mar',
              'apr', 'may', 'jun',
              'jul', 'aug', 'sep',
              'okt', 'nov', 'dec']

    fig, ax = plt.subplots(rows, cols, figsize=(20, 15))
    # Loop over rows and cols
    k = 0
    for i in range(rows):
        for j in range(cols):
            df_tmp = df[['stock', months[k]]]
            df_tmp = df_tmp[(df_tmp != 0).all(1)]
            sns.barplot(x='stock', y=months[k], data=df_tmp, ax=ax[i, j])
            ax[i, j].set_title(months[k])
            ax[i, j].xaxis.label.set_visible(False)
            k = k + 1

    for ax in fig.axes:
        plt.sca(ax)
        plt.xticks(rotation=30, ha='center')

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.6)
    return plt


if __name__ == '__main__':
    """Test."""
    file = "dividend_months.csv"
    df_test = load_div_months_csv_2(file)
    print(df_test.head())
    #plot_obj = load_div_months_plot(df_test)
    plot_obj = load_div_months_plot_2(df_test)
    plot_obj.show()
