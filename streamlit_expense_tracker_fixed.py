import streamlit as st
import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Personal Expense Tracker", layout="centered")
st.title("🧾 Personal Expense Tracker")

filename = "expenses.csv"

# Create the CSV file if not exists
try:
    with open(filename, 'x', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Category', 'Amount'])
except FileExistsError:
    pass

# Function to add expense
def add_expense(category, amount):
    date = datetime.now().strftime("%Y-%m-%d")
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([date, category, amount])
    st.success(f"Added: {category} - Rs. {amount} on {date}")

# Sidebar: Add new expense
st.sidebar.header("➕ Add New Expense")
category = st.sidebar.text_input("Category")
amount = st.sidebar.number_input("Amount (Rs.)", min_value=0.0, step=10.0)
if st.sidebar.button("Add Expense"):
    if category and amount > 0:
        add_expense(category, amount)
    else:
        st.sidebar.warning("Please enter valid data.")

# Load data
df = pd.read_csv(filename)

# Clean and format Date
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df.dropna(subset=['Date', 'Amount', 'Category'], inplace=True)
df['Date'] = df['Date'].dt.date  # keep only date part
df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M')

st.subheader("📋 Recent Expenses")
st.dataframe(df.tail(10), use_container_width=True)

# Summary
total_spent = df['Amount'].sum()
category_summary = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
monthly_summary = df.groupby('Month')['Amount'].sum()

st.subheader("💰 Total Spent")
st.metric(label="Total", value=f"Rs. {total_spent:.2f}")

st.subheader("📊 Expenses by Category")
st.bar_chart(category_summary)

st.subheader("📆 Monthly Expense Trend")
st.line_chart(monthly_summary)

st.subheader("🥧 Category Share")
fig, ax = plt.subplots()
category_summary.plot(kind='pie', autopct='%1.1f%%', startangle=140, ax=ax)
ax.set_ylabel("")
st.pyplot(fig)
