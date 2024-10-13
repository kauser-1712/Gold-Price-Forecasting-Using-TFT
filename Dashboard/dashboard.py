import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

august_data = pd.read_csv("Dashboard/august 2024.csv")
september_data = pd.read_csv("Dashboard/september 2024.csv")
october_data = pd.read_csv("Dashboard/october 2024.csv")
predicted_df = pd.read_csv("Dashboard/predicted_df.csv")  
predicted_tft = pd.read_csv("Dashboard/predicted_tft.csv")  
# Convert date column to datetime
predicted_df['Date'] = pd.to_datetime(predicted_df['Date'])

# Get today's date
today = datetime.today().date()

# Extract the forecast for today
today_forecast = predicted_df[predicted_df['Date'] == pd.Timestamp(today)]

# Display the forecast for today
st.markdown('<h1 style="color:#FFF113;">Gold Trend Analyzer</h1>', unsafe_allow_html=True)
if not today_forecast.empty:
    st.metric(label=f"Forecast for {today.strftime('%B %d, %Y')}", 
              value=f"{today_forecast.iloc[0]['Predicted Gold Price']:.2f} INR")
else:
    st.write(f"No forecast available for today ({today.strftime('%B %d, %Y')}).")

def display_collapsible_tables():
    st.markdown('<h3 style="color:#FFF113;">Forecasted Values</h3>', unsafe_allow_html=True)

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
predicted_tft['date'] = pd.to_datetime(predicted_tft['date'], dayfirst=True)
filtered_predicted_tft = predicted_tft[predicted_tft['date'] >= '2023-01-01']
st.markdown('<h3 style="color:#FFF113;">Actual vs Forecasted Gold Prices (2023 Onwards)', unsafe_allow_html=True)
fig_actual_vs_forecasted = go.Figure()
fig_actual_vs_forecasted.add_trace(go.Scatter(
    x=filtered_predicted_tft['date'],
    y=filtered_predicted_tft['actual_gold_Price'],
    mode='lines',
    name='Actual Gold Price',
    line=dict(color='royalblue', width=1.5),
    text=filtered_predicted_tft.apply(lambda row: f"Date: {row['date'].date()}<br>Actual: {row['actual_gold_Price']}", axis=1),
    hoverinfo='text'
))

fig_actual_vs_forecasted.add_trace(go.Scatter(
    x=filtered_predicted_tft['date'],
    y=filtered_predicted_tft['predicted_gold_Price'],
    mode='lines',
    name='Forecasted Gold Price',
    line=dict(color='orange', width=1.5),
    text=filtered_predicted_tft.apply(lambda row: f"Date: {row['date'].date()}<br>Forecasted: {row['predicted_gold_Price']}", axis=1),
    hoverinfo='text'
))

fig_actual_vs_forecasted.update_layout(
    title='Actual vs Forecasted Gold Prices (2023 Onwards)',
    xaxis_title='Date',
    yaxis_title='Price',
    width=900,
    height=500,
    hovermode='x'
)

st.plotly_chart(fig_actual_vs_forecasted)

data = pd.read_excel("Dashboard/dataset.xlsx")
data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y')

date_range = (pd.Timestamp("2011-12-01"), pd.Timestamp("2024-10-01"))

col1, col2 = st.columns([3, 1])  
with col1:
    st.markdown('<h3 style="color:#FFF113;">Gold Price Forecast Over Time', unsafe_allow_html=True)

    fig_forecast = px.line(data, x='Date', y='Gold Price', 
                            title='Gold Price Forecast Over Time',
                            labels={'Gold Price': 'Gold Price (INR)'})
    st.plotly_chart(fig_forecast)

with col2:
    st.subheader("Range")
    st.write("**2011 - 2024**")


file_path = "Dashboard/final_dataset.xlsx"

data = pd.read_excel(file_path, usecols=['Date', 'CPI', 'USD/INR', 'Crude Price', 'Gold Price'
                                         , 'Bond Price', 'Nifty Price',
                                         'Repo Rate', 'Inflation Rate (%)', 'GPR', 'GPRC IND', 'BSE Price',
                                         'US federal', 'WPI', 'Silver Price'])

data['Date'] = pd.to_datetime(data['Date'])
st.markdown('<h3 style="color:#FFF113;">Correlation of Gold Price with Other Variables', unsafe_allow_html=True)

selected_variable = st.selectbox(
    "Choose a variable to correlate with Gold Price:",
    options=['BSE Price', 'Nifty Price', 'Crude Price', 'Silver Price','CPI', 'USD/INR', 
             'Bond Price', 'Repo Rate', 'Inflation Rate (%)', 'GPR', 'GPRC IND', 
             'US federal', 'WPI', 'Silver Price'],
    index=0
)

correlation_data = data[['Gold Price', selected_variable]].dropna()

correlation_value = correlation_data.corr().loc['Gold Price', selected_variable]

fig_corr = px.scatter(correlation_data, x=selected_variable, y='Gold Price',
                      trendline='ols',
                      title=f'Scatter Plot of Gold Price vs {selected_variable} (Correlation: {correlation_value:.2f})')

fig_corr.update_layout(xaxis_title=selected_variable, 
                       yaxis_title='Gold Price (INR)')

st.plotly_chart(fig_corr)

st.write(f"Correlation coefficient between Gold Price and {selected_variable}: {correlation_value:.2f}")
