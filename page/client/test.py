from graduation.diagnosis import testclassify
from graduation.page.client import preprocess
from  PIL import Image
import numpy as np
import  cv2
import matplotlib.pyplot as plt
from skimage import measure,draw
import  dicom
import  datetime
# getpt = dicom.read_file("D:/FILE/python_code/graduation/page/client/data1/bojingyi/src/PT/PT_006")
# print(getpt.PatientBirthDate)
# age = int(datetime.datetime.now().year) - int(getpt.PatientBirthDate[:4])
#
# print(age)
import pymysql
db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='graduationdesigner')
# 使用cursor()方法获取操作游标
cursor = db.cursor()
sql = 'select id from patient where name = "%s"'% "123"
# SQL 查询语ju
num = 0
sql1 = 'select count(*) from patient'
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()

    if len(results) == 0:
        cursor.execute(sql1)
        results1 = cursor.fetchall()
        for row1 in results1:
            num = int(row1[0]) + 1
        sql = 'insert into patient(id,name,gender,age,data,diatime,diaresult) VALUES("%d","%s","%s","%s","%s","%s","%s")' % (
        num, '2', '3', '4', '5', '6', '7')
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            db.commit()
        except:
            db.rollback()
    else:
        for row in results:
            num = int(row[0])
            sql = 'update patient set diatime = "%s"  where id = "%d"' % (
                '2018-05-20 14:13:40',num)
            try:
                # 执行SQL语句
                cursor.execute(sql)
                # 获取所有记录列表
                db.commit()
            except:
                db.rollback()

except:
    print("Error: unable to fecth data")


print(num)


# 关闭数据库连接
db.close()


