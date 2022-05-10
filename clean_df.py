import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import re
import warnings


class CleanDataframe:
    def __init__(self, df: pd.DataFrame):
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

    def drop_unwanted_columns(self):
        # Drop columns which have more than 25% missing values of the total data size

        missing_ratio = self.df.isna().sum() / self.df.shape[0]

        col_to_drop = missing_ratio[missing_ratio > 0.25].keys()

        self.df.drop(col_to_drop, axis=1, inplace=True)

        return self.df

    def fix_data_types(self):
        self.df['Handset Manufacturer'] = self.df['Handset Manufacturer'].astype('str',
                                                                                 errors='ignore').str.capitalize()
        self.df['Handset Type'] = self.df['Handset Type'].astype('str', errors='ignore').str.capitalize()
        return self.df

    def fill_missing_values(self):
        # separating columns based on datatype
        cols_numeric = self.df.columns.difference(['Bearer Id', 'Start', 'End', 'IMSI', 'MSISDN/Number',
                                                   'IMEI', 'Last Location Name',
                                                   'Handset Manufacturer', 'Handset Type']).to_list()
        cols_cat = ['Handset Manufacturer', 'Handset Type']
        # Filling in missing values using mean value or median value depending on the previous histogram and skeweness

        for col in cols_numeric:
            if self.df[col].skew() >= 1 or self.df[col].skew() <= -1:
                self.df[col] = self.df[col].fillna(self.df[col].median())
            else:
                self.df[col] = self.df[col].fillna(self.df[col].median())

        self.df[cols_cat] = self.df[cols_cat].fillna('Undefined')

        return self.df

# if __name__ == "__main__":
# df_original = pd.read_excel('Week1_challenge_data_source.xlsx',
#                             dtype={'Bearer Id': str, 'IMSI': str, 'MSISDN/Number': str, 'IMEI': str,
#                                    'Handset Manufacturer': str, 'Handset Type': str}, engine='openpyxl')
# cleaner = CleanDataframe(df_original)
