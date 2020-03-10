# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hh_designer.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(774, 872)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.openers_label = QtWidgets.QLabel(self.centralwidget)
        self.openers_label.setGeometry(QtCore.QRect(90, 390, 321, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.openers_label.setFont(font)
        self.openers_label.setObjectName("openers_label")
        self.closers_label = QtWidgets.QLabel(self.centralwidget)
        self.closers_label.setGeometry(QtCore.QRect(100, 510, 321, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.closers_label.setFont(font)
        self.closers_label.setObjectName("closers_label")
        self.openers_number = QtWidgets.QLCDNumber(self.centralwidget)
        self.openers_number.setGeometry(QtCore.QRect(420, 380, 221, 91))
        self.openers_number.setObjectName("openers_number")
        self.closers_number = QtWidgets.QLCDNumber(self.centralwidget)
        self.closers_number.setGeometry(QtCore.QRect(420, 500, 221, 91))
        self.closers_number.setObjectName("closers_number")
        self.on_button = QtWidgets.QPushButton(self.centralwidget)
        self.on_button.setGeometry(QtCore.QRect(210, 210, 351, 151))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.on_button.setFont(font)
        self.on_button.setObjectName("on_button")
        self.off_button = QtWidgets.QPushButton(self.centralwidget)
        self.off_button.setGeometry(QtCore.QRect(210, 660, 351, 151))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.off_button.setFont(font)
        self.off_button.setObjectName("off_button")
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setGeometry(QtCore.QRect(230, 70, 321, 61))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.title_label.setFont(font)
        self.title_label.setObjectName("title_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionIncrease = QtWidgets.QAction(MainWindow)
        self.actionIncrease.setObjectName("actionIncrease")
        self.actionDecrease = QtWidgets.QAction(MainWindow)
        self.actionDecrease.setObjectName("actionDecrease")
        self.action20 = QtWidgets.QAction(MainWindow)
        self.action20.setObjectName("action20")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.openers_label.setText(_translate("MainWindow", "Openers Stimulation Intensity"))
        self.closers_label.setText(_translate("MainWindow", "Closers Stimulation Intensity"))
        self.on_button.setText(_translate("MainWindow", "ON"))
        self.off_button.setText(_translate("MainWindow", "OFF"))
        self.title_label.setText(_translate("MainWindow", "Helping Hand "))
        self.actionIncrease.setText(_translate("MainWindow", "Increase"))
        self.actionDecrease.setText(_translate("MainWindow", "Decrease"))
        self.action20.setText(_translate("MainWindow", "100"))
