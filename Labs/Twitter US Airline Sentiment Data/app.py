# import libraries
import streamlit as st
import pandas as pd
import numpy as np

# Create two columns and display info
st.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets about US Airlines")
st.markdown("This application is a Streamlit dashboard to analyze the sentiments of Tweets 🐦")
st.sidebar.markdown("This application is a Streamlit dashboard to analyze the sentiments of Tweets 🐦")

DATA_URL = ("C:/Users/md/Downloads/DS_projects/ds_projects/Labs/Twitter US Airline Sentiment Data/Data/Tweets.csv")

@st.cache_data(persist=True) # prevent re-loading the data to save on resource usage
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created']) # convert to pandas datetime format
    return data

data = load_data()

# Display Random User Sentiment on Sidebar
st.sidebar.subheader("Show Random Tweet")
random_tweet = st.sidebar.radio('Sentiment', ('positive', 'neutral', 'negative'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])

