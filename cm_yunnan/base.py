# -*- coding: utf-8 -*-
"""
Created on Mon Aug 07 10:00:27 2017

@author: Administrator
"""
#%%
import re
import traceback
import pandas as pd
import MySQLdb
import hashlib
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, NoSuchWindowException
import time
import uuid


class Qcc():

    def __init__(self, username, password):
        self.username = username
        self.password = password

        # 设置浏览器
#        self.baseurl = "https://www.tianyancha.com/login"
#        self.browser = webdriver.Firefox()
        self.ip_port = {'ip': ["111.62.251.107", "183.136.218.253", "182.16.69.196", "111.13.7.121", "183.169.128.30", "111.13.7.119", "124.165.252.72", "47.89.22.200", "111.13.7.123", "125.77.25.116", "120.199.224.78", "219.239.142.253", "61.136.163.245", "121.248.112.20", "125.77.25.124"],
                        'port': [8080, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 3128, 3128, 3128, 80]}
        self.baseurl = "http://www.qichacha.com/user_login"

        #number = np.random.randint(1, 15)
        profile = webdriver.FirefoxProfile()
        #profile.set_preference('network.proxy.type', 1)
        #profile.set_preference('network.proxy.http', self.ip_port['ip'][number])  # '183.222.102.104'
        #profile.set_preference('network.proxy.http_port', self.ip_port['port'][number])  # int  8080
        profile.update_preferences()
        self.browser = webdriver.Firefox(firefox_profile=profile)  # 火狐浏览器
        self.browser.get(self.baseurl)
        self.browser.set_page_load_timeout(120)
        self.browser.set_script_timeout(60)

        # 初始化数据库
        # self.db = MySQLdb.connect(
        #        host='172.16.50.100',
        #        port = 3306,
        #        user = 'zrpd',
        #        passwd = 'zrpd@123',
        #        db = 'china_merchants')
        # self.db.set_character_set('utf8')
        # self.cursor = self.db.cursor()
    
    def login(self):
        browser = self.browser
        try:
            browser.get(self.baseurl)
        except:
            browser.execute_script('window.stop()')
        while True:
            if self.isElementExist("//div[@id='normalLogin']"):
                browser.find_element_by_id("normalLogin").click()
                break
            else:
                time.sleep(5)
                continue
        account = {'user': self.username, 'password': self.password}
        option1 = self.find_elements_by_xpath('//input[@class="form-control input-lg"]')[0]
        option2 = self.find_elements_by_xpath('//input[@class="form-control input-lg"]')[1]
        # option3 = self.find_element_by_xpath('//button[@class="btn btn-primary     m-t-n-xs btn-block btn-lg font-15"]')
        option1.send_keys(account['user'])
        option2.send_keys(account['password'])
        browser.implicitly_wait(30)
        order = raw_input(u"请完成滑动滑块的动作后，手动点击登录，按任意键+回车后继续运行".encode("gbk"))
        print u"登陆成功，最大化"
        # 最大化
        browser.maximize_window()
        # 去广告
        try:
            self.find_element_by_xpath(
                "//div[@class='closeSuspend']").click()
            browser.implicitly_wait(30)
        except:
            print u"请手动去除广告！"
            
    def getUUID(self):
        uid = str(uuid.uuid1())
        return uid.replace('-','')

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
            #elif i == 0 or i == 1:
                #result.append(int(l))
            else:
                #l = MySQLdb.escape_string(l)
                result.append(l)
        return result

    def isElementExist(self, element):
        flag = True
        try:
            browser = self.browser
            browser.find_element_by_xpath(element)
            return flag
        except:
            flag = False
            return flag
   
    def find_elements_by_xpath(self, xpath):
        browser = self.browser
        max_retry = 5
        cur_retry_num = 1
        while cur_retry_num <= max_retry:
            try:
                return browser.find_elements_by_xpath(xpath)
            except StaleElementReferenceException:
                print u"页面元素没有找到，进行第%d重试" % (cur_retry_num)
                browser.implicitly_wait(3)
            finally:
                cur_retry_num += 1

    def find_element_by_xpath(self, xpath):
        browser = self.browser
        max_retry = 5
        cur_retry_num = 1
        while cur_retry_num <= max_retry:
            try:
                return browser.find_element_by_xpath(xpath)
            except StaleElementReferenceException:
                print u"页面元素没有找到，进行第%d重试" % (cur_retry_num)
                browser.implicitly_wait(3)
            finally:
                cur_retry_num += 1            

    def skip(self, title_str, skip_str):
        browser = self.browser
        # 跳转至知识产权/法律诉讼页面
        button = browser.find_element_by_id(title_str)
        while button.get_attribute("class") != "current":
            ActionChains(browser).move_to_element(button).click(button).perform()
            print u"鼠标移到%s后休息10s" %title_str
            browser.implicitly_wait(10)
            button = browser.find_element_by_id(title_str)
        title_element = '//a[@onclick="boxScroll(\'#%slist\');"]' % skip_str
        if self.isElementExist(title_element):
            # 跳转至专利信息/开庭公告页面
            option = self.find_element_by_xpath(title_element)
            browser.implicitly_wait(30)
            ActionChains(browser).move_to_element(option).click(option).perform()
            browser.implicitly_wait(30)

    def turnhandle(self):
        browser = self.browser
        browser.switch_to_window(browser.window_handles[-1])

    def turnbutton(self, element):
        flag = False
        try:
            t = element.text
            if t == u">":
                flag = True
            return flag
        except:
            flag = False
            return flag

    def test(self):
        browser = self.browser
        ActionChains(browser).key_down(Keys.CONTROL).send_keys(
            "t").key_up(Keys.CONTROL).perform()
        browser.switch_to_window(browser.window_handles[-1])
        browser.get(
            "http://www.qichacha.com/firm_ab603b8e94724170604c95f2bd3bcc9d.shtml")

    def turnpage(self, field="zhuanli", company_name=u"test", company_link="https://www.tianyancha.com/company/17416832"):
        browser = self.browser
        answer = "continue"
        title_str = ""
        if field == "zhuanli":
            title_str, skip_str = "assets_title", "zhuanli"
        elif field == "notice":
            title_str, skip_str = "susong_title", "notice"

        # 页面跳转
        self.skip(title_str, skip_str)

        # 判断是否存在数据且需要翻页
        if self.isElementExist('//section[@id="%slist"]//ul[@class="pagination pagination-md"]' % field):
            # 需要翻页，先确定翻页按钮
            browser.implicitly_wait(30)
            for i in [-1, -2]:
                button_element = self.find_elements_by_xpath(
                    '//section[@id="%slist"]//ul[@class="pagination pagination-md"]//a' % field)[i]
                if self.turnbutton(button_element):
                    break
            # 总页数
            if i == -2:
                n = self.find_elements_by_xpath(
                    '//section[@id="%slist"]//ul[@class="pagination pagination-md"]//a' % field)[-1].text[3:]
            else:
                n = self.find_elements_by_xpath(
                    '//section[@id="%slist"]//ul[@class="pagination pagination-md"]//a' % field)[-2].text
            print n
            n = int(n)  # 提取页数

            # 先获取第一页的数据
            self.onepage_data(company_name, company_link)
            page_now = self.find_element_by_xpath(
                '//section[@id="%slist"]//ul[@class="pagination pagination-md"]/li[@class="active"]' % field).text
            if page_now == '':
                page_now = '2'
            page_after = page_now
            print u"已提交第 %s 页的数据" % page_now
            while int(page_now) < n:
                needRetry = True
                max_retry = 5
                cur_retry_num = 1
                while needRetry and cur_retry_num <= max_retry:
                    try:
                        # 模拟翻页行为，点击下一页
                        while page_after == page_now:
                            self.find_elements_by_xpath(
                                '//section[@id="%slist"]//ul[@class="pagination pagination-md"]//a' % field)[i].click()
                            time.sleep(10)
                            # 更新页面后重新获取元素
                            page_after = self.find_element_by_xpath(
                                '//section[@id="%slist"]//ul[@class="pagination pagination-md"]/li[@class="active"]' % field).text
                            browser.implicitly_wait(30)
                        print page_now, page_after
                        # 提交该页数据
                        self.onepage_data(company_name, company_link)
                        browser.implicitly_wait(30)
                        # 得到该页的页码
                        page_now = self.find_element_by_xpath(
                            '//section[@id="%slist"]//ul[@class="pagination pagination-md"]/li[@class="active"]' % field).text
                        print page_now
                        print u"已提交第 %s 页的数据" % page_after
                        time.sleep(10)
                        needRetry = False
                    except StaleElementReferenceException:
                        print u"获取第 %s 页的数据出现错误: 页面元素没有找到，进行第%d重试" % (int(page_now) + 1, cur_retry_num)
                    except Exception:
                        browser.implicitly_wait(30)
                        print u"获取第 %s 页的数据出现错误，进行第%d重试" % (int(page_now) + 1, cur_retry_num)
                        print 'traceback.format_exc():\n%s' % traceback.format_exc()
                        # print u"输入任意字符继续获取，输入quit停止采集此公司数据。"
                        # answer = raw_input("go on?")
                        # if answer == "quit":
                        #    break
                        # 提交该页数据
                        # self.onepage_data(company_name, company_link)

                        # 得到该页的页码
                        # page_now = self.find_element_by_xpath('//div[@id="_container_%s"]//li[@class="pagination-page  active "]' % field).text
                        # print u"已提交第 %s 页的数据" % page_now
                        # continue
                    finally:
                        cur_retry_num += 1
                if cur_retry_num >= max_retry:
                    browser.refresh()  # 刷新页面
                    print u"刷新页面"
                    browser.implicitly_wait(30)
                    self.skip(title_str, skip_str)  # 跳转到字段
                    # 跳转到刷新前,需获取的页数前一页
                    page_to_start = int(page_now)
                    page_now = self.find_element_by_xpath(
                        '//section[@id="%slist"]//ul[@class="pagination pagination-md"]/li[@class="active"]' % field).text
                    while int(page_now) < int(page_to_start):
                        # 翻页按钮
                        self.find_elements_by_xpath(
                            '//section[@id="%slist"]//ul[@class="pagination pagination-md"]//a' % field)[i].click()
                        # 重新获取元素
                        browser.implicitly_wait(30)
                        page_now = self.find_element_by_xpath(
                            '//section[@id="%slist"]//ul[@class="pagination pagination-md"]/li[@class="active"]' % field).text
                        browser.implicitly_wait(30)
        elif self.isElementExist('//section[@id="%slist"]' % field):
            # 不需要翻页,存在第一页数据
            print u"不需要翻页,存在第一页数据"
            self.onepage_data(company_name, company_link)
            print u"已提交第 1 页数据"
        else:
            # 无数据
            print u"无数据"
            self.onepage_data(company_name, company_link)
            print u"已提交 空值 "
        return answer

    def get_onecomp(self, company_link, company_name, field):
        """
		  打开新标签页，加载一个公司网址的链接，获取数据后关闭
		  """
        browser = self.browser
        # 新建标签页
        ActionChains(browser).key_down(Keys.CONTROL).send_keys("t").key_up(Keys.CONTROL).perform()
        browser.switch_to_window(browser.window_handles[-1])
        try:
            browser.get(company_link)
            print(u"after open link  sleep 15s")
            browser.implicitly_wait(15)
            #while self.isElementExist('//a[@onclick="boxScroll(\'#noticelist\');"]'):
            #    browser.refresh()
            #    browser.implicitly_wait(30)
        except:
            browser.execute_script('window.stop()')

        # 提交一个公司的所有翻页数据
        result = self.turnpage(field, company_name, company_link)

        # 关闭标签页
        browser.close()
        browser.switch_to_window(browser.window_handles[-1])

        return result

    def fetch(self, filePath, field):
        try:
            # 读取文件，包含相关链接
            link_df = pd.read_excel(filePath)
            # 遍历网址获取数据
            for i in range(len(link_df)):
 #           for i in range(2):
                company_link, company_name, fetched = link_df.link_qcc[
                    i], link_df.name[i], link_df.get(field)[i]
                print(u'第%d个 %s %s 抓取%s：%s' %
                      (i, company_name, company_link, field, fetched))
                if cmp(company_link, u'空') == 0 or cmp(fetched, u'已抓取') == 0:
                    continue
                # 提交一个公司的数据
                result = self.get_onecomp(company_link, company_name, field)
                # 保存文件
                if result != "quit":
                    link_df.loc[i, field] = u"已抓取"
                    link_df.to_excel(filePath)
        except Exception, e:
            print 'str(Exception):\t', str(Exception)
            print 'str(e):\t\t', str(e)
            print 'repr(e):\t', repr(e)
            print 'e.message:\t', e.message
            print 'traceback.print_exc():'
            traceback.print_exc()
            print 'traceback.format_exc():\n%s' % traceback.format_exc()


