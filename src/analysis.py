"""Food delivery order analysis using pandas."""
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "food_orders.csv"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    # Merge two spellings of the same restaurant before aggregating.
    df["restaurant"] = df["restaurant"].replace({"Bake N Shake": "Bake n Shake"})
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    return df


def main() -> None:
    df = load_data()
    delivered = df[df["order_status"].eq("Delivered")]
    cancelled = df[df["order_status"].eq("Cancelled")]

    total_orders = len(df)
    cancellation_rate = len(cancelled) / total_orders * 100 if total_orders else 0
    rating_response_rate = delivered["rating"].notna().mean() * 100 if len(delivered) else 0

    print("FOOD DELIVERY DATA ANALYSIS")
    print("=" * 38)
    print(f"Dataset shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"Total orders: {total_orders:,}")
    print(f"Delivered orders: {len(delivered):,}")
    print(f"Cancelled orders: {len(cancelled):,}")
    print(f"Cancellation rate: {cancellation_rate:.2f}%")
    print(f"Food sales before discounts and delivery fees: Rs. {df['item_total'].sum():,.2f}")
    print(f"Average food order value: Rs. {df['item_total'].mean():,.2f}")
    print(f"Duplicate rows: {df.duplicated().sum()}")

    print("\nMISSING VALUES")
    print(df.isna().sum().to_string())
    print(f"\nCustomer rating response rate among delivered orders: {rating_response_rate:.2f}%")

    print("\nTOP 5 CITIES BY FOOD SALES")
    print(df.groupby("city")["item_total"].sum().sort_values(ascending=False).head(5).round(2).to_string())

    print("\nTOP 5 RESTAURANTS BY FOOD SALES")
    print(df.groupby("restaurant")["item_total"].sum().sort_values(ascending=False).head(5).round(2).to_string())

    print("\nCANCELLATION RATE BY CITY (%)")
    city_cancellations = df.assign(
        cancelled=df["order_status"].eq("Cancelled")
    ).groupby("city")["cancelled"].mean().mul(100)
    print(city_cancellations.sort_values(ascending=False).round(2).to_string())

    print("\nFASTEST 5 RESTAURANTS BY AVERAGE DELIVERY TIME (MINUTES)")
    print(delivered.groupby("restaurant")["delivery_time"].mean().sort_values().head(5).round(2).to_string())

    print("\nTOP 5 RESTAURANTS BY AVERAGE CUSTOMER RATING")
    ratings = delivered.groupby("restaurant")["rating"].mean().dropna().sort_values(ascending=False)
    print(ratings.head(5).round(2).to_string())


if __name__ == "__main__":
    main()
