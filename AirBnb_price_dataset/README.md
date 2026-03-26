# Airbnb Pricing Analysis Dashboard

An interactive Streamlit dashboard for analyzing Airbnb listing prices, room characteristics, and market segments.

## Project Overview

This project explores Airbnb pricing behavior using interactive visual analytics. The dashboard helps users understand how listing prices vary by:

- Price segment
- Property type
- Room type
- Listing features such as bedrooms, bathrooms, beds, and guest capacity

The goal is to turn raw Airbnb data into a business-style dashboard that supports pricing and segmentation analysis.

---

## Key Features

- Interactive sidebar filters:
  - Price Category
  - Property Type
  - Room Type
  - Top N Categories

- KPI summary cards:
  - Average Price
  - Average Bedrooms
  - Average Accommodates
  - Total Listings

- Visualizations:
  - Price Comparison by Segment
  - Price Distribution
  - Listings by Price Category
  - Average Price by Property Type
  - Average Price by Room Type
  - Correlation Heatmap
  - Segment Summary Table

- Dynamic insight messages based on selected filters

---

## Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit

---

## Project Structure

````text
AirBnb_price_dataset/
│
├── data/
│   ├── Airbnb_Data.csv
│   └── input_Data.csv
│
├── dashboard/
│   └── app.py
│
├── README.md
└── requirements.txt
´´´
---
##  Data Description

### 1. Airbnb_Data.csv
Main dataset containing:
- Price (or log_price)
- Bedrooms, bathrooms, beds
- Accommodates
- Other listing features

### 2. input_Data.csv
Feature-engineered dataset including:
- One-hot encoded property types
- Room types
- Cancellation policies
- Booking features

-> Both datasets have:
- Same number of rows
- Same row order

So they are merged **column-wise** using `pd.concat()`.

---

##  Data Processing

The dashboard performs:

- Data merging (main + engineered dataset)
- Price reconstruction (from log_price if needed)
- Price segmentation:
  - Budget (< €100)
  - Mid-Range (€100–€200)
  - Premium (> €200)
- Decoding one-hot encoded columns into readable labels:
  - Property Type
  - Room Type

---

##  How to Run

### 1. Clone the repository

```bash
git clone https://github.com/your-username/airbnb-pricing-dashboard.git
cd airbnb-pricing-dashboard
´´´

### 2. Install dependencies
´´´bash
pip install -r requirements.txt
´´´

### 3. Run the dashboard
´´´bash
streamlit run dashboard/app.py
´´´

##  Example Insights

- Budget and Mid-Range listings dominate the market
- Premium listings are fewer but significantly higher priced
- Price increases with:
  - Number of bedrooms
  - Guest capacity (accommodates)
- Property type has a strong influence on pricing
- Room type impacts average price significantly

---

##  Business Value

This dashboard demonstrates how data can be used to:

- Optimize pricing strategies
- Identify market segments
- Compare listing categories
- Support data-driven decisions
- Build interactive BI tools using Python

---

##  Use Cases

- Airbnb hosts analyzing pricing strategy
- Data analysts exploring marketplace data
- Students building portfolio projects
- Recruiters evaluating data and dashboard skills

---

##  Future Improvements

- Add location-based analysis (maps)
- Integrate machine learning price prediction
- Deploy dashboard online (Streamlit Cloud)
- Add more booking-related insights
- Improve UI with custom styling

---

##  Author

**Mainuddin Monsur Robin**
Aspiring Data Analyst / Data Engineer
Hamburg, Germany
