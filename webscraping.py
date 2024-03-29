import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

url = 'https://finance.yahoo.com/gainers/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

def ticker_symbol(url):
    stocks = []
    names = soup.find_all(attrs={'data-test': 'quoteLink'})
    for stock in names:
        stocks.append(stock.text)
    return stocks

def convert_volume(entry):
    if 'M' in entry:
        return float(entry.replace(',', '').rstrip('M')) * 1000000
    elif 'B' in entry:
        return float(entry.replace(',', '').rstrip('B'))   
    else:
        return float(entry.replace(',', ''))

def get_important_data():
    data = []
    prices = []
    percent_change = []
    current_volume = []
    average_volume = []
    all_data = soup.find_all(attrs={'data-test': 'colorChange'})
    for values in all_data:
        data.append(values.text)
    prices = [float(entry) for entry in data[::5]]
    percent_change = [float(entry[:-1]) for entry in data[2::5]]
    current_volume = [convert_volume(entry) for entry in data[3::5]]
    average_volume = [convert_volume(entry) for entry in data[4::5]]

    meets_conditions = [
        (current_val >= (6 * avg_val)) and (5 <= price <= 20) and (percent_change >= 10)
        for current_val, avg_val, price, percent_change in zip(current_volume, average_volume, prices, percent_change)
    ]

    return prices, percent_change, current_volume, average_volume, meets_conditions

print(get_important_data())

# st.title('Stock Analysis Table')
# if st.button("Update and Display DataFrame"):
#     rounded_prices = []
#     rounded_percent_change = []
#     rounded_current_volume = []
#     stock_names = ticker_symbol(url)
#     prices, percent_change, current_volume, average_volume, meets_conditions = get_important_data()
#     for price in prices:
#         rounded_prices.append(round(price, 2))
    
#     for percent in percent_change:
#         rounded_percent_change.append(round(percent, 2))

#     for volume in current_volume:
#         rounded_current_volume.append(round(volume, 2))

#     df = pd.DataFrame({
#         'Stock Name': stock_names,
#         'Prices ($)': rounded_prices,
#         'Percent Change (%)': rounded_percent_change,
#         'Current Volume': rounded_current_volume,
#         'Meets Conditions': meets_conditions
#     })

#     sorted_df = df.sort_values(by='Meets Conditions', ascending=False)

#     st.dataframe(sorted_df)
