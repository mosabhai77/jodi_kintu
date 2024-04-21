import streamlit as st
import pandas as pd
import ta
import plotly.express as px
import pytz
from datetime import datetime
import yfinance as yf

# Define the title
st.title('Indian Stock Market Analysis')

# User input for stock ticker
ticker = st.text_input('Enter the stock ticker', 'RELIANCE.NS')

# Fetch data
def fetch_data(ticker):
    data = yf.download(ticker, start='2020-01-01', end='2024-04-19')
    data['Date'] = pd.to_datetime(data.index).tz_localize('UTC').tz_convert('Asia/Kolkata')
    return data

data = fetch_data(ticker)

# Calculate RSI
data['RSI'] = ta.momentum.rsi(data['Close'])

# Calculate price change ratio
data['Price Change Ratio'] = data['Close'].pct_change()

# Calculate RSI change ratio
data['RSI Change'] = data['RSI'].diff() / data['RSI'].shift()

rsi_ranges = [(10, 20), (20, 30), (30, 40), (40, 50), (50, 60), (60, 70), (70, 80)]

# Initialize a dictionary to store the duration for each range
rsi_duration = {f'{lower}-{upper}': 0 for lower, upper in rsi_ranges}

# Iterate through the RSI values
for i in range(len(data)-1):
    for lower, upper in rsi_ranges:
        # Check if the RSI value falls within the range
        if lower <= data['RSI'][i] < upper:
            # Increment the duration count for the corresponding range
            rsi_duration[f'{lower}-{upper}'] += 1

# Define the RSI ranges
rsi_ranges = [(10, 20), (20, 30), (30, 40), (40, 50), (50, 60), (60, 70), (70, 80)]

# Initialize a dictionary to store the last occurrence timestamp for each range
last_occurrence_timestamp = {f'{lower}-{upper}': None for lower, upper in rsi_ranges}

# Iterate through the RSI values
for i in range(len(data)-1):
    date = data.index[i]
    for lower, upper in rsi_ranges:
        # Check if the RSI value falls within the range
        if lower <= data['RSI'][i] < upper:
            # Update the last occurrence timestamp for the corresponding range
            last_occurrence_timestamp[f'{lower}-{upper}'] = date

# Display the last occurrence timestamp for each range
st.subheader('Last Time RSI Was in Different Ranges')
for range_str, timestamp in last_occurrence_timestamp.items():
    if timestamp:
        st.write(f"Last time RSI was between {range_str}: {timestamp.strftime('%Y-%m-%d')}")
    else:
        st.write(f"No data available for RSI range {range_str}")


# Display the duration for each range
st.subheader('Duration of RSI in Different Ranges')
for range_str, duration in rsi_duration.items():
    st.write(f"Duration of RSI between {range_str}: {duration} days")
# Replace NaN values with 0
data.fillna(0, inplace=True)

# Define the RSI ranges
rsi_ranges = [(10, 20), (20, 30), (30, 40), (40, 50), (50, 60), (60, 70), (70, 80)]

# Initialize a dictionary to store the duration of continuous occurrence for each range
continuous_duration = {f'{lower}-{upper}': 0 for lower, upper in rsi_ranges}

# Iterate through the RSI values
for i in range(len(data)-1):
    date = data.index[i]
    for lower, upper in rsi_ranges:
        # Check if the RSI value falls within the range
        if lower <= data['RSI'][i] < upper:
            # Check if the previous RSI value also falls within the range
            if lower <= data['RSI'][i - 1] < upper:
                # Increment the duration of continuous occurrence
                continuous_duration[f'{lower}-{upper}'] += 1
            else:
                # If not continuous, reset the duration to 1
                continuous_duration[f'{lower}-{upper}'] = 1

# Display the duration of continuous occurrence for each range
st.subheader('Duration of Continuous RSI in Different Ranges')
for range_str, duration in continuous_duration.items():
    st.write(f"Duration of continuous RSI between {range_str}: {duration} days")

# Calculate the ratio of the change of price to ratio of change in RSI
data['Price to RSI Change Ratio'] = data['Price Change Ratio'] / data['RSI Change']

# Display the data
st.subheader('Data')
st.write(data)

# Plot the Price to RSI Change Ratio
st.subheader('Price to RSI Change Ratio over Time')
fig = px.line(data, y='Price to RSI Change Ratio')
fig.update_xaxes(dtick="D1", tickformat="%Y-%m-%d %H:%M:%S")  # This will show the x-axis in a calendar format (Year-Month-Day Hour:Minute:Second)
st.plotly_chart(fig)

# Display the current date and time in IST
now_ist = datetime.now(pytz.timezone('Asia/Kolkata'))
st.write('Current date and time in IST:', now_ist.strftime('%Y-%m-%d %H:%M:%S'))
