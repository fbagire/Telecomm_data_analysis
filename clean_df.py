import pandas as pd
import matplotlib.pyplot as plt


class CleanDataframe:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def check_missing_values(self):
        """"
            This function takes the dataframe and calculate the percentage of missing values in every column
            returns an horizontal bar plot with columns with many missing values at the top
        """

        # Check the percentage of missing values in every column
        ax = self.df.isna().sum().sort_values().plot(kind='barh', figsize=(9, 12))
        plt.title('Percentage of Missing Values Per Column in XDR data', fontdict={'size': 15})

        for p in ax.patches:
            percentage = '{:,.3f}%'.format((p.get_width() / self.df.shape[0]) * 100)
            width, height = p.get_width(), p.get_height()
            x = p.get_x() + width + 0.02
            y = p.get_y() + height / 2
            ax.annotate(percentage, (x, y))
        plt.show()

    def drop_unwanted_columns(self):
        # Drop columns which have more than 25% missing values of the total data size

        missing_ratio = self.df.isna().sum() / self.df.shape[0]

        col_to_drop = missing_ratio[missing_ratio > 0.25].keys().to_list()
        col_to_drop.append('Dur. (ms).1')
        self.df.drop(col_to_drop, axis=1, inplace=True)

        return self.df

    def fix_data_types(self):
        self.df['Handset Manufacturer'] = self.df['Handset Manufacturer'].astype('str',
                                                                                 errors='ignore').str.capitalize()
        self.df['Handset Type'] = self.df['Handset Type'].astype('str', errors='ignore').str.capitalize()
        return self.df

    def convert_bytes_to_megabytes(self, bytes_data):
        """
            This function takes the dataframe and the column which has the bytes values
            returns the megabytes of that value

            Args:
            -----
            self.df: dataframe
            bytes_data: column with bytes values

            Returns:
            --------
            A converted original dataframe
        """
        megabyte = 1 * 10e+5
        self.df[bytes_data] = self.df[bytes_data] / megabyte

        return self.df

    def fill_missing_values(self, cols_numeric=None, cols_cat=None):
        """
            separating columns based on datatype
            Filling in missing values using mean value or median value depending on the previous histogram and skewness

            parameters
            ----------
            cols_numeric: A list of numerical columns
            cols_cat:    a list of categorical columns

            Returns
            -------
            DataFrame
        """
        if cols_cat is None:
            cols_cat = []
        if cols_numeric is None:
            cols_numeric = []
        for col in cols_numeric:
            if self.df[col].skew() >= 1 or self.df[col].skew() <= -1:
                self.df[col] = self.df[col].fillna(self.df[col].median())
            else:
                self.df[col] = self.df[col].fillna(self.df[col].mean())

        self.df[cols_cat] = self.df[cols_cat].fillna('Undefined')

        return self.df
