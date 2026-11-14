from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "food_orders.csv"
OUTPUT_PATH = PROJECT_ROOT / "images" / "dashboard.png"

df = pd.read_csv(DATA_PATH)
#---------------------------
#city sales
#------------------------------
city_sales = (
    df.groupby("city")["item_total"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print(city_sales)
fig, axes = plt.subplots(2,2,figsize =(14,10))

axes[0,0].bar(city_sales.index, city_sales.values ,
         color = "red" , 
         edgecolor = "black")

axes[0,0].set_title("Top 5 Cities by Food Sales")
axes[0,0].set_xlabel("City")
axes[0,0].set_ylabel("Total Sales (Rs.)")
for i, value in enumerate(city_sales.values):
 axes[0,0].text(i, value, f"{value:,.0f}", ha="center")
axes[0,0].grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
#----------------------------
#resturant sales
#-----------------------------
restaurant_sales = (df.groupby("restaurant")["item_total"]
                   .sum()
                   .sort_values(ascending= False)
                    .head(5))
print(restaurant_sales)

axes[0,1].barh(restaurant_sales.index , restaurant_sales.values
         ,color ="yellow"
         ,edgecolor = "black")
for i, value in enumerate(restaurant_sales.values):
 axes[0,1].text(value, i, f"{value:,.0f}", va="center")
axes[0,1].set_ylabel("resturant")
axes[0,1].set_xlabel("total sales(Rs.)")
axes[0,1].set_title("top 5 resturant by food sales")
axes[0,1].grid(axis="x", linestyle="--", alpha=0.5)
plt.tight_layout()
#-------------------
#order_status_annalysis
#----------------------
order_status = df["order_status"].value_counts()
print(order_status)
axes[1,0].bar(order_status.index,order_status.values,color="blue")
axes[1,0].set_xlabel("order status")
axes[1,0].set_ylabel("number of orders")
axes[1,0].set_title("order status annalysis")
axes[1,0].grid(axis = "y",linestyle = "--",alpha = 0.5)
plt.tight_layout()
#-----------------------
#customer 
#-----------------------
rating_counts= df["rating"].dropna().value_counts().sort_index()
print(rating_counts)
axes[1,1].bar(rating_counts.index,rating_counts.values)
axes[1,1].set_title("customer rating distribution")
axes[1,1].set_xlabel("rating 1-5")
axes[1,1].set_ylabel("Number of customer")
axes[1,1].grid(axis = "y",linestyle = "--",alpha = 0.5)
plt.tight_layout(rect=[0, 0, 1, 0.96])
fig.suptitle("Food Delivery Analytics Dashboard", fontsize=16)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight")
print(f"Dashboard saved to: {OUTPUT_PATH}")

plt.show()
