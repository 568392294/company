# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 09:19:31 2017

法院公告列表和详情


@author: Administrator
"""
#%%
import time
import MySQLdb
from selenium.webdriver.common.action_chains import ActionChains
from util import mysql
from base import Tianyan
import json
class CourtAnn(Tianyan):
    
    def insert_db(self, line, isexistdata="yes"):
        # SQL 插入语句
        if isexistdata == "yes":
            sql = "insert into cmp_court_announcement(create_time, update_time, company_name, fetch_url, \
                   announcement_date, prosecution, appellee, announcement_type, \
                   announce_id, court, content, content_json)  \
                   values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        else:
            sql = "insert into cmp_court_announcement(create_time, update_time, company_name, fetch_url) \
                   values(%s, %s, %s, %s)"
        # 执行sql语句
        result = mysql.execute(sql, line)
        print result
        
    def trans_encode(self,alist):
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

    def onepage_court_detail(self, line, j):
        browser = self.browser
        #弹出页面源码部分
        while not self.isElementExist('//div[@id="_modal_container"]'):#若不存在，重复点击
            #点击详情
            line[j].find_elements_by_tag_name("span")[-1].click()
            browser.implicitly_wait(5)
        #若弹窗存在， 判断是否为所取行的详情弹窗页面   
        condition = [line[0].text, line[1].text, line[2].text]
        small_window_1 = browser.find_element_by_xpath('//p[@ng-if="items.publishdate"]').text.split(u"：")[1]
        small_window_2 = browser.find_element_by_xpath('//span[@ng-bind-html="items.party1 | trustHtml"]').text
        small_window_3 = browser.find_element_by_xpath('//span[@ng-bind-html="items.party2 | trustHtml"]').text
        small_window = [small_window_1, small_window_2, small_window_3]
        while condition != small_window:
            #不符合条件，先关闭弹窗
            browser.find_element_by_xpath('//div[@id="_modal_container"]//i[@class="tic tic-close"]').click()
            #点击详情
            line[j].find_elements_by_tag_name("span")[-1].click()
            browser.implicitly_wait(5)
            #重新获取判断条件
            small_window_1 = browser.find_element_by_xpath('//p[@ng-if="items.publishdate"]').text.split(u"：")[1]
            small_window_2 = browser.find_element_by_xpath('//span[@ng-bind-html="items.party1 | trustHtml"]').text
            small_window_3 = browser.find_element_by_xpath('//span[@ng-bind-html="items.party2 | trustHtml"]').text
            small_window = [small_window_1, small_window_2, small_window_3]
        #保存源码
        option = browser.find_element_by_xpath('//div[@id="_modal_container"]')
        InnerElement = option.get_attribute('innerHTML')
        print u"获得数据 %s" % small_window[2]
        #关闭详情弹窗
        close = browser.find_element_by_xpath('//div[@id="_modal_container"]//i[@class="tic tic-close"]')
        ActionChains(browser).move_to_element(close).click(close).perform()
        browser.implicitly_wait(5)
        return InnerElement    
   
    def onepage_data(self, company_name, company_link):
        """
        一行提交一次
        """
        browser = self.browser
        if self.isElementExist('//div[@id="_container_court"]'):
            elements = browser.find_elements_by_xpath('//div[@id="_container_court"]//table[@class="table  companyInfo-table"]/tbody/tr')
            for i in range(len(elements)):
                #第 i 行
                curDate = time.strftime("%Y%m%d%H%M%S")#当前日期
                line_data = [curDate, curDate, company_name, company_link]
                elt = elements[i]
                line = elt.find_elements_by_tag_name("td")
                for j in range(len(line)):
                    if j == 5: 
                        data = self.onepage_court_detail(line,j)
                    else:
                        data = line[j].text
                    line_data.append(data)
                #增加字段，content_json
                originstr = line[5].find_element_by_tag_name("span").get_attribute("onclick")
                start = originstr.find('(') + 1
                end = len(originstr) - 1
                content_json = originstr[start:end]
                line_data.append(content_json)
                #增加字段, announce_id
                d = json.loads(content_json)
                announce_id = d[u"announce_id"]
                line_data.insert(8, announce_id)
                #一行提交一次
                line_data = self.trans_encode(line_data) #转成utf-8编码
                line_data = tuple(line_data)             #转成元组数据类型
                self.insert_db(line_data, isexistdata = "yes") 
                print u"等待2秒"
                time.sleep(2)
        else:#不存在法院公告字段
            curDate = time.strftime("%Y%m%d%H%M%S")#当前日期
            line_data = [curDate, curDate, company_name, company_link]
            line_data = self.trans_encode(line_data) #转成utf-8编码
            line_data = tuple(line_data)             #转成元组数据类型
            self.insert_db(line_data, isexistdata = "no")   

    def get_total_page_count(self, total_page_count):

        if total_page_count > 20 :
            return 20
        return total_page_count            
            
#%%                              
#==============================================================================
#                               登录
#==============================================================================
username = "15623247485"   #第一个参数为用户名
password = "123456abc"   #第二个参数为密码
win = CourtAnn(username, password) 
win.login()   

win.turnhandle()
#%%
#==============================================================================
#                               法院公告详情
#==============================================================================
filePath = u"1000家企业.xlsx" 
field = "court"
win.fetch(filePath, field);
