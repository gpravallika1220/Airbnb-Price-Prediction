# Airbnb Price Prediction

This repository contains a Big Data & Machine Learning project that predicts **nightly Airbnb prices** and exposes the results through a simple **Streamlit dashboard**.

The project uses the **US Airbnb Open Data** from Kaggle (2020 & 2023) to:
- Clean and integrate large multi-year datasets  
- Explore key pricing patterns across cities and room types  
- Train regression models to predict nightly price  
- Provide an interactive dashboard with visualizations and a **price-per-night estimator**

---

## 1. Problem Statement & Motivation

Airbnb hosts often set prices manually or rely on simple rules (e.g., “similar listings nearby”), which can:

- **Underprice** listings → loss of potential revenue  
- **Overprice** listings → low occupancy and fewer bookings  

Because price depends on many factors—**city, room type, capacity, reviews, and demand**—there is a strong need for a **data-driven pricing assistant**.

**Project goal:**  
Build a pipeline that uses historical listing data to **predict a fair, competitive nightly price** for a given listing based on its characteristics, and expose the insights in an accessible dashboard.

---

## 2. Dataset

This project uses the public **US Airbnb Open Data** from Kaggle:

- `AB_US_2020.csv`  
- `AB_US_2023.csv`  

The dataset contains **hundreds of thousands of listings** across multiple US cities with:

- Listing details: `room_type`, `property_type`, `accommodates`, `bedrooms`, `bathrooms`  
- Location: `city`, `state`, `latitude`, `longitude`  
- Demand & availability: `availability_365`, `minimum_nights`  
- Reviews: `number_of_reviews`, review scores  
- Target: **`price`** (nightly price in USD)

Because of GitHub size limits, the **full raw CSV files are not stored** in this repository.

All dataset links are documented in:

- **`DATASET_SOURCES.md`**

### Using the data locally

1. Download `AB_US_2020.csv` and `AB_US_2023.csv` from Kaggle (links in `DATASET_SOURCES.md`).
2. Place them in your local project folder (e.g., `data/`).
3. Run the data preparation notebook/script to generate a cleaned file such as:

- `cleaned_data.csv` – full cleaned dataset used for modeling and dashboard

(You can also create a smaller `cleaned_sample.csv` for demo purposes.)

---

## 3. Project Structure

A typical structure for this repo:

```text
.
├── s.py or streamlit_app.py      # Streamlit dashboard
├── requirements.txt              # Python dependencies
├── DATASET_SOURCES.md            # Dataset URLs and usage notes
├── notebooks/
│   ├── 01_data_preparation.ipynb # Cleaning & merging 2020 + 2023
│   ├── 02_eda.ipynb              # Exploratory data analysis
│   └── 03_modeling.ipynb         # Model training & evaluation
├── reports/
│   ├── GROUP_07_Problem_and_Dataset.pdf
│   ├── GROUP_07_Data_Preparation_and_EDA_Report.pdf
│   ├── GROUP_07_Midterm_Progress_Report.pdf
│   └── GROUP_07_Project_Progress_Report.pdf
├── cleaned_sample.csv            # (Optional) smaller sample dataset
└── README.md
