#! -*-coding:utf-8-*-
'''
date:2017-03-24
author:liuzesi
info:

'''

import sys,subprocess,os,time
from datetime import datetime,date
sys.path.append('/ngbss/credit/practice/code')
from autobase.Dao.dbPool import dbPool
from autobase.analyzeConf.analyzeConf import ParseConf

#读取配置文件的数据库连接信息
confpath = '/ngbss/credit/practice/code/etc/autotest.conf'
pc = ParseConf(confpath) #获取parseconf实例
procpath = '/ngbss/credit/practice/code/src/utils/importUserInfo/'

class userValueImport(object):
	"""docstring for userValueImport"""
	def __init__(self):
		super(userValueImport, self).__init__()
		self.db = ''
		self._user_id = ''
		self._billid = ''
		self._value = ''
		self._domain = ''
		self._l_userinfo = []

	def setUserId(self,_user_id):
		self._user_id = _user_id

	def setBillId(self,_billid):
		self._billid = _billid

	def setValue(self,_value):
		self._value = _value

	def setDomain(self,_domain):
		self._domain = _domain

	def doShellCmd(self,sql):
		shellcmd = procpath+'istqcubic.sh '+'\"'+sql+'\"'
		subprocess.Popen(shellcmd,shell=True)
		print('------------')
		return 'success'

	#获取dbPool单例
	def getDBIns(self):
		db_info = pc.getSectInfo('TACT'+self._domain)
		db = dbPool.get_instance(db_info)
		return db

	#获取资费实例及套餐上限
	def getValue(self):
		if not self.db:
			self.db = self.getDBIns()
		qsql = ('select a.feepolicy_ins_id, b.addup_upper from tf_f_feepolicy a, td_b_feepolicy_addup b where a.feepolicy_id = b.feepolicy_id and a.id_type = \'0\' and a.id = \''+self._user_id+'\' and b.addup_item_code = \''+self._billid+'\'')

		#generator获取查询结果，组成list返回
		_user_fee_ins_id = list(self.db.execQuery(qsql)[i]['feepolicy_ins_id'] for i in range(len(self.db.execQuery(qsql))))
		_user_max_value = list(self.db.execQuery(qsql)[i]['addup_upper'] for i in range(len(self.db.execQuery(qsql))))
		_luserinfo = [_user_fee_ins_id,_user_max_value]
		return _luserinfo

	#导入操作
	def importValue(self):
		try:
			month = datetime.now().strftime('%m')
			if self._billid in ('99996','99997','99998'):
				isql = ('insert into bill_user_sum1_'+month+' values (\''+self._user_id+'\',\'0\',\''+self._billid+'\','
						'\''+self._value+'\',\'99999999999999\',\'2\',\'0\',\'0\',\'0\');')
			else:
				self._l_userinfo = self.getValue()
				if not (self._l_userinfo[0] or self._l_userinfo[1]):
					print ('Cannot get user info from Oracle! Please Check')
					return 'fail'
				else:
					#循环获取fee_ins_id
					fee_ins_id = str(self._l_userinfo[0][0])
					#循环获取max_value
					max_value = str(self._l_userinfo[1][0])

					isql = ('insert into bill_user_sum1_'+month+' values (\''+self._user_id+'\',\''+fee_ins_id+'\',\''+self._billid+'\','
							'\''+self._value+'\',\''+max_value+'\',\'2\',\'0\',\'0\',\'0\');')
			print (isql)

			return self.doShellCmd(isql)
		except Exception as e:
			print ('Error:%s' % e)
			return 'fail'


'''
a = userValueImport()
a.setDomain('1')
a.setUserId('1116120667220004')
a.setValue('873628372')
a.setBillId('99995')
print(a.importValue())
a.setBillId('40000')
print(a.importValue())
a.setValue('42949672961')
a.setBillId('99996')
print(a.importValue())
'''