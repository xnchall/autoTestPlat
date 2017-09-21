#coding = utf-8

import sys
sys.path.append('/ngbss/credit/practice/code')
from autobase.baseHelper.baseHelper import baseUtils as utils

class importInfo(object):
	"""docstring for importUserInfoFromPro"""
	def __init__(self):
		self.user_id=[]
		self.pool = None#数据库缓存池句柄

	def setRegion(self, region):
		self.pool = utils.db_getInstance(region)

	def setUserid(self, userid):
		self.user_id = user_id.split(',')