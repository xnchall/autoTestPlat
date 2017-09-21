#-*-coding:utf-8-*-
'''
date:2017-04-26
author:liuzesi
info:
	自封装log模块
API:
	调用Log(loggername)实例化
	getLogger方法获取logger
'''

from datetime import datetime
import logging,logging.handlers

now=str(datetime.strftime(datetime.now(),'%Y%m%d'))
class Log(object):
	"""docstring for Log"""
	def __init__(self,name):
		super(Log, self).__init__()
		self._path = '/ngbss/credit/practice/log/' #log存放地址
		self._name = name # loggername
		self._filename=self._path+self._name+'/'+now+'.log'

	def setLogger(self):
		self.logger = logging.getLogger(self._name) #获取logger
		self.logger.setLevel(logging.DEBUG) #设置logger级别

		self.fh = logging.FileHandler(self._filename) #设置logger文件handler
		self.fh.setFormatter(logging.Formatter('%(asctime)s-%(filename)s[line:%(lineno)d]-%(name)s-%(levelname)s %(message)s')) #设置logger文件格式
		self.logger.addHandler(self.fh)

		self.sh = logging.StreamHandler() #设置logger终端handler
		self.sh.setFormatter(logging.Formatter('%(asctime)s-%(filename)s[line:%(lineno)d]-%(name)s-%(levelname)s %(message)s')) #设置logger终端格式
		self.logger.addHandler(self.sh)

		return self.logger

	def getLogger(self):
		return self.setLogger()