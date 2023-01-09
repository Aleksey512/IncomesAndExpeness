from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from UI import Ui_GroupBox     

import sys

from sqlalchemy.orm import sessionmaker
import db
import sqlite3


Session = sessionmaker(bind=db.engine)
session = Session()


class MainClass(QtWidgets.QGroupBox, Ui_GroupBox):

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.pushButton.clicked.connect(self.on_button_clicked)

        for u in session.query(db.Income).all():
            rows = self.tableWidget.rowCount()
            row_as_dict = u.__dict__
            self.tableWidget.setRowCount(rows + 1)
            self.tableWidget.setItem(rows, 0, QtWidgets.QTableWidgetItem(str(row_as_dict["id"])))
            self.tableWidget.setItem(rows, 1, QtWidgets.QTableWidgetItem(str(row_as_dict["date"])))
            self.tableWidget.setItem(rows, 2, QtWidgets.QTableWidgetItem(row_as_dict["name"]))
            self.tableWidget.setItem(rows, 3, QtWidgets.QTableWidgetItem(str(row_as_dict["value"])))
        self.tableWidget.resizeColumnsToContents()

    def on_button_clicked(self):
        db.add()


if __name__ == "__main__":
    def createConnection():
        con = QSqlDatabase.addDatabase("QSQLITE")
        con.setDatabaseName("myDB.db")
        if not con.open():
            QtWidgets.QMessageBox.critical(
                None,
                "QTableView Example - Error!",
                "Database Error: %s" % con.lastError().databaseText(),
            )
            return False
        return True

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    if not createConnection():
        sys.exit(1)
    w = MainClass()
    w.show()

    sys.exit(app.exec())