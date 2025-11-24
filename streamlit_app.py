import os
from datetime import timedelta

import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Airbnb Simple Dashboard", layout="wide")
st.title("🏠 Airbnb Simple Dashboard")

# =============== Load data ===============
DATA_PATH = "cleaned_data.csv"   # make sure this file is in the same folder

@st.cache_data(show_spinner=True)
def load_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Could not find '{path}'. "
            "Place cleaned_data.csv in the same folder as this script."
        )
    return pd.read_csv(path)

try:
    df = load_data(DATA_PATH)
except Exception as e:
    st.error(str(e))
    st.stop()

st.write(f"Loaded **{len(df):,} rows** and **{df.shape[1]} columns**.")
st.dataframe(df.head(), use_container_width=True)

# =============== Charts ===============
st.subheader("📊 Airbnb Price Visualizations")

# 1️⃣ Histogram – Price distribution
st.markdown("### 1. Price distribution")

price_cap = df["price"].quantile(0.99)
df_price = df[df["price"] <= price_cap]

fig_price_hist = px.histogram(
    df_price,
    x="price",
    nbins=50,
    labels={"price": "Nightly price"},
    title="Nightly price distribution (capped at 99th percentile)",
)
st.plotly_chart(fig_price_hist, use_container_width=True)

# 2️⃣ Bar chart – Average price by room type
if "room_type" in df.columns:
    st.markdown("### 2. Average price by room type")

    room_price = (
        df.groupby("room_type")["price"]
        .mean()
        .reset_index()
        .sort_values("price", ascending=False)
    )

    fig_room_bar = px.bar(
        room_price,
        x="room_type",
        y="price",
        labels={"room_type": "Room type", "price": "Average nightly price"},
        text_auto=".0f",
        title="Average nightly price by room type",
    )
    st.plotly_chart(fig_room_bar, use_container_width=True)
else:
    st.info("Column 'room_type' not found – skipping room-type chart.")

# 3️⃣ Pie chart – Share of listings by room type
if "room_type" in df.columns:
    st.markdown("### 3. Share of listings by room type")

    room_counts = (
        df["room_type"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "room_type", "room_type": "count"})
    )

    fig_room_pie = px.pie(
        room_counts,
        names="room_type",
        values="count",
        title="Listing share by room type",
    )
    st.plotly_chart(fig_room_pie, use_container_width=True)

# 4️⃣ Bar chart – Top 10 cities by average price
if "city" in df.columns:
    st.markdown("### 4. Top 10 cities by average price")

    city_price = (
        df.groupby("city")["price"]
        .mean()
        .reset_index()
        .sort_values("price", ascending=False)
        .head(10)
    )

    fig_city_bar = px.bar(
        city_price,
        x="city",
        y="price",
        labels={"city": "City", "price": "Average nightly price"},
        text_auto=".0f",
        title="Top 10 cities by average nightly price",
    )
    st.plotly_chart(fig_city_bar, use_container_width=True)
else:
    st.info("Column 'city' not found – skipping city chart.")

# =============== DATE-AWARE PRICE PREDICTOR (NO ML) ===============
st.subheader("🧮 Date-aware price per night prediction")

if ("city" in df.columns) and ("room_type" in df.columns):

    colp1, colp2 = st.columns(2)

    with colp1:
        city_val = st.selectbox(
            "City",
            options=sorted(df["city"].dropna().unique()),
        )

    with colp2:
        room_type_val = st.selectbox(
            "Room type",
            options=sorted(df["room_type"].dropna().unique()),
        )

    # Dates
    colp3, colp4 = st.columns(2)
    with colp3:
        check_in = st.date_input("Check-in date")
    with colp4:
        check_out = st.date_input(
            "Check-out date",
            value=check_in + timedelta(days=1),
        )

    if check_out <= check_in:
        st.warning("Check-out date must be after check-in date.")
    else:
        if st.button("Get date-aware price per night"):
            # 1) Base price from historical data
            subset = df[(df["city"] == city_val) & (df["room_type"] == room_type_val)]

            if len(subset) == 0:
                subset = df[df["city"] == city_val]
            if len(subset) == 0:
                subset = df

            base_price = subset["price"].median()

            # 2) Apply simple seasonal + weekend multipliers per night
            stay_dates = pd.date_range(check_in, check_out - timedelta(days=1))

            def date_multiplier(d):
                m = 1.0
                # WEEKEND bump: Fri (4), Sat (5)
                if d.weekday() in [4, 5]:
                    m *= 1.30   # +30%
                # SUMMER bump (June–Aug)
                if d.month in [6, 7, 8]:
                    m *= 1.20   # +20%
                # HOLIDAY season (December)
                if d.month == 12:
                    m *= 1.40   # +40%
                return m

            if len(stay_dates) > 0:
                mults = [date_multiplier(d) for d in stay_dates]
                avg_mult = sum(mults) / len(mults)
            else:
                avg_mult = 1.0

            adjusted_price = base_price * avg_mult
            nights = (check_out - check_in).days

            st.success(
                f"Estimated date-aware price per night: "
                f"**${adjusted_price:,.2f}** "
                f"for a **{room_type_val}** in **{city_val}** "
                f"({nights} night stay)."
            )

else:
    st.info("Need 'city' and 'room_type' columns to run the predictor.")
