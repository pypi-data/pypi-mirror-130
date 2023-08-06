# -*- coding: utf-8 -*-
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import io
import os
import sys
import json
import datetime

coding = 'utf-8'

def string_to_json(unicode_string):
    return json.loads(unicode_string)

def test():
    import sys
    import Pyodbc_Knight as pyodbc
    conn = pyodbc.connect("DSN=jsvftestdbs")
    conn.setdecoding(pyodbc.SQL_CHAR,encoding=coding)
    conn.setdecoding(pyodbc.SQL_WCHAR, encoding=coding)
    conn.setdecoding(pyodbc.SQL_WMETADATA, encoding=coding)
    conn.setencoding(encoding=coding)
    conn.add_output_converter(pyodbc.SQL_JSON, string_to_json)
    id = 1
    name = '张三极乐空间阿斯顿减肥'
    sex =  json.dumps({1:1,'测试':'结果','数组': [1,2,3]});
    content =  pyodbc.Binary("adfadsf",coding)
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    with open('/etc/passwd', 'rb') as f:
        bindata = f.read()
    pic =  pyodbc.Binary(bindata)
    mycursor = conn.cursor()
    mycursor.execute("drop table if exists tpyodbc")
    mycursor.execute("create table tpyodbc(id serial, name varchar(60), sex json,dt datetime year to fraction(5) ,content text,pic byte)")
    #mycursor.execute("create table tpyodbc(id serial, name varchar(60), sex varchar(200),dt datetime year to fraction(5) ,content text,pic byte)")
    mycursor.execute("insert into tpyodbc(id,name,sex,dt,content,pic) values(?,?,?,?,?,?)", id,name,sex,dt, content ,pic)
    data = []
    #for i in range(10000):
    #    data.append([id,name,sex,dt])
    #mycursor.executemany("insert into tpyodbc(id,name,sex,dt) values(?,?,?,?)", data)
    conn.commit()
    cursor1 = conn.cursor()
    cursor1.execute('select id,name,sex,dt,content,pic from tpyodbc')
    rows = cursor1.fetchall()
    for i, (id, name, sex, dt, content, pic) in enumerate(rows):
        print(type(id),type(name),type(sex),type(dt),type(content),type(pic))
        #print(id,str(name),sex,dt,content,pic.hex())
        print(id,str(name),sex,dt)
    conn.close()
    sys.exit(0)

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    test()


