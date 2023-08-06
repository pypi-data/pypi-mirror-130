#!/usr/local/python3/bin/python3.9
# -*- coding: utf-8 -*-
import io
import os
import sys
import json
import datetime
import decimal
from time import *
import cgi
import cgitb

coding = 'utf-8'
cgitb.enable()

os.environ['GBASEDBTDIR'] = '/opt/GBASE/gbase'
os.environ['GBASEDBTSERVER'] = 'ol_gbasedbt10'
os.environ['GBASEDBTSQLHOSTS'] = '/opt/GBASE/gbase/etc/sqlhosts.ol_gbasedbt10'


def test():
    import informixdb
    conn = informixdb.connect('odbc_demodb@ol_gbasedbt10','gbasedbt','P@ssw0rd0LD')
    conn.autocommit = 0  # WE NEED THIS FOR DDL TX COMMIT
    cursor = conn.cursor()
    cursor.execute("drop table if exists ifxdbtest;")
    stmt_list = ['create table ifxdbtest(']
    stmt_list.append('uid integer')
    stmt_list.append(',uname varchar(100)')
    stmt_list.append(',udate date')
    stmt_list.append(',udatetime datetime year to fraction(5)')
    stmt_list.append(',ufloat float')
    stmt_list.append(',udecimal decimal(12,3)')
    stmt_list.append(',utext text')
    stmt_list.append(',uclob clob')
    stmt_list.append(',ubyte byte')
    stmt_list.append(',ublob blob')
    stmt_list.append(',primary key (uid)')
    stmt_list.append(') put ublob in (')
    stmt_list.append('sbdbs')
    stmt_list.append(');')
    stmt = ''.join(stmt_list)
    print('<tr>')
    print('<th colspan="5">')
    print(stmt)
    print('</th>')
    print('</tr>')
    cursor.execute(stmt)

    stmt_list = ['insert into ifxdbtest(']
    stmt_list.append('uid')
    stmt_list.append(',uname')
    stmt_list.append(',udate')
    stmt_list.append(',udatetime')
    stmt_list.append(',ufloat')
    stmt_list.append(',udecimal')
    stmt_list.append(',utext')
    stmt_list.append(',uclob')
    stmt_list.append(',ubyte')
    stmt_list.append(',ublob')
    stmt_list.append(')')
    stmt_list.append(' values(?')
    stmt_list.append(',?')
    stmt_list.append(',?')
    stmt_list.append(',?')
    stmt_list.append(',?')
    stmt_list.append(',?')
    stmt_list.append(',?')
    stmt_list.append(',?')
    stmt_list.append(',?')
    stmt_list.append(',?')
    stmt_list.append(')')
    stmt = ''.join(stmt_list)

    begin_time = time()
    print('<tr>')
    print('<th colspan="5">')
    print(stmt)
    print('</th>')
    print('</tr>')
    params = []
    lobbuf_size=int(1024000)
   
    uid = int(666)
    params.append(uid)

    uname = '卡布达'
    params.append(uname)

    udate = datetime.date(2021,12,3)
    params.append(udate)

    udatetime = datetime.datetime.now()
    params.append(udatetime)

    ufloat = float(514.123)
    params.append(ufloat)

    udecimal = decimal.Decimal('123123.412')
    params.append(udecimal)

    with open('/etc/passwd', 'rb') as f:
        utext = f.read()
    params.append(utext)

    uclob = conn.Sblob(1)   # DEFINED IN SOURCE FILE
    with open('/etc/services', 'rb') as f:
        while True:
            t = f.read(lobbuf_size);
            if(t):
                uclob.write(t)
            else:
                break
    uclob.close()
    params.append(uclob)

    with open('./cat.jpg', 'rb') as f:
        ubyte = f.read()
    params.append(ubyte)

    ublob = conn.Sblob(0)    # DEFINED IN SOURCE FILE
    with open('./cat.jpg', 'rb') as f:
        while True:
            t = f.read(lobbuf_size);
            if(t):
                ublob.write(t)
            else:
                break
    ublob.close()
    params.append(ublob)

    cursor.prepare(stmt)
    data = []
    ts = []
    ret = cursor.execute(None,params)

    #BULK INSERT CAN ONLY WORK FAST WITHOUT ANY LOB/SLOB TYPE
    #for i in range(10000):
        #th = threading.Thread(target=cursor.execute,args=[None,params])
        #s.append(th)
        #ret = cursor.execute(None,params)  # INSERT 10000 TIME ROW BY ROW ELASPED 2s
        #data.append(params)
    end_time = time()
    paratime = end_time - begin_time
    print('<tr>')
    print('<th colspan="5">')
    print('paratime:',paratime)
    print('</th>')
    print('</tr>')
    begin_time = time()
    #for t in ts:
    #    t.start()
    #    t.join()

    #ret = cursor.executemany(None,data)  # INSERT 10000 ROWS IN BULK ELAPSED 0.8s
    #use cursor.callproc(func,param[1,2,3])
    conn.commit()
    end_time = time()
    exectime = end_time - begin_time
    print('<tr>')
    print('<th colspan="5">')
    print('exectime:',exectime)
    print('</th>')
    print('</tr>')
    begin_time = time()
    print('<tr>')
    print('<th colspan="5">')
    print('Rows Affected:' + str(ret))
    print('</th>')
    print('</tr>')
    print('</tr>')
    
    stmt = "select * from ifxdbtest"
    cursor.execute(stmt)
    colno = len(cursor.description)
    print('<tr>')
    print('<th colspan="5">')
    print('Column Number:' + str(colno))
    print('</th>')
    print('</tr>')

    print('<tr>')
    for r in cursor.description:
        print('<th>')
        print("Name:" + r[0] + "\t", end='')
        print('</th>')
        print('<th>')
        print("Type:" + r[1] + "\t", end='')
        print('</th>')
        print('<th>')
        print("Xid:" + str(r[2]) + "\t", end='')
        print('</th>')
        print('<th>')
        print("Length:" + str(r[3]) + "\t", end='')
        print('</th>')
        print('<th>')
        print("Nullable:" + str(r[6]))
        print('</th>')
        print('</tr>')
    ret = cursor.fetchall()
    # use fetchone or fetchmany(N) as need

    print('<tr>')
    print('<th colspan="5" rowspan="1" height="20">')
    print('</th>')
    print('</tr>')

    for row in ret:
        for idx,col in enumerate(row):
            type = cursor.description[idx][1]
            if(type == 'text'):
                with open('./text_passwd', 'wb') as f:
                    f.write(col)
            elif (type == 'byte'):
                with open('./byte_cat.jpg', 'wb') as f:
                    f.write(col)
            #Sblob can also "seek", "tell", "stat", "truncate" as needed
            elif(cursor.description[idx][1] == 'fixed udt \'clob\''):
                col.open()
                with open('./clob_services', 'wb') as f:
                    while (1):
                        buf=col.read(lobbuf_size)
                        if(buf):
                            f.write(buf)
                        else:
                            break
                col.close()
            elif (cursor.description[idx][1] == 'fixed udt \'blob\''):
                col.open()
                with open('./blob_cat.jpg', 'wb') as f:
                    while (1):
                        buf=col.read(lobbuf_size)
                        if(buf):
                            f.write(buf)
                        else:
                            break
                col.close()
            else:
                print('<tr>')
                print('<th colspan="5">')
                print(col)
                print('</th>')
                print('</tr>')
    print('<tr>')
    print('<th colspan="5">')
    print("Row Count:"+str(len(ret)))
    print('</th>')
    print('</tr>')
    conn.close()
    sys.exit(0)

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    print('Content-type:text/html\r\n\r\n')
    print('<html><body>')
    print('<table border="1">')
    test()
    print('</table>')
    print('</body></html>')


