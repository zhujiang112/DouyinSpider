#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:zj time: 2019/8/3 9:30
import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client['douyin']
collection = db['fans']

def save_fans(task):
	'''
	爬取的粉丝存在更新，不存在新增
	:param task:
	:return:
	'''
	collection.update({'share_id': task['share_id']}, task, True)

def get_douyin_id():
	collection.find_one_and_delete()