from graduation.page.server import serverUI,server
from PyQt5 import QtWidgets
import socketserver
class firstWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = serverUI.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.iniServer)


    def iniServer(self):
        try:
            print("服务器开始运行：")
            self.ui.textEdit.setText("服务器开始运行：")
            sever = socketserver.ThreadingTCPServer(("127.0.0.1", 8888),
                                                server.MyServer)  # 传入 端口地址 和 我们新建的继承自socketserver模块下的BaseRequestHandler类  实例化对象

            sever.serve_forever()  # 通过调用对象的serve_forever()方法来激活服务端
        except:
            print("出错了")