#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:zj time: 2019/8/3 11:01
import time
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import multiprocessing
from douyin_save import get_douyin_id

def get_size(driver):
	'''
	获取屏幕的大小，用来决定滑动动作
	:param driver:
	:return:
	'''
	x = driver.get_window_size()['width']
	y = driver.get_window_size()['height']
	return x, y


def get_fans(driver, douyin_id):
	# 定位搜索框
	while True:
		if WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath("//android.widget.TextView[@resource-id='com.ss.android.ugc.aweme:id/dd3']")):
			driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.ss.android.ugc.aweme:id/dd3']").click()
			driver.find_element_by_xpath(
				"//android.widget.TextView[@resource-id='com.ss.android.ugc.aweme:id/dd3']").send_keys(douyin_id)
			while driver.find_element_by_xpath(
				"//android.widget.TextView[@resource-id='com.ss.android.ugc.aweme:id/dd3']").text != douyin_id:
				driver.find_element_by_xpath(
					"//android.widget.TextView[@resource-id='com.ss.android.ugc.aweme:id/dd3']").send_keys(
					douyin_id)

		driver.find_element_by_id("com.ss.android.ugc.aweme:id/a5s").click()
		if WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath("//android.widget.HorintallScrollView/android.widget.TextView[3]")):
			driver.find_element_by_xpath("//android.widget.HorintallScrollView/android.widget.TextView[3]").click()

		if WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("com.ss.android.ugc.aweme:id/bsr")):
			driver.find_element_by_xpath("//android.widget.HorintallScrollView/android.widget.TextView[1]").click()

		if WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("//android.widget.TextView[@resource-id='com.ss.android.ugc.aweme:id/ah7']")):
			driver.find_element_by_id("//android.widget.TextView[@resource-id='com.ss.android.ugc.aweme:id/ah7']").click()

		time.sleep(1)

		# 设置滑动位置和方向
		l = get_size(driver)
		x1 = int(l[0]*0.5)
		y1 = int(l[1]*0.85)
		y2 = int(l[1]*0.15)

		# 判断是否有粉丝
		while True:
			if '没有更多了' in driver.page_source:
				break
			elif 'TA还没有粉丝':
				break
			else:
				driver.swipe(x1, y1, x1, y2)
				time.sleep(0.5)

		# 回退，重新输入抖音id
		# driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.ss.android.ugc.aweme:id/j2']").click()
		# driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.ss.android.ugc.aweme:id/j2']']").click()

def handle_driver(device, port):
	cap = {
	  "platformName": "Android",
	  "platformVersion": "4.4.2",
	  "deviceName": device,
		"udid": device
	  "appPackage": "com.ss.android.ugc.aweme",
	  "appActivity": "com.ss.android.ugc.aweme.splash.SplashActivity",
	  "noReset": True,
	  "unicodekeyboard": True,
	  "resetkeyboard": True
	}

	driver = webdriver.Remote("http://localhost:{}/wd/hub".format(port), cap)

	try:
		if WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("com.ss.android.ugc.aweme:id/aci")):
			driver.find_element_by_id("com.ss.android.ugc.aweme:id/aci").click()
	except:
		pass

	# 获取要爬取的抖音id
	douyin_id = get_douyin_id
	get_fans(driver, douyin_id)

if __name__ == '__main__':
	m_list = []
	# 定义两台虚拟设备
	devices_list = ['127.0.0.1:62001', '127.0.0.1:62025']
	# 设置端口号
	for device in range(len(devices_list)):
		port = 4723 + 2*device
		m_list.append(multiprocessing.Process(target=handle_driver, args=(devices_list[device], port,)))

	for m1 in m_list:
		m1.start()

	for m2 in m_list:
		m2.join()