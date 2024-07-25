# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 12:29:19 2024

Simple energy efficiency calculator for LED replacement of traditional
light fittings using Streamlit as an interface.

@author: hallam.smith
"""

import pandas as pd
import locale
import streamlit as st

# Set locale for currency formatting (example for GBP)
locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')

# Function to format numbers as currency
def format_currency(value):
    return locale.currency(value, grouping=True)

# Global Settings
UsageHours = 16 
UsageDays = 365 
Rate = 0.175

life = 5000
lamp_cost = 2.5
labour_cost = 5
CO2_Factor = 0.575

# Initialize lists (existing fittings)
names = []
quantities = []
wattages = []
kw_load_per_hour = []
changed_per_year = []
annual_relamp_cost = []
annual_KWH = []
annual_running_cost = []
annual_CO2 = []

#Initialize lists (replacement fittings)
names_2 = []
quantities_2 = []
wattages_2 = []
kw_load_per_hour_2 = []
annual_relamp_cost_2 = []
annual_KWH_2 = []
annual_running_cost_2 = []
annual_CO2_2 = []

## FUNCTION DEFINITIONS
# Calculates how many Kilowatts are used per hour by fitting
def KWPerHour(qty, watt):
    return (qty * watt) / 1000

# Calculates how freqently lamp changes are required
def LampChange(MTBF, hours, days):
    return 1 / (MTBF / (hours * days))

# How much it costs annually to replace lamps
def RelampCost(qty, relamp, labour, peryear):
    return format_currency(qty * (relamp + labour) * peryear)

# How many Kilowatt hours are used per year
def KWHPerYear(KWH, hours, days):
    return KWH * hours * days

# Calculates the annual cost of running the lights
def RunningCost(KWH, KWHRate):
    return float(KWH * KWHRate)

# Works out annual CO2 emissions (based on C02 factor)
def CO2Tonnes(KWH, CO2Rate, hours, days):
    return hours * days * KWH * CO2Rate / 1000

## LAYOUT
#Title and header
st.title("LED Efficiency Calculator")
st.divider()
st.header("Getting Started")
st.write("""To get started, select how many fittings types you need using the 'Input Data' section on the sidebar.
Once you've added all the fittings you need, click the 'calculate' button to see the results.""")
st.divider()

#Columns Layout
col1, col2 = st.columns(2)

#Side Bar
with st.sidebar:
    st.subheader('Global Settings')
    st.divider()
    UsageHours = st.slider('Usage Hours: ', 1, 24, 16)
    UsageDays = st.slider('Usage Days: ', 1, 365, 365)
    
    # Choose how many fittings to add
    st.header("Input Data")
    num_fittings = st.number_input("Enter the number of fitting types: ", value = 1, step = 1, placeholder = "Type a number...")
    st.divider()
    PaybackOn = st.toggle("Enable Payback Calculator")
    if PaybackOn:
        Purchase = st.number_input("LED Purchase Cost (£)", placeholder = "Type a number...")
        Install = st.number_input("LED Install Cost (£)", placeholder = "Type a number...")
        Rate = st.number_input('KWH Rate (£): ', value = 0.175)
        Years = st.slider("Years", 1, 15, 10)

# Input parameters for multiple fittings
for i in range(num_fittings):
    with col1:
        st.write(f"\n:red[Existing Fitting {i+1}:]")
        name = st.text_input(f"\nName of existing fitting {i+1}: ", placeholder = "Type a name...")
        qty = st.number_input(f"\nQuantity of existing fitting {i+1}: ", step = 1, placeholder="Type a qty...")
        wattage = st.number_input(f"\nWatts per existing fitting {i+1}: ", step = 0.1, placeholder="Type a wattage...")
        st.divider()
   
    with col2:
        st.write(f"\n:green[Replacement Fitting {i+1}:]")
        name_2 = st.text_input(f"\nName of replacement fitting {i+1}: ", placeholder = "Type a name...")
        qty_2 = st.number_input(f"\nQuantity of replacement fitting {i+1}: ", value = qty, step = 1, placeholder="Type a qty...")
        wattage_2 = st.number_input(f"\nWatts per replacement fitting {i+1}: ", step = 0.1, placeholder="Type a wattage...")
        st.divider()
    
    # Perform calculations (Existing fittings)
    kw_load = KWPerHour(qty, wattage)
    changes_per_year = LampChange(life, UsageHours, UsageDays)
    annual_cost = RelampCost(qty, lamp_cost, labour_cost, changes_per_year)
    KWH = KWHPerYear(kw_load, UsageHours, UsageDays)
    Annual_Running_Cost = RunningCost(KWH, Rate)
    CO2Emissions = CO2Tonnes(kw_load, CO2_Factor, UsageHours, UsageDays)

    # Perform calculations (Replacement fittings)
    kw_load_2 = KWPerHour(qty_2, wattage_2)
    KWH_2 = KWHPerYear(kw_load_2, UsageHours, UsageDays)
    Annual_Running_Cost_2 = RunningCost(KWH_2, Rate)
    CO2Emissions_2 = CO2Tonnes(kw_load_2, CO2_Factor, UsageHours, UsageDays)

    # Append to lists (Existing fittings)
    names.append(name)
    quantities.append(qty)
    wattages.append(wattage)
    kw_load_per_hour.append(kw_load)
    changed_per_year.append(changes_per_year)
    annual_relamp_cost.append(annual_cost)
    annual_KWH.append(KWH)
    annual_running_cost.append(Annual_Running_Cost)
    annual_CO2.append(CO2Emissions)

    # Append to lists (Replacement fittings)
    names_2.append(name_2)
    quantities_2.append(qty_2)
    wattages_2.append(wattage_2)
    kw_load_per_hour_2.append(kw_load_2)
    annual_KWH_2.append(KWH_2)
    annual_running_cost_2.append(Annual_Running_Cost_2)
    annual_CO2_2.append(CO2Emissions_2)

