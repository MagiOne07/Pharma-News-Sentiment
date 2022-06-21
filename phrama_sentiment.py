import streamlit as st

if "down" not in st.session_state:
    st.session_state.down= False
if st.session_state.down == False:
    nltk.download('vader_lexicon')
    st.session_state.down == True

from nltk.sentiment.vader import SentimentIntensityAnalyzer
vader = SentimentIntensityAnalyzer()
import numpy as np
key_words = np.array(['Anticoagulants', 'Heparin', 'Enoxaparin','Fragmin','Lovenox','Vaccine','Flu','Pneumo','Travel vaccine','Covid-19 vaccine','Pediatric vaccine','Hyaluronic acid','small molecules','Vials to Prefillable' ,'Trulicity','Humira','Eylea','Copaxone','ozempic','Enbrel','Prevnar','Gardasil','Zarxio','Pegasys'])
import pandas as pd
df = pd.DataFrame(index=key_words, columns=['headline'])
import pandas as pd
df = pd.DataFrame(index=key_words, columns=['headline'])
from bs4 import BeautifulSoup
import requests

url = 'https://news.google.com/search?q='
for word in key_words:
    headlines = []
    response = requests.get(url+word+' when:7d', headers={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"})
    soup = BeautifulSoup(response.text, 'lxml')
    data = soup.find_all('a', {'class':'DY5T1d RZIKme'})
    for i in range(len(data)):
        headlines.append(data[i].text)
    df.loc[word, 'headline'] = headlines
scores=[]
for c in range(len(df['headline'])):
    score=[]
    for k in df['headline'][c]:
        score.append(vader.polarity_scores(k))
    score_mean = np.array([score[com]['compound'] for com in range(len(score))]).mean()
    scores.append(score_mean)
df['score']=scores
df['positive'] = df['score']>0
import altair as alt
new=df[['score']]
new['y']=new.index
new['pos']=df['positive']
chart=alt.Chart(new).mark_bar().encode(x='score',y='y',color=alt.condition(alt.datum.pos == True, alt.value('green'), alt.value('red')))
st.header('Pharma News Sentiment')
st.altair_chart(chart, use_container_width=True)
key=st.selectbox('Select Option', (key_words))
st.write(df.loc[key,'headline'])
del(i,c,k,word,)
