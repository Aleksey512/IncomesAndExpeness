import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

from datetime import date
from calendar import monthrange, Calendar

import warnings

warnings.filterwarnings(action="once")

plt.style.use("seaborn-v0_8-whitegrid")

large = 22
med = 16
small = 12
params = {
    "axes.titlesize": med,
    "legend.fontsize": large,
    "figure.figsize": (1, 1),
    "axes.labelsize": med,
    "axes.titlesize": med,
    "xtick.labelsize": small,
    "ytick.labelsize": med,
    "figure.titlesize": large,
}
plt.rcParams.update(params)


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

months_dict_plural = {
    1: "Января",
    2: "Февраля",
    3: "Марта",
    4: "Апреля",
    5: "Мая",
    6: "Июня",
    7: "Июля",
    8: "Августа",
    9: "Сентября",
    10: "Октября",
    11: "Ноября",
    12: "Декабря",
}



def first_and_fifth_day():
    """
    Функция для создания массива каждого 1 и 15 дней, каждого месяца
    :param: void
    :return:  numpy.array
    """
    all_days = []
    for x in np.arange(1, 13):
        for y in np.fromiter(
            calendar.itermonthdays(date.today().year, x), dtype="int32"
        ):
            if y != 0 and (y == 1 or y == 15):
                all_days.append(date(date.today().year, x, y))
    np_all_days = np.array(all_days)
    return np_all_days


def custom_read(query):
    """
    Возвращает pandas DataFrame из Sqlalchemy.query запроса
    """
    return pd.DataFrame(
        {i: j.__dict__ for i, j in enumerate(query.all())},
    ).T


def pie_month(query, name):
    """
    Функция создает круговую диаграмму
    :param query: Sqlalchemy.query
    :param name: str
    :return fig : matplotlib.Figure
    """
    try:
        df = custom_read(query)
        df["date"] = pd.to_datetime(df["date"])

        def func(pct):
            return "{:1.2f}%".format(pct)

        fig, ax = plt.subplots(figsize=(6, 3), nrows=1, ncols=2)

        data_fact = df[df["fact"] == 1][["name", "value"]].groupby("name")["value"].sum()
        data_not_fact = (
            df[df["fact"] == 0][["name", "value"]].groupby("name")["value"].sum()
        )

        wedges, texts, autotext = ax[0].pie(data_fact, autopct=lambda pct: func(pct))
        wedges_1, texts_1, autotext_1 = ax[1].pie(
            data_not_fact, autopct=lambda pct: func(pct)
        )

        ax[0].set_title(
            f"Фактическое распределение \n{name}", pad=16, color="navy", fontsize=16
        )
        ax[1].set_title(
            f"Плановое распределение \n{name}", pad=16, color="navy", fontsize=16
        )

        ax[0].legend(
            wedges,
            [f"{index}:\n({value} р.)" for index, value in data_fact.items()],
            title="Категория",
            loc="center left",
            bbox_to_anchor=(-0.25, 0, 0.5, 1),
            fontsize=12,
        )

        ax[1].legend(
            wedges_1,
            [f"{index}:\n({value} р.)" for index, value in data_not_fact.items()],
            title="Категория",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            fontsize=12,
        )

        return fig
    except Exception as e:
        print(e)




def plot_month(query, name, days_in_month: int):
    """
    Функция создает линейную диаграмму
    :param query: Sqlalchemy.query
    :param name: str
    :param days_in_month : int
    :return fig : matplotlib.Figure
    """
    try:
        df = custom_read(query)
        df["date"] = pd.to_datetime(df["date"]).dt.day

        fig, ax = plt.subplots(figsize=(6, 3))

        data_fact = df[df["fact"] == 1][["date", "value"]].groupby("date")["value"].sum()
        data_not_fact = (
            df[df["fact"] == 0][["date", "value"]].groupby("date")["value"].sum()
        )


        ax.plot(data_fact, label="Фактическое", color="red", alpha=0.8)
        ax.plot(data_not_fact, label="Плановое", color="green", alpha=0.8)

        ax.set_xlabel("День")
        ax.set_ylabel("Кол-во, руб.")
        ax.set_xticks(list(range(0, days_in_month, 1)) + [days_in_month])
        ax.set_xticklabels(
            list(x if x % 2 == 0 else None for x in range(0, days_in_month, 1))
            + [days_in_month]
        )
        ax.legend(title="Изменение", loc="upper right")
        ax.grid(color="grey", linestyle=":", linewidth=0.5)
        ax.set_title(f"Изменение \n{name}", pad=16, color="navy", fontsize=16)

        fig.tight_layout()

        return fig

    except Exception as e:
        print(e)


