# -*- coding: utf-8 -*-
"""
Created on Mon Aug 07 09:53:44 2017


补全红色字段：
注册时间
组织机构代码
工商注册号
统一信用代码
企业类型
纳税人识别号
行业
营业期限
核准日期
登记机关

@author: Administrator
"""
#%%
#import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from util import oracle
from base import Tianyan


class Basicinfo(Tianyan):
    
    def insert_db(self, line, isexistdata="yes"):
        # SQL 插入语句
        sql = "INSERT INTO \"T_CMP_BASICINFO_COPY\" (\"F_CREATE_TIME\", \"F_UPDATE_TIME\", \"F_COMPANY_NAME\", \"F_FETCH_URL\", \
               \"F_PHONE\", \"F_EMAIL\", \"F_WEBSITE\", \"F_COMPANY_ADDRESS\", \
               \"F_REGISTERED_NO\", \"F_ORGANIZATION_CODE\", \"F_UNIFORM_CREDIT_CODE\", \
               \"F_COMPANY_TYPE\", \"F_TAXPAYER_ID\", \"F_INDUSTRY\", \"F_BUSINESS_TERM\", \"F_APPROVED_DATE\", \
               \"F_REGISTRATION_ORGAN\", \"F_REGISTERED_ADDRESS\", \"F_BUSINESS_SCOPE\", \"F_CMP_ID\", \"F_REG_CAPITAL\", \
               \"F_CMP_LR\", \"F_CMP_OPERATING_STATUS\",\"F_CMP_INTRO\",\"F_LISTED\", \"F_ENNAME\",\"F_REG_DATE\") \
               VALUES(SYSDATE, SYSDATE, :1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18, :19, :20, :21, :22, :23, :24, :25)"
        # 执行sql语句
        result = oracle.execute(sql, line)
        print result
  
    def get_12_field(self, company_name):
        print "a"
        browser = self.browser
        #点击经营范围的详细页面
        if browser.find_elements_by_xpath("//a[@class='js-shrink-btn ']") != []:
            browser.find_element_by_xpath("//a[@class='js-shrink-btn ']").click()
        #获取各个字段
        fieldDic = {}
        
        # ake 20171103 注释。原因：页面改版
        #options = browser.find_elements_by_xpath("//table[@style='border:none']//td[@class='basic-td']")
        #for option in options:
        #    print option.text
        #    a = option.text
        #    b = a.split(u"：")
        #    field_name = b[0]
        #    field_data = b[1]
        #    fieldDic[field_name] = field_data               
        options = browser.find_elements_by_xpath("//div[@class='base0910']//tbody//td")
        for index in range(len(options)):
            print "index:%d,text:%s" %(index, options[index].text)
            if index < 5:
                if index % 2 != 0:   
                    field_name = options[index-1].text
                    field_data = options[index].text
                    fieldDic[field_name] = field_data        
            else: 
                if index % 2 == 0:
                    field_name = options[index-1].text
                    field_data = options[index].text
                    fieldDic[field_name] = field_data        
        #time
        timeElement = "//div[@class='baseinfo-module-content-value']"
        if self.isElementExist(timeElement):
            reg_capital = browser.find_elements_by_xpath(timeElement)[0].text
            regis_date = browser.find_elements_by_xpath(timeElement)[1].text
            print u'注册资本：%s' % reg_capital
            fieldDic[u"注册资本"] = reg_capital
            fieldDic[u"注册时间"] = regis_date
            fieldDic[u"公司名"] = company_name
            print u"%s 工商注册号等信息获取成功" % company_name
            
        operatingElement = "//div[@class='baseinfo-module-content-value statusType1']"
        if self.isElementExist(operatingElement):
            operating_status = browser.find_elements_by_xpath(operatingElement)[0].text
            print u'企业状态：%s' % operating_status
            fieldDic[u"企业状态"] = operating_status            
            
        humanElement = "//div[@class='baseInfo_model2017']//div[@class='f18 overflow-width sec-c3']/a"
        if self.isElementExist(humanElement):
            human = browser.find_elements_by_xpath(humanElement)[0].text
            print u'企业法人：%s' % human
            fieldDic[u"企业法人"] = human
        
        return fieldDic

    def get_4_field(self, company_name):
        print "b"
        fieldDic = {}
        browser = self.browser
        
        # ake 20171103 注释。原因：页面改版
        #if browser.find_elements_by_xpath("//div[@class='f14 new-c3 mt10']") != []:
        #    #获取各个字段
        #    options = browser.find_elements_by_xpath("//div[@class='f14 new-c3 mt10']/div")
        #    for option in options:
        #        a = option.text
        #        b = a.split(u"：")
        #        field_name = b[0]
        #        field_data = b[1]
        #        fieldDic[field_name] = field_data  
        #    options = browser.find_elements_by_xpath("//div[@class='f14 new-c3']/div")
        #    for option in options:
        #        a = option.text
        #        b = a.split(u"：")
        #        field_name = b[0]
        #        field_data = b[1]
        #        fieldDic[field_name] = field_data  
        #    print u"%s 电话网址邮箱地址获取成功" % company_name
        
        if browser.find_elements_by_xpath("//div[@class='company_header_width ie9Style']//div[@class='f14 sec-c2 mt10']") != []:
            #获取各个字段
            options = browser.find_elements_by_xpath("//div[@class='company_header_width ie9Style']//div[@class='f14 sec-c2 mt10']/div")        
            for option in options:
                a = option.text
                b = a.split(u"：")
                field_name = b[0]
                field_data = b[1]
                fieldDic[field_name] = field_data  
            options = browser.find_elements_by_xpath("//div[@class='company_header_width ie9Style']//div[@class='f14 sec-c2']/div")
            for option in options:
                a = option.text
                b = a.split(u"：")
                field_name = b[0]
                field_data = b[1]
                fieldDic[field_name] = field_data  
            print u"%s 电话网址邮箱地址获取成功" % company_name   
        
        introElement = "//script[@id='company_base_info_detail']"
        if self.isElementExist(introElement):
            intro = browser.find_elements_by_xpath(introElement)[0].text
            print u'企业简介：%s' % intro
            fieldDic[u"企业简介"] = intro
            
        listedElement = "//div[@class='company_header_width ie9Style']//span[@class='border-radio2 f12 pl8 pr8 pt3 pb3 company-tag mr5']"
        if self.isElementExist(listedElement):
            options = browser.find_elements_by_xpath(listedElement+"/span")
            listed = ""
            for option in options:
                listed = listed + " " + option.text
            print u'上市信息：%s' % listed
            fieldDic[u"上市信息"] = listed            
        
        return fieldDic
    
    def get_onecomp(self, field, comp_name, comp_link, i):
        print (u"basicinfo get_onecomp")
        browser = self.browser
        #新建标签页
        ActionChains(browser).key_down(Keys.CONTROL).send_keys("t").key_up(Keys.CONTROL).perform()
        browser.switch_to_window(browser.window_handles[-1])
        browser.get(comp_link)
        #获取数据
        print "begin fetch"
        data1 = self.get_12_field(comp_name)
        data2 = self.get_4_field(comp_name)
        dictMerged = data1.copy()
        dictMerged.update(data2)
        print "end fetch"
        
        if len(dictMerged) > 0:
            #curDate = time.strftime("%Y%m%d%H%M%S")#当前日期
            line_data = [comp_name, comp_link]
            line_data.append(dictMerged[u"电话"] if dictMerged.has_key(u"电话") else "")
            line_data.append(dictMerged[u"邮箱"] if dictMerged.has_key(u"邮箱") else "")
            line_data.append(dictMerged[u"网址"] if dictMerged.has_key(u"网址") else "")
            line_data.append(dictMerged[u"地址"] if dictMerged.has_key(u"地址") else "")
            line_data.append(dictMerged[u"工商注册号"] if dictMerged.has_key(u"工商注册号") else "")
            line_data.append(dictMerged[u"组织机构代码"] if dictMerged.has_key(u"组织机构代码") else "")
            line_data.append(dictMerged[u"统一信用代码"] if dictMerged.has_key(u"统一信用代码") else "")
            line_data.append(dictMerged[u"企业类型"] if dictMerged.has_key(u"企业类型") else "")
            line_data.append(dictMerged[u"纳税人识别号"] if dictMerged.has_key(u"纳税人识别号") else "")
            line_data.append(dictMerged[u"行业"] if dictMerged.has_key(u"行业") else "")
            line_data.append(dictMerged[u"营业期限"] if dictMerged.has_key(u"营业期限") else "")
            line_data.append(dictMerged[u"核准日期"] if dictMerged.has_key(u"核准日期") else "")
            line_data.append(dictMerged[u"登记机关"] if dictMerged.has_key(u"登记机关") else "")
            line_data.append(dictMerged[u"注册地址"] if dictMerged.has_key(u"注册地址") else "")
            line_data.append(dictMerged[u"经营范围"] if dictMerged.has_key(u"经营范围") else "")
            id = self.getUUID()
            line_data.append(id)    
            line_data.append(dictMerged[u"注册资本"] if dictMerged.has_key(u"注册资本") else "")
            line_data.append(dictMerged[u"企业法人"] if dictMerged.has_key(u"企业法人") else "")
            line_data.append(dictMerged[u"企业状态"] if dictMerged.has_key(u"企业状态") else "")
            line_data.append(dictMerged[u"企业简介"] if dictMerged.has_key(u"企业简介") else "")
            line_data.append(dictMerged[u"上市信息"] if dictMerged.has_key(u"上市信息") else "")
            line_data.append(dictMerged[u"英文名称"] if dictMerged.has_key(u"英文名称") else "")
            line_data.append(dictMerged[u"注册时间"] if dictMerged.has_key(u"注册时间") else "")
            self.insert_db(line_data)
        
        #for key in dictMerged:
        #    print "%s:%s" %(key,dictMerged[key])
        
        # 关闭标签页
        # ActionChains(browser).key_down(Keys.CONTROL).send_keys("w").key_up(Keys.CONTROL).perform()
        browser.close()
        browser.switch_to_window(browser.window_handles[-1])
        
        #return dictMerged 
       
#%%                              
#==============================================================================
#                               登录
#==============================================================================
username = "15623247485"   #第一个参数为用户名
password = "123456abc"   #第二个参数为密码
win = Basicinfo(username, password) 
win.login()
win.turnhandle()

#%%
#==============================================================================
#                               基本信息块
#==============================================================================
filePath = u"T_CMP_BASICINFO.xlsx" 
field = "basicinfo"
win.fetch(filePath, field);






