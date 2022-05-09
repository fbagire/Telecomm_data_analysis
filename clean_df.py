import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import re
import warnings


df = pd.read_csv('Week1_challenge_data_source.csv')

print(df.shape)
df.head()

all_cols = df.columns.to_list()

# Check the percentage of missing values in every column
ax = df.isna().sum().sort_values().plot(kind='barh', figsize=(9, 12))
plt.title('Percentage of Missing Values Per Column in XDR data', fontdict={'size': 15})

for p in ax.patches:
    percentage = '{:,.3f}%'.format((p.get_width() / df.shape[0]) * 100)
    width, height = p.get_width(), p.get_height()
    x = p.get_x() + width + 0.02
    y = p.get_y() + height / 2
    ax.annotate(percentage, (x, y))


def removeMissingvalues(df: pd.DataFrame) -> pd.DataFrame:
    missing_ratio = df.isna().sum() / df.shape[0]

    # Below code gives list of columns having more than 25% nan
    col_to_drop = missing_ratio[missing_ratio > 0.25].keys()

    df.drop(col_to_drop, axis=1, inplace=True)

    return df


df = removeMissingvalues(df)

df
