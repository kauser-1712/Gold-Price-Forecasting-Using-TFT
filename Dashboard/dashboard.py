import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Load the data
august_data = pd.read_csv("Dashboard/august 2024.csv")
september_data = pd.read_csv("Dashboard/september 2024.csv")
october_data = pd.read_csv("Dashboard/october 2024.csv")
predicted_df = pd.read_csv("Dashboard/predicted_df.csv")
predicted_tft = pd.read_csv("Dashboard/predicted_tft.csv")

# Convert date column to datetime
predicted_df['Date'] = pd.to_datetime(predicted_df['Date']).dt.date

# Get today's date
today = datetime.today().date()

# Extract the forecast for today
today_forecast = predicted_df[predicted_df['Date'] == today]

# Display the forecast for today
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

# Prepare the prediction data for the next 7 days
predicted_df['Date'] = pd.to_datetime(predicted_df['Date'])
today = pd.Timestamp.today()

next_7_days_forecast = predicted_df[predicted_df['Date'] > today].head(7)

# Check if forecast data is available
if not next_7_days_forecast.empty and 'Predicted Gold Price' in next_7_days_forecast.columns:
    
    # Drop rows with missing values in 'Predicted Gold Price'
    next_7_days_forecast = next_7_days_forecast.dropna(subset=['Predicted Gold Price'])

    # Calculate the percentage change for the next 7 days
    average_change = next_7_days_forecast['Predicted Gold Price'].pct_change().mean()

    # Output average change for debugging
    st.write(f"Average Change in Predicted Gold Price: {average_change:.4f}")

    # Determine recommendation and gauge value based on average price change
    if pd.isna(average_change):
        recommendation = "No Data"
        gauge_value = 2
    elif average_change < -0.03:
        recommendation = "Strong Sell"
        gauge_value = 0
    elif -0.03 <= average_change < -0.01:
        recommendation = "Sell"
        gauge_value = 1
    elif -0.01 <= average_change <= 0.01:
        recommendation = "Neutral"
        gauge_value = 2
    elif 0.01 < average_change <= 0.03:
        recommendation = "Buy"
        gauge_value = 3
    else:
        recommendation = "Strong Buy"
        gauge_value = 4  # This will trigger "Strong Buy"

    # Display gauge chart for recommendation
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=gauge_value,
        title={'text': f"Recommendation: {recommendation}"},
        gauge={
            'axis': {'range': [0, 4]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 1], 'color': "red"},  # Strong Sell
                {'range': [1, 2], 'color': "orange"},  # Sell
                {'range': [2, 3], 'color': "yellow"},  # Neutral
                {'range': [3, 4], 'color': "lightgreen"},  # Buy and Strong Buy
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
