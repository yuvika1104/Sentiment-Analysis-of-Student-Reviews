import streamlit as st
from joblib import load
import numpy as np
import pandas as pd
from main import vectorize, clean

# Load model
model = load('saved_model.joblib')

def main():
    st.set_page_config(page_title="Sentiment Analysis", page_icon="📈", layout="centered")
    
    # Custom CSS
    st.markdown("""
        <style>
            .main {
                background-color: #f0f0f0;
            }
            h1, h2 {
                color: #004085;
            }
            .stButton>button {
                background-color: #004085;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
            }
            .stTextInput>div>input {
                border: 1px solid #004085;
                border-radius: 5px;
                padding: 10px;
            }
            .stForm {
                margin: 0 auto;
                padding: 20px;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                max-width: 600px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("Sentiment Analysis")
    st.markdown('<div style="color:#004085">Developed by Yuvika Gupta</div>', unsafe_allow_html=True)
    
    html_temp = """
    <div style="background-color:#6699CC;padding:10px;border-radius:10px;margin-bottom:10px;">
    <h2 style="color:whitesmoke;text-align:center;">Review Analysis</h2>
    
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    
    with st.form(key='input_form'):
        review = st.text_input("Enter review", "")
        submit_button = st.form_submit_button(label='Analyze')
    
    if submit_button:
        review = clean(review)
        review = [review]
        X = vectorize(review)
        pred = model.predict(X)
        st.markdown(f'<div class="output-container"style="background-color:#6699CC;padding:10px;border-radius:10px;margin-bottom:10px;">   The text is classified as {pred[0]}</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
