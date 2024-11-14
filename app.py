import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import re

# Set Seaborn style for charts
sns.set_theme(style="whitegrid")

# Read CSV data (replace 'taylor_Train.csv' with your actual file path)
try:
    df = pd.read_csv('taylor_Train.csv', encoding="1252")
except FileNotFoundError:
    st.error("The file 'taylor_Train.csv' was not found. Please make sure it's in the correct directory.")
    st.stop()

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
    try:
        return float(re.sub(r'[^\d.]', '', val)) if isinstance(val, str) else 0.0
    except ValueError:
        return 0.0

def clean_tickets(val):
    if isinstance(val, str) and '/' in val:
        return int(val.split("/")[0].replace(',', ''))
    return 0

def clean_available(val):
    if isinstance(val, str) and '/' in val:
        return int(val.split("/")[1].replace(',', ''))
    return 0

# Clean data
df['Revenue'] = df['Revenue'].apply(clean_revenue)
df['tickets_sold'] = df['Tickets_sold_and_available'].apply(clean_tickets)
df['tickets_available'] = df['Tickets_sold_and_available'].apply(clean_available)
df.drop("Tickets_sold_and_available", axis=1, inplace=True)

# Fill missing opening acts with previous values
df['Opening_act'].fillna(method='ffill', inplace=True)

# Calculate cost per ticket
df['Cost_per_ticket'] = df.apply(lambda row: row['Revenue'] / row['tickets_sold'] if row['tickets_sold'] > 0 else np.nan, axis=1)

# Reorder columns for better presentation
repos_index = ["City", "Country", "Venue", "tickets_sold", "tickets_available",
               "Revenue", "Cost_per_ticket", "Tour", "Opening_act"]
df = df.reindex(columns=repos_index)

# ------------------------ Streamlit App ------------------------

# Sidebar for tour selection
st.sidebar.title("Taylor Swift Concert Analysis")
st.sidebar.markdown("Explore revenue, ticket sales, and cost per ticket by tour.")
tour_selection = st.sidebar.selectbox("Select a Tour:", ["All"] + list(df["Tour"].dropna().unique()))

# Filter DataFrame based on user selection (if applicable)
df_filtered = df if tour_selection == "All" else df[df["Tour"] == tour_selection]

# Main app title and introduction
st.title("Taylor Swift Concert Tour Analysis")
st.write("Analyze Taylor Swift's concert data, including revenue, ticket sales, cost per ticket, and more.")

# Display Key Metrics
st.subheader("Key Metrics")
total_revenue = df_filtered['Revenue'].sum()
total_tickets_sold = df_filtered['tickets_sold'].sum()
avg_cost_per_ticket = df_filtered['Cost_per_ticket'].mean()

# Show key metrics with st.metric
st.columns(3)
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Tickets Sold", f"{total_tickets_sold}")
col3.metric("Avg. Cost Per Ticket", f"${avg_cost_per_ticket:,.2f}")

# Tabs for different sections
tab1, tab2 = st.tabs(["Overview", "Visualizations"])

with tab1:
    st.subheader("Concert Data Overview")
    st.write("Here is a table of concert data based on your tour selection.")
    st.dataframe(df_filtered)

    # Descriptive Statistics for Cost per Ticket
    st.subheader("Cost Per Ticket Statistics")
    st.write(df_filtered["Cost_per_ticket"].describe())

with tab2:
    st.subheader("Visualizations")

    # Average Cost Per Ticket Bar Chart by Tour
    fig, ax = plt.subplots(figsize=(10, 6))
    avg_cost_per_ticket = df_filtered.groupby("Tour")["Cost_per_ticket"].mean()
    sns.barplot(x=avg_cost_per_ticket.index, y=avg_cost_per_ticket.values, ax=ax, palette="viridis")
    ax.set_xlabel("Tour")
    ax.set_ylabel("Average Cost Per Ticket (Dollars)")
    ax.set_title("Average Cost Per Ticket by Tour")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Revenue Distribution Histogram
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df_filtered['Revenue'], bins=20, kde=True, ax=ax, color="purple")
    ax.set_xlabel("Revenue (Dollars)")
    ax.set_title("Revenue Distribution")
    st.pyplot(fig)
