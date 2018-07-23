# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 16:57:41 2017

对外投资
@author: Administrator
"""
#%%
#import time
import MySQLdb
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from util import oracle
from base import Tianyan


class Investment(Tianyan):

    def insert_db(self, line, isexistdata="yes"):
        # SQL 插入语句
        if isexistdata == "yes":
            sql = "insert into \"cmp_investment\" (\"create_time\", \"update_time\", \"company_name\", \"fetch_url\",\
                    \"invested_company_name\", \"invested_company_url\", \"legal_person\", \"legal_person_url\",\
                   \"registered_capital\", \"investment_amount\", \"investment_proportion\", \
                   \"register_date\", \"status\", \"unique_key\", \"id\") \
                   values(SYSDATE, SYSDATE, :1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13)"
        else:
            sql = "insert into \"cmp_investment\" (\"create_time\", \"update_time\", \"company_name\", \"fetch_url\", \"id\") \
                   values(SYSDATE, SYSDATE, :1, :2, :3)"
        # 执行sql语句
        result = oracle.execute(sql, line)
        print result

    def trans_encode(self, alist):
        """
        将列表中的各个元素转换成utf-8编码
        """
        result = []
        for i in range(len(alist)):
            l = alist[i]
            if type(l) == unicode:
                l = l.encode("utf-8")
#                l = MySQLdb.escape_string(l)
                result.append(l)
            elif i == 0 or i == 1:
                result.append(int(l))
            elif i == 3:
                l = MySQLdb.escape_string(l)
                result.append(l)
            else:
                result.append(l)
        return result

    def onepage_data(self, company_name, company_link):
        """
        一行提交一次
        """
        browser = self.browser
        if self.isElementExist('//div[@id="_container_invest"]'):
            elements = browser.find_elements_by_xpath(
                '//div[@id="_container_invest"]//table[@class="table companyInfo-table"]/tbody/tr')
            for i in range(len(elements)):
                # 第 i 行
                #curDate = time.strftime("%Y%m%d%H%M%S")  # 当前日期
                line_data = [company_name, company_link]
                elt = elements[i]
                line = elt.find_elements_by_tag_name("td")
                for j in range(len(line)):
                    if j == 0:
                        data1 = line[j].text
                        data2 = line[j].find_element_by_tag_name(
                            "a").get_attribute("href")
                        line_data.extend([data1, data2])
                    elif j == 1:
                        if line[j].find_elements_by_tag_name("a") != []:
                            data1 = line[j].find_element_by_tag_name(
                                "a").get_attribute("title")
                            data2 = line[j].find_element_by_tag_name(
                                "a").get_attribute("href")
                            line_data.extend([data1, data2])
                        else:
                            data = line[j].text
                            line_data.extend([data, data])
                    else:
                        data = line[j].text
                        line_data.append(data)
                # 生成加密键值
                comb = company_name + line_data[4]
                unique_key = self.md5(comb.encode("utf-8"))
                line_data.append(unique_key)
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
username = "15623670705"   #第一个参数为用户名
password = "q12345678"   #第二个参数为密码
win = Investment(username, password) 
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
filePath = u"cmp_investment.xlsx" 
field = "invest"
win.fetch(filePath, field)
