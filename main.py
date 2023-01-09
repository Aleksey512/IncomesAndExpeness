from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from UI import Ui_GroupBox     

import sys

import db
import sqlite3

class MainClass(QtWidgets.QGroupBox, Ui_GroupBox):

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.pushButton.clicked.connect(self.on_button_clicked)

        # Set up the model
        self.model = QSqlTableModel(self)
        self.model.setTable("Income")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Date")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Name")
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Value")
        self.model.select()
        # Set up the view
        self.tableWidget.setModel(self.model)
        self.view.resizeColumnsToContents()

        # query = QSqlQuery('SELECT id, date, name, value FROM Income')
        # while query.next():
        #     rows = self.tableWidget.rowCount()
        #     self.tableWidget.setRowCount(rows + 1)
        #     self.tableWidget.setItem(rows, 0, QtWidgets.QTableWidgetItem(query.value(0)))
        #     self.tableWidget.setItem(rows, 1, QtWidgets.QTableWidgetItem(query.value(1)))
        #     self.tableWidget.setItem(rows, 2, QtWidgets.QTableWidgetItem(query.value(2)))
        #     self.tableWidget.setItem(rows, 3, QtWidgets.QTableWidgetItem(str(query.value(3))))
        # self.tableWidget.resizeColumnsToContents()


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