# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 09:22:02 2017

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
            sql = "insert into \"cmp_hearing_announcement\" (\"create_time\", \"update_time\", \"company_name\", \"fetch_url\", \
                   \"announcement_date\", \"cause\", \"accuser\", \"appellee\", \"announce_id\", \"content\", \"id\")  \
                   values(SYSDATE, SYSDATE, :1, :2, :3, :4, :5, :6, :7, :8, :9)"
        else:
            sql = "insert into \"cmp_hearing_announcement\" (\"create_time\", \"update_time\", \"company_name\", \"fetch_url\", \"id\") \
                   values(SYSDATE, SYSDATE, :1, :2, :3)"
        # 执行sql语句
        #print u"sql: %s" %(sql) 
        #print line
        result = oracle.execute(sql, line)
        print result
        
    def onepage_notice_detail(self, line, j):
        browser = self.browser
#    def onepage_notice_detail(line, j):
        #弹出页面源码部分，若弹窗不存在，重复点击至出现
        iselementexist = self.find_element_by_xpath('//div[@id="ktnoticeModal"]').get_attribute("aria-hidden")
        while iselementexist == u"true":#
            #点击详情
            line[j].find_element_by_tag_name("a").click()
            browser.implicitly_wait(30)
            iselementexist = self.find_element_by_xpath('//div[@id="ktnoticeModal"]').get_attribute("aria-hidden")
        time.sleep(2)
        #若弹窗存在， 判断——是否为所取行的详情弹窗页面 / 无数据  
        if self.isElementExist('//div[@id="ktnoticeModal"]//table[@class="table table-bordered"]'):
            window_elements = self.find_elements_by_xpath('//div[@id="ktnoticeModal"]//table[@class="table table-bordered"]//td')
            browser.implicitly_wait(30)
            small_window_2 = window_elements[1].text
            browser.implicitly_wait(30)
            # condition = [line[1].text, line[2].text, line[3].text]
            # window_elements = self.find_elements_by_xpath('//div[@id="ktnoticeModal"]//table[@class="table table-bordered"]//td')
            # small_window_1 = window_elements[5].text
            # small_window_2 = window_elements[1].text
            # small_window_3 = window_elements[15].text
            # small_window = [small_window_1, small_window_2, small_window_3]
            # while condition != small_window:
            #     #不符合条件，先关闭弹窗
            #     ActionChains(browser).key_down(Keys.CONTROL).send_keys(Keys.ESCAPE).key_up(Keys.CONTROL).perform()
            #     browser.implicitly_wait(30)
            #     #点击详情
            #     line[j].find_element_by_tag_name("a").click()
            #     browser.implicitly_wait(30)
            #     #重新获取判断条件
            #     elements = self.find_elements_by_xpath('//div[@id="ktnoticeModal"]//table[@class="table table-bordered"]//td')
            #     small_window_1 = elements[5].text
            #     small_window_2 = elements[1].text
            #     small_window_3 = elements[15].text
            #     small_window = [small_window_1, small_window_2, small_window_3]
        else:
            small_window_2 = None
            print u"表格为空，无详情数据"                
    
        #保存源码和案号
        option = self.find_element_by_xpath('//div[@id="ktnoticeModal"]//div[@class="modal-content"]')
        InnerElement = option.get_attribute('innerHTML')
        print u"获得数据 %s" % small_window_2
        #关闭详情弹窗
        # while self.isElementExist('//div[@id="ktnoticeModal"]//table[@class="table table-bordered"]'):
        ActionChains(browser).key_down(Keys.CONTROL).send_keys(Keys.ESCAPE).key_up(Keys.CONTROL).perform()
        browser.implicitly_wait(30)
        return InnerElement

    def onepage_data(self, company_name, company_link):
       
        """
        一行提交一次
        """
        #browser = self.browser
        if self.isElementExist('//section[@id="noticelist"]'):
            elements = self.find_elements_by_xpath('//section[@id="noticelist"]//table[@class="m_changeList"]/tbody/tr')
            for i in range(1,len(elements)): #第一个元素为列名
                if i == 0:
                    continue
                #第 i 行
                #curDate = time.strftime("%Y%m%d%H%M%S")#当前日期
                #line_data = [curDate, curDate, company_name, company_link]
                line_data = [company_name, company_link]
                elt = elements[i]#第 i 行
                line = elt.find_elements_by_tag_name("td")
                #获取所有字段数据
                for j in range(len(line)):
                    if j==0: 
                        continue
                    elif j==5:
                        #annouce_id
                        originstr = line[j].find_element_by_tag_name("a").get_attribute("onclick")
                        start = originstr.find('(') + 1
                        end = len(originstr) - 1
                        annouce_id = originstr[start:end]
                        #content
                        content = self.onepage_notice_detail(line, j)
                        line_data.extend([annouce_id, content])
                    else:
                        data = line[j].text  
                        line_data.append(data)
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
            #line_data = [curDate, curDate, company_name, company_link]
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
#                               企查查开庭公告详情
#==============================================================================
filePath = u"1000家企业qcc.xlsx" 
field = "notice"
win.fetch(filePath, field);
