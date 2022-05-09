import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import re
import warnings

df = pd.read_csv('Week1_challenge_data_source.csv')


class CleanDataframe:
    def __init__(self, df):
        self.df = df

    def check_missing_values(self):
        # Check the percentage of missing values in every column
        ax = self.df.isna().sum().sort_values().plot(kind='barh', figsize=(9, 12))
        plt.title('Percentage of Missing Values Per Column in XDR data', fontdict={'size': 15})

        for p in ax.patches:
            percentage = '{:,.3f}%'.format((p.get_width() / self.df.shape[0]) * 100)
            width, height = p.get_width(), p.get_height()
            x = p.get_x() + width + 0.02
            y = p.get_y() + height / 2
            ax.annotate(percentage, (x, y))

    def remove_missing_values(self):
        # Drop columns which have more than 25% missing values of the total data size

        missing_ratio = self.df.isna().sum() / self.df.shape[0]

        col_to_drop = missing_ratio[missing_ratio > 0.25].keys()

        self.df.drop(col_to_drop, axis=1, inplace=True)

        return self.df
