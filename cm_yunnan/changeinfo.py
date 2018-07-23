# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 16:57:41 2017

企业分支机构
@author: Administrator
"""
#%%
#import time

from util import oracle
from base import Tianyan


class ChangeInfo(Tianyan):

    def insert_db(self, line, isexistdata="yes"):
        # SQL 插入语句
        if isexistdata == "yes":
            sql = "INSERT INTO \"T_CMP_BASEINFO_MODIFY\" (\"F_CREATE_TIME\", \"F_UPDATE_TIME\", \"F_COMPANY_NAME\", \"F_FETCH_URL\",\
                    \"F_MODIFY_DATE\", \"F_MODIFY_ITEM\", \"F_MODIFY_DEFORE\", \"F_MODIFY_AFTER\", \"F_MODIFY_ID\") \
                   VALUES(SYSDATE, SYSDATE, :1, :2, :3, :4, :5, :6, :7)"
        else:
            sql = "INSERT INTO \"T_CMP_BASEINFO_MODIFY\" (\"F_CREATE_TIME\", \"F_UPDATE_TIME\", \"F_COMPANY_NAME\", \"F_FETCH_URL\", \"F_MODIFY_ID\") \
                   VALUES(SYSDATE, SYSDATE, :1, :2, :3)"
        # 执行sql语句
        result = oracle.execute(sql, line)
        print result

    def onepage_data(self, company_name, company_link):
        """
        一行提交一次
        """
        browser = self.browser
        if self.isElementExist('//div[@id="_container_changeinfo"]'):
            elements = browser.find_elements_by_xpath(
                '//div[@id="_container_changeinfo"]//table/tbody/tr')
            for i in range(len(elements)):
                # 第 i 行
                #curDate = time.strftime("%Y%m%d%H%M%S")  # 当前日期
                line_data = [company_name, company_link]
                elt = elements[i]
                line = elt.find_elements_by_tag_name("td")
                for j in range(len(line)):
                    data = line[j].text
                    line_data.append(data)
                # 生成加密键值
                #comb = company_name + line_data[4]
                #unique_key = self.md5(comb.encode("utf-8"))
                #line_data.append(unique_key)
                # 一行提交一次
                id = self.getUUID()
                line_data.append(id)    
                #line_data = self.trans_encode(line_data)  # 转成utf-8编码
                line_data = tuple(line_data)  # 转成元组数据类型
                self.insert_db(line_data, isexistdata="yes")
        else:  # 不存在对外投资字段
            #curDate = time.strftime("%Y%m%d%H%M%S")  # 当前日期
            line_data = [company_name, company_link]
            id = self.getUUID()
            line_data.append(id)
            #line_data = self.trans_encode(line_data)  # 转成utf-8编码
            line_data = tuple(line_data)  # 转成元组数据类型
            #self.insert_db(line_data, isexistdata="no")


#%%
#==============================================================================
#                               登录
#==============================================================================
username = "13871230544"   #第一个参数为用户名
password = "zrpd123456"   #第二个参数为密码
win = ChangeInfo(username, password) 
win.login()   

win.turnhandle()
#%%
#==============================================================================
#==============================================================================
# #                    对外投资详情
#
# 注意####            需要手动将页面缩放至【最小】
#
#==============================================================================
#==============================================================================
filePath = u"1000家企业.xlsx" 
field = "changeinfo"
win.fetch(filePath, field)
