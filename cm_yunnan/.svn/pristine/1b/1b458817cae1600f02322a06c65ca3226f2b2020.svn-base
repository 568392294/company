# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 16:10:43 2017

招投标
@author: Administrator
"""
#%%
import time
import MySQLdb
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from util import mysql
from base import Tianyan

class Bid(Tianyan):
    
    def insert_db(self, line, isexistdata="yes"):
        # SQL 插入语句
        if isexistdata == "yes":
            sql = "insert into cmp_bid(create_time, update_time, company_name, fetch_url, \
                   publish_date, title, url, purchaser, content, unique_key) \
                   values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        else:
            sql = "insert into cmp_bid(create_time, update_time, company_name, fetch_url) \
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
    
    def onepage_bid_detail(self, detail_link):
        browser = self.browser
        #打开详情链接
        ActionChains(browser).key_down(Keys.CONTROL).send_keys("t").key_up(Keys.CONTROL).perform()
        browser.switch_to_window(browser.window_handles[-1])
        try:  
            browser.get(detail_link)            
        except:  
            browser.execute_script('window.stop()')
        
        #获取指定源码
        element = browser.find_element_by_xpath('//div[@class="lawsuitbox"]')
        content = element.get_attribute('innerHTML')
        print u"已获取源码 %s" % detail_link
                
        # 关闭标签页
        while browser.current_url == detail_link:
            browser.close()
            browser.switch_to_window(browser.window_handles[-1]) 
        return content
        
        
    def onepage_data(self, company_name, company_link):
        """
        一行提交一次
        """
        browser = self.browser
        if self.isElementExist('//div[@id="_container_bid"]'):
            elements = browser.find_elements_by_xpath('//div[@id="_container_bid"]//table[@class="table  companyInfo-table"]/tbody/tr')
            for i in range(len(elements)):
                #第 i 行
                curDate = time.strftime("%Y%m%d%H%M%S")#当前日期
                line_data = [curDate, curDate, company_name, company_link]
                elt = elements[i]
                line = elt.find_elements_by_tag_name("td")
                for j in range(len(line)):
                    if j == 1:
                        data = line[j].text
                        url = line[j].find_element_by_tag_name("a").get_attribute("href")
                        line_data.extend([data, url])
                    else:
                        data = line[j].text
                        line_data.append(data)
                #增加字段，content
                content = self.onepage_bid_detail(url)
                line_data.append(content)
                #生成加密键值
                comb = company_name + line_data[4] + line_data[5] + line_data[7]
                unique_key = self.md5(comb.encode('utf-8'))
                line_data.append(unique_key)
                #一行提交一次
                line_data = self.trans_encode(line_data) #转成utf-8编码
                line_data = tuple(line_data)             #转成元组数据类型
                self.insert_db(line_data, isexistdata = "yes") 
                print u"等待2秒"
                time.sleep(2)
        else: #不存在商标字段
            curDate = time.strftime("%Y%m%d%H%M%S")#当前日期
            line_data = [curDate, curDate, company_name, company_link]
            line_data = self.trans_encode(line_data) #转成utf-8编码
            line_data = tuple(line_data)             #转成元组数据类型
            self.insert_db(line_data, isexistdata = "no")   
                
            
#%%                              
#==============================================================================
#                               登录
#==============================================================================
username = "15623247485"   #第一个参数为用户名
password = "123456abc"   #第二个参数为密码
win = Bid(username, password) 
win.login()   

win.turnhandle()
#%%
#==============================================================================
#                               招投标详情
#==============================================================================
filePath = u"1000家企业.xlsx" 
field = "bid"
win.fetch(filePath, field);


    
    


