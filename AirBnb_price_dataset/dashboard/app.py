import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

st.set_page_config(page_title="Airbnb Pricing Dashboard", layout="wide")

# Load data
BASE_DIR = Path(__file__).resolve().parent.parent
main_path = BASE_DIR / "data" / "Airbnb_Data.csv"
input_path = BASE_DIR / "data" / "input_Data.csv"

main_data = pd.read_csv(main_path)
input_data = pd.read_csv(input_path)


new_cols = [col for col in input_data.columns if col not in main_data.columns]
data = pd.concat([main_data, input_data[new_cols]], axis=1)

# Ensure price exists
if 'price' not in data.columns:
    data['price'] = np.exp(data['log_price'])

# Ensure price category exists
def price_category(price):
    if price < 100:
        return "Budget"
    elif price < 200:
        return "Mid-Range"
    else:
        return "Premium"

def decode_property_type(row):
    for col in data.columns:
        if col.startswith("property_type_"):
            value = row[col]
            if pd.notna(value) and str(value) in ["1", "1.0", "True", "true"]:
                return col.replace("property_type_", "")
    return "Apartment / Base Category"

def decode_room_type(row):
    for col in data.columns:
        if col.startswith("room_type_"):
            value = row[col]
            if pd.notna(value) and str(value) in ["1", "1.0", "True", "true"]:
                return col.replace("room_type_", "")
    return "Entire home / apt"


if 'price_category' not in data.columns:
    data['price_category'] = data['price'].apply(price_category)

if 'property_type_label' not in data.columns:
    data['property_type_label'] = data.apply(decode_property_type, axis=1)

if 'room_type_label' not in data.columns:
    data['room_type_label'] = data.apply(decode_room_type, axis=1)

#################################
############ Sidebar ############
#################################
st.sidebar.header("Filters")

st.sidebar.markdown("### Pricing")
category = st.sidebar.selectbox(
    "Price Category",
    ["All"] + list(data['price_category'].unique())
)

st.sidebar.markdown("### Property")
selected_property = st.sidebar.selectbox(
    "Property Type",
    ["All"] + sorted(data['property_type_label'].dropna().unique().tolist())
)

st.sidebar.markdown("### Room")
selected_room = st.sidebar.selectbox(
    "Room Type",
    ["All"] + sorted(data['room_type_label'].dropna().unique().tolist())
)

st.sidebar.markdown("### Controls")
top_n = st.sidebar.slider(
    "Top N Categories",
    min_value=5,
    max_value=20,
    value=10
)
#################################
########## Filter data ##########
#################################

# Start with full data
filtered_data = data.copy()

# Apply price category filter
if category != "All":
    filtered_data = filtered_data[filtered_data['price_category'] == category]

# Apply property type filter
if selected_property != "All":
    filtered_data = filtered_data[filtered_data['property_type_label'] == selected_property]

# Apply room type filter
if selected_room != "All":
    filtered_data = filtered_data[filtered_data['room_type_label'] == selected_room]


# Check if filtered data is empty
if filtered_data.empty:
    st.warning("No data available for the selected filters. Please choose different filter values.")
    st.stop()

#############################
########### Title ###########
#############################
st.title("Airbnb Pricing Analysis Dashboard")
st.markdown(
    "Interactive dashboard for exploring pricing patterns, listing characteristics, and market segments."
)
st.markdown("### Executive Overview")

# KPI row
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Average Price (€)", f"{filtered_data['price'].mean():.2f}")
kpi2.metric("Avg Bedrooms", f"{filtered_data['bedrooms'].mean():.2f}")
kpi3.metric("Avg Accommodates", f"{filtered_data['accommodates'].mean():.2f}")
kpi4.metric("Total Listings", f"{len(filtered_data)}")

st.markdown("---")

avg_price = filtered_data['price'].mean()
avg_capacity = filtered_data['accommodates'].mean()

st.success(
    f"Filtered data shows an average price of €{avg_price:.2f} with average capacity of {avg_capacity:.1f} guests."
)
st.markdown("### Price Comparison by Segment")

