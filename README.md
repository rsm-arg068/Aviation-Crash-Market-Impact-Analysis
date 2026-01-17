# ✈️ Aviation Crash & Stock Market Impact Analysis

This project analyzes the relationship between aviation incidents and their impact on stock market performance of airlines and aircraft manufacturers. Using an event study framework, the dashboard evaluates how markets react to aviation crashes in terms of **immediate price impact**, **recovery time**, and **cumulative abnormal returns**.

The analysis is presented through an interactive **Streamlit dashboard** with dynamic filters and visualizations.

---

## 📊 Key Concepts & Metrics

The dashboard focuses on three core event-study metrics:

- **MAE (Maximum Absolute Effect)**  
  Measures the largest absolute abnormal return observed during the event window.

- **TTR (Time to Recovery)**  
  Measures how many days it takes for stock prices to recover after an aviation incident.

- **CAR / CAAR (Cumulative Abnormal Returns)**  
  Captures the cumulative market impact before and after an incident, averaged across events.

---

## 🧠 Dashboard Features

- Interactive sidebar filters for:
  - Accident severity (Minor / Moderate / Severe)
  - Aircraft manufacturer (Boeing / Airbus)
  - Year range
- Distribution and box plots for MAE and TTR
- Event-study style CAAR plots around crash dates
- Severity and manufacturer comparisons
- Correlation analysis between market impact, fatalities, and injuries
- Clean, responsive UI built with Streamlit and Plotly

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** – interactive dashboard
- **Pandas & NumPy** – data handling
- **Plotly** – interactive visualizations
- **Statsmodels** – OLS trendlines for event-study plots
- **Git LFS** – large dataset version control

---
