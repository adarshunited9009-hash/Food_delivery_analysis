"""Generate a four-chart food delivery analytics dashboard."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "food_orders.csv"
OUTPUT_PATH = PROJECT_ROOT / "images" / "dashboard.png"


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    df["restaurant"] = df["restaurant"].replace({"Bake N Shake": "Bake n Shake"})

    city_sales = df.groupby("city")["item_total"].sum().sort_values(ascending=False).head(5)
    restaurant_sales = df.groupby("restaurant")["item_total"].sum().sort_values().tail(5)
    order_status = df["order_status"].value_counts().reindex(["Delivered", "Cancelled"], fill_value=0)
    rating_counts = (
        df["rating"].dropna().astype(int).value_counts()
        .sort_index().reindex([1, 2, 3, 4, 5], fill_value=0)
    )

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.labelsize": 10,
    })
    fig, axes = plt.subplots(2, 2, figsize=(14, 9), constrained_layout=True)
    fig.suptitle("Food Delivery Analytics Dashboard", fontsize=18, fontweight="bold")

    ax = axes[0, 0]
    bars = ax.bar(city_sales.index, city_sales.values, color="#3977A8", edgecolor="white")
    ax.set_title("Top 5 Cities by Food Sales")
    ax.set_xlabel("City")
    ax.set_ylabel("Food sales (Rs.)")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)
    ax.bar_label(bars, labels=[f"{v:,.0f}" for v in city_sales.values], padding=3, fontsize=9)
    ax.margins(y=0.14)

    ax = axes[0, 1]
    bars = ax.barh(restaurant_sales.index, restaurant_sales.values, color="#E5A93D", edgecolor="white")
    ax.set_title("Top 5 Restaurants by Food Sales")
    ax.set_xlabel("Food sales (Rs.)")
    ax.set_ylabel("Restaurant")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)
    ax.bar_label(bars, labels=[f"{v:,.0f}" for v in restaurant_sales.values], padding=4, fontsize=9)
    ax.set_xlim(0, restaurant_sales.max() * 1.18)

    ax = axes[1, 0]
    bars = ax.bar(order_status.index, order_status.values,
                  color=["#3A9D75", "#D96B5F"], edgecolor="white")
    ax.set_title("Order Status")
    ax.set_xlabel("Order status")
    ax.set_ylabel("Number of orders")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)
    ax.bar_label(bars, padding=3, fontsize=9)
    ax.margins(y=0.12)

    ax = axes[1, 1]
    bars = ax.bar(rating_counts.index.astype(str), rating_counts.values,
                  color="#648FC2", edgecolor="white")
    ax.set_title("Customer Rating Distribution")
    ax.set_xlabel("Rating (1 to 5)")
    ax.set_ylabel("Number of ratings")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)
    ax.bar_label(bars, padding=3, fontsize=9)
    ax.text(
        0.98, 0.95,
        f"Ratings recorded: {rating_counts.sum():,}\nMissing ratings: {df['rating'].isna().sum():,}",
        transform=ax.transAxes, ha="right", va="top", fontsize=8,
        bbox={"boxstyle": "round,pad=0.4", "facecolor": "white",
              "edgecolor": "#cccccc", "alpha": 0.9},
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight")
    print(f"Dashboard saved to: {OUTPUT_PATH}")
    plt.show()


if __name__ == "__main__":
    main()
