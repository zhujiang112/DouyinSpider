#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:zj time: 2019/8/2 18:05
import json
from douyin_save import save_fans

def response(flow):
	'''
	mitmdump运行，用来抓包后存储
	:param flow:
	:return:
	'''
	fans = {}
	# 判断url是否为粉丝列表的url
	if '/aweme/v1/user/follower/list/' in flow.request.url:
		for user in json.loads(flow.response.text)['followers']:
			fans['share_id'] = user['uid']
			# 用来判断粉丝的抖音id，全数字和有英文不相同
			if user['short_id'] == '0':
				fans['douyin_id'] = user['unique_id']
			else:
				fans['douyin_id'] = user['short_id']
			fans['nickname'] = user['nickname']
			save_fans(fans)


