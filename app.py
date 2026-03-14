from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    df = pd.read_csv("data/transactions.csv")

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month

    # DEFAULT VALUES
    selected_category = None
    selected_month = None

    if request.method == "POST":
        selected_category = request.form.get("category")
        selected_month = request.form.get("month")

        # APPLY FILTERS
        if selected_category and selected_category != "All":
            df = df[df["category"] == selected_category]

        if selected_month and selected_month != "All":
            df = df[df["month"] == int(selected_month)]

    # CATEGORY CHART
    category_spend = df.groupby("category")["amount"].sum()
    plt.figure()
    category_spend.plot(kind="bar")
    plt.title("Category Spending")
    plt.savefig("static/category.png")
    plt.close()

    # MONTHLY TREND
    monthly_spend = df.groupby("month")["amount"].sum()
    plt.figure()
    monthly_spend.plot(kind="line", marker="o")
    plt.title("Monthly Spending")
    plt.savefig("static/monthly.png")
    plt.close()

    total_spend = df["amount"].sum()
    avg_spend = df["amount"].mean()
    total_transactions = len(df)

    return render_template(
    "index.html",
    categories=df["category"].unique(),
    selected_category=selected_category,
    selected_month=selected_month,
    total_spend=round(total_spend, 2),
    avg_spend=round(avg_spend, 2),
    total_transactions=total_transactions

    )

if __name__ == "__main__":
    app.run(debug=True)