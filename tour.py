import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import re
import random

# Read CSV data (replace 'taylor_Train.csv' with your actual file path)
df = pd.read_csv('taylor_Train.csv', encoding="1252")

# Column renaming for better readability
new_col = {
    'City': 'City',
    'Country': 'Country',
    'Venue': 'Venue',
    'Opening act(s)': 'Opening_act',
    'Attendance (tickets sold / available)': 'Tickets_sold_and_available',
    'Revenue': 'Revenue',
    'Tour': 'Tour',
}
df = df.rename(columns=new_col)

# Data cleaning functions
def clean_revenue(val):
    if val:
        return val.replace('$', '').replace(',', '')
    else:
        return 0

def clean_tickets(val):
    if val:
        return int(val.split("/")[0].replace(',', ''))
    else:
        return 0

def clean_available(val):
    if val:
        return int(val.split("/")[1].replace(',', ''))
    else:
        return 0

# Clean data
df['Revenue'] = df['Revenue'].apply(clean_revenue)
df['tickets_sold'] = df['Tickets_sold_and_available'].apply(clean_tickets)
df['tickets_available'] = df['Tickets_sold_and_available'].apply(clean_available)
df = df.fillna(3)  # Replace missing values with a placeholder (can be adjusted)
df.drop("Tickets_sold_and_available", axis=1, inplace=True)

# Convert data types
df['tickets_sold'] = df['tickets_sold'].astype(int)
df['tickets_available'] = df['tickets_available'].astype(int)
df['Revenue'] = df['Revenue'].astype(int)

# Handle duplicate rows
dupe = df.duplicated()
dupe_idx = df[dupe].index
for dupes in dupe_idx:
    df.at[dupes, 'tickets_sold'] = 0
    df.at[dupes, 'tickets_available'] = 0
    df.at[dupes, 'Revenue'] = 0

# Fill missing opening acts with previous values
df['Opening_act'].fillna(method='ffill', inplace=True)

# Calculate cost per ticket
df['Cost_per_ticket'] = df['Revenue'] / df['tickets_sold']

# Reorder columns for better presentation
repos_index = ["City", "Country", "Venue", "tickets_sold", "tickets_available",
                "Revenue", "Cost_per_ticket", "Tour", "Opening_act"]
df = df.reindex(columns=repos_index)

# ------------------------ Streamlit App ------------------------

# Title and Introduction
st.title("Taylor Swift Concert Analysis")
st.write("This app analyzes data from Taylor Swift's concert tours, providing insights into revenue, ticket sales, cost per ticket, and more.")

# User Input for Tour Selection (Optional)
tour_selection = st.selectbox("Select a Tour (Optional):", df["Tour"].unique())

# Filter DataFrame based on user selection (if applicable)
if tour_selection:
    df_filtered = df[df["Tour"] == tour_selection]
else:
    df_filtered = df.copy()

# Descriptive Statistics for Cost per Ticket (Overall)
st.subheader("Cost Per Ticket Statistics (Overall)")
st.write(df_filtered["Cost_per_ticket"].describe())

# Cost Per Ticket Bar Chart (Overall)
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(df_filtered["Tour"], df_filtered["Cost_per_ticket"])
ax.set_xlabel("Tour")
ax.set_ylabel("Average Cost Per Ticket (Dollars)")
ax.set_title("Average Cost Per Ticket by Tour (Overall)")
st.pyplot(fig)

