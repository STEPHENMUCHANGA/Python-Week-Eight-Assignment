# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.title("CORD-19 Data Explorer")
st.write("Simple exploration of COVID-19 research papers")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/metadata.csv")
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    return df.dropna(subset=['title', 'publish_time'])

df = load_data()

# Sidebar filters
years = st.slider("Select year range:", int(df['year'].min()), int(df['year'].max()), (2020,2021))
df_filtered = df[(df['year'] >= years[0]) & (df['year'] <= years[1])]

st.subheader("Publications by Year")
year_counts = df_filtered['year'].value_counts().sort_index()
st.bar_chart(year_counts)

st.subheader("Top Journals")
top_journals = df_filtered['journal'].value_counts().head(10)
st.bar_chart(top_journals)

st.subheader("Word Cloud of Titles")
text = " ".join(df_filtered['title'].dropna().tolist())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
st.image(wordcloud.to_array())
