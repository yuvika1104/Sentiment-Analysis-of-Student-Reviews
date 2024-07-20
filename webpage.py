import streamlit as st
from joblib import load
import numpy as np
import pandas as pd
from main import vectorize, clean
from inputscr import scrape_coursera_reviews
import matplotlib.pyplot as plt
import csv

# Load model
model = load('saved_model.joblib')
output_file = "input_coursera_reviews.csv"
with open(output_file, 'w', newline='', encoding='utf-8',) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Review"])

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
    
    st.title("Sentiment Analysis of Reviews")
    st.markdown('<div style="color:#004085">Developed by Yuvika Gupta</div>', unsafe_allow_html=True)
    html_temp = """
    <div style="background-color:#6699CC;padding:10px;border-radius:10px;margin-bottom:20px;">
    <h2 style="color:whitesmoke;text-align:center;">Coursera Review Analysis</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    
    with st.form(key='input_form'):
        url = st.text_input("Enter Coursera URL")
        submit_button = st.form_submit_button(label='Analyze')
    
    if submit_button:
        scrape_coursera_reviews(url, output_file)
        dataset = pd.read_csv(output_file)
        dataset["Review"] = dataset["Review"].fillna("")
        dataset["Review"] = dataset["Review"].apply(clean)
        x = np.array(dataset["Review"])
        X = vectorize(x)
        y_pred = model.predict(X)
        dataset['Predictions'] = y_pred
        dataset.to_csv(output_file, index=False)
        plot_predictions_distribution(dataset)

def plot_predictions_distribution(dataset):
    prediction_counts = dataset['Predictions'].value_counts()
    pastel_blue = (0.4, 0.6, 0.8, 0.8)
    fig, ax = plt.subplots()
    ax.bar(prediction_counts.index, prediction_counts.values, color=pastel_blue, width=0.3, linewidth=1)
    ax.set_xlabel('Predictions')
    ax.set_ylabel('Number of Reviews')
    ax.set_title('Distribution of Predictions')
    ax.tick_params(axis='x', rotation=45)
    fig.patch.set_facecolor('whitesmoke')
    st.pyplot(fig)

if __name__ == '__main__':
    main()