segment_order = ["Budget", "Mid-Range", "Premium"]
segment_avg = (
    filtered_data.groupby("price_category")["price"]
    .mean()
    .reindex(segment_order)
    .dropna()
)

fig_seg, ax_seg = plt.subplots(figsize=(5, 2.5))
segment_avg.plot(kind="bar", ax=ax_seg, color="purple")
ax_seg.set_ylabel("Average Price (€)")
ax_seg.set_title("Average Price per Segment", fontsize=10)
ax_seg.grid(axis="y", linestyle="--", alpha=0.7)

st.pyplot(fig_seg, clear_figure=True)

st.markdown("---")

st.info(
    "Most listings are concentrated in the Budget and Mid-Range segments, while Premium listings are fewer but significantly higher priced."
)

st.markdown("---")

# First row of charts
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Price Distribution")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.histplot(filtered_data['price'], kde=True, ax=ax)
    ax.set_xlabel("Price")
    ax.set_ylabel("Count")
    st.pyplot(fig, clear_figure=True)

# category chart
with col2:
    st.markdown("#### Listings by Price Category")
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    filtered_data['price_category'].value_counts().plot(kind='bar', ax=ax2, color='green')
    ax2.set_title("Listings by Price Category")
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    ax2.set_xlabel("Price Category")
    ax2.set_ylabel("Count")
    st.pyplot(fig2, clear_figure=True)

st.markdown("---")

# Second row of charts
col3, col4 = st.columns(2)

with col3:
    st.markdown("#### Average Price by Property Type")

    property_price = (
        filtered_data.groupby('property_type_label')['price']
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
    )

    fig4, ax4 = plt.subplots(figsize=(6, 4))
    property_price.plot(kind='bar', ax=ax4, color='skyblue')
    ax4.set_title("Average Price by Property Type")
    ax4.grid(axis='y', linestyle='--', alpha=0.7)
    ax4.set_xlabel("Property Type")
    ax4.set_ylabel("Average Price (€)")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig4, clear_figure=True)

# Room type chart
with col4:
    st.markdown("#### Average Price by Room Type")

    room_price = (
        filtered_data.groupby('room_type_label')['price']
        .mean()
        .sort_values(ascending=False)
    )

    fig5, ax5 = plt.subplots(figsize=(6, 4))
    room_price.plot(kind='bar', ax=ax5, color='orange')
    ax5.set_title("Average Price by Room Type")
    ax5.grid(axis='y', linestyle='--', alpha=0.7)
    ax5.set_xlabel("Room Type")
    ax5.set_ylabel("Average Price (€)")
    plt.xticks(rotation=30, ha='right')
    st.pyplot(fig5, clear_figure=True)

st.markdown("---")
col5, col6 = st.columns(2)

with col5:
    st.markdown("#### Correlation Heatmap")
    corr_cols = ['price', 'accommodates', 'bedrooms', 'bathrooms', 'beds']
    corr = filtered_data[corr_cols].corr()

    fig3, ax3 = plt.subplots(figsize=(7, 4))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax3)
    ax3.set_title("Feature Correlation")
    st.pyplot(fig3, clear_figure=True)

with col6:
    st.markdown("#### Segment Summary")
    segment_summary = filtered_data.groupby('price_category')[
        ['price', 'accommodates', 'bedrooms', 'bathrooms', 'beds']
    ].mean().round(2)
    st.dataframe(segment_summary, width="stretch")


# Insights section
left, right = st.columns(2)
top_segment = filtered_data['price_category'].value_counts().idxmax()

with left:
    st.markdown("#### Key Insights")
    st.markdown(f"""
    - The dominant segment in the current filtered view is **{top_segment}**.
    - Higher prices are generally associated with larger guest capacity and more bedrooms.
    - Property and room type both influence average pricing levels.
    - Filtered results help identify the most relevant market segment for analysis.
    """)

with right:
    st.markdown("#### Recommendations")
    st.markdown("""
    - Focus on the Mid-Range segment for broader market reach.
    - Increase capacity and bedroom count to support higher pricing.
    - Position Premium listings toward families and group travelers.
    - Use listing features to guide pricing strategy.
    """)