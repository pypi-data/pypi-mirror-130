#!/usr/local/python3/bin/python3.9
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import io
import os
import sys
import json
import datetime
import locale
import codecs
import cgi
import cgitb

coding = 'utf-8'
cgitb.enable()

os.environ['GBASEDBTDIR'] = '/opt/GBASE/gbase'
os.environ['GBASEDBTSERVER'] = 'ol_gbasedbt10'
os.environ['GBASEDBTSQLHOSTS'] = '/opt/GBASE/gbase/etc/sqlhosts.ol_gbasedbt10'
os.environ['ODBCINI'] = '/opt/GBASE/gbase/demo/python/pyodbc/pyodbc-4.0.32/mytest/odbc.ini'

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
    mycursor.execute("insert into tpyodbc(id,name,sex,dt,content,pic) values(?,?,?,?,?,?)", id,name,sex,dt, content ,pic)
    data = []
    #for i in range(10000):
    #    data.append([id,name,sex,dt])
    #mycursor.executemany("insert into tpyodbc(id,name,sex,dt) values(?,?,?,?)", data)
    conn.commit()
    cursor1 = conn.cursor()
    stmt = "select id,name,sex,dt,content,pic from tpyodbc where name like '张三极%'"
    print('<tr>')
    print('<th colspan="6">')
    print(stmt)
    print('</th>')
    print('</tr>')
    cursor1.execute(stmt)
    rows = cursor1.fetchall()
    for i, (id, name, sex, dt, content, pic) in enumerate(rows):
        print('<tr>')
        print('<th>')
        print(type(id).__name__)
        print('</th>')
        print('<th>')
        print(type(name).__name__)
        print('</th>')
        print('<th>')
        print(type(sex).__name__)
        print('</th>')
        print('<th>')
        print(type(dt).__name__)
        print('</th>')
        print('<th>')
        print(type(content).__name__)
        print('</th>')
        print('<th>')
        print(type(pic).__name__)
        print('</th>')
        print('</tr>')
        print('<tr>')
        print('<th>')
        print(id)
        print('</th>')
        print('<th>')
        print(name)
        print('</th>')
        print('<th>')
        print(sex)
        print('</th>')
        print('<th>')
        print(dt)
        print('</th>')
        print('<th>')
        print(content)
        print('</th>')
        print('<th>')
        print("PIC SBLOB")
        print('</th>')
        print('</tr>')
    conn.close()
    sys.exit(0)

if __name__ == '__main__':
    #sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    locale.setlocale(locale.LC_ALL, "zh_CN.UTF-8")
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stdin = codecs.getwriter('utf-8')(sys.stdin.detach())
    print('Content-type:text/html\r\n\r\n')
    print('<html><body>')
    print('<table border="1">')
    test()
    print('</table>')
    print('</body></html>')
