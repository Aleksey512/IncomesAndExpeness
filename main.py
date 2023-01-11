import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from UI import Ui_QGroupBox

from sqlalchemy.orm import sessionmaker
from sqlalchemy import delete, and_, or_

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
import matplotlib.pyplot as plt

import db

from statistic import pie_month, plot_month, bar_year

from datetime import date

Session = sessionmaker(bind=db.engine)
session = Session()

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

expeness_dict = {
    1: "Дом",
    2: "Еда",
    3: "Долги",
    4: "Транспорт",
    6: "Счета и услуги",
    7: "Личные расходы",
    8: "Сбережения",
    9: "Другие расходы",
}

incomes_dict = {
    1: "Аванс",
    2: "Алименты",
    3: "Возврат налогов",
    4: "Грант",
    5: "Доход от бизнеса",
    6: "Зарплата",
    7: "Пенсия",
    8: "Подарки",
    9: "Помощь (родителей, супруга, детей)",
    10: "Премия",
    11: "Приз (выигрыш)",
    12: "Приработок",
    13: "Проценты по депозиту",
    14: "Cоциальное пособие",
    15: "Cтипендия",
}


def selected_month(index):
    """Если месяц от 1 до 9 добавляет 0 перед номером месяца"""
    if 1 <= index <= 9:
        return f"0{index}"
    else:
        return index