def bar_year(query, name, color="#1f77b4"):
    """
    Функция создает столбчатую диаграмму
    :param query: Sqlalchemy.query
    :param name: str
    :param color default='#1f77b4' : str
    :return fig : matplotlib.Figure
    """
    try:
        df = custom_read(query)
        df["date"] = pd.to_datetime(df["date"]).dt.month

        fig, ax = plt.subplots(figsize=(6, 3), nrows=1, ncols=2, sharey=True)

        data_fact = df[df["fact"] == 1][["date", "value"]].groupby("date")["value"].sum()
        data_not_fact = (
            df[df["fact"] == 0][["date", "value"]].groupby("date")["value"].sum()
        )

        lenght_fact = list(months_dict[i] for i in data_fact.index)
        lenght_not_fact = list(months_dict[i] for i in data_not_fact.index)


        ax[0].bar(lenght_fact, data_fact, label="Факт", color=color)
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
    except Exception as e:
        print(e)


def plot_year_all(query_inc, query_exp, name):
    """

    :param query_inc: Sqlalchemy.query
    :param query_exp: Sqlalchemy.query
    :param name: str
    :return: matplotlib.Figure
    """
    try:
        df_inc = custom_read(query_inc)
        df_exp = custom_read(query_exp)

        df_inc["date"] = pd.to_datetime(df_inc["date"]).dt.date
        df_exp["date"] = pd.to_datetime(df_exp["date"]).dt.date

        fig, ax = plt.subplots(figsize=(12, 8))

        inc_fact = (
            df_inc[df_inc["fact"] == 1][["date", "value"]].groupby("date")["value"].sum()
        )
        inc_not_fact = (
            df_inc[df_inc["fact"] == 0][["date", "value"]].groupby("date")["value"].sum()
        )

        exp_fact = (
            df_exp[df_exp["fact"] == 1][["date", "value"]].groupby("date")["value"].sum()
        )
        exp_not_fact = (
            df_exp[df_exp["fact"] == 0][["date", "value"]].groupby("date")["value"].sum()
        )

        ax.plot(inc_fact, label="Фактический доход", color="green")
        ax.plot(
            inc_not_fact, label="Плановый доход", color="green", linestyle="--", alpha=0.6
        )

        ax.plot(exp_fact, label="Фактический расход", color="red")
        ax.plot(
            exp_not_fact, label="Плановый расход", color="red", linestyle="--", alpha=0.6
        )

        labels = first_and_fifth_day()

        ax.set_xlabel("День в году")
        ax.set_ylabel("Кол-во, руб.")
        ax.set_xticks(labels)
        ax.set_xticklabels(
            list(f"{label.day}-{months_dict_plural[label.month]}" for label in labels),
            rotation=45,
        )
        ax.legend(title="Изменение", loc="upper right")
        ax.set_title(f"Изменение \n{name}", pad=16, color="navy", fontsize=16)

        return fig
    except Exception as e:
        print(e)

def text_statistic(query_inc, query_exp):
    try:
        df_inc = custom_read(query_inc)
        df_exp = custom_read(query_exp)

        inc = {
        "all_f" : 0,
        "all_p" : 0,
        "relative" : 0,
        "absolute" : 0,
        }

        exp = {
        "all_f" : 0,
        "all_p" : 0,
        "relative" : 0,
        "absolute" : 0,
        }

        inc["all_f"] = df_inc[df_inc["fact"] == 1]['value'].sum()
        inc["all_p"] = df_inc[df_inc["fact"] == 0]['value'].sum()
        inc["absolute"] =inc["all_f"]-inc["all_p"]
        inc["relative"] = ((inc["absolute"])/inc["all_p"])*100

        exp["all_f"] = df_exp[df_exp["fact"] == 1]['value'].sum()
        exp["all_p"] = df_exp[df_exp["fact"] == 0]['value'].sum()
        exp["absolute"] =exp["all_f"]-exp["all_p"]
        exp["relative"] = ((exp["absolute"])/(exp["all_p"]))*100

        return inc, exp
    except Exception as e:
        print(e)
