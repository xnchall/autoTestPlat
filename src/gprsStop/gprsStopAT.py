#! -*-coding:utf-8-*-
'''
date:2017-04-25
author:liuzesi
info:

'''

from datetime import datetime,date
import sys,subprocess,os,time
sys.path.append('/ngbss/credit/practice/code')
from src.utils.logger.logger import Log

class gprsStopAT(object):
	"""docstring for gprsStopAT"""
	def __init__(self):
		super(gprsStopAT, self).__init__()
		self.logger=Log('gprsStop').getLogger( )
		self.binpath='/ngbss/credit/bin/'
		self._prov=''

	def setProv(self,_prov):
		self._prov = _prov

	def doProcess(self):
		self.logger.info('gprsStop begin')
		#log='sdfasdfasdfasdfasdfasdfasd'
		for i in range(10):
			t=datetime.now()
			self.logger.debug(t)
			tt=datetime.now()-t
			self.logger.debug(tt)

		#subprocess.Popen(self.binpath+'gprsStop -c0 -p'+self._prov,shell=True)
		self.logger.info('gprsStop end')

a=gprsStopAT()
a.setProv('11')
a.doProcess()