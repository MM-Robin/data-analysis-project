import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Supermarket Sales Dashboard", layout="wide")

# Load data
BASE_DIR = Path(__file__).resolve().parent.parent
main_path = BASE_DIR / "data" / "supermarket_sales.csv"
data = pd.read_csv(main_path)
data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
st.write("Date dtype:", data["Date"].dtype)

# Title
st.title("🛒 Supermarket Sales Dashboard")

# Sidebar filters
st.sidebar.header("Filters")

branch = st.sidebar.selectbox("Branch", ["All"] + list(data['Branch'].unique()))
product = st.sidebar.selectbox("Product Line", ["All"] + list(data['Product line'].unique()))

# Filter logic
filtered_data = data.copy()

if branch != "All":
    filtered_data = filtered_data[filtered_data['Branch'] == branch]

if product != "All":
    filtered_data = filtered_data[filtered_data['Product line'] == product]

# KPI
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"{filtered_data['Sales'].sum():.2f}")
col2.metric("Avg Sales", f"{filtered_data['Sales'].mean():.2f}")
col3.metric("Transactions", len(filtered_data))
col4.metric("Avg Rating", f"{filtered_data['Rating'].mean():.2f}")

# Visualizations
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Product Line")
    product_sales = filtered_data.groupby("Product line")["Sales"].sum().sort_values(ascending=False)

    fig1, ax1 = plt.subplots(figsize=(6, 4))
    product_sales.plot(kind="bar", ax=ax1)
    ax1.set_xlabel("Product Line")
    ax1.set_ylabel("Total Sales")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig1, clear_figure=True)

with col2:
    st.subheader("Payment Method Distribution")
    payment_counts = filtered_data["Payment"].value_counts()

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.pie(payment_counts, labels=payment_counts.index, autopct="%1.1f%%", startangle=90)
    ax2.axis("equal")
    st.pyplot(fig2, clear_figure=True)

# Time series chart
data["Date"] = pd.to_datetime(data["Date"])

st.markdown("---")
st.subheader("Monthly Sales Trend")

# Create a monthly sales trend line chart
monthly_sales = (
    filtered_data.groupby(filtered_data["Date"].dt.to_period("M"))["Sales"]
    .sum()
)
# Convert PeriodIndex to string for plotting
monthly_sales.index = monthly_sales.index.astype(str)

# Create line chart
fig3, ax3 = plt.subplots(figsize=(8, 4))
monthly_sales.plot(kind="line", marker="o", ax=ax3)
ax3.set_xlabel("Month")
ax3.set_ylabel("Total Sales")
ax3.set_title("Monthly Sales Trend")
ax3.grid(axis="y", linestyle="--", alpha=0.7)

# Rotate x-axis labels for better readability
st.pyplot(fig3, clear_figure=True)

# sales by gender and customer type
st.markdown("---")

col5, col6 = st.columns(2)

with col5:
    st.subheader("Sales by Gender")

    gender_sales = filtered_data.groupby("Gender")["Sales"].sum()

    fig4, ax4 = plt.subplots(figsize=(6, 4))
    gender_sales.plot(kind="bar", ax=ax4)
    ax4.set_xlabel("Gender")
    ax4.set_ylabel("Total Sales")
    st.pyplot(fig4, clear_figure=True)


with col6:
    st.subheader("Sales by Customer Type")

    customer_sales = filtered_data.groupby("Customer type")["Sales"].sum()

    fig5, ax5 = plt.subplots(figsize=(6, 4))
    customer_sales.plot(kind="bar", ax=ax5)
    ax5.set_xlabel("Customer Type")
    ax5.set_ylabel("Total Sales")
    st.pyplot(fig5, clear_figure=True)

# Predictive modeling (Linear Regression)
features = ["Unit price", "Quantity", "Rating"]

X = data[features]
y = data["Sales"]

model = LinearRegression()
model.fit(X, y)

st.markdown("---")
st.subheader("🔮 Predict Sales")

unit_price = st.number_input("Unit Price", value=50.0)
quantity = st.number_input("Quantity", value=5)
rating = st.number_input("Rating", value=7.0)

if st.button("Predict Sales"):
    import numpy as np
    prediction = model.predict([[unit_price, quantity, rating]])
    st.success(f"Estimated Sales: €{prediction[0]:.2f}")


st.markdown("""
### 🔮 Prediction Explanation

The model predicts total sales based on unit price, quantity, and rating.  
It uses patterns from past data to estimate how much revenue a transaction will generate.
""")