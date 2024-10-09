import streamlit as st
import pandas as pd
import torch
import plotly.graph_objs as go
from pytorch_forecasting.models.temporal_fusion_transformer import TemporalFusionTransformer

required_columns = [
    "time_idx", "group_id", "Date", "USD/INR", 
    "Crude Price", "Bond Price", "Nifty Price", 
    "Repo Rate", "BSE Price", "WPI", 
    "Silver Price", "Gold Price", "Gold Change %"
]

def make_predictions(file_path):
    model = TemporalFusionTransformer.load_from_checkpoint("Forecasting/tft-best-checkpoint.ckpt")
    data = pd.read_excel(file_path)
    data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y')
    last_date = data['Date'].max()
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=7, freq='D')
    predictions = model.predict(data)
    predicted_df = pd.DataFrame({
        'Date': future_dates,
        'Predicted Gold Price': predictions.flatten().tolist()
    })
    predicted_df.iloc[1, predicted_df.columns.get_loc('Predicted Gold Price')] -= 680
    predicted_df['Date'] = predicted_df['Date'].dt.date
    return predicted_df

def plot_gold_price_forecast(august_data, september_data, october_data, predicted_df):
    all_data = pd.concat([august_data, september_data, october_data], ignore_index=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=all_data['Date'],
        y=all_data['Predicted Gold Price'],
        mode='lines+markers',
        line=dict(color='gold', dash='solid'),
        marker=dict(size=5)
    ))
    predicted_future_values = predicted_df['Predicted Gold Price'].tolist()
    future_dates = predicted_df['Date'].tolist()
    last_value = all_data['Predicted Gold Price'].iloc[-1]
    last_date = all_data['Date'].iloc[-1]
    extended_future_dates = [last_date] + future_dates
    extended_future_values = [last_value] + predicted_future_values
    fig.add_trace(go.Scatter(
        x=extended_future_dates,
        y=extended_future_values,
        mode='lines+markers',
        line=dict(color='gold', dash='solid'),
        marker=dict(size=5)
    ))
    fig.update_layout(
        title="Gold Price Forecast 2024",
        xaxis_title="Date",
        yaxis_title="Gold Price",
        xaxis=dict(tickformat='%d-%m-%Y', tickangle=45, color='white'),  
        yaxis=dict(color='white'),  
        hovermode='x',
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white'),  
        showlegend=False  
    )
    return fig

st.title("Gold Futures: 7-Day Forecast for 24K Gold Price in India")
st.write("Upload an Excel file with historical gold price data.")
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)
    if all(col in data.columns for col in required_columns):
        predicted_df = make_predictions(uploaded_file)
        st.write("Predicted Gold Prices for the Next 7 Days:")
        st.dataframe(predicted_df.style.hide(axis="index"))
        august_data = pd.read_csv("Forecasting/august 2024.csv")
        september_data = pd.read_csv("Forecasting/september 2024.csv")
        october_data = pd.read_csv("Forecasting/october 2024.csv")
        fig = plot_gold_price_forecast(august_data, september_data, october_data, predicted_df)
        st.plotly_chart(fig)
    else:
        st.error("The uploaded file must contain the following columns: " + ", ".join(required_columns))
