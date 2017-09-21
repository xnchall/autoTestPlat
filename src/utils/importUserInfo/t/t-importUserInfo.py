#! -*-coding:utf-8-*-
'''
date:2017-03-24
2017-09-19
author: liuzesi
info:
	实现对于输入的用户，取Oracle资料，导入dmdb的功能
	更新：增加_domain，支持前台传域别，不同域的数据
	            增加_importflag，支持号码导入开关
	            修改代码结构，从CATinit.py文件配置sql，增加表

'''

import sys,subprocess,os,time
sys.path.append('/ngbss/credit/practice/code')
from autobase.CATinit.CATinit import dsql_dmdb,sql_dmdb
from autobase.Dao.dbPool import dbPool
from autobase.analyzeConf.analyzeConf import ParseConf


#读取配置文件的数据库连接信息
confpath = '/ngbss/credit/practice/code/etc/autotest.conf'
pc = ParseConf(confpath) #获取parseconf实例

class userInfoImport(object):
	def __init__(self):
		self._user_id = ''
		self._domain = ''
		self._flag = ''
		self.db = ''

	def setUserId(self,_user_id):
		self._user_id = _user_id

	def setDomain(self,_domain):
		if self._domain != _domain:
			self._domain = _domain
		else:
			pass

	#是否执行操作，1执行，0不执行
	def setImportFlag(self,_flag):
		self._flag = _flag

	def getDBIns(self):
		#获取数据库连接
		db_info = pc.getSectInfo('TACT'+self._domain)
		self.db = dbPool(db_info)
		#db = dbPool.get_instance(db_info) #获取dbPool单例
		#return db

	def importInfo(self):
		'''
		TF_F_USER
		TF_F_CUSTOMER
		TF_F_USER_PARAM
		TF_F_USER_SERV
		TF_F_USER_SERVSTATE
		TF_F_USER_IMPORTINFO
		TF_F_FEEPOLICY
		TF_F_FEEPOLICY_PARAM
		TF_F_ACCOUNT
		TF_F_PAYRELATION
		TF_F_USER_PRODUCT
		TF_F_USER_MEMBER
		'''
		path = '/ngbss/credit/practice/code/src/utils/importUserInfo/sqlfile'
		fname = 'info.sql'
		shellcmd = './istdmdb.sh '+fname
		rmcmd = 'rm '+fname
		
		if self._flag == '0': #不执行操作，直接返回成功
			return 'success'
		else:
			if not self.db:
				self.getDBIns()
			#path = '/ngbss/credit/practice/code/src/utils/importUserInfo'
			#fname = 'info.sql'
			#shellcmd = './istdmdb.sh '+fname
			#rmcmd = 'rm '+fname
			dsql = dsql_dmdb.replace('self._user_id',self._user_id)
			isql = sql_dmdb.replace('self._user_id',self._user_id)
			#切换路径
			os.chdir(path)
			
			#删除语句写入文件
			with open(fname,'a') as f:
				f.write(dsql)

			#插入语句写入文件
			r = (self.db.execQuery(isql)[i]['istsql'] for i in range(len(self.db.execQuery(isql))))
			for i in r:
				with open(fname,'a') as f:
					f.write(i+'\n')

			try:
				#raise Exception('err test')
				#subprocess.call([shellcmd],shell=True) #执行shell
				#time.sleep(1)
				#subprocess.call([rmcmd],shell=True) #删除文件
				print ('done!')
				return 'success'
			except Exception as e:
				print ('Method importInfo error! info:',e)
				return 'fail'

a = userInfoImport()
a.setUserId('1114061524350998')
a.setDomain('1')
a.setImportFlag('1')
a.importInfo()