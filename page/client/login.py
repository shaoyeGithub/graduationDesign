from graduation.page.client import ui_login
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import socket

class Login(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.ui = ui_login.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.userEdit.insert("123")
        self.ui.passwordEdit.insert("123")


    def loginCheck(self):
        try:
            self.sk = socket.socket()
            self.sk.connect(("127.0.0.1", 8888))  # 主动初始化与服务器端的连接
            user = self.ui.userEdit.text()
            psw = self.ui.passwordEdit.text()
            send_data = "Login~" + user+ "#" + psw
            print("客户端发送消息：" + send_data)
            self.sk.sendall(bytes(send_data, encoding="utf8"))
            accept_data = str(self.sk.recv(1024), encoding="utf8")
            print("客户端接受消息：" + accept_data)
            if  accept_data == "1":
                self.accept()
            else:
                reply = QMessageBox.information(self,  # 使用infomation信息框
                                                "warning",
                                                "用户名或密码错误",
                                                QMessageBox.Ok )
        except:
           reply = QMessageBox.information(self,
                                     "warning",
                                     "服务器未登录",
                                     QMessageBox.Ok)