# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_login.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(60, 100, 281, 110))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.loginButton = QtWidgets.QPushButton(self.layoutWidget)
        self.loginButton.setStyleSheet("background-color: rgb(85, 85, 255);")
        self.loginButton.setObjectName("loginButton")
        self.gridLayout.addWidget(self.loginButton, 0, 1, 1, 1)
        self.passwordEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordEdit.setObjectName("passwordEdit")
        self.gridLayout.addWidget(self.passwordEdit, 1, 0, 1, 1)
        self.pswButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pswButton.setStyleSheet("")
        self.pswButton.setObjectName("pswButton")
        self.gridLayout.addWidget(self.pswButton, 1, 1, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 2, 0, 1, 1)
        self.userEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.userEdit.setObjectName("userEdit")
        self.gridLayout.addWidget(self.userEdit, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(140, 40, 81, 18))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        self.loginButton.clicked.connect(Dialog.loginCheck)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "登录"))
        self.loginButton.setText(_translate("Dialog", "登陆"))
        self.pswButton.setText(_translate("Dialog", "修改密码"))
        self.checkBox.setText(_translate("Dialog", "记住密码"))
        self.label.setText(_translate("Dialog", "淋巴瘤CAD系统"))

