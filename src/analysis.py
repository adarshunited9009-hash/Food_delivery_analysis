"""Food delivery data analysis.

Run from the repository root:
    python src/analysis.py
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "food_orders.csv"


def load_data() -> pd.DataFrame:
    """Load the dataset and apply basic, documented cleaning."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}\n"
            "Place food_orders.csv inside the repository's data/ folder."
        )

    df = pd.read_csv(DATA_PATH)

    required_columns = {
        "order_id", "order_date", "customer_id", "restaurant", "city",
        "cuisine", "item_total", "delivery_fee", "discount",
        "delivery_time", "rating", "order_status", "payment_method",
    }
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing_columns)}")

    # These two labels refer to the same restaurant in the supplied dataset.
    df["restaurant"] = df["restaurant"].replace(
        {"Bake N Shake": "Bake n Shake"}
    )
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    numeric_columns = [
        "item_total", "delivery_fee", "discount", "delivery_time", "rating"
    ]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


def print_section(title: str) -> None:
    """Print a consistent section heading."""
    print(f"\n{title}")
    print("-" * len(title))


def main() -> None:
    df = load_data()

    delivered = df[df["order_status"].eq("Delivered")].copy()
    cancelled = df[df["order_status"].eq("Cancelled")].copy()
    total_orders = len(df)

    # 1. Dataset overview
    print("FOOD DELIVERY DATA ANALYSIS")
    print("=" * 40)
    print_section("1. DATASET OVERVIEW")
    print(f"Dataset shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"Total orders: {total_orders:,}")
    print("\nFirst five rows:")
    print(df.head().to_string(index=False))
    print("\nData types and non-null counts:")
    df.info()

    # 2. Data quality
    print_section("2. DATA QUALITY CHECK")
    print("Missing values by column:")
    print(df.isna().sum().to_string())
    print(f"\nDuplicate rows: {df.duplicated().sum():,}")
    print("\nMissing delivery times by order status:")
    print(df.groupby("order_status")["delivery_time"].apply(
        lambda values: values.isna().sum()
    ).to_string())
    print("\nMissing ratings by order status:")
    print(df.groupby("order_status")["rating"].apply(
        lambda values: values.isna().sum()
    ).to_string())

    # 3. Order value and food sales
    print_section("3. ORDER VALUE AND FOOD SALES")
    print(f"Total food sales before discounts and delivery fees: Rs. {df['item_total'].sum():,.2f}")
    print(f"Average food order value: Rs. {df['item_total'].mean():,.2f}")
    print(f"Highest food order value: Rs. {df['item_total'].max():,.2f}")
    print(f"Lowest food order value: Rs. {df['item_total'].min():,.2f}")
    print(f"Orders above Rs. 500: {(df['item_total'] > 500).sum():,}")
    print(f"Orders below Rs. 200: {(df['item_total'] < 200).sum():,}")
    print("\nFood order value descriptive statistics:")
    print(df["item_total"].describe().round(2).to_string())

    # 4. City and cuisine analysis
    print_section("4. CITY AND CUISINE ANALYSIS")
    print("Orders by city:")
    print(df["city"].value_counts().to_string())
    print("\nFood sales by city:")
    print(df.groupby("city")["item_total"].sum()
          .sort_values(ascending=False).round(2).to_string())
    print("\nAverage food order value by city:")
    print(df.groupby("city")["item_total"].mean()
          .sort_values(ascending=False).round(2).to_string())
    print("\nOrders by cuisine:")
    print(df["cuisine"].value_counts().to_string())

    # 5. Restaurant performance
    print_section("5. RESTAURANT PERFORMANCE")
    restaurant_summary = df.groupby("restaurant").agg(
        orders=("order_id", "count"),
        food_sales=("item_total", "sum"),
        average_order_value=("item_total", "mean"),
    ).sort_values("food_sales", ascending=False)
    print("Restaurant performance (sorted by food sales):")
    print(restaurant_summary.round(2).to_string())

    print("\nTop five restaurants by food sales:")
    print(restaurant_summary["food_sales"].head(5).round(2).to_string())

    # 6. Order status and cancellations
    print_section("6. ORDER STATUS AND CANCELLATIONS")
    print("Order status counts:")
    print(df["order_status"].value_counts().to_string())
    cancellation_rate = (
        len(cancelled) / total_orders * 100 if total_orders else 0
    )
    print(f"\nOverall cancellation rate: {cancellation_rate:.2f}%")

    city_cancellation = (
        df.assign(is_cancelled=df["order_status"].eq("Cancelled"))
        .groupby("city")["is_cancelled"]
        .mean()
        .mul(100)
        .sort_values(ascending=False)
    )
    print("\nCancellation rate by city (%):")
    print(city_cancellation.round(2).to_string())

    # 7. Delivery performance
    print_section("7. DELIVERY TIME ANALYSIS")
    print(f"Delivered orders with a recorded delivery time: {delivered['delivery_time'].notna().sum():,}")
    print(f"Average delivery time: {delivered['delivery_time'].mean():.2f} minutes")
    print(f"Median delivery time: {delivered['delivery_time'].median():.2f} minutes")
    print("\nAverage delivery time by restaurant (minutes):")
    delivery_by_restaurant = (
        delivered.groupby("restaurant")["delivery_time"]
        .mean()
        .dropna()
        .sort_values()
    )
    print(delivery_by_restaurant.round(2).to_string())
    print("\nFive fastest restaurants by average delivery time:")
    print(delivery_by_restaurant.head(5).round(2).to_string())

    # 8. Payment method analysis
    print_section("8. PAYMENT METHOD ANALYSIS")
    payment_counts = df["payment_method"].value_counts()
    payment_share = df["payment_method"].value_counts(normalize=True).mul(100)
    payment_summary = pd.DataFrame({
        "orders": payment_counts,
        "share_percent": payment_share,
    })
    print(payment_summary.round(2).to_string())

    # 9. Discounts
    print_section("9. DISCOUNT ANALYSIS")
    discounted_orders = df[df["discount"].fillna(0) > 0]
    non_discounted_orders = df[df["discount"].fillna(0) == 0]
    print(f"Orders with a discount: {len(discounted_orders):,}")
    print(f"Orders without a discount: {len(non_discounted_orders):,}")
    print(f"Total recorded discounts: Rs. {df['discount'].sum():,.2f}")
    print(f"Average discount amount: Rs. {df['discount'].mean():,.2f}")
    print(
        "Average food order value (discounted orders): "
        f"Rs. {discounted_orders['item_total'].mean():,.2f}"
    )
    print(
        "Average food order value (non-discounted orders): "
        f"Rs. {non_discounted_orders['item_total'].mean():,.2f}"
    )
    print(
        "\nNote: these are descriptive comparisons; they do not prove that "
        "discounts caused a change in order value."
    )

    # 10. Customer ratings
    print_section("10. CUSTOMER RATING ANALYSIS")
    recorded_ratings = delivered["rating"].dropna()
    rating_response_rate = (
        recorded_ratings.size / len(delivered) * 100 if len(delivered) else 0
    )
    print(f"Recorded ratings: {recorded_ratings.size:,}")
    print(f"Average customer rating: {recorded_ratings.mean():.2f}")
    print(f"Rating response rate among delivered orders: {rating_response_rate:.2f}%")
    print("\nRating distribution:")
    print(recorded_ratings.value_counts().sort_index().to_string())
    print("\nAverage rating by restaurant:")
    restaurant_ratings = (
        delivered.groupby("restaurant")["rating"]
        .mean()
        .dropna()
        .sort_values(ascending=False)
    )
    print(restaurant_ratings.round(2).to_string())

    # 11. Final summary
    print_section("11. BUSINESS SUMMARY")
    if not city_cancellation.empty:
        print(f"City with highest cancellation rate: {city_cancellation.index[0]} "
              f"({city_cancellation.iloc[0]:.2f}%)")
    if not restaurant_summary.empty:
        print(f"Highest food sales restaurant: {restaurant_summary.index[0]} "
              f"(Rs. {restaurant_summary.iloc[0]['food_sales']:,.2f})")
    if not delivery_by_restaurant.empty:
        print(f"Fastest average delivery: {delivery_by_restaurant.index[0]} "
              f"({delivery_by_restaurant.iloc[0]:.2f} minutes)")
    if not restaurant_ratings.empty:
        print(f"Highest average rating: {restaurant_ratings.index[0]} "
              f"({restaurant_ratings.iloc[0]:.2f}/5)")

    print("\nInterpretation note: item_total represents food-item sales before "
          "discounts and delivery fees, not net revenue or total customer payment.")


if __name__ == "__main__":
    main()
