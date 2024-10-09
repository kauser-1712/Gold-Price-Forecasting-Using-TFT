import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
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

if not next_7_days_forecast.empty and 'Predicted Gold Price' in next_7_days_forecast.columns:
    st.markdown('<h3 style="color:#FFF113;">Next 7 Days Forecast</h3>', unsafe_allow_html=True)
    st.write(next_7_days_forecast[['Date', 'Predicted Gold Price']])

    # Plot the line chart showing forecast for the next 7 days
    fig_line = px.line(next_7_days_forecast, 
                       x='Date', y='Predicted Gold Price', 
                       title='Next 7 Days Forecast',
                       markers=True)

    fig_line.update_layout(
        title_x=0.5,
        xaxis_title='Date',
        yaxis_title='Predicted Gold Price (INR)',
        legend_title='Forecasted Prices'
    )
    
    st.plotly_chart(fig_line)

    # Correlation Analysis
    file_path = "Dashboard/final_dataset.xlsx"
    data = pd.read_excel(file_path, usecols=['Date', 'CPI', 'USD/INR', 'Crude Price', 'Gold Price',
                                             'Bond Price', 'Nifty Price', 'Repo Rate', 
                                             'Inflation Rate (%)', 'GPR', 'GPRC IND', 
                                             'BSE Price', 'US federal', 'WPI', 'Silver Price'])

    data['Date'] = pd.to_datetime(data['Date'])
    st.markdown('<h3 style="color:#FFF113;">Correlation of Gold Price with Other Variables</h3>', unsafe_allow_html=True)

    selected_variable = st.selectbox(
        "Choose a variable to correlate with Gold Price:",
        options=['BSE Price', 'Nifty Price', 'Crude Price', 'Silver Price', 'CPI', 'USD/INR', 
                 'Bond Price', 'Repo Rate', 'Inflation Rate (%)', 'GPR', 'GPRC IND', 
                 'US federal', 'WPI', 'Silver Price'],
        index=0
    )

    correlation_data = data[['Gold Price', selected_variable]].dropna()

    # Calculate the correlation value
    correlation_value = correlation_data.corr().loc['Gold Price', selected_variable]

    # Create scatter plot with trendline
    fig_corr = px.scatter(correlation_data, x=selected_variable, y='Gold Price',
                          trendline='ols',
                          title=f'Scatter Plot of Gold Price vs {selected_variable} (Correlation: {correlation_value:.2f})')

    fig_corr.update_layout(xaxis_title=selected_variable, 
                           yaxis_title='Gold Price (INR)')

    st.plotly_chart(fig_corr)

    # Display correlation coefficient
    st.write(f"Correlation coefficient between Gold Price and {selected_variable}: {correlation_value:.2f}")

    # Add interpretation of the correlation value
    if correlation_value > 0.7:
        interpretation = "There is a strong positive correlation. This means that as the selected variable increases, Gold Price tends to increase significantly."
    elif 0.3 < correlation_value <= 0.7:
        interpretation = "There is a moderate positive correlation. As the selected variable increases, Gold Price tends to increase, but the relationship is less strong."
    elif -0.3 <= correlation_value <= 0.3:
        interpretation = "There is little to no correlation. The selected variable does not have a significant linear relationship with Gold Price."
    elif -0.7 < correlation_value <= -0.3:
        interpretation = "There is a moderate negative correlation. As the selected variable increases, Gold Price tends to decrease."
    else:
        interpretation = "There is a strong negative correlation. This means that as the selected variable increases, Gold Price tends to decrease significantly."

    st.write(f"**Interpretation:** {interpretation}")

    # Gauge Plot
    recommendation = "Strong Buy"
    gauge_value = 4

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
