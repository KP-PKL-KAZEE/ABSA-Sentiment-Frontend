#Import Library Needed.
import streamlit as st
from streamlit_option_menu import option_menu
import requests
import pandas as pd

## Function Request Analyize Article for ALL Emiten.
def analyze_all_emiten(news : str):
    r = requests.post(f"http://127.0.0.1:8000/predict_sentiment_all_emiten/?news={news}")
    return r

## Function Request Analyize Article for Spesific Emiten.
def analyze_specific_emiten(news : str, aspect : str):
    t = requests.post(f"http://127.0.0.1:8000/predict_sentiment_specific_emiten/?news={news}&aspect={aspect}")
    return t

## Get Data List of Emiten From .csv in Data.
def get_data_emiten():
  return pd.read_csv("./data/daftar_emiten.csv")

# UI Layout

## Sidemenu / Sidebar
with st.sidebar:
    choose = option_menu("Predict", ["All Emiten", "Specific Emiten"],
                         icons=['grid fill', 'search heart'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "20px"}, 
        "nav-link": {"font-size": "17px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )

## Analyize Article for ALL Emiten.
if choose == "All Emiten":
    st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Sentiment Analysis</p>', unsafe_allow_html=True)    
    st.subheader("Sentiment Analysis of Indonesian Stock Company Articles with BERT.")

    st.caption("Predict Sentiment All Emiten")
    with st.form(key='nlpForm'):
        news = st.text_area("Enter Article Here", height=200)
        submit_button = st.form_submit_button(label='Analyze')
        
        # Button Analyize On-click :
        if submit_button:
            st.info("Results")
            # Predict Function
            predict = analyze_all_emiten(news)
            # Output Status Request
            st.write(predict)
            # Output JSON
            st.json(predict.text)

## Request Analyize Article for Spesific Emiten.
elif choose == "Specific Emiten":
    st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;}
        span[data-baseweb="tag"]{background-color: #95e85a !important;} 
        </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Sentiment Analysis</p>', unsafe_allow_html=True)    
    st.subheader("Sentiment Analysis of Indonesian Stock Company Articles with BERT.")
    
    st.caption("Predict Sentiment Specific Emiten")
    with st.form(key='nlpForm'):
        emiten_list = get_data_emiten().KodeEmiten
        news = st.text_area("Enter Article Here", height=200)
        aspect = st.multiselect(
            'Select emiten',
            emiten_list)

        submit_button = st.form_submit_button(label='Analyze')

        str_aspect = ' '.join(aspect)

        # Button Analyize On-click :
        if submit_button:
            st.info("Results")
            # Predict Function 
            predict = analyze_specific_emiten(news, str_aspect)
            # Output Status Request
            st.write(predict)
            # Output JSON
            st.json(predict.text)        
