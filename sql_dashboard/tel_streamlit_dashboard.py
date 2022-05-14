import streamlit as st
import pandas as pd
import mysql.connector as mysql
import matplotlib.pyplot as plt

import plotly.express as px
import seaborn as sns
import pandas.io.sql as sqlio
import re

st.set_page_config(page_title="Tel Analysis Dashboard",
                   page_icon=":bar_chart:", layout="wide")
st.markdown("##")
st.markdown("<h1 style='text-align: center; color: grey;'>TellCo Analysis Dashboard</h1>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: white;'> by Faith Bagire </h3>", unsafe_allow_html=True)


# conn = mysql.connect(host='localhost', user='root', password='my_pass', database='tweets', buffered=True)
# cursor = conn.cursor()

# query = '''SELECT * FROM telcomdata'''


@st.cache
def read_data(df_path: str) -> pd.DataFrame:
    """"
        cached function to read the data since xlsx file takes too long to read
        :rtype: Dataframe
    """
    # df = sqlio.read_sql_query(query, conn)

    df = pd.read_excel(df_path, dtype={'Bearer Id': str, 'IMSI': str, 'MSISDN/Number': str, 'IMEI': str,
                                       'Handset Manufacturer': str, 'Handset Type': str}, engine='openpyxl')
    return df


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