#%%
class Tianyan():

    def __init__(self, username, password):
        self.username = username
        self.password = password

        # 设置浏览器
#        self.baseurl = "https://www.tianyancha.com/login"
#        self.browser = webdriver.Firefox()
        self.ip_port = {'ip': ["111.62.251.107", "183.136.218.253", "182.16.69.196", "111.13.7.121", "183.169.128.30", "111.13.7.119", "124.165.252.72", "47.89.22.200", "111.13.7.123", "125.77.25.116", "120.199.224.78", "219.239.142.253", "61.136.163.245", "121.248.112.20", "125.77.25.124"],
                        'port': [8080, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 3128, 3128, 3128, 80]}
        self.baseurl = "https://www.tianyancha.com/login"
        number = np.random.randint(1, 15)
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.http', self.ip_port[
                               'ip'][number])  # '183.222.102.104'
        profile.set_preference('network.proxy.http_port', self.ip_port[
                               'port'][number])  # int  8080
        #profile.set_preference("permissions.default.image", 2)
        #profile.set_preference("dom.ipc.plugins.enabled.libflashplayer.so", False)
        profile.update_preferences()
        self.browser = webdriver.Firefox(firefox_profile=profile)  # 火狐浏览器
        self.browser.get(self.baseurl)
        self.browser.set_page_load_timeout(240)
        self.browser.set_script_timeout(60)

        # 初始化数据库
        # self.db = MySQLdb.connect(
        #        host='172.16.50.100',
        #        port = 3306,
        #        user = 'zrpd',
        #        passwd = 'zrpd@123',
        #        db = 'china_merchants')
        # self.db.set_character_set('utf8')
        # self.cursor = self.db.cursor()
        
    def getUUID(self):
        uid = str(uuid.uuid1())
        return uid.replace('-','')        
    
    def load_dict_from_file(self, filepath):
        _dict = {}
        try:
            with open(u"总进度.txt", 'r') as dict_file:
                for line in dict_file:
                    (key, value) = line.strip('\n').split(':')
                    _dict[key] = value
        except IOError as ioerr:
            print u"文件 %s 不存在" % (filepath)
        return _dict

    def save_dict_to_file(self, _dict, filepath):
        try:
            with open(filepath, 'w') as dict_file:
                for (key, value) in _dict.items():
                    dict_file.write('%s:%s\n' % (key, value))
            print u"已保存进度"
        except IOError as ioerr:
            print u"文件 %s 无法创建" % (filepath)

    def md5(self, str):
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()

    def login(self):
        browser = self.browser
        try:
            browser.get(self.baseurl)
        except:
            browser.execute_script('window.stop()')
        account = {'user': self.username, 'password': self.password}
        option1 = self.find_element_by_xpath(
            '//div[@class="modulein modulein1 mobile_box pl30 pr30 f14 collapse in"]//input[@type = "text"]')
        option2 = self.find_element_by_xpath(
            '//div[@class="modulein modulein1 mobile_box pl30 pr30 f14 collapse in"]//input[@type = "password"]')
        option3 = self.find_element_by_xpath(
            '//div[@class="modulein modulein1 mobile_box pl30 pr30 f14 collapse in"]/div[@class="c-white b-c9 pt8 f18 text-center login_btn"]')
        option1.send_keys(account['user'])
        option2.send_keys(account['password'])
        try:
            # 删除广告
            browser.find_element_by_id("bannerClose").click()
            browser.implicitly_wait(5)
            option3.click()
        except:
            browser.execute_script('window.stop()')
        print u"登陆成功，删除广告并最大化，若未删除，请删除后继续运行"
        # 最大化
        browser.maximize_window()

    def isElementExist(self, element):
        flag = True
        try:
            self.find_element_by_xpath(element)
            return flag
        except:
            flag = False
            return flag
        
    def find_elements_by_xpath(self, xpath):
        browser = self.browser
        max_retry = 5
        cur_retry_num = 1
        while cur_retry_num <= max_retry:
            try:
                return browser.find_elements_by_xpath(xpath)
            except StaleElementReferenceException:
                print u"页面元素没有找到，进行第%d重试" % (cur_retry_num)
                browser.implicitly_wait(3)
            finally:
                cur_retry_num += 1

    def find_element_by_xpath(self, xpath):
        browser = self.browser
        max_retry = 5
        cur_retry_num = 1
        while cur_retry_num <= max_retry:
            try:
                return browser.find_element_by_xpath(xpath)
            except StaleElementReferenceException:
                print u"页面元素没有找到，进行第%d重试" % (cur_retry_num)
                browser.implicitly_wait(3)
            finally:
                cur_retry_num += 1                
            
    def skip_field(self, field, title_str, skip_str):
        browser = self.browser
        # 页面跳转至指定字段处
        title = self.find_element_by_xpath(
            '//div[@onclick="goToPage(\'nav-main-%s\')"]' % title_str)
        browser.implicitly_wait(3)
        ActionChains(browser).move_to_element(title).perform()
        # 跳转至视野内
        if field == "dishonest" or field == "zhixing" or field == "seniorPeople":
            skip = self.find_element_by_xpath(
                '//div[@onclick="goToPage(\'nav-main-%s\')"]' % skip_str)
        else:
            skip = self.find_element_by_xpath(
                '//div[@onclick="goToPage(\'nav-main-%sCount\')"]' % skip_str)
        browser.implicitly_wait(10)
        ActionChains(browser).move_to_element(skip).click(skip).perform()
        browser.implicitly_wait(10)
        print u"页面已滑动至指定字段处"

    def skip_page(self, field, filepath):
        browser = self.browser
        progress = self.load_dict_from_file(filepath)
        page_to_start = int(progress[field].split(',')[1])
        print u"从第 %s 页 开始" % (page_to_start + 1)
        # 当前页为
        page_now = self.find_element_by_xpath(
            '//div[@id="_container_%s"]//li[@class="pagination-page  active "]' % field).text
        for i in range(10):
            try:
                # 先每次跳转10页
                tries = (page_to_start - int(page_now)) / 10
                for i in range(tries):
                    self.find_elements_by_xpath(
                        '//div[@id="_container_%s"]//li[@class="pagination-page "]/a' % field)[-1].click()
                    browser.implicitly_wait(30)
                    page_now = self.find_element_by_xpath(
                        '//div[@id="_container_%s"]//li[@class="pagination-page  active "]' % field).text
                    browser.implicitly_wait(30)
                time.sleep(5)
                # 再一页接着一页
                while int(page_now) < int(page_to_start):
                    button = self.find_element_by_xpath(
                        '//div[@id="_container_%s"]//li[@class="pagination-next  "]/a' % field)
                    ActionChains(browser).move_to_element(
                        button).click(button).perform()
                    browser.implicitly_wait(60)
                    page_now = self.find_element_by_xpath(
                        '//div[@id="_container_%s"]//li[@class="pagination-page  active "]' % field).text
                    browser.implicitly_wait(60)
                break
            except:
                print u"重新跳转"
                continue

    def test(self):
        browser = self.browser
        ActionChains(browser).key_down(Keys.CONTROL).send_keys(
            "t").key_up(Keys.CONTROL).perform()
        browser.switch_to_window(browser.window_handles[-1])
        browser.get("https://www.tianyancha.com/company/17416832")

    def turnhandle(self):
        browser = self.browser
        browser.switch_to_window(browser.window_handles[-1])

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
            else:
                l = MySQLdb.escape_string(l)
                result.append(l)
        return result

    def get_total_page_count(self, total_page_count):
        return total_page_count

    def turnpage(self, field="bid", company_name=u"安邦财险", company_link="https://www.tianyancha.com/company/17416832", i=0):
        browser = self.browser
        answer = "continue"
        # 判断是否需要翻页
        print u"判断是否需要翻页"
        ele = '//div[@id="_container_%s"]//div[@class="total"]' % field
        print ele
        if self.isElementExist(ele):
            if field == "copyright":
                title_str, skip_str = "knowledgeProperty", "cpoyR"
            elif field == "tmInfo":
                title_str, skip_str = "knowledgeProperty", "tm"
            elif field == "court":
                title_str, skip_str = "lawDangerous", "court"
            elif field == "bid":
                title_str, skip_str = "manageStatus", "bid"
            elif field == "invest":
                title_str, skip_str = "backgroundItem", "inverst"
            elif field == "bond":
                title_str, skip_str = "manageStatus", "bond"
            elif field == "patent":
                title_str, skip_str = "knowledgeProperty", "patent"
            elif field == "dishonest":
                title_str, skip_str = "lawDangerous", "dishonest"
            elif field == "zhixing":
                title_str, skip_str = "lawDangerous", "zhixing"
            elif field == "taxcredit":
                title_str, skip_str = "manageStatus", "taxCredit"
            elif field == "lawsuit":
                title_str, skip_str = "lawDangerous", "lawsuit"
            elif field == "branch":
                title_str, skip_str = "backgroundItem", "branch"
            elif field == "changeinfo":
                title_str, skip_str = "backgroundItem", "change"
            elif field == "seniorPeople":
                title_str, skip_str = "shangshiitem", "seniorExecutiveNum"
            elif field == "holder":
                title_str, skip_str = "backgroundItem", "holder"
            # 页面跳转至指定字段处
            print u"设置页面跳转至指定字段处"
            self.skip_field(field, title_str, skip_str)
            time.sleep(5)
            # 页面跳转到指定页码处
            self.skip_page(field, u'总进度.txt')

            # 总页数
            n = self.find_element_by_xpath(
                '//div[@id="_container_%s"]//div[@class="total"]' % field).text  # 总页数
            print n
            p = re.compile(ur"共(\d+)页")
            m = p.search(n)
            pageCount = 0
            if m:
                pageCount = int(m.group(1))
            print u"提取分页总数： %d" %pageCount
            #n = int(n.split(" ")[1])  # 提取页数
            total_page_count = self.get_total_page_count(pageCount)
            print u'抓取%d页' % total_page_count
            # 先获取第一页的数据
            for i in range(10):
                try:
                    self.onepage_data(company_name, company_link)
                    break
                except:
                    continue
            page_now = self.find_element_by_xpath('//div[@id="_container_%s"]//li[@class="pagination-page  active "]' % field).text
            print u"已提交第 %s 页的数据" % page_now
            while int(page_now) < total_page_count:
                needRetry = True
                max_retry = 5
                cur_retry_num = 1
                while needRetry and cur_retry_num <= max_retry:
                    print u'当前第%d页' % cur_retry_num
                    try:
                        # 模拟翻页行为，点击下一页
                        print u"current_url: %s。长度：%d" % (browser.current_url,len(browser.current_url))
                        print u"company_link: %s。长度：%d" % (company_link,len(company_link))
                        if cmp(browser.current_url, company_link) != 0:
                            print u"当前页面网址不是公司网址，关闭浏览器标签。"
                            browser.close()
                            browser.switch_to_window(browser.window_handles[-1])
                        page_after = self.find_element_by_xpath('//div[@id="_container_%s"]//li[@class="pagination-page  active "]' % field).text
                        print u'page_after:%s,page_now:%s' %(page_after,page_now)
                        while int(page_after) >= int(page_now) + 2:  
                            print u'翻多了一页,回到视野中页码条的第一个页码'
                            self.find_element_by_xpath('//div[@id="_container_%s"]//li[@class="pagination-prev  "]/a' % field).click()
                            browser.implicitly_wait(30)
                            page_after = self.find_element_by_xpath('//div[@id="_container_%s"]//li[@class="pagination-page  active "]' % field).text
                        skip_page_num = 1
                        while int(page_after) <= int(page_now):
                            print u'没翻过去'
                            self.find_element_by_xpath('//div[@id="_container_%s"]//li[@class="pagination-next  "]/a' % field).click()
                            browser.implicitly_wait(30)
                            page_after = self.find_element_by_xpath('//div[@id="_container_%s"]//li[@class="pagination-page  active "]' % field).text
                            skip_page_num = skip_page_num + 1
                            if skip_page_num > 50:
                                print u'翻页失败次数太多，已超过50次，重新刷新浏览器'
                                browser.refresh()  # 刷新页面
                                time.sleep(60)
                                skip_page_num = 1
                        # 提交该页数据
                        print u'开始获取该页数据'
                        self.onepage_data(company_name, company_link)
                        
                        # 得到该页的页码
                        page_now = self.find_element_by_xpath('//div[@id="_container_%s"]//li[@class="pagination-page  active "]' % field).text
                        print u"已提交第 %s 页的数据" % page_now

                        # 保存执行进度
                        progress = self.load_dict_from_file(u"总进度.txt")  # 字典
                        progress[field] = '%s,%s' % (i, page_now)
                        self.save_dict_to_file(progress, u"总进度.txt")

                        cur_retry_num = 1
                        needRetry = False
                        print u'等待5s再翻下一页'
                        #browser.implicitly_wait(10)
                        time.sleep(5)
                    except StaleElementReferenceException:
                        print u"获取第 %s 页的数据出现错误: 页面元素没有找到，进行第%d重试" % (int(page_now) + 1, cur_retry_num)
                        if cur_retry_num == max_retry:
                            print u"获取第 %s 页的数据出现错误: 页面元素没有找到，已重试%d次，隐式等待30s再继续" % (int(page_now) + 1, cur_retry_num)
                            browser.implicitly_wait(30)
                    except Exception:
                        browser.implicitly_wait(30)
                        print u"获取第 %s 页的数据出现错误，进行第%d重试" % (int(page_now) + 1, cur_retry_num)
                        print 'traceback.format_exc():\n%s' % traceback.format_exc()
                        # print u"输入任意字符继续获取，输入quit停止采集此公司数据。"
                        # answer = raw_input("go on?")
                        # if answer == "quit":
                        #    break
                        # 提交该页数据
                        # self.onepage_data(company_name, company_link)

                        # 得到该页的页码
                        # page_now = self.find_element_by_xpath('//div[@id="_container_%s"]//li[@class="pagination-page  active "]' % field).text
                        # print u"已提交第 %s 页的数据" % page_now
                        # continue
                    finally:
                        cur_retry_num = cur_retry_num + 1
                if cur_retry_num >= max_retry:
                    print u"已达到最大重试次数，刷新页面。cur_retry_num = %d" % (cur_retry_num)
                    browser.refresh()  # 刷新页面
                    browser.implicitly_wait(30)
                    self.skip_field(field, title_str, skip_str)  # 跳转到字段
                    # 跳转到刷新前,需获取的页数前一页
                    page_to_start = int(page_now)
                    page_now = self.find_element_by_xpath(
                        '//div[@id="_container_%s"]//li[@class="pagination-page  active "]' % field).text
                    if page_to_start <= 10:
                        while int(page_now) < int(page_to_start):
                            self.find_element_by_xpath(
                                '//div[@id="_container_%s"]//li[@class="pagination-next  "]/a' % field).click()
                            browser.implicitly_wait(30)
                            page_now = self.find_element_by_xpath(
                                '//div[@id="_container_%s"]//li[@class="pagination-page  active "]' % field).text
                            browser.implicitly_wait(30)
                    else:
                        tries = int(page_to_start) / 10
                        # 先每次跳转10页
                        for i in range(tries):
                            self.find_elements_by_xpath(
                                '//div[@id="_container_%s"]//li[@class="pagination-page "]/a' % field)[-1].click()
                            browser.implicitly_wait(30)
                            page_now = self.find_element_by_xpath(
                                '//div[@id="_container_%s"]//li[@class="pagination-page  active "]' % field).text
                            browser.implicitly_wait(30)
                        # 再一页接着一页
                        while int(page_now) < int(page_to_start):
                            self.find_element_by_xpath(
                                '//div[@id="_container_%s"]//li[@class="pagination-next  "]/a' % field).click()
                            browser.implicitly_wait(30)
                            page_now = self.find_element_by_xpath(
                                '//div[@id="_container_%s"]//li[@class="pagination-page  active "]' % field).text
                            browser.implicitly_wait(30)
        elif self.isElementExist('//div[@id="_container_%s"]' % field):
            # 不需要翻页,存在第一页数据
            print u"不需要翻页,存在第一页数据"
            self.onepage_data(company_name, company_link)
            print u"已提交第 1 页数据"
        else:
            # 无数据
            print u"无数据"
            self.onepage_data(company_name, company_link)
            print u"已提交 空值 "
        return answer

    def get_onecomp(self, field, company_name, company_link, i):
        print(u"base get_onecomp")
        """
		打开新标签页，加载一个公司网址的链接，获取数据后关闭
		"""
        browser = self.browser
        # 新建标签页
        ActionChains(browser).key_down(Keys.CONTROL).send_keys(
            "t").key_up(Keys.CONTROL).perform()
        browser.switch_to_window(browser.window_handles[-1])
        try:
            browser.get(company_link)
            print u"等待10秒再获取下一个公司数据"
            browser.implicitly_wait(10)
        except:
            browser.execute_script('window.stop()')

        # 提交一个公司的所有翻页数据
        print u"开始抓取数据"
        result = self.turnpage(field, company_name, company_link, i)

        # 关闭标签页
        browser.close()
        browser.switch_to_window(browser.window_handles[-1])
        return result

    def fetch(self, filePath, field):
        try:
            # 读取文件，包含相关链接
            link_df = pd.read_excel(filePath)
            # 遍历网址获取数据
            for i in range(len(link_df)):
                # for i in range(2):
                company_link, company_name, fetched = link_df.link[
                    i], link_df.name[i], link_df.get(field)[i]
                print(u'第%d个 %s %s 抓取%s：%s' %
                      (i, company_name, company_link, field, fetched))
                if cmp(company_link, u'空') == 0 or cmp(fetched, u'已抓取') == 0:
                    continue
                # 提交一个公司的数据
                result = self.get_onecomp(field, company_name, company_link, i)

                # 提交后更新执行进度为0
                progress = self.load_dict_from_file(u"总进度.txt")  # 字典
                progress[field] = '%s,%s' % (i + 1, 0)
                self.save_dict_to_file(progress, u"总进度.txt")

                # 保存文件
                if result != "quit":
                    link_df.loc[i, field] = u"已抓取"
                    link_df.to_excel(filePath)
        except Exception, e:
            print 'str(Exception):\t', str(Exception)
            print 'str(e):\t\t', str(e)
            print 'repr(e):\t', repr(e)
            print 'e.message:\t', e.message
            print 'traceback.print_exc():'
            traceback.print_exc()
            print 'traceback.format_exc():\n%s' % traceback.format_exc()
        # self.browser.quit()
