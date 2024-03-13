# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ResultWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ResultWindow(object):
    def setupUi(self, ResultWindow):
        ResultWindow.setObjectName("ResultWindow")
        #ResultWindow.resize(619, 708)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ResultWindow.sizePolicy().hasHeightForWidth())
        ResultWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        ResultWindow.setFont(font)
        ResultWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        ResultWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(ResultWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.main_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_label.sizePolicy().hasHeightForWidth())
        self.main_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.main_label.setFont(font)
        self.main_label.setTextFormat(QtCore.Qt.AutoText)
        self.main_label.setAlignment(QtCore.Qt.AlignCenter)
        self.main_label.setWordWrap(False)
        self.main_label.setObjectName("main_label")
        self.verticalLayout.addWidget(self.main_label)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.result_label = QtWidgets.QLabel(self.centralwidget)
        self.result_label.setObjectName("result_label")
        self.verticalLayout.addWidget(self.result_label)
        self.result_table = QtWidgets.QTableWidget(self.centralwidget)
        self.result_table.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.result_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.result_table.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.result_table.setObjectName("result_table")
        self.result_table.setColumnCount(6)
        self.result_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(5, item)
        self.result_table.horizontalHeader().setVisible(True)
        self.result_table.verticalHeader().setVisible(True)
        self.verticalLayout.addWidget(self.result_table)
        self.weight_label = QtWidgets.QLabel(self.centralwidget)
        self.weight_label.setObjectName("weight_label")
        self.verticalLayout.addWidget(self.weight_label)
        self.result_weight_table = QtWidgets.QTableWidget(self.centralwidget)
        self.result_weight_table.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.result_weight_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.result_weight_table.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.result_weight_table.setObjectName("result_weight_table")
        self.result_weight_table.setColumnCount(4)
        self.result_weight_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.result_weight_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.result_weight_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.result_weight_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.result_weight_table.setHorizontalHeaderItem(3, item)
        self.result_weight_table.horizontalHeader().setVisible(True)
        self.result_weight_table.verticalHeader().setVisible(True)
        self.verticalLayout.addWidget(self.result_weight_table)
        self.knf_label = QtWidgets.QLabel(self.centralwidget)
        self.knf_label.setObjectName("knf_label")
        self.verticalLayout.addWidget(self.knf_label)

        self.continue_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.continue_button.sizePolicy().hasHeightForWidth())
        self.continue_button.setSizePolicy(sizePolicy)
        self.continue_button.setMinimumSize(QtCore.QSize(0, 40))
        self.continue_button.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.continue_button.setObjectName("continue_button")
        self.verticalLayout.addWidget(self.continue_button)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)

        # Для масштабирования виджета таблицы
        self.result_table.setWordWrap(True)
        self.result_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.result_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.result_weight_table.setWordWrap(True)
        self.result_weight_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.result_weight_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)


        ResultWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ResultWindow)
        QtCore.QMetaObject.connectSlotsByName(ResultWindow)

    def retranslateUi(self, ResultWindow):
        _translate = QtCore.QCoreApplication.translate
        ResultWindow.setWindowTitle(_translate("ResultWindow", "MainWindow"))
        self.main_label.setText(_translate("ResultWindow", "Предполагаемый диагноз"))
        self.result_label.setText(_translate("ResultWindow", "Все формулы. Выберите результаты, с которыми согласны"))
        self.result_table.setSortingEnabled(True)
        item = self.result_table.horizontalHeaderItem(0)
        item.setText(_translate("ResultWindow", "Согласен?"))
        item = self.result_table.horizontalHeaderItem(1)
        item.setText(_translate("ResultWindow", "Нужно посетить?"))
        item = self.result_table.horizontalHeaderItem(2)
        item.setText(_translate("ResultWindow", "Врач"))
        item = self.result_table.horizontalHeaderItem(3)
        item.setText(_translate("ResultWindow", "Корректность, %"))
        item = self.result_table.horizontalHeaderItem(4)
        item.setText(_translate("ResultWindow", "Причина"))
        item = self.result_table.horizontalHeaderItem(5)
        item.setText(_translate("ResultWindow", "Формула"))
        self.weight_label.setText(_translate("ResultWindow", "Формулы с учетом весов"))
        self.result_weight_table.setSortingEnabled(True)
        item = self.result_weight_table.horizontalHeaderItem(0)
        item.setText(_translate("ResultWindow", "Нужно посетить?"))
        item = self.result_weight_table.horizontalHeaderItem(1)
        item.setText(_translate("ResultWindow", "Врач"))
        item = self.result_weight_table.horizontalHeaderItem(2)
        item.setText(_translate("ResultWindow", "Результат"))
        item = self.result_weight_table.horizontalHeaderItem(3)
        item.setText(_translate("ResultWindow", "Причина"))
        self.knf_label.setText(_translate("ResultWindow", "Упрощенные формулы"))


        self.continue_button.setText(_translate("ResultWindow", "Продолжить"))
