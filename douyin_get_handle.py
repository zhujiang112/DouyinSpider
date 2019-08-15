#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:zj time: 2019/8/2 10:44
'''
映射字体文件得到真正字体，Windows端抓取抖音个人信息
'''
import re

import requests
from lxml import etree
from fontTools.ttLib import TTFont

# 读取字体文件
ttfont = TTFont('iconfont_9eb9a50.woff')
# 读取引射表 映射 网页中的加密的字符串到num_x
best_font = ttfont['cmap'].getBestCmap()

def best_cmap():
	'''
	:return:返回编码表
	'''
	last_font = {}
	for key, value in best_font.items():
		last_key = hex(key)
		last_font[last_key] = value
	return last_font

def num_cmap():
	'''
	:return:返回真正数字映射关系
	'''
	num = {
		'x': '', 'num_': '1', 'num_1': '0',
		'num_2': '3', 'num_3': '2',
		'num_4': '4', 'num_5': '5',
		'num_6': '6', 'num_7': '9',
		'num_8': '7', 'num_9': '8'
	}
	return num

def map_cmap_num(best_cmap, num_cmap):
	'''
	最终映射
	:param best_cmap:
	:param get_num_cmap:
	:return:
	'''
	last_font = {}
	for key, value in best_cmap().items():
		key = re.sub('0', '&#', key, count=1) + ';'
		last_font[key] = num_cmap()[value]
	return last_font

def get_html(url):
	headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
	}
	response = requests.get(url, headers=headers).text
	return response

def replace_font(result , response):
	for key, value in result.items():
		if key in response:
			response = re.sub(key, value, response)
	return response

def message_handle(resp):
	message = {}
	html = etree.HTML(resp)
	nickname = html.xpath("//p[@class='nickname']/text()")[0]
	# short = su
	prof = html.xpath("//span[@class='info']/text()")
	if prof:
		prof = prof[0].strip()
	else:
		prof = ''
	describe = html.xpath("//p[@class='signature']/text()")[0]
	follow = ''.join(html.xpath("//span[@class='focus block']//i[@class='icon iconfont follow-num']/text()")).replace(' ', '')
	follower = ''.join(html.xpath("//span[@class='follower block']//i[@class='icon iconfont follow-num']/text()")).replace(' ', '')
	f = ''.join(html.xpath("//span[@class='follower block']//span[@class='num']/text()"))
	if 'w' in f:
		follower = str(int(follower)/10) + 'w'
	prais = ''.join(html.xpath("//span[@class='liked-num block']/span/i/text()")).replace(' ', '')
	p  = ''.join(html.xpath("//span[@class='liked-num block']/span/text()"))
	if  'w' in p:
		prais = str(int(prais)/10) + 'w'
	product =  ''.join(html.xpath("//div[@class='user-tab active tab get-list']//i/text()")).replace(' ', '')
	like = ''.join(html.xpath("//div[@class='like-tab tab get-list']//i/text()")).replace(' ', '')
	message['nickname'] = nickname
	message['prof'] = prof
	message['descibe'] = describe
	message['follow'] = follow
	message['follower'] = follower
	message['praise'] = prais
	message['product'] = product
	message['like'] = like
	return message

if __name__ == '__main__':
	result = map_cmap_num(best_cmap, num_cmap)
	base_url = 'https://www.iesdouyin.com/share/user/72956256590'
	response = get_html(base_url)
	html = replace_font(result, response)
	print(message_handle(html))