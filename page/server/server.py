import socketserver  # 导入socketserver模块
import pymysql

class MyServer(socketserver.BaseRequestHandler):  # 创建一个类，继承自socketserver模块下的BaseRequestHandler类

    def handle(self):  # 要想实现并发效果必须重写父类中的handler方法，在此方法中实现服务端的逻辑代码（不用再写连接准备，包括bind()、listen()、accept()方法）

        conn = self.request
        addr = self.client_address
        # 上面两行代码，等于 conn,addr = socket.accept()，只不过在socketserver模块中已经替我们包装好了，还替我们包装了包括bind()、listen()、accept()方法

        accept_data = str(conn.recv(1024), encoding="utf8")
        print("服务器端接受信息："+accept_data)
        accept_list = accept_data.split("~")

        if accept_list[0] == "Login":
            inf = accept_list[1].split("#")
            en1_value = inf[0]
            en2_value = inf[1]
            send_data = self.checkLogin(en1_value, en2_value)
            print("服务器端发送信息："+send_data)
            conn.sendall(bytes(send_data,encoding="utf8"))
        # send_data = bytes(input(">>>>>"), encoding="utf8")
        # conn.sendall(send_data)
        conn.close()
    def checkLogin(self,en1_value,en2_value):
        #打开数据库连接
        db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='graduationdesigner')
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # SQL 查询语ju
        sql = "select * from user"
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                username = row[0]
                pwd = row[1]
                if username == en1_value and pwd == en2_value:
                    print("数据库检查结果正确")
                    return "1"
        except:
            print("Error: unable to fecth data")

        # 关闭数据库连接
        db.close()
        return "0"

if __name__ == '__main__':
    print("服务器开始运行：")
    sever = socketserver.ThreadingTCPServer(("127.0.0.1", 8888),
                                            MyServer)  # 传入 端口地址 和 我们新建的继承自socketserver模块下的BaseRequestHandler类  实例化对象

    sever.serve_forever()  # 通过调用对象的serve_forever()方法来激活服务端