class MyMplCanavas(FigureCanvas):
    def __init__(self, fig, parent=None):
        self.fig = fig
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(
            self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        FigureCanvas.updateGeometry(self)


class MainClass(QtWidgets.QGroupBox, Ui_QGroupBox):
    def __init__(self):
        super(MainClass, self).__init__()

        self.setupUi(self)

        for month in months_dict.items():
            self.tab6_cbox.addItem(month[1])
            self.tab5_cbox.addItem(month[1])
            self.tab4_cbox.addItem(month[1])
            self.tab3_cbox.addItem(month[1])
            self.tab2_cbox.addItem(month[1])
            self.tab1_cbox.addItem(month[1])

        for incomes in incomes_dict.items():
            self.tab3_cbox_2.addItem(incomes[1])
            self.tab1_cbox_2.addItem(incomes[1])

        for expeness in expeness_dict.items():
            self.tab4_cbox_2.addItem(expeness[1])
            self.tab2_cbox_2.addItem(expeness[1])

        self.tab1_pushButton.clicked.connect(self.tab1_add_button_clicked)
        self.tab1_pushButton_2.clicked.connect(self.tab1_month_show_button_clicked)
        self.tab1_pushButton_3.clicked.connect(self.tab1_delete_row_button_clicked)
        self.tab1_pushButton_4.clicked.connect(self.tab1_day_show_button_clicked)

        self.tab2_pushButton.clicked.connect(self.tab2_add_button_clicked)
        self.tab2_pushButton_2.clicked.connect(self.tab2_month_show_button_clicked)
        self.tab2_pushButton_3.clicked.connect(self.tab2_delete_row_button_clicked)
        self.tab2_pushButton_4.clicked.connect(self.tab2_day_show_button_clicked)

        self.tab3_pushButton.clicked.connect(self.tab3_add_button_clicked)
        self.tab3_pushButton_2.clicked.connect(self.tab3_month_show_button_clicked)
        self.tab3_pushButton_3.clicked.connect(self.tab3_delete_row_button_clicked)
        self.tab3_pushButton_4.clicked.connect(self.tab3_day_show_button_clicked)

        self.tab4_pushButton.clicked.connect(self.tab4_add_button_clicked)
        self.tab4_pushButton_2.clicked.connect(self.tab4_month_show_button_clicked)
        self.tab4_pushButton_3.clicked.connect(self.tab4_delete_row_button_clicked)
        self.tab4_pushButton_4.clicked.connect(self.tab4_day_show_button_clicked)

        self.tab5_layout = QtWidgets.QVBoxLayout(self.tab5_widget)
        self.tab5_pie_month.clicked.connect(self.tab5_mounth_pie_clicked)
        self.tab5_plot_month.clicked.connect(self.tab5_mounth_plot_clicked)
        self.tab5_pie_year.clicked.connect(self.tab5_year_pie_clicked)
        self.tab5_bar_year.clicked.connect(self.tab5_year_bar_clicked)

        self.tab6_layout = QtWidgets.QVBoxLayout(self.tab6_widget)
        self.tab6_pie_month.clicked.connect(self.tab6_mounth_pie_clicked)
        self.tab6_plot_month.clicked.connect(self.tab6_mounth_plot_clicked)
        self.tab6_pie_year.clicked.connect(self.tab6_year_pie_clicked)
        self.tab6_bar_year.clicked.connect(self.tab6_year_bar_clicked)

        # self.tab6_pushButton.clicked.connect(self.tab6_get_pie_exp_clicked)

    def tab1_add_button_clicked(self):
        with session:
            income = db.Income(
                name=self.tab1_cbox_2.currentText(),
                value=self.tab1_value.value(),
                date=date(
                    self.tab1_dateEdit.date().year(),
                    self.tab1_dateEdit.date().month(),
                    self.tab1_dateEdit.date().day(),
                ),
                fact=False,
            )
            session.add(income)
            session.commit()

    def tab1_month_show_button_clicked(self):
        self.tab1_table.setRowCount(0)
        index = self.tab1_cbox.currentIndex() + 1
        ses_query = session.query(db.Income).filter(
            and_(
                db.Income.fact == False,
                db.Income.date.between(
                    f"{date.today().year}-{selected_month(index)}-{0}",
                    f"{date.today().year}-{selected_month(index)}-{31}",
                ),
            )
        )
        for query in ses_query:
            rows = self.tab1_table.rowCount()
            row_as_dict = query.__dict__
            self.tab1_table.setRowCount(rows + 1)
            self.tab1_table.setItem(
                rows, 0, QtWidgets.QTableWidgetItem(str(row_as_dict["id"]))
            )
            self.tab1_table.setItem(
                rows, 1, QtWidgets.QTableWidgetItem(str(row_as_dict["date"]))
            )
            self.tab1_table.setItem(
                rows, 2, QtWidgets.QTableWidgetItem(row_as_dict["name"])
            )
            self.tab1_table.setItem(
                rows, 3, QtWidgets.QTableWidgetItem(str(row_as_dict["value"]))
            )
        self.tab1_table.resizeColumnsToContents()

    def tab1_day_show_button_clicked(self):
        self.tab1_table.setRowCount(0)
        ses_query = session.query(db.Income).filter(
            and_(
                db.Income.fact == False,
                db.Income.date
                == date(
                    self.tab1_dateEdit_2.date().year(),
                    self.tab1_dateEdit_2.date().month(),
                    self.tab1_dateEdit_2.date().day(),
                ),
            )
        )
        for query in ses_query:
            rows = self.tab1_table.rowCount()
            row_as_dict = query.__dict__
            self.tab1_table.setRowCount(rows + 1)
            self.tab1_table.setItem(
                rows, 0, QtWidgets.QTableWidgetItem(str(row_as_dict["id"]))
            )
            self.tab1_table.setItem(
                rows, 1, QtWidgets.QTableWidgetItem(str(row_as_dict["date"]))
            )
            self.tab1_table.setItem(
                rows, 2, QtWidgets.QTableWidgetItem(row_as_dict["name"])
            )
            self.tab1_table.setItem(
                rows, 3, QtWidgets.QTableWidgetItem(str(row_as_dict["value"]))
            )
        self.tab1_table.resizeColumnsToContents()

    def tab1_delete_row_button_clicked(self):
        id = self.tab1_table.item(self.tab1_table.currentRow(), 0).text()
        stmt = delete(db.Income).where(db.Income.id == id)
        self.tab1_table.removeRow(self.tab1_table.currentRow())
        session.execute(stmt)
        session.commit()

    def tab2_add_button_clicked(self):
        with session:
            expeness = db.Expeness(
                name=self.tab2_cbox_2.currentText(),
                value=self.tab2_value.value(),
                date=date(
                    self.tab2_dateEdit.date().year(),
                    self.tab2_dateEdit.date().month(),
                    self.tab2_dateEdit.date().day(),
                ),
                fact=False,
            )
            session.add(expeness)
            session.commit()

    def tab2_month_show_button_clicked(self):
        self.tab2_table.setRowCount(0)
        index = self.tab2_cbox.currentIndex() + 1
        ses_query = session.query(db.Expeness).filter(
            and_(
                db.Expeness.fact == False,
                db.Expeness.date.between(
                    f"{date.today().year}-{selected_month(index)}-{0}",
                    f"{date.today().year}-{selected_month(index)}-{31}",
                ),
            )
        )
        for query in ses_query:
            rows = self.tab2_table.rowCount()
            row_as_dict = query.__dict__
            self.tab2_table.setRowCount(rows + 1)
            self.tab2_table.setItem(
                rows, 0, QtWidgets.QTableWidgetItem(str(row_as_dict["id"]))
            )
            self.tab2_table.setItem(
                rows, 1, QtWidgets.QTableWidgetItem(str(row_as_dict["date"]))
            )
            self.tab2_table.setItem(
                rows, 2, QtWidgets.QTableWidgetItem(row_as_dict["name"])
            )
            self.tab2_table.setItem(
                rows, 3, QtWidgets.QTableWidgetItem(str(row_as_dict["value"]))
            )
        self.tab2_table.resizeColumnsToContents()

    def tab2_day_show_button_clicked(self):
        self.tab2_table.setRowCount(0)
        ses_query = session.query(db.Expeness).filter(
            and_(
                db.Expeness.fact == False,
                db.Expeness.date
                == date(
                    self.tab2_dateEdit_2.date().year(),
                    self.tab2_dateEdit_2.date().month(),
                    self.tab2_dateEdit_2.date().day(),
                ),
            )
        )
        for query in ses_query:
            rows = self.tab2_table.rowCount()
            row_as_dict = query.__dict__
            self.tab2_table.setRowCount(rows + 1)
            self.tab2_table.setItem(
                rows, 0, QtWidgets.QTableWidgetItem(str(row_as_dict["id"]))
            )
            self.tab2_table.setItem(
                rows, 1, QtWidgets.QTableWidgetItem(str(row_as_dict["date"]))
            )
            self.tab2_table.setItem(
                rows, 2, QtWidgets.QTableWidgetItem(row_as_dict["name"])
            )
            self.tab2_table.setItem(
                rows, 3, QtWidgets.QTableWidgetItem(str(row_as_dict["value"]))
            )
        self.tab2_table.resizeColumnsToContents()

    def tab2_delete_row_button_clicked(self):
        id = self.tab2_table.item(self.tab2_table.currentRow(), 0).text()
        stmt = delete(db.Expeness).where(db.Expeness.id == id)
        self.tab2_table.removeRow(self.tab2_table.currentRow())
        session.execute(stmt)
        session.commit()

    def tab3_add_button_clicked(self):
        with session:
            income = db.Income(
                name=self.tab3_cbox_2.currentText(),
                value=self.tab3_value.value(),
                date=date(
                    self.tab3_dateEdit.date().year(),
                    self.tab3_dateEdit.date().month(),
                    self.tab3_dateEdit.date().day(),
                ),
                fact=True,
            )
            session.add(income)
            session.commit()

    def tab3_month_show_button_clicked(self):
        self.tab3_table.setRowCount(0)
        index = self.tab3_cbox.currentIndex() + 1
        ses_query = session.query(db.Income).filter(
            and_(db.Income.fact == True),
            (
                db.Income.date.between(
                    f"{date.today().year}-{selected_month(index)}-{0}",
                    f"{date.today().year}-{selected_month(index)}-{31}",
                )
            ),
        )
        for query in ses_query:
            rows = self.tab3_table.rowCount()
            row_as_dict = query.__dict__
            self.tab3_table.setRowCount(rows + 1)
            self.tab3_table.setItem(
                rows, 0, QtWidgets.QTableWidgetItem(str(row_as_dict["id"]))
            )
            self.tab3_table.setItem(
                rows, 1, QtWidgets.QTableWidgetItem(str(row_as_dict["date"]))
            )
            self.tab3_table.setItem(
                rows, 2, QtWidgets.QTableWidgetItem(row_as_dict["name"])
            )
            self.tab3_table.setItem(
                rows, 3, QtWidgets.QTableWidgetItem(str(row_as_dict["value"]))
            )
        self.tab3_table.resizeColumnsToContents()

    def tab3_day_show_button_clicked(self):
        self.tab3_table.setRowCount(0)
        ses_query = session.query(db.Income).filter(
            and_(
                db.Income.fact == True,
                db.Income.date
                == date(
                    self.tab3_dateEdit_2.date().year(),
                    self.tab3_dateEdit_2.date().month(),
                    self.tab3_dateEdit_2.date().day(),
                ),
            )
        )
        for query in ses_query:
            rows = self.tab3_table.rowCount()
            row_as_dict = query.__dict__
            self.tab3_table.setRowCount(rows + 1)
            self.tab3_table.setItem(
                rows, 0, QtWidgets.QTableWidgetItem(str(row_as_dict["id"]))
            )
            self.tab3_table.setItem(
                rows, 1, QtWidgets.QTableWidgetItem(str(row_as_dict["date"]))
            )
            self.tab3_table.setItem(
                rows, 2, QtWidgets.QTableWidgetItem(row_as_dict["name"])
            )
            self.tab3_table.setItem(
                rows, 3, QtWidgets.QTableWidgetItem(str(row_as_dict["value"]))
            )
        self.tab3_table.resizeColumnsToContents()

    def tab3_delete_row_button_clicked(self):
        id = self.tab3_table.item(self.tab3_table.currentRow(), 0).text()
        stmt = delete(db.Income).where(db.Income.id == id)
        self.tab3_table.removeRow(self.tab3_table.currentRow())
        session.execute(stmt)
        session.commit()

    def tab4_add_button_clicked(self):
        with session:
            expeness = db.Expeness(
                name=self.tab4_cbox_2.currentText(),
                value=self.tab4_value.value(),
                date=date(
                    self.tab4_dateEdit.date().year(),
                    self.tab4_dateEdit.date().month(),
                    self.tab4_dateEdit.date().day(),
                ),
                fact=True,
            )
            session.add(expeness)
            session.commit()

    def tab4_month_show_button_clicked(self):
        self.tab4_table.setRowCount(0)
        index = self.tab4_cbox.currentIndex() + 1
        ses_query = session.query(db.Expeness).filter(
            and_(db.Expeness.fact == True),
            (
                db.Expeness.date.between(
                    f"{date.today().year}-{selected_month(index)}-{0}",
                    f"{date.today().year}-{selected_month(index)}-{31}",
                )
            ),
        )
        for query in ses_query:
            rows = self.tab4_table.rowCount()
            row_as_dict = query.__dict__
            self.tab4_table.setRowCount(rows + 1)
            self.tab4_table.setItem(
                rows, 0, QtWidgets.QTableWidgetItem(str(row_as_dict["id"]))
            )
            self.tab4_table.setItem(
                rows, 1, QtWidgets.QTableWidgetItem(str(row_as_dict["date"]))
            )
            self.tab4_table.setItem(
                rows, 2, QtWidgets.QTableWidgetItem(row_as_dict["name"])
            )
            self.tab4_table.setItem(
                rows, 3, QtWidgets.QTableWidgetItem(str(row_as_dict["value"]))
            )
        self.tab4_table.resizeColumnsToContents()

    def tab4_day_show_button_clicked(self):
        self.tab4_table.setRowCount(0)
        ses_query = session.query(db.Expeness).filter(
            and_(
                db.Expeness.fact == True,
                db.Expeness.date
                == date(
                    self.tab4_dateEdit_2.date().year(),
                    self.tab4_dateEdit_2.date().month(),
                    self.tab4_dateEdit_2.date().day(),
                ),
            )
        )
        for query in ses_query:
            rows = self.tab4_table.rowCount()
            row_as_dict = query.__dict__
            self.tab4_table.setRowCount(rows + 1)
            self.tab4_table.setItem(
                rows, 0, QtWidgets.QTableWidgetItem(str(row_as_dict["id"]))
            )
            self.tab4_table.setItem(
                rows, 1, QtWidgets.QTableWidgetItem(str(row_as_dict["date"]))
            )
            self.tab4_table.setItem(
                rows, 2, QtWidgets.QTableWidgetItem(row_as_dict["name"])
            )
            self.tab4_table.setItem(
                rows, 3, QtWidgets.QTableWidgetItem(str(row_as_dict["value"]))
            )
        self.tab4_table.resizeColumnsToContents()

    def tab4_delete_row_button_clicked(self):
        id = self.tab4_table.item(self.tab4_table.currentRow(), 0).text()
        stmt = delete(db.Expeness).where(db.Expeness.id == id)
        self.tab4_table.removeRow(self.tab4_table.currentRow())
        session.execute(stmt)
        session.commit()

    def tab5_mounth_pie_clicked(self):
        index = self.tab5_cbox.currentIndex() + 1
        query = session.query(db.Income).filter(
            db.Income.date.between(
                f"{date.today().year}-{selected_month(index)}-{0}",
                f"{date.today().year}-{selected_month(index)}-{31}",
            )
        )
        try:
            self.fig.clear()
            self.tab5_layout.removeWidget(self.tab5_canavas)
            self.tab5_layout.removeWidget(self.tab5_navbar)
            self.fig = pie_month(query, f"дохода за {months_dict[index]} по категориям")
            self.tab5_canavas = MyMplCanavas(self.fig)
            self.tab5_navbar = NavigationToolbar(self.tab5_canavas)
            self.tab5_layout.addWidget(self.tab5_navbar)
            self.tab5_layout.addWidget(self.tab5_canavas)
        except:
            self.fig = pie_month(query, f"дохода за {months_dict[index]} по категориям")
            self.tab5_canavas = MyMplCanavas(self.fig)
            self.tab5_navbar = NavigationToolbar(self.tab5_canavas)
            self.tab5_layout.addWidget(self.tab5_navbar)
            self.tab5_layout.addWidget(self.tab5_canavas)

    def tab5_mounth_plot_clicked(self):
        index = self.tab5_cbox.currentIndex() + 1
        query = session.query(db.Income).filter(
            db.Income.date.between(
                f"{date.today().year}-{selected_month(index)}-{0}",
                f"{date.today().year}-{selected_month(index)}-{31}",
            )
        )
        try:
            self.fig.clear()
            self.tab5_layout.removeWidget(self.tab5_canavas)
            self.tab5_layout.removeWidget(self.tab5_navbar)
            self.fig = plot_month(query, f"дохода по дням за {months_dict[index]}")
            self.tab5_canavas = MyMplCanavas(self.fig)
            self.tab5_navbar = NavigationToolbar(self.tab5_canavas)
            self.tab5_layout.addWidget(self.tab5_navbar)
            self.tab5_layout.addWidget(self.tab5_canavas)

        except:
            self.fig = plot_month(query, f"дохода по дням за {months_dict[index]}")
            self.tab5_canavas = MyMplCanavas(self.fig)
            self.tab5_navbar = NavigationToolbar(self.tab5_canavas)
            self.tab5_layout.addWidget(self.tab5_navbar)
            self.tab5_layout.addWidget(self.tab5_canavas)

    def tab5_year_pie_clicked(self):
        start_year = date(date.today().year, 1, 1)
        end_year = date(date.today().year + 1, 1, 1)
        query = session.query(db.Income).filter(
            and_(db.Income.date >= start_year, db.Income.date < end_year)
        )
        try:
            self.fig.clear()
            self.tab5_layout.removeWidget(self.tab5_canavas)
            self.tab5_layout.removeWidget(self.tab5_navbar)
            self.fig = pie_month(query, f"дохода за год по категориям")
            self.tab5_canavas = MyMplCanavas(self.fig)
            self.tab5_navbar = NavigationToolbar(self.tab5_canavas)
            self.tab5_layout.addWidget(self.tab5_navbar)
            self.tab5_layout.addWidget(self.tab5_canavas)
        except:
            self.fig = pie_month(query, f"дохода за год по категориям")
            self.tab5_canavas = MyMplCanavas(self.fig)
            self.tab5_navbar = NavigationToolbar(self.tab5_canavas)
            self.tab5_layout.addWidget(self.tab5_navbar)
            self.tab5_layout.addWidget(self.tab5_canavas)

    def tab5_year_bar_clicked(self):
        start_year = date(date.today().year, 1, 1)
        end_year = date(date.today().year + 1, 1, 1)
        query = session.query(db.Income).filter(
            and_(db.Income.date >= start_year, db.Income.date < end_year)
        )
        try:
            self.fig.clear()
            self.tab5_layout.removeWidget(self.tab5_canavas)
            self.tab5_layout.removeWidget(self.tab5_navbar)
            self.fig = bar_year(query, "дохода за год по месяцам", color="green")
            self.tab5_canavas = MyMplCanavas(self.fig)
            self.tab5_navbar = NavigationToolbar(self.tab5_canavas)
            self.tab5_layout.addWidget(self.tab5_navbar)
            self.tab5_layout.addWidget(self.tab5_canavas)
        except:
            self.fig = bar_year(query, "дохода за год по месяцам", color="green")
            self.tab5_canavas = MyMplCanavas(self.fig)
            self.tab5_navbar = NavigationToolbar(self.tab5_canavas)
            self.tab5_layout.addWidget(self.tab5_navbar)
            self.tab5_layout.addWidget(self.tab5_canavas)

    def tab6_mounth_pie_clicked(self):
        index = self.tab6_cbox.currentIndex() + 1
        query = session.query(db.Expeness).filter(
            db.Expeness.date.between(
                f"{date.today().year}-{selected_month(index)}-{0}",
                f"{date.today().year}-{selected_month(index)}-{31}",
            )
        )
        try:
            self.fig.clear()
            self.tab6_layout.removeWidget(self.tab6_canavas)
            self.tab6_layout.removeWidget(self.tab6_navbar)
            self.fig = pie_month(
                query, f"расхода за {months_dict[index]} по категориям"
            )
            self.tab6_canavas = MyMplCanavas(self.fig)
            self.tab6_navbar = NavigationToolbar(self.tab6_canavas)
            self.tab6_layout.addWidget(self.tab6_navbar)
            self.tab6_layout.addWidget(self.tab6_canavas)
        except:
            self.fig = pie_month(
                query, f"расхода за {months_dict[index]} по категориям"
            )
            self.tab6_canavas = MyMplCanavas(self.fig)
            self.tab6_navbar = NavigationToolbar(self.tab6_canavas)
            self.tab6_layout.addWidget(self.tab6_navbar)
            self.tab6_layout.addWidget(self.tab6_canavas)

    def tab6_mounth_plot_clicked(self):
        index = self.tab6_cbox.currentIndex() + 1
        query = session.query(db.Expeness).filter(
            db.Expeness.date.between(
                f"{date.today().year}-{selected_month(index)}-{0}",
                f"{date.today().year}-{selected_month(index)}-{31}",
            )
        )
        try:
            self.fig.clear()
            self.tab6_layout.removeWidget(self.tab6_canavas)
            self.tab6_layout.removeWidget(self.tab6_navbar)
            self.fig = plot_month(query, f"расхода по дням за {months_dict[index]}")
            self.tab6_canavas = MyMplCanavas(self.fig)
            self.tab6_navbar = NavigationToolbar(self.tab6_canavas)
            self.tab6_layout.addWidget(self.tab6_navbar)
            self.tab6_layout.addWidget(self.tab6_canavas)

        except:
            self.fig = plot_month(query, f"расхода по дням за {months_dict[index]}")
            self.tab6_canavas = MyMplCanavas(self.fig)
            self.tab6_navbar = NavigationToolbar(self.tab6_canavas)
            self.tab6_layout.addWidget(self.tab6_navbar)
            self.tab6_layout.addWidget(self.tab6_canavas)

    def tab6_year_pie_clicked(self):
        start_year = date(date.today().year, 1, 1)
        end_year = date(date.today().year + 1, 1, 1)
        query = session.query(db.Expeness).filter(
            and_(db.Expeness.date >= start_year, db.Expeness.date < end_year)
        )
        try:
            self.fig.clear()
            self.tab6_layout.removeWidget(self.tab6_canavas)
            self.tab6_layout.removeWidget(self.tab6_navbar)
            self.fig = pie_month(query, f"расхода за год по категориям")
            self.tab6_canavas = MyMplCanavas(self.fig)
            self.tab6_navbar = NavigationToolbar(self.tab6_canavas)
            self.tab6_layout.addWidget(self.tab6_navbar)
            self.tab6_layout.addWidget(self.tab6_canavas)
        except:
            self.fig = pie_month(query, f"расхода за год по категориям")
            self.tab6_canavas = MyMplCanavas(self.fig)
            self.tab6_navbar = NavigationToolbar(self.tab6_canavas)
            self.tab6_layout.addWidget(self.tab6_navbar)
            self.tab6_layout.addWidget(self.tab6_canavas)

    def tab6_year_bar_clicked(self):
        start_year = date(date.today().year, 1, 1)
        end_year = date(date.today().year + 1, 1, 1)
        query = session.query(db.Expeness).filter(
            and_(db.Expeness.date >= start_year, db.Expeness.date < end_year)
        )
        try:
            self.fig.clear()
            self.tab6_layout.removeWidget(self.tab6_canavas)
            self.tab6_layout.removeWidget(self.tab6_navbar)
            self.fig = bar_year(query, "расхода за год по месяцам", color="red")
            self.tab6_canavas = MyMplCanavas(self.fig)
            self.tab6_navbar = NavigationToolbar(self.tab6_canavas)
            self.tab6_layout.addWidget(self.tab6_navbar)
            self.tab6_layout.addWidget(self.tab6_canavas)
        except:
            self.fig = bar_year(query, "расхода за год по месяцам", color="red")
            self.tab6_canavas = MyMplCanavas(self.fig)
            self.tab6_navbar = NavigationToolbar(self.tab6_canavas)
            self.tab6_layout.addWidget(self.tab6_navbar)
            self.tab6_layout.addWidget(self.tab6_canavas)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    qssFile = "./stylesheet/Ubuntu.qss"
    with open(qssFile, "r") as fh:
        app.setStyleSheet(fh.read())
    w = MainClass()
    w.show()

    sys.exit(app.exec())