# Create DataFrame (Existing fittings)
Exist_df = pd.DataFrame({
    'Product Name': names,
    'Quantity': quantities,
    'Wattage': wattages,
    'KW Load Per Hour': kw_load_per_hour,
    'Annual Relamp Cost': annual_relamp_cost,
    'Annual KWH Use': annual_KWH,
    'Annual Running Cost': annual_running_cost,
    'Annual CO2 Emissions': annual_CO2
})

# Create DataFrame (Replacement fittings)
Replace_df = pd.DataFrame({
    'Product Name': names_2,
    'Quantity': quantities_2,
    'Wattage': wattages_2,
    'KW Load Per Hour': kw_load_per_hour_2,
    'Annual KWH Use': annual_KWH_2,
    'Annual Running Cost': annual_running_cost_2,
    'Annual CO2 Emissions': annual_CO2_2
})

## RESULTS
# Calculate energy savings
TotalExistKW = sum(Exist_df['Annual KWH Use'])
TotalReplaceKW = sum(Replace_df['Annual KWH Use'])
KWHourSaving = round(float(TotalExistKW-TotalReplaceKW),2)

# Calculate financial savings
TotalExistCost = sum(Exist_df['Annual Running Cost'])
TotalReplaceCost = sum(Replace_df['Annual Running Cost'])
CostSaving = format_currency(TotalExistCost-TotalReplaceCost)

# Calculate carbon savings
TotalExistCarbon = sum(Exist_df['Annual CO2 Emissions'])
TotalReplaceCarbon = sum(Replace_df['Annual CO2 Emissions'])
CO2Saving = round(float(TotalExistCarbon-TotalReplaceCarbon),2)

# Format dataframes to display currency
Exist_df['Annual Running Cost'] = Exist_df['Annual Running Cost'].apply(format_currency)
Replace_df['Annual Running Cost'] = Replace_df['Annual Running Cost'].apply(format_currency)

Carbon_df = pd.DataFrame({
    'Name': ['Existing', 'Replacement'],
    'Amount': [TotalExistCarbon, TotalReplaceCarbon]
})


year_count = []
existing_cost = []
replacement_cost = []
cost_difference = []

for i in range(Years):
    current_year = (f"\nYear {i+1}")
    current_existing_cost = (TotalExistCost*(i+1))
    current_replace_cost = ((TotalReplaceCost*(i+1)) + Purchase + Install)
    current_cost_diff = current_existing_cost - current_replace_cost

    year_count.append(current_year)
    existing_cost.append(current_existing_cost)
    replacement_cost.append(current_replace_cost)
    cost_difference.append(current_cost_diff)

Payback_df = pd.DataFrame({
    'Year': year_count,
    'Existing': existing_cost,
    'Replacement': replacement_cost,
    'Cost Difference': cost_difference
})

# Print results
st.button("Reset", type = "primary", key = 'calculate')
if st.button("Calculate"):
    st.header("Results")
    st.write(":red[Existing Fittings]")
    st.write(Exist_df[['Product Name','Quantity','Wattage','Annual KWH Use','Annual Running Cost','Annual CO2 Emissions']])
    st.write('')
    st.write(":green[Replacement Fittings]")
    st.write(Replace_df[['Product Name','Quantity','Wattage','Annual KWH Use','Annual Running Cost','Annual CO2 Emissions']])
    st.write('')
    st.subheader("Summary:")
    rescol1, rescol2 = st.columns(2)
    with rescol2:
        st.write("Annual KW Hour Reduction: ", KWHourSaving , 'KWH')
        st.write("Annual Electricity Bill Reduction: ", CostSaving)
        st.write("Annual CO2 Reduction: ", CO2Saving , 'Tonnes')
    with rescol1:
        st.bar_chart(Carbon_df, x = 'Name', x_label = "Tonnes Per Year", y_label = "CO2 Emissions", color = "#C39D50", horizontal=True, height = 200)
    if PaybackOn:
        st.write(Payback_df)

