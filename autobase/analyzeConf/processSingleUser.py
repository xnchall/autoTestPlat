#! -*-coding:utf-8-*-

import analyzeConf as ac

class processSingleUser(object):
	def __init__(self):
		self._user_id = ''
		self._confname = ''
		#self._sectname = ''
		self._insertret = 0
		
	def setUserId(self,_user_id):
		self._user_id = _user_id
	
	def setConfName(self,_confname):
		self._confname = _confname
	
	def setSectName(self,_sectname):
		self._sectname = _sectname
	
	def doInsert(self):
		istret = ac.ParseConf('/ngbss/credit/practice/code/autobase/analyzeConf/etc/' + self._confname)
		#_insertret = istret.insertStr(self._sectname,'user_id in (',self._user_id)
		_insertret = istret.insertStr(self._sectname,'user_id in (',self._user_id)
		return _insertret




