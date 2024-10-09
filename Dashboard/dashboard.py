import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

august_data = pd.read_csv("Dashboard/august 2024.csv")
september_data = pd.read_csv("Dashboard/september 2024.csv")
october_data = pd.read_csv("Dashboard/october 2024.csv")
predicted_df = pd.read_csv("Dashboard/predicted_df.csv")
predicted_tft = pd.read_csv("Dashboard/predicted_tft.csv")

predicted_df['Date'] = pd.to_datetime(predicted_df['Date']).dt.date

today = datetime.today().date()

today_forecast = predicted_df[predicted_df['Date'] == today]

st.markdown('<h1 style="color:#FFF113;">Gold Trend Analyzer</h1>', unsafe_allow_html=True)
if not today_forecast.empty:
    st.metric(label=f"Forecast for {today.strftime('%B %d, %Y')}",
              value=f"{today_forecast.iloc[0]['Predicted Gold Price']:.2f} INR")
else:
    st.write(f"No forecast available for today ({today.strftime('%B %d, %Y')}).")

def display_collapsible_tables():
    st.markdown('<h3 style="color:#FFF113;">Forecasted Values</h3>', unsafe_allow_html=True)
    predicted_df['Date'] = predicted_df['Date'].astype(str)
    with st.expander("Weekly Forecast"):
        st.write(predicted_df)

    st.markdown('<h3 style="color:#FFF113;">Past Forecast</h3>', unsafe_allow_html=True)
    with st.expander("October 2024"):
        st.write(october_data[['Date', 'Actual Gold Price', 'Predicted Gold Price']])
    with st.expander("September 2024"):
        st.write(september_data[['Date', 'Actual Gold Price', 'Predicted Gold Price']])
    with st.expander("August 2024"):
        st.write(august_data[['Date', 'Actual Gold Price', 'Predicted Gold Price']])

display_collapsible_tables()

predicted_df['Date'] = pd.to_datetime(predicted_df['Date'])
today = pd.Timestamp.today()

next_7_days_forecast = predicted_df[predicted_df['Date'] > today].head(7)

if not next_7_days_forecast.empty and 'Predicted Gold Price' in next_7_days_forecast.columns:
    st.markdown('<h3 style="color:#FFF113;">Next 7 Days Forecast</h3>', unsafe_allow_html=True)
    st.write(next_7_days_forecast[['Date', 'Predicted Gold Price']])

    recommendation = "Strong Buy"
    gauge_value = 4

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=gauge_value,
        title={'text': f"Recommendation: {recommendation}"},
        gauge={
            'axis': {'range': [0, 4]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 1], 'color': "red"},
                {'range': [1, 2], 'color': "orange"},
                {'range': [2, 3], 'color': "yellow"},
                {'range': [3, 4], 'color': "lightgreen"},
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': gauge_value
            }
        }
    ))

    st.markdown('<h3 style="color:#FFF113;">Investment Recommendation</h3>', unsafe_allow_html=True)
    st.plotly_chart(fig_gauge)

else:
    st.write("No valid forecast data available for the next 7 days.")
