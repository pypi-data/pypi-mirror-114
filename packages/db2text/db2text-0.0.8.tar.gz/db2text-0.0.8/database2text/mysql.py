#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys,pymysql
import database2text.tool as dbtt
from database2text.tool import *

class mysql(object):
    def ana_TABLE(otype):
        for oname, in db.exec("show tables"):
            print(oname)
            _,odata=db.res1("show create table %s" %(oname))
            print(odata)
            maxcsize=db.res1("select max(length(COLUMN_NAME)) from information_schema.COLUMNS where TABLE_SCHEMA='%s' and table_name='%s'" %(database,oname))
            c=db.conn.cursor()
            for i in db.exec2("select * from information_schema.COLUMNS where TABLE_SCHEMA='%s' and table_name='%s'" %(database,oname)):
            	print(i)
            for column_name,data_type,char_length,data_precision,data_scale,nullable,default_length,data_default in db.exec("select column_name,data_type,char_length,data_precision,data_scale,nullable,default_length,data_default from all_tab_cols where owner='%s' and table_name='%s' order by column_id" %(owner,oname)):
                if data_type=="NUMBER":
                    if data_precision is not None and data_scale is not None:
                        if data_scale==0:
                            odata=odata+"NUMBER(%d)" %(data_precision)
                        else:
                            odata=odata+"NUMBER(%d,%d)" %(data_precision,data_scale)
                    elif data_precision is None and data_scale==0:
                        odata=odata+"INTEGER"
                    else:
                        print(column_name,char_length,data_precision,data_scale)
                        sys.exit(0)
                elif data_type in ("VARCHAR2","VARCHAR","CHAR"):
                    odata=odata+"%s(%d)" %(data_type,char_length)
                elif data_type.startswith("TIMESTAMP"):
                    odata=odata+"%s" %(data_type)
                elif data_type in("DATE","BLOB"):
                    odata=odata+"%s" %(data_type)
                else:
                    print(column_name,data_type,char_length,data_precision,data_scale)
                    sys.exit(0)
                if default_length:
                    odata=odata+" default %s" %(data_default.strip())
                if nullable=="N":
                    odata=odata+" not null"
                odata=odata+",\n"
            odata=odata[:-2]
            odata=odata+"\n);"
            dbdata["sql"][otype][oname]=odata
    def ana_VIEW(otype):
        for oname, in db.exec("show table status where comment ='view'"):
            dbdata["sql"][otype][oname]=getobjtext(otype,oname)

    def getobjtext(otype,oname):
        _,ssql=db.res1("show create %s %s" %(otype,oname))
        return ssql

def readdata(stdata,storidata):
    dbdata["sql"]={}
    for i in vars(mysql):
        if i.startswith("ana_"):
            otype=i[4:]
            dbdata["sql"][otype]={}
            getattr(mysql,i)(otype)

def connect(stdata,storidata):
    global database
    database=stdata["database"]
    try:
        db.conn=pymysql.connect(host=stdata["host"],user=stdata["user"],password=stdata["password"], database=stdata["database"], port=int(stdata["port"]))
    except:
        dbtt.quit("connect error!")

def export(stdata,storidata):
    dbtt.export(stdata,storidata,dbdata)

__all__=[]
