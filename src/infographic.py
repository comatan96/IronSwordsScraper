import plotly.express as px
import streamlit as st
import polars as pd
import urllib.request
import json


st.write('Plot the distribution of alerts in your city')
df = pd.read_csv('data.csv').with_columns(
   pd.col('date').str.to_datetime()
)

url = 'https://data.gov.il/api/3/action/datastore_search?resource_id=5c78e9fa-c2e2-4771-93ff-7f400a12f7ba&limit=1270'
with urllib.request.urlopen(url) as u:
    cities = json.loads(u.read().decode())
nafas = set([r['שם_נפה'].strip() for r in cities['result']['records']])
settlements = set([r['שם_ישוב'].strip() for r in cities['result']['records']])
cities = nafas.union(settlements)

df_cities = df['city']
new_cities, unwanted = [], []
for i, c in enumerate(df_cities):
    for s in cities:
        if s in c:
            new_cities.append(s)
            break
    else:
        new_cities.append(None)
df = df.with_columns(pd.Series(new_cities).alias('city'))
df = df.drop_nulls()

city = st.selectbox('city', sorted(list(set(new_cities) - {None})))

df_to_plot = df.filter(df['city'] == city)
df_to_plot = df_to_plot.with_columns(df_to_plot['date'].dt.hour().alias('hour'))
fig = px.histogram(
    df_to_plot,
    x='hour',
    title=f'Distribution of alerts in {city}',
    range_x=[0, 24]
)
st.plotly_chart(fig)
