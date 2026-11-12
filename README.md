# Food Delivery Data Analysis

An exploratory data analysis project using Python, Pandas and Matplotlib to understand food delivery orders, sales patterns, restaurant performance, delivery operations and customer ratings.

## Dashboard

![Food Delivery Analytics Dashboard](images/dashboard.png)

## Project overview

The dataset contains **1,000 orders** and **13 columns** covering order details, customers, restaurants, cities, cuisine, order values, delivery information, ratings, order status and payment methods.

The analysis includes:
- Dataset exploration, missing-value checks and duplicate checks
- Food sales and average order value calculations
- City- and restaurant-level sales comparisons
- Order status and cancellation analysis
- Delivery-time analysis for delivered orders
- Customer rating analysis and rating-response coverage
- A four-chart Matplotlib dashboard

## Key findings

| Metric | Result |
|---|---:|
| Total orders | 1,000 |
| Delivered orders | 916 |
| Cancelled orders | 84 |
| Cancellation rate | 8.40% |
| Food sales (item_total) | Rs. 4,27,690.36 |
| Average food order value | Rs. 427.69 |
| Duplicate rows | 0 |
| Missing delivery times | 84 |
| Missing customer ratings | 256 |

### Business observations

- Indore has the highest food sales among the cities in the dataset.
- Bake n Shake is the highest-selling restaurant after combining its two spellings.
- Jabalpur has the highest cancellation rate among the listed cities.
- Manohar Dairy has the lowest average delivery time among restaurants with delivered-order timing data.
- Goodluck Cafe has the highest average customer rating in the dataset.

## Data quality notes

- `Bake N Shake` and `Bake n Shake` are standardized to `Bake n Shake` before restaurant-level aggregation so the same restaurant is not counted twice.
- Missing delivery times belong to cancelled orders in this dataset; they are not treated as zero-minute deliveries.
- Missing ratings are excluded from rating averages and rating-distribution charts. The dataset has 744 recorded ratings.
- `item_total` is treated as food-item sales before discounts and delivery fees. It should not be described as net revenue or total customer payment.
- This is a descriptive analysis of the supplied dataset; it does not establish why cancellations or rating patterns occur.

## Repository structure

```text
Food_delivery_analysis/
├── data/
│   └── food_orders.csv
├── images/
│   └── dashboard.png
├── src/
│   ├── analysis.py
│   └── dashboard.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Run locally

1. Clone the repository:

   ```bash
   git clone https://github.com/adarshunited9009-hash/Food_delivery_analysis.git
   cd Food_delivery_analysis
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the analysis:

   ```bash
   python src/analysis.py
   ```

4. Generate the dashboard:

   ```bash
   python src/dashboard.py
   ```

The dashboard image is saved to `images/dashboard.png`.

## Tools used

- Python
- Pandas
- Matplotlib
- VS Code

## Learning outcomes

This project provided hands-on practice with data loading, data inspection, missing-value analysis, filtering, grouping and aggregation, sorting, descriptive statistics, data cleaning, and data visualization.

---

*Created as a learning and portfolio project.*
