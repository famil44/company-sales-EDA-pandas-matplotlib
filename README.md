# 📊 Company Sales Dashboard

An interactive Streamlit dashboard for exploring monthly company sales data. Pick a graph from the sidebar, switch between light and dark mode, and see profit and product sales trends at a glance.

## Features

- Select from 7 graphs:
  - Month vs Total Profit (line)
  - Month vs Sales of all products (line, with product filter)
  - Total Profit by Month (bar)
  - Total Profit by Month (scatter)
  - Total Profit share by Month (pie)
  - Multi-chart dashboard (2x2)
  - Total Units distribution (histogram)
- Light and dark themes, with charts and text colours adjusted for readability
- Summary metrics: total profit, total units, best month, duplicate rows
- Data overview: head, column types, missing values
- Upload your own CSV from the sidebar

## Dataset

`company_sales_data.csv` contains monthly sales for six products and the totals.

| Column | Description |
|---|---|
| month_number | Month (1-12) |
| facecream, facewash, toothpaste, bathingsoap, shampoo, moisturizer | Units sold per product |
| total_units | Total units sold in the month |
| total_profit | Total profit in the month |

## Project structure

```
├── app.py                  # Streamlit dashboard
├── analysis.ipynb          # original pandas/matplotlib exploration
├── company_sales_data.csv  # dataset
├── requirements.txt        # dependencies
└── README.md
```

## Run locally

```bash
git clone https://github.com/famil44/company-sales-EDA-pandas-matplotlib.git
cd company-sales-EDA-pandas-matplotlib
pip install -r requirements.txt
streamlit run app.py
```

The app opens at http://localhost:8501.

## Tech stack

Python, Streamlit, pandas, matplotlib

## Author

FAMIL · [GitHub](https://github.com/famil44)
