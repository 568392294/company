# -*- coding: utf-8 -*-
"""
Created on Mon Aug 07 10:00:27 2017

@author: ke.liu
"""

import cx_Oracle
import traceback

import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

def connection():
    conn = None
    try:
        #conn = MySQLdb.connect(host='172.16.50.100', user='zrpd', passwd='zrpd@123', db='china_merchants', port=3306, charset="utf8")
        #conn = cx_Oracle.connect('zwy_test','zwy_test123','172.16.50.131:1521/orcl')  
        conn = cx_Oracle.connect('ynzscj','ynzscj','172.16.50.130:1521/orcl')
    except Exception, e:
        print 'str(Exception):\t', str(Exception)
        print 'str(e):\t\t', str(e)
        print 'traceback.format_exc():\n%s' % traceback.format_exc()
    return conn

def execute(sql,tup=None):
    result = None
    conn = None
    cursor = None
    try:
        conn = connection()
        cursor = conn.cursor()
        if tup == None:
            result = cursor.execute(sql)
        else:
            result = cursor.execute(sql, tup)
        conn.commit()
    except Exception, e:
        print 'str(Exception):\t', str(Exception)
        print 'str(e):\t\t', str(e)
        print 'traceback.format_exc():\n%s' % traceback.format_exc()
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    return result

def executeQuery(sql, size=None):
    result = None
    conn = None
    cursor = None
    try:
        conn = connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        if size == None:
            result = cursor.fetchall()
        else:
            result = cursor.fetchmany(size)
    except Exception, e:
        print 'str(Exception):\t', str(Exception)
        print 'str(e):\t\t', str(e)
        print 'traceback.format_exc():\n%s' % traceback.format_exc()
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    return result





