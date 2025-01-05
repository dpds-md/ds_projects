# import libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

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

# Display User Sentiment on Sidebar
st.sidebar.subheader("Show Random Tweet")
random_tweet = st.sidebar.radio('Sentiment', ('positive', 'neutral', 'negative')) # show random tweet based on sentiment values
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0]) 

# Display Number of Tweets by Sentiment
st.sidebar.markdown("### Number of tweets by Sentiment")
select = st.sidebar.selectbox('Visualization type', ['Histogram', 'Pie Chart'], key = '1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})

# Display Visualization type
if not st.sidebar.checkbox("Hide", True):
    st.markdown("### Number of tweets by sentiment")
    if select == "Histogram":
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)

