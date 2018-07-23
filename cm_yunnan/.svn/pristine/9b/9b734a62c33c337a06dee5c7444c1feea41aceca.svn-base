# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 11:43:47 2017

@author: Administrator
"""

#%%
import re
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from util import oracle
from base import Tianyan
import MySQLdb

import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


class Lawsuit(Tianyan):

    def insert_db(self, line, isexistdata="yes"):
        
        #print line
          
        # SQL 插入语句
        if isexistdata == "yes":
            sql = "insert into CMP_LAWSUIT (CREATE_TIME, UPDATE_TIME, COMPANY_NAME, FETCH_URL, \
                   LAWSUIT_DATE, TITLE, URL, CASE_CAUSE, CASE_STATUS, CASE_NO, CONTENT, ID)  \
                   values(SYSDATE, SYSDATE, :1, :2, :3, :4, :5, :6, :7, :8, :9, :10)" 
        else:
            sql = "insert into CMP_LAWSUIT (CREATE_TIME, UPDATE_TIME, COMPANY_NAME, FETCH_URL, ID) \
                   values(SYSDATE, SYSDATE, :1, :2, :3)" 
        # 执行sql语句
        #print u"sql: %s" %(sql) 
      
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

    def onepage_lawsuit_detail(self, detail_link):
        browser = self.browser
        # 打开详情链接
        ActionChains(browser).key_down(Keys.CONTROL).send_keys("t").key_up(Keys.CONTROL).perform()
        browser.switch_to_window(browser.window_handles[-1])
        try:
            browser.get(detail_link)
        except:
            browser.execute_script('window.stop()')
        page_source = browser.page_source
        p = re.compile(ur"(?:.*)tyc-404.jpg(?:.*)")
        m = p.search(page_source)
        content = ""
        if m:
            print u"页面报404错误 %s" % detail_link
        else:
            # 获取指定源码
            #element = self.find_element_by_xpath('//div[@class="lawsuitbox "]')
            #element = self.find_element_by_xpath('//div[@class="lawsuit mr15 b-c-white pt50 pb50 pr40 pl40 position-rel"]') #20170921 变更 by ake
            element = self.find_element_by_xpath('//div[@class="lawsuit mr15 pl25 pr25 b-c-white position-rel"]') #20170929 变更 by ake
            
            content = element.get_attribute('innerHTML')
            print u"已获取源码 %s" % detail_link

        # 关闭标签页
        browser.close()
        browser.switch_to_window(browser.window_handles[-1])
        return content

    def onepage_data(self, company_name, company_link):
        """
        一行提交一次
        """
        #browser = self.browser
        if self.isElementExist('//div[@id="_container_lawsuit"]'):
            elements = self.find_elements_by_xpath(
                '//div[@id="_container_lawsuit"]//table[@class="table  companyInfo-table"]/tbody/tr')
            for i in range(len(elements)):
                # 第 i 行
                #curDate = time.strftime("%Y%m%d%H%M%S")  # 当前日期
                line_data = [company_name, company_link]
                elt = elements[i]
                line = elt.find_elements_by_tag_name("td")
                for j in range(len(line)):
                    if j == 1:
                        data = line[j].text
                        url = line[j].find_element_by_tag_name(
                            "a").get_attribute("href")
                        line_data.extend([data, url])
                    else:
                        data = line[j].text
                        line_data.append(data)
                # 增加字段，content
                content = self.onepage_lawsuit_detail(url)
                line_data.append(content)
                # 一行提交一次
                id = self.getUUID()
                line_data.append(id)                
                #line_data = self.trans_encode(line_data)  # 转成utf-8编码
                line_data = tuple(line_data)  # 转成元组数据类型
                self.insert_db(line_data, isexistdata="yes")
                time.sleep(2)
        else:  # 不存在该字段
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
username = "18064063503"  # 第一个参数为用户名
password = "wzswjmm123"  # 第二个参数为密码
win = Lawsuit(username, password)
win.login()

win.turnhandle()
#%%
#==============================================================================
#                               法律诉讼详情
#==============================================================================
#filePath = u"1000家企业.xlsx"
filePath = u"otherCompany.xlsx"
field = "lawsuit"
win.fetch(filePath, field)
