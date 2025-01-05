# import libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

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
select = st.sidebar.selectbox('Visualization type', ['Histogram', 'Pie Chart'], key = 'unique_key_close_1')
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

# Plotting Location Data on an Interactive Map
st.sidebar.subheader('When and where are users tweeting from?')
hour = st.sidebar.slider("Hour of Day", 0, 23)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox("Hide", True, key='unique_key_close_2'):
    st.markdown("### Tweets location based on the time of day")
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)

# Plotting number of Tweets by Sentiment for each airline
st.sidebar.subheader("Breakdown airline tweets by sentiment")
choice = st.sidebar.multiselect("Pick Airline", ("US Airways", "United", "American", "Delta", "Southwest", "Virgin America"), key='unique_key_close_3')
if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x='airline', y='airline_sentiment', histfunc='count', color='airline_sentiment',
                              facet_col='airline_sentiment', labels={'airline_sentiment':'tweets'}, height=600, width=800)
    st.plotly_chart(fig_choice)

# Add WordCloud for Positive, Negative, and Neutral Tweets
st.sidebar.header("Wordcloud")
word_sentiment = st.sidebar.radio('Display word cloud for what sentiment?', ('positive', 'neutral', 'negative'))
if not st.sidebar.checkbox("Hide", True, key='unique_key_close_4'):
    st.header('Word Cloud for %s sentiment' % (word_sentiment))
    df = data[data['airline_sentiment']==word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height = 640, width = 800).generate(processed_words)
    fig_wordcloud, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig_wordcloud)