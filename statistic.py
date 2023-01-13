import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import db

from datetime import date
from calendar import monthrange, Calendar

calendar = Calendar()

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

def all_days():
    all_days = []
    for x in np.arange(1, 13):
        for y in np.fromiter(calendar.itermonthdays(date.today().year, x), dtype="int32"):
            if y != 0:
                all_days.append(date(date.today().year, x, y))
    np_all_days = np.array(all_days)
    return np_all_days

def custom_read(query):
        return pd.DataFrame({i:j.__dict__ for i,j in enumerate(query.all())},).T.drop(columns='_sa_instance_state')

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

    def func(pct):
        return "{:1.2f}%".format(pct)

    fig, ax = plt.subplots(figsize=(6, 3), nrows=1, ncols=2)

    data_fact = df[df["Fact"] == 1][["Name", "Value"]].groupby("Name")["Value"].sum()
    data_not_fact = (
        df[df["Fact"] == 0][["Name", "Value"]].groupby("Name")["Value"].sum()
    )

    wedges, texts, autotext = ax[0].pie(
        data_fact, autopct=lambda pct: func(pct)
    )
    wedges_1, texts_1, autotext_1 = ax[1].pie(
        data_not_fact, autopct=lambda pct: func(pct)
    )

    ax[0].set_title(f"Фактическое распределение \n{name}", pad=16, color="navy", fontsize=16)
    ax[1].set_title(f"Плановое распределение \n{name}", pad=16, color="navy", fontsize=16)
    
    ax[0].legend(
        wedges,
        [f"{index}:\n({value} р.)" for index, value in data_fact.items()],
        title="Категория",
        loc="center left",
        bbox_to_anchor=(-0.25, 0, 0.5, 1),
        fontsize=14,
    )
    
    ax[1].legend(
        wedges_1,
        [f"{index}:\n({value} р.)" for index, value in data_not_fact.items()],
        title="Категория",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=14,
    )

    
    return fig


def plot_month(query, name, days_in_month: int):

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
    ax.set_xticks(list(range(0, days_in_month, 1)) + [days_in_month])
    ax.set_xticklabels(list(x if x%2==0 else None for x in range(0, days_in_month, 1)) + [days_in_month] )
    ax.legend(title="Изменение", loc="upper right")
    ax.grid(color="grey", linestyle=":", linewidth=0.5)
    ax.set_title(f"Изменение \n{name}", pad=16, color="navy", fontsize=16)

    fig.tight_layout()

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

    lenght_fact = list(months_dict[i] for i in data_fact.index)
    lenght_not_fact = list(months_dict[i] for i in data_not_fact.index)

    ax[0].bar(
        lenght_fact, data_fact, label="Факт", color=color
    )
    ax[1].bar(
        lenght_not_fact,
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
    ax[0].set_xticklabels(lenght_fact, rotation=45)

    ax[1].set_xlabel("Месяц")
    ax[1].set_ylabel("Кол-во, руб.")
    ax[1].set_title(
        f"Плановое распределение \n{name}", pad=16, color="navy", fontsize=16
    )
    ax[1].grid(color="grey", linestyle=":", linewidth=0.5)
    ax[1].set_xticklabels(lenght_not_fact, rotation=45)

    fig.tight_layout()

    return fig


def plot_year_all(query_inc, query_exp, name):

    df_inc = custom_read(query_inc)
    df_exp = custom_read(query_exp)

    df_inc["date"] = pd.to_datetime(df_inc["date"])
    df_exp["date"] = pd.to_datetime(df_exp["date"])

    fig, ax = plt.subplots(figsize=(6, 3), sharey=True)

    inc_fact = df_inc[df_inc["fact"] == 1][["date", "value"]].groupby("date")["value"].sum()
    inc_not_fact = df_inc[df_inc["fact"] == 0][["date", "value"]].groupby("date")["value"].sum()

    exp_fact = df_exp[df_exp["fact"] == 1][["date", "value"]].groupby("date")["value"].sum()
    exp_not_fact = df_exp[df_exp["fact"] == 0][["date", "value"]].groupby("date")["value"].sum()
    
    ax.plot(inc_fact, label="Фактический доход", color="green")
    ax.plot(inc_not_fact, label="Плановый доход", color="green", linestyle="--", alpha=0.6)

    ax.plot(exp_fact, label="Фактический расход", color="red")
    ax.plot(exp_not_fact, label="Плановый расход", color="red", linestyle="--", alpha=0.6)

    all_d = all_days()

    ax.set_xlabel("День в году")
    ax.set_ylabel("Кол-во, руб.")
    ax.set_xticks(all_d[all_d==date(2023, 1, 1)])
    # ax.set_xticklabels(np.where((all_d.day==1)&(all_d.day==15), all_d, None))
    ax.legend(title="Изменение", loc="upper right")
    ax.grid(color="grey", linestyle=":", linewidth=0.5)
    ax.set_title(f"Изменение \n{name}", pad=16, color="navy", fontsize=16)

    return fig

if __name__ == "__main__":
    plot_year_all()
    pie_month()
    plot_month()
    bar_year()
        
