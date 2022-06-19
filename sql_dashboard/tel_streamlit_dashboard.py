import streamlit as st
import pandas as pd
import mysql.connector as mysql
import matplotlib.pyplot as plt

import plotly.express as px
import seaborn as sns
import pandas.io.sql as sqlio
import re


def plot_box_multi(df: pd.DataFrame, x_col: str, y_col: str, title: str, rot=0, figsize: tuple = (8, 5)) -> None:
    plt.figure(figsize=figsize)
    sns.boxplot(data=df, x=x_col, y=y_col)
    plt.title(title)
    plt.xticks(fontsize=14, rotation=rot)
    plt.yticks(fontsize=14)
    plt.show()


st.set_page_config(page_title="Tel Analysis Dashboard",
                   page_icon=":bar_chart:", layout="wide")
st.markdown("##")
st.markdown("<h1 style='text-align: center; color: grey;'>TellCo Analysis Dashboard</h1>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: white;'> by Faith Bagire </h3>", unsafe_allow_html=True)


# conn = mysql.connect(host='localhost', user='root', password='my_pass', database='tweets', buffered=True)
# cursor = conn.cursor()

# query = '''SELECT * FROM telcomdata'''


@st.cache
def read_data(path) -> pd.DataFrame:
    """"
        cached function to read the data since xlsx file takes too long to read
        :rtype: Dataframe
    """
    # df = sqlio.read_sql_query(query, conn)
    df = pd.read_excel(path,
                       dtype={'Bearer Id': str, 'IMSI': str, 'MSISDN/Number': str, 'IMEI': str,
                              'Handset Manufacturer': str, 'Handset Type': str}, engine='openpyxl')
    return df


# df = read_data(query, conn)
df = read_data("Week1_challenge_data_cleaned.xlsx")

hand_type = pd.DataFrame(df.query('`Handset Type`!="Undefined"')['Handset Type'].value_counts()[:10])
hand_manfact = pd.DataFrame(df.query('`Handset Manufacturer`!="Undefined"')['Handset Manufacturer'].value_counts()[:3])

colfig1, colfig2 = st.columns(2)

with colfig1:
    st.write("Top 10 handsets used by the customers")
    st.plotly_chart(px.bar(hand_type, x=hand_type.index, y='Handset Type', labels={'Handset Type': 'Handset Count'}))
with colfig2:
    st.write("Top 3 handset manufacturers")
    st.plotly_chart(
        px.bar(hand_manfact, x=hand_manfact.index, y='Handset Manufacturer', labels={'Handset Manufacturer': 'Count'}))

st.markdown('---')

col1, col2 = st.columns(2)
with col1:
    app_usage = df.groupby(by='MSISDN/Number').aggregate({'Social Media Total (megabytes)': 'sum',
                                                          'Email Total (megabytes)': 'sum',
                                                          'Google Total (megabytes)': 'sum',
                                                          'Youtube Total (megabytes)': 'sum',
                                                          'Netflix Total (megabytes)': 'sum',
                                                          'Gaming Total (megabytes)': 'sum',
                                                          'Other Total (megabytes)': 'sum'})
    app_usage = app_usage.aggregate(['sum'])

    app_plot = px.bar(app_usage.T, x=app_usage.T.index, title='Data volume used per Application',
                      y='sum', labels={'sum': 'Total data(UL+DL)(Mbs)', 'index': 'Application'})
    st.plotly_chart(app_plot)

with col2:
    df_manfact = df.query('`Handset Manufacturer`=="Apple" or `Handset Manufacturer`=="Samsung"\
                           or `Handset Manufacturer`=="Huawei"')
    df_manfact_goup = df_manfact.groupby(['Handset Manufacturer', 'Handset Type']).aggregate({'Handset Type': 'count'})

    tophandset = pd.DataFrame(
        df_manfact_goup['Handset Type'].groupby('Handset Manufacturer', group_keys=False).nlargest(5))
    st.write('Top 5 handset types from top 3 manufacturers')
    st.dataframe(tophandset.rename(columns={'Handset Type': 'Number of Handsets'})
                 )

st.markdown('---')

expe_df = df.groupby(by='MSISDN/Number').agg({'Avg RTT DL (ms)': 'mean', 'Avg RTT UL (ms)': 'mean',
                                              'Avg Bearer TP DL (kbps)': 'mean',
                                              'Avg Bearer TP UL (kbps)': 'mean',
                                              'Handset Manufacturer': 'unique'})
expe_df['Handset Manufacturer'] = expe_df['Handset Manufacturer'].apply(lambda x: x[0])


@st.cache
def read_orginal(path):
    df_og = pd.read_excel(path,
                          dtype={'Bearer Id': str, 'IMSI': str, 'MSISDN/Number': str, 'IMEI': str,
                                 'Handset Manufacturer': str, 'Handset Type': str}, engine='openpyxl')
    return df_og


df_original = read_orginal("Week1_challenge_data_source.xlsx")

tcp_data = df_original.groupby(by='MSISDN/Number', as_index=True).aggregate({'TCP DL Retrans. Vol (Bytes)': 'mean',
                                                                             'TCP UL Retrans. Vol (Bytes)': 'mean'})
expe_df = expe_df.merge(tcp_data, how='left', left_index=True, right_index=True)

devices_top = expe_df["Handset Manufacturer"].value_counts(sort=True, ascending=False)[:30]
devices_top = devices_top.to_dict()
devices_top.pop('Undefined')
devices_df = expe_df[expe_df['Handset Manufacturer'].apply(lambda x: True if x in devices_top.keys() else False)]

# ---- SIDEBAR ----
st.sidebar.header("Please select manufacturer")

manfa = st.sidebar.multiselect(
    "Select the manufacturer:",
    options=devices_df["Handset Manufacturer"].unique(),
    default=['Apple', 'Samsung', 'Huawei']
)

devices_df = devices_df.query("`Handset Manufacturer` ==@manfa")
bx_plot1 = px.box(devices_df, x='Handset Manufacturer', y='Avg Bearer TP DL (kbps)', color='Handset Manufacturer',
                  title='Avg Bearer TP DL (kbps) by Device Manufacturer')
bx_plot1.update_layout(width=1000, height=700)

st.write("Boxplot of average throughput down link for top 30 Handset Manufacturer")
st.plotly_chart(bx_plot1)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
