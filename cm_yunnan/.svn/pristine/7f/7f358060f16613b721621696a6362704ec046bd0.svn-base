# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 13:50:54 2017

@author: Administrator
"""
#%%
#import time
from selenium.webdriver.common.action_chains import ActionChains
from util import oracle
from base import Tianyan



class Patent(Tianyan):
    
    def insert_db(self, line, isexistdata="yes"):
        # SQL 插入语句
        if isexistdata == "yes":
            sql = "insert into CMP_PATENT_TYC (CREATE_TIME, UPDATE_TIME, COMPANY_NAME, FETCH_URL, \
                   APPLICATION_PUBLISH_DATE, PATENT_NAME, APPLICATION_NUMBER, \
                   APPLICATION_PUBLISH_NUMBER, CONTENT, CONTENT_JSON, ID)  \
                   values(SYSDATE, SYSDATE, :1, :2, :3, :4, :5, :6, :7, :8, :9)"
        else:
            sql = "insert into CMP_PATENT_TYC (CREATE_TIME, UPDATE_TIME, COMPANY_NAME, FETCH_URL, ID) \
                   values(SYSDATE, SYSDATE, :1, :2, :3)"
        # 执行sql语句
        result = oracle.execute(sql, line)
        print result
        
    def onepage_patent_detail(self, line, k, j):
        browser = self.browser
        softw_name = line[k].find_element_by_tag_name("span").text
        tries = 1 #尝试次数
        while tries<6:#
            if self.isElementExist('//table[@class="table"]'):
                break             
            #点击详情
            line[j].find_elements_by_tag_name("span")[-1].click()
            browser.implicitly_wait(5)
            tries += 1
        if self.isElementExist('//table[@class="table"]'):
            #弹出页面源码部分，若弹窗不存在，重复点击至出现
            #若弹窗存在， 判断是否为所取行的详情弹窗页面   
            # table_name = browser.find_elements_by_xpath('//div[@class="modal-body"]/table[@class="table"]/tbody/tr/td')[3].text
            # while table_name != softw_name:
            #     #不符合条件，先关闭弹窗
            #     browser.find_element_by_xpath('//div[@id="_modal_container"]//i[@class="tic tic-close"]').click()
            #     #点击详情
            #     line[j].find_elements_by_tag_name("span")[-1].click()
            #     browser.implicitly_wait(5)
            #     #重新获取判断条件
            #     table_name = browser.find_elements_by_xpath('//div[@class="modal-body"]/table[@class="table"]/tbody/tr/td')[3].text
            # #保存源码
            option = browser.find_element_by_xpath('//div[@id="_modal_container"]')
            InnerElement = option.get_attribute('innerHTML')
            print u"获得数据 %s" % softw_name
            #关闭详情弹窗
            close = browser.find_element_by_xpath('//div[@ng-click="cancel()"]//i[@class="tic tic-close"]')
            ActionChains(browser).move_to_element(close).click(close).perform()
            browser.implicitly_wait(5)
        else:
            InnerElement = u""
        return InnerElement
                
    def onepage_data(self, company_name, company_link):
        """
        一行提交一次
        """
        browser = self.browser
        if self.isElementExist('//div[@id="_container_patent"]'):
            elements = browser.find_elements_by_xpath('//div[@id="_container_patent"]//table[@class="table  companyInfo-table"]/tbody/tr')
            for i in range(len(elements)):
                #第 i 行
                #curDate = time.strftime("%Y%m%d%H%M%S")#当前日期
                line_data = [company_name, company_link]
                elt = elements[i]#第 i 行
                line = elt.find_elements_by_tag_name("td")
                for j in range(len(line)):
                    if j == 4:
                        data = self.onepage_patent_detail(line, 1, j)
                    else:
                        data = line[j].text
                    line_data.append(data)
                #增加字段,content_json
                originstr = line[4].find_element_by_tag_name("span").get_attribute("onclick")
                start = originstr.find('(') + 1
                end = len(originstr) - 1
                content_json = originstr[start:end]
                line_data.append(content_json)
                #一行提交一次
                id = self.getUUID()
                line_data.append(id)                    
                #line_data = self.trans_encode(line_data) #转成utf-8编码
                line_data = tuple(line_data)             #转成元组数据类型
                self.insert_db(line_data, isexistdata = "yes")   
        else:#不存在专利字段
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
username = "15872735169"   #第一个参数为用户名
password = "L03274824"   #第二个参数为密码
win = Patent(username, password) 
win.login()   

win.turnhandle()
#%%
#==============================================================================
#                               专利详情
#==============================================================================
filePath = u"1000家企业.xlsx"
field = "patent" 
win.fetch(filePath, field);
