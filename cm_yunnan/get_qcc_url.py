# -*- coding: utf-8 -*-

import time
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from util import mysql
from base import Qcc

username = "18064063503"  # 第一个参数为用户名
password = "wzswjmm123"  # 第二个参数为密码
win = Qcc(username, password)
win.login()
browser = win.browser


def prepare(browser):
    browser.find_element_by_id("searchkey").clear()
    browser.find_element_by_id("searchkey").send_keys(u"安邦")
    browser.find_element_by_id("V3_Search_bt").click()
    browser.implicitly_wait(60)
prepare(browser)


def get_link_qcc(company_name, browser):
    # 新建标签页
    # ActionChains(browser).key_down(Keys.CONTROL).send_keys(
    #     "t").key_up(Keys.CONTROL).perform()
    # browser.switch_to_window(browser.window_handles[-1])
    try:
        browser.find_element_by_id("headerKey").clear()
        browser.find_element_by_id("headerKey").send_keys(company_name)
        browser.find_element_by_xpath('//button[@type="submit"]').click()
        browser.implicitly_wait(60)
    except:
        browser.execute_script('window.stop()')
        browser.refresh()
        browser.implicitly_wait(30)
    # 选择一个公司的链接
    url_title = browser.find_element_by_xpath(
        '//section[@id="searchlist"]//tbody/tr//a').text
    company_link = browser.find_element_by_xpath(
        '//section[@id="searchlist"]//tbody/tr//a').get_attribute("href")
    # result = self.turnpage(field, company_name, company_link)

    # 关闭标签页
    # browser.close()
    # browser.switch_to_window(browser.window_handles[-1])
    return url_title, company_link

name_df = pd.read_excel(u"1000家企业_企查查链接.xlsx")
for i in range(len(name_df)):
    if type(name_df.title[i]) != float:
        continue
    company_name = name_df.name[i]
    try:
        url_title, company_link = get_link_qcc(company_name, browser)
    except:
        continue
    time.sleep(3)
    name_df.title[i] = url_title
    name_df.link[i] = company_link
    name_df.to_excel(u"1000家企业_企查查链接.xlsx")
    browser.implicitly_wait(30)
