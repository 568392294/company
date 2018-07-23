# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 09:09:53 2017

@author: Administrator
"""


#%%
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from util import oracle
from base import Qcc

import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'



class Patent(Qcc):
    
    def insert_db(self, line, isexistdata="yes"):
        # SQL 插入语句
        if isexistdata == "yes":
            sql = "insert into CMP_PATENT_QCC (CREATE_TIME, UPDATE_TIME, COMPANY_NAME, FETCH_URL, \
                   APPLICATION_PUBLISH_DATE, PATENT_NAME, PATENT_TYPE, APPLICATION_NUMBER, \
                   APPLICATION_PUBLISH_NUMBER, STATUS, CONTENT, ID)  \
                   values(SYSDATE, SYSDATE, :1, :2, :3, :4, :5, :6, :7, :8, :9, :10)"
        else:
            sql = "insert into CMP_PATENT_QCC (CREATE_TIME, UPDATE_TIME, COMPANY_NAME, FETCH_URL, ID) \
                   values(SYSDATE, SYSDATE, :1, :2, :3)"
        # 执行sql语句
        result = oracle.execute(sql, line)
        print result
        
    def onepage_patent_detail(self, line, j):
        browser = self.browser
        softw_name = line[2].text 
        #弹出页面源码部分，若弹窗不存在，重复点击至出现
        iselementexist = browser.find_element_by_xpath('//div[@id="zlModal"]').get_attribute("aria-hidden")
        while iselementexist == u"true":#
            #点击详情
            line[j].find_element_by_tag_name("a").click()
            browser.implicitly_wait(30)
            iselementexist = browser.find_element_by_xpath('//div[@id="zlModal"]').get_attribute("aria-hidden")
        #若弹窗存在， 判断是否为所取行的详情弹窗页面   
        table_name = browser.find_elements_by_xpath('//div[@id="zlModal"]//table[@class="table table-bordered"]//td')[3].text
        while table_name != softw_name:
            #不符合条件，先关闭弹窗
            ActionChains(browser).key_down(Keys.CONTROL).send_keys(Keys.ESCAPE).key_up(Keys.CONTROL).perform()
            browser.implicitly_wait(30)
            #点击详情
            line[j].find_element_by_tag_name("a").click()
            browser.implicitly_wait(30)
            #重新获取判断条件
            table_name = browser.find_elements_by_xpath('//div[@id="zlModal"]//table[@class="table table-bordered"]//td')[3].text
            time.sleep(5)    
        #保存源码
        option = browser.find_element_by_xpath('//div[@id="zlModal"]//div[@class="modal-content"]')
        InnerElement = option.get_attribute('innerHTML')
        print u"获得数据 %s" % softw_name
        #六个字段：名称(above) 申请号 申请公布号 申请公布日 专利类型 法律状态
        table_fields = browser.find_elements_by_xpath('//div[@id="zlModal"]//table[@class="table table-bordered"]//td')
        patent_name = table_fields[1].text
        anumber = table_fields[3].text
        apnumber = table_fields[7].text
        apdate = table_fields[9].text
        ptype = table_fields[13].text
        status = table_fields[17].text
        #关闭详情弹窗
        for i in range(4):
            ActionChains(browser).key_down(Keys.CONTROL).send_keys(Keys.ESCAPE).key_up(Keys.CONTROL).perform()
            browser.implicitly_wait(30)
            # print u"第%s次关闭弹窗" % i
        return [apdate, patent_name, ptype, anumber, apnumber, status, InnerElement]
    
    def onepage_data(self, company_name, company_link):
        """
        一行提交一次
        """
        browser = self.browser
        if self.isElementExist('//section[@id="zhuanlilist"]'):
            elements = browser.find_elements_by_xpath('//section[@id="zhuanlilist"]//table[@class="m_changeList"]/tbody/tr')
            for i in range(1,len(elements)): #第一个元素为列名
                if i == 0:
                    continue
                #第 i 行
                #curDate = time.strftime("%Y%m%d%H%M%S")#当前日期
                line_data = [company_name, company_link]
                elt = elements[i]#第 i 行
                line = elt.find_elements_by_tag_name("td")
                #获取所有字段数据
                x = 0
                while x < 10:
                    try:
                        line_data.extend(self.onepage_patent_detail(line, 4))
                        break
                    except:
                        x += 1
                #一行提交一次
                id = self.getUUID()
                line_data.append(id)                
                #line_data = self.trans_encode(line_data) #转成utf-8编码
                line_data = tuple(line_data)             #转成元组数据类型
                self.insert_db(line_data, isexistdata = "yes")  
                print u"等待2秒"
                time.sleep(2)
        else:#不存在该字段
            #curDate = time.strftime("%Y%m%d%H%M%S")#当前日期
            line_data = [company_name, company_link]
            id = self.getUUID()
            line_data.append(id)
            #line_data = self.trans_encode(line_data) #转成utf-8编码
            line_data = tuple(line_data)             #转成元组数据类型
            #self.insert_db(line_data, isexistdata = "no")   
#        return line_data
            
            
#%%                              
#==============================================================================
#                               登录
#==============================================================================
username = "18064063503"   #第一个参数为用户名
password = "wzswjmm123"   #第二个参数为密码
win = Patent(username, password) 
win.login()   

win.turnhandle()
#%%
#==============================================================================
#                               企查查专利详情
#==============================================================================
filePath = u"1000家企业qcc.xlsx" 
field = "zhuanli"
win.fetch(filePath, field);
