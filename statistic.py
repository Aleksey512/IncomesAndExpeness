import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

months_dict = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь",
}


def pie_month(query, name):

    data = {
        "Name": [],
        "Value": [],
        "Date": [],
        "Fact": [],
    }

    for q in query:
        q_as_dict = q.__dict__

        data["Name"].append(q_as_dict["name"])
        data["Value"].append(q_as_dict["value"])
        data["Date"].append(q_as_dict["date"])
        data["Fact"].append(q_as_dict["fact"])

    df = pd.DataFrame(data=data)
    df["Date"] = pd.to_datetime(df["Date"])

    def func(pct, allvals):
        absolute = int(pct / 100.0 * np.sum(allvals))
        return f"{pct:1.2f}%\n({absolute} руб.)"

    fig, ax = plt.subplots(figsize=(6, 3), nrows=1, ncols=2)

    data_fact = df[df["Fact"] == 1][["Name", "Value"]].groupby("Name")["Value"].sum()
    data_not_fact = (
        df[df["Fact"] == 0][["Name", "Value"]].groupby("Name")["Value"].sum()
    )

    wedges, texts, _ = ax[0].pie(
        data_fact, autopct=lambda pct: func(pct, data_fact.values)
    )
    wedges_1, texts_1, _ = ax[1].pie(
        data_not_fact, autopct=lambda pct: func(pct, data_not_fact.values)
    )

    ax[0].set_title(f"Фактическое распределение \n{name}", pad=16, color="navy")
    ax[1].set_title(f"Плановое распределение \n{name}", pad=16, color="navy")

    ax[0].legend(
        wedges,
        data_fact.index,
        title="Категория",
        loc="center left",
        bbox_to_anchor=(0, 0.5, 0.5, 0),
    )

    ax[1].legend(
        wedges_1,
        data_not_fact.index,
        title="Категория",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    return fig


def plot_month(query, name):

    data = {
        "Name": [],
        "Value": [],
        "Date": [],
        "Fact": [],
    }

    for q in query:
        q_as_dict = q.__dict__

        data["Name"].append(q_as_dict["name"])
        data["Value"].append(q_as_dict["value"])
        data["Date"].append(q_as_dict["date"])
        data["Fact"].append(q_as_dict["fact"])

    df = pd.DataFrame(data=data)
    df["Date"] = pd.to_datetime(df["Date"]).dt.day

    fig, ax = plt.subplots(figsize=(6, 3))

    data_fact = df[df["Fact"] == 1][["Date", "Value"]].groupby("Date")["Value"].sum()
    data_not_fact = (
        df[df["Fact"] == 0][["Date", "Value"]].groupby("Date")["Value"].sum()
    )

    ax.plot(data_fact, label="Фактическое", color="red", alpha=0.8)
    ax.plot(data_not_fact, label="Плановое", color="green", alpha=0.8)

    ax.set_xlabel("День")
    ax.set_ylabel("Кол-во, руб.")
    ax.set_xticks(list(range(0, 32, 2)) + [31])
    ax.legend(title="Изменение", loc="upper right")
    ax.grid(color="grey", linestyle=":", linewidth=0.5)
    ax.set_title(f"Изменение \n{name}", pad=16, color="navy")

    return fig


def bar_year(query, name, color="#1f77b4"):

    data = {
        "Name": [],
        "Value": [],
        "Date": [],
        "Fact": [],
    }

    for q in query:
        q_as_dict = q.__dict__

        data["Name"].append(q_as_dict["name"])
        data["Value"].append(q_as_dict["value"])
        data["Date"].append(q_as_dict["date"])
        data["Fact"].append(q_as_dict["fact"])

    df = pd.DataFrame(data=data)
    df["Date"] = pd.to_datetime(df["Date"]).dt.month

    fig, ax = plt.subplots(figsize=(6, 3), nrows=1, ncols=2, sharey=True)

    data_fact = df[df["Fact"] == 1][["Date", "Value"]].groupby("Date")["Value"].sum()
    data_not_fact = (
        df[df["Fact"] == 0][["Date", "Value"]].groupby("Date")["Value"].sum()
    )

    ax[0].bar(
        [months_dict[i] for i in data_fact.index], data_fact, label="Факт", color=color
    )
    ax[1].bar(
        [months_dict[i] for i in data_not_fact.index],
        data_not_fact,
        label="План",
        color=color,
    )

    ax[0].set_xlabel("Месяц")
    ax[0].set_ylabel("Кол-во, руб.")
    ax[0].set_title(
        f"Фактическое распределение \n{name}", pad=16, color="navy", fontsize=16
    )
    ax[0].grid(color="grey", linestyle=":", linewidth=0.5)

    ax[1].set_xlabel("Месяц")
    ax[1].set_ylabel("Кол-во, руб.")
    ax[1].set_title(
        f"Плановое распределение \n{name}", pad=16, color="navy", fontsize=16
    )
    ax[1].grid(color="grey", linestyle=":", linewidth=0.5)

    fig.tight_layout()

    return fig


if __name__ == "__main__":
    pie_month()
    plot_month()
    bar_year()
