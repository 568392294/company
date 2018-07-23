# -*- coding: utf-8 -*-
"""
Created on Mon Aug 07 10:00:27 2017

@author: ke.liu
"""

import MySQLdb

def connection():
    conn = None
    try:
        conn = MySQLdb.connect(host='172.16.50.100', user='zrpd', passwd='zrpd@123', db='china_merchants', port=3306, charset="utf8")
    except MySQLdb.Error, e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return conn

def execute(sql,tup=None):
    result = None
    conn = None
    try:
        conn = connection()
        cursor = conn.cursor()
        if tup == None:
            result = cursor.execute(sql)
        else:
            result = cursor.execute(sql, tup)
        conn.commit()
    except BaseException, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
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
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    return result





