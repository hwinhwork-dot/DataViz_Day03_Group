"""GoMart · Operations report 2025 (draft by the intern team).

This is the code that produced gomart_bad_report.pdf. It is given to you on purpose:
the six charts are BAD examples. Run it to see how each one was made, then audit and
redesign them (Group Homework 3). Do NOT copy its design choices into your own work.

Needs: gomart_orders_2025_clean.csv, gomart_districts.csv, gomart_targets_2025.csv
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

orders = pd.read_csv("gomart_orders_2025_clean.csv", parse_dates=["order_time"])
districts = pd.read_csv("gomart_districts.csv")
targets = pd.read_csv("gomart_targets_2025.csv")
orders = orders.merge(districts, on="district", how="left")
orders["month"] = orders["order_time"].dt.strftime("%Y-%m")
delivered = orders[orders["status"] == "delivered"]


def page(fig, n, title):
    fig.suptitle(f"GoMart Operations Report 2025  |  Chart {n}: {title}", fontsize=10, x=0.02, ha="left",
                 color="grey")


def chart1():
    """Orders by district."""
    counts = orders["district"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(counts.values, labels=counts.index, autopct="%1.2f%%", shadow=True,
           explode=[0.05] * len(counts), colors=plt.cm.jet(np.linspace(0, 1, len(counts))),
           textprops=dict(fontsize=8))
    ax.legend(counts.index, loc="center left", bbox_to_anchor=(1.0, 0.5), title="District")
    ax.set_title("ORDERS BY DISTRICT")
    page(fig, 1, "Orders by district")
    return fig


def chart2():
    """Orders and e-wallet share per month."""
    n = orders.groupby("month").size()
    share = orders.groupby("month")["payment"].apply(lambda s: (s == "E-wallet").mean() * 100)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(n.index, n.values, color=plt.cm.rainbow(np.linspace(0, 1, 12)), label="Orders")
    ax.set_ylim(380, 560)
    ax2 = ax.twinx()
    ax2.plot(share.index, share.values, color="red", marker="s", lw=3, label="E-wallet %")
    ax2.set_ylim(25, 65)
    ax.grid(True, color="black", lw=0.5)
    ax.set_xticks(range(12), n.index, rotation=45)
    ax.legend(loc="upper left"); ax2.legend(loc="upper right")
    ax.set_title("Orders and E-wallet Payments 2025")
    page(fig, 2, "Payments")
    return fig


def chart3():
    """Average delivery time per district."""
    avg = delivered.groupby("district")["delivery_min"].mean()        # alphabetical order
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(avg.index, avg.values, color=plt.cm.jet(np.linspace(0, 1, len(avg))),
                  edgecolor="black")
    ax.bar_label(bars, labels=[f"{v:.4f}" for v in avg.values], fontsize=8)
    ax.set_ylim(25, 55)
    plt.xticks(rotation=90)
    ax.set_title("Average Delivery Time (minutes) by District")
    page(fig, 3, "Delivery")
    return fig


def chart4():
    """Orders by weekday and hour."""
    orders["weekday"] = orders["order_time"].dt.day_name()
    t = orders.pivot_table(index="weekday", columns=orders["order_time"].dt.hour,
                           values="order_id", aggfunc="count").fillna(0)     # alphabetical rows
    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(t.values, cmap="jet", aspect="auto")
    ax.set_yticks(range(len(t)), t.index)
    ax.set_xticks(range(len(t.columns)), t.columns)
    fig.colorbar(im)
    ax.set_title("Orders heatmap")
    page(fig, 4, "Peak times")
    return fig


def chart5():
    """Orders against target, by zone."""
    act = orders.groupby(["zone", "month"]).size().rename("actual").reset_index()
    t = act.merge(targets, on=["zone", "month"])
    t["gap"] = t["actual"] - t["target_orders"]
    fig, axs = plt.subplots(3, 1, figsize=(10, 7))
    for ax, (z, g) in zip(axs, t.groupby("zone")):
        ax.bar(g["month"], g["gap"], color=["green" if v >= 0 else "red" for v in g["gap"]])
        ax.set_title(z, fontsize=9)
        ax.set_xticks(range(12), g["month"], fontsize=7)
    fig.text(0.01, 0.5, "Actual - Target", rotation=90, va="center")
    page(fig, 5, "Targets")
    fig.tight_layout(rect=(0.02, 0, 1, 0.95))
    return fig


def chart6():
    """Average basket value by member tier."""
    avg = orders.groupby("member_tier")["basket_value_vnd"].mean()     # alphabetical order
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(range(len(avg)), [1] * len(avg), s=(avg.values / 1000) ** 2 / 2,
               c=range(len(avg)), cmap="rainbow", alpha=0.8, edgecolor="black")
    for i, (tier, v) in enumerate(avg.items()):
        ax.text(i, 1, f"{tier}\n{v:,.0f}", ha="center", va="center", fontsize=9)
    ax.set_xlim(-0.8, len(avg) - 0.2)
    ax.set_title("Basket Value by Tier (VND)")
    ax.axis("off")
    page(fig, 6, "Customers")
    return fig


if __name__ == "__main__":
    with PdfPages("gomart_bad_report.pdf") as pdf:
        for make in [chart1, chart2, chart3, chart4, chart5, chart6]:
            fig = make()
            pdf.savefig(fig)
            plt.close(fig)
    print("saved gomart_bad_report.pdf")
