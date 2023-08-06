#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Alrash
# @Email: alrash@nuaa.edu.cn
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 等待用
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os, time, sys
from urllib.parse import urlencode, unquote

import argparse

website = 'Alrash小站'
username, passwd = '黑白全彩', 'I7M8nY4hnztt8Rjd#VPBZ8#b'


def login_address(redirect = None):
    data = {'redirect_to': redirect if redirect is not None else 'https://alrash.xyz', 'reauth': 1}
    return 'https://alrash.xyz/wp-login.php?%s' % (urlencode(data))


def logout_address(driver, redirect = None):
    logout = driver.find_element_by_css_selector("li#wp-admin-bar-logout>a")
    href = logout.get_attribute('href')
    href = href if redirect is None else href + '&' + urlencode({'redirect_to': redirect})
    driver.execute_script("arguments[0].setAttribute('href', '%s'); arguments[0].click();" % href, logout)
    print('==== 退出登录 ====')

## 定义提交函数
def comment_submit_func(driver, comment, log):
    textarea = driver.find_element_by_css_selector('textarea#comment')
    textarea.send_keys(comment)
    print(log)
    submit = driver.find_element_by_class_name('submit')
    submit.click()


def test(browser = False, proxy = False, devicepath = '/usr/bin/chromedriver',
         username = username, passwd = passwd, website = website):
    assert os.path.exists(devicepath)

    # 代理选项
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    if browser == False:
        chrome_options.add_argument('headless')
    chrome_options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
    # 加socks5代理
    if proxy:
        chrome_options.add_argument("proxy-server=socks5://127.0.0.1:1080")

    print('==== 准备加载alrash.xyz主页 ====')
    driver = webdriver.Chrome(devicepath, options = chrome_options)
    driver.get('https://alrash.xyz')


    # 等待文章加载
    try:
        element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "post-342"))
                )
    finally:
        print('==== 页面加载结束 ====')


    # 断言是否是需要的网页
    assert website in driver.title
    
    
    # 进入Github
    print('\n==== 准备进入github主页 ====')
    ## 修改a标记属性
    js = "document.getElementsByClassName('oceanwp-github')[0].getElementsByTagName('a')[0].target='_blank'"
    driver.execute_script(js)
    ## 发现github标记
    link = driver.find_element_by_css_selector('li.oceanwp-github>a')
    link.click()
    ## 切换窗口句柄
    driver.switch_to.window(driver.window_handles[1])
    print("\t当前窗口标题为：%s" % driver.title)
    ## 关闭窗口
    # time.sleep(1)
    driver.close()
    print('==== 关闭窗口，退出github ====')
    
    # 点击文章
    print('\n==== 准备进入post-342文章 ====')
    ## 切换窗口句柄
    driver.switch_to.window(driver.window_handles[0])
    link = driver.find_element_by_css_selector('article#post-342 div.blog-entry-readmore>a')
    link.click()
    
    assert '域泛化 – %s' % website in driver.title
    print('==== 已进入文章 ====')
    
    
    try:
        component = driver.find_element_by_css_selector('textarea#comment1')
    except selenium.common.exceptions.NoSuchElementException:
        print('==== 发现元素失败[未发现id为comment1的元素] ====')
    
    
    ## 不登录直接评论文章
    comment_submit_func(driver, "测试", '==== 已填写评论，准备不登录提交 ====')
    
    if '评论提交失败' in driver.title:
        print('\t功能正常[不登录无法评论]')
        driver.find_element_by_tag_name('a').click()
    else:
        print('已登录')
    
    ## 登录
    print('\t准备登录...')
    driver.get(login_address(driver.current_url))
    driver.find_element_by_id('user_login').send_keys(username)
    driver.find_element_by_id('user_pass').send_keys(passwd)
    print('\t用户名与密码填充完毕')
    login = driver.find_element_by_id('wp-submit')
    login.click()
    print('\t登录成功')
    
    ## 评论文章
    ##comment_submit_func(driver, "测试", '==== 再次提交 ====')
    print('==== 提交成功 ====')
    
    
    # 标签云及搜索
    sys.stdout.write('\n')
    ## 标签云
    tagname = '文章'
    tagcloud = driver.find_elements_by_css_selector('div.tagcloud>a')
    ### tagcloud > 1
    for elem in tagcloud:
        if tagname in elem.text:
            print('==== 已发现Tag[%s] ====' % tagname)
            elem.click()
            print('==== 已加载URL[%s] ====' % unquote(driver.current_url))
            break
    
    ## 搜索框
    print('==== 准备测试搜索框 ====')
    searchkey = '域'
    search = driver.find_element_by_id('ocean-search-form-2')
    search.clear()
    search.send_keys(searchkey)
    search.send_keys(Keys.ENTER)
    assert searchkey in unquote(driver.current_url)
    print('==== 搜索测试成功 ====')
    
    ## 发现文章列表
    lst = driver.find_elements_by_tag_name('article')
    print('\t已发现%d文章:' % len(lst))
    for idx, elem in enumerate(lst):
        print('\t\t[%.2d] %s' % (idx + 1, elem.find_element_by_css_selector('header.search-entry-header a').text))
    print('==== 结束搜索测试 ====')
    
    ## 点击home链接返回
    print('\n==== 准备使用HOME返回主页 ====')
    link = driver.find_element_by_link_text('HOME')
    link.click()
    assert website in driver.title and 'Home' in driver.title
    print('==== 返回成功 ====')
    
    # 退出登录
    sys.stdout.write('\n')
    logout_address(driver, redirect = 'https://alrash,xyz')
    
    driver.close()
    driver.quit()
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Homework for Software Testing -- Alrash')
    parser.add_argument('-b', action = "store_false", default = True)
    parser.add_argument('-p', action = "store_true", default = False)
    parser.add_argument('-d', action = "store", default = '/usr/bin/chromedriver')
    
    pars = parser.parse_args()
    
    test(browser = pars.b, proxy = pars.p, devicepath = pars.d)
