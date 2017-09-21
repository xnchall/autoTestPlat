#! -*-coding:utf-8-*-
'''
date:2017-03-24
author:liuzesi
info:
	实现对于输入的用户，取Oracle资料，导入dmdb的功能
	更新：增加_domain，支持前台传域别，不同域的数据
		  增加_importflag，支持号码导入开关
'''

import sys,subprocess,os,time
sys.path.append('/ngbss/credit/practice/code')
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
		db_info = pc.getSectInfo('TACT'+self._domain)
		db = dbPool.get_instance(db_info) #获取dbPool单例
		return db

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
		print (self._flag)
		if self._flag == '0': #不执行操作，直接返回成功
			return 'success'
		else:
			if not self.db:
				self.db = self.getDBIns()
			path = '/ngbss/credit/practice/code/src/utils/importUserInfo'
			fname = 'info.sql'
			shellcmd = './istdmdb.sh '+fname
			rmcmd = 'rm '+fname
			dsql = ('delete from tf_f_user where user_id in ('+self._user_id+');\n'
					'delete from tf_f_user_servstate where user_id in ('+self._user_id+');\n'
					'delete from tf_f_user_param where user_id in ('+self._user_id+');\n'
					'delete from tf_f_feepolicy where id_type = 0 and id in ('+self._user_id+');\n'
					'delete from tf_f_user_importinfo where user_id in ('+self._user_id+');\n'
					'delete from tf_f_user_product where user_id in ('+self._user_id+');\n'
					'delete from tf_f_user_serv where user_id in ('+self._user_id+');\n'
					'delete from tf_f_account where acct_id = (select acct_id from tf_f_payrelation where sysdate between start_date and end_date and user_id in ('+self._user_id+'));\n')
			isql = ('select \'insert into tf_f_user (user_id,dummy_tag,net_type_code,serial_number,eparchy_code,city_code,cust_id,usecust_id,brand_code,product_id,user_type_code,prepay_tag,service_state_code,open_mode,acct_tag,remove_tag,in_date,open_date,pre_destroy_date,destroy_date,first_call_date,last_stop_date,credit_class,base_credit_value,credit_value,credit_control_id,changeuser_date,score_value,update_time,province_code) values (\'\'\'||a.USER_ID||\'\'\',\'\'\'||a.DUMMY_TAG||\'\'\',\'\'\'||a.NET_TYPE_CODE||\'\'\',\'\'\'||a.SERIAL_NUMBER||\'\'\',\'\'\'||a.EPARCHY_CODE||\'\'\',\'\'\'||a.CITY_CODE||\'\'\',\'\'\'||a.CUST_ID||\'\'\',\'\'\'||a.USECUST_ID||\'\'\',\'\'\'||a.BRAND_CODE||\'\'\',\'\'\'||a.PRODUCT_ID||\'\'\',\'\'\'||a.USER_TYPE_CODE||\'\'\',\'\'\'||a.PREPAY_TAG||\'\'\',\'\'\'||a.SERVICE_STATE_CODE||\'\'\',\'\'\'||a.OPEN_MODE||\'\'\',\'\'\'||a.ACCT_TAG||\'\'\',\'\'\'||a.REMOVE_TAG||\'\'\',\'\'\'||to_char(a.IN_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||to_char(a.IN_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||a.PRE_DESTROY_DATE||\'\'\',\'\'\'||to_char(a.DESTROY_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||to_char(a.FIRST_CALL_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||to_char(a.LAST_STOP_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||a.CREDIT_CLASS||\'\'\',\'\'\'||a.BASE_CREDIT_VALUE||\'\'\',\'\'\'||a.CREDIT_VALUE||\'\'\',\'\'\'||a.CREDIT_CONTROL_ID||\'\'\',\'\'\'||to_char(a.CHANGEUSER_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||a.SCORE_VALUE||\'\'\',\'\'\'||to_char(a.UPDATE_TIME,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||a.PROVINCE_CODE||\'\'\');\' istsql'
					' from tf_f_user a where a.user_id in ('+self._user_id+')'
					' union all '
					'select \'insert into tf_f_user_serv (serv_ins_id,user_id,serv_id,prior_order_time,main_tag,product_id,serv_bund_id,start_date,end_date) values (\'\'\'||a.SERV_INS_ID||\'\'\',\'\'\'||a.USER_ID||\'\'\',\'\'\'||a.SERV_ID||\'\'\',\'\'\'||a.PRIOR_ORDER_TIME||\'\'\',\'\'\'||a.MAIN_TAG||\'\'\',\'\'\'||a.PRODUCT_ID||\'\'\',\'\'\'||a.SERV_BUND_ID||\'\'\',\'\'\'||to_char(a.START_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||to_char(a.END_DATE,\'YYYYMMDDHH24MISS\')||\'\'\');\' istsql'
					' from tf_f_user_serv a where a.user_id in ('+self._user_id+') and sysdate between a.start_date and a.end_date'
					' union all '
					'select \'insert into tf_f_user_servstate (user_id,serv_id,serv_ins_id,main_tag,serv_state_code,start_date,end_date) values (\'\'\'||a.USER_ID||\'\'\',\'\'\'||a.SERV_ID||\'\'\',\'\'\'||a.SERV_INS_ID||\'\'\',\'\'\'||a.MAIN_TAG||\'\'\',\'\'\'||a.SERV_STATE_CODE||\'\'\',\'\'\'||to_char(a.START_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||to_char(a.END_DATE,\'YYYYMMDDHH24MISS\')||\'\'\');\' istsql'
					' from tf_f_user_servstate a where a.user_id in ('+self._user_id+') and sysdate between a.start_date and a.end_date'
					' union all '
					'select \'insert into tf_f_user_param(USER_ID,PARAM_ID,PARAM_VALUE,START_DATE,END_DATE) values (\'\'\'||user_id||\'\'\',\'\'\'||param_id||\'\'\',\'\'\'||param_value||\'\'\',\'\'\'||to_char(start_date,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||to_char(end_date,\'YYYYMMDDHH24MISS\')||\'\'\');\' istsql'
					' from tf_f_user_param a where user_id in ('+self._user_id+') and sysdate between a.start_date and a.end_date'
					' union all '
					'select \'insert into tf_f_feepolicy (FEEPOLICY_INS_ID,ID_TYPE,ID,FEEPOLICY_ID,RELA_USER_ID,PRODUCT_ID,SERV_BUND_ID,SERV_ID,FEEPOLICY_BUND_ID,START_DATE,END_DATE) values (\'\'\'||FEEPOLICY_INS_ID||\'\'\',\'\'\'||ID_TYPE||\'\'\',\'\'\'||ID||\'\'\',\'\'\'||FEEPOLICY_ID||\'\'\',\'\'\'||RELA_USER_ID||\'\'\',\'\'\'||PRODUCT_ID||\'\'\',\'\'\'||SERV_BUND_ID||\'\'\',\'\'\'||SERV_ID||\'\'\',\'\'\'||FEEPOLICY_BUND_ID||\'\'\',\'\'\'||to_char(START_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||to_char(END_DATE,\'YYYYMMDDHH24MISS\')||\'\'\');\' istsql'
					' from tf_f_feepolicy a where a.id_type = 0 and a.id in ('+self._user_id+') and sysdate between a.start_date and a.end_date'
					' union all '
					'select \'insert into tf_f_user_importinfo (USER_ID,NET_TYPE_CODE,PREPAY_TAG,PRODUCT_ID,BRAND_CODE,LOGIC_PHONE,PHYICAL_PHONE,START_DATE,END_DATE) values (\'\'\'||USER_ID||\'\'\',\'\'\'||NET_TYPE_CODE||\'\'\',\'\'\'||PREPAY_TAG||\'\'\',\'\'\'||PRODUCT_ID||\'\'\',\'\'\'||BRAND_CODE||\'\'\',\'\'\'||LOGIC_PHONE||\'\'\',\'\'\'||PHYICAL_PHONE||\'\'\',\'\'\'||to_char(START_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||to_char(END_DATE,\'YYYYMMDDHH24MISS\')||\'\'\');\' istsql'
					' from tf_f_user_importinfo a where user_id in ('+self._user_id+') and sysdate between a.start_date and a.end_date'
					' union all '
					'select \'insert into tf_f_user_product (USER_ID,PRODUCT_MODE,PRODUCT_ID,BRAND_CODE,START_DATE,END_DATE,ITEM_ID,USER_ID_A) values (\'\'\' || a.USER_ID || \'\'\',\'\'\' || a.PRODUCT_MODE || \'\'\',\'\'\' || a.PRODUCT_ID || \'\'\',\'\'\' ||a.BRAND_CODE|| \'\'\',\'\'\' || to_char(a.START_DATE, \'YYYYMMDDHH24MISS\') || \'\'\',\'\'\' || to_char(a.END_DATE, \'YYYYMMDDHH24MISS\') || \'\'\',\'\'\' ||a.ITEM_ID|| \'\'\',\'\'\' ||a.USER_ID_A|| \'\'\');\' istsql'
					' from tf_f_user_product a where a.user_id in ('+self._user_id+') and sysdate between a.start_date and a.end_date')

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
				subprocess.call([shellcmd],shell=True) #执行shell
				time.sleep(1)
				subprocess.call([rmcmd],shell=True) #删除文件
				print ('done!')
				return 'success'
			except Exception as e:
				print ('Method importInfo error! info:',e)
				return 'fail'
