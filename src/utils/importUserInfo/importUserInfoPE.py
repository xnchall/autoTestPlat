#! -*-coding:utf-8-*-

#date:2017-05-02
#update:2017-06-08 增加表，优化sql获取方式
#author:liuzesi
#info:
#	实现对于输入的用户，取生产库资料(Production Environment)，导入测试库的功能


import sys
sys.path.append('/ngbss/credit/practice/code')
from autobase.CATinit.CATinit import *
from autobase.Dao.dbPool import dbPool
from autobase.analyzeConf.analyzeConf import ParseConf
#from src.utils.logger.logger import Log

#读取配置文件的数据库连接信息
confpath = '/ngbss/credit/practice/code/etc/autotest.conf'
pc = ParseConf(confpath) #获取parseconf实例

class userInfo(object):

	def __init__(self):
		self._user_id = ''
		self._domain = ''
		self._flag = ''
		#self._table = ''
		self.db = ''
		#self.logger = Log('import').getLogger()

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

	def getDBIns(self,dbconf):
		#获取数据库连接
		db_info = pc.getSectInfo(dbconf)
		self.db = dbPool(db_info)

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
		#self.logger.info('importInfo start!')

		sqllist = []
		try:
			self.getDBIns('PROD_ENV') #获取生产库连接信息
			sisql = '' #本地变量
			sisql = sql.replace('self._domain',self._domain) #替换
			sisql = sisql.replace('self._user_id',self._user_id)
			#self.logger.debug(sisql)
			
			r = (self.db.execQuery(sisql)[i]['istsql'] for i in range(len(self.db.execQuery(sisql)))) #迭代器获取插入语句
			for i in r: #循环获取所有插入语句，塞入sql列表
				#self.logger.debug(i)
				sqllist.append(i)

			if not self.inDb(sqllist): #调用插入方法
				return 'success'
			else:
				return 'fail'

		except Exception as err:
			raise err

	def inDb(self,tact_isql=[]):
		#获取测试库连接信息
		self.getDBIns('TACT'+self._domain)
		try:
			#删除物理库数据
			tact_dsql = [i for i in range(len(dsql))]
			for i in range(len(dsql)):
				tact_dsql[i] = dsql[i].replace('self._user_id',self._user_id)
				#self.logger.debug(tact_dsql[i])
				self.db.execute(tact_dsql[i])
				self.db.commit()
		except Exception as inDberr:
			raise inDberr
		
		try:
			#插入生产获取的数据
			for i in range(len(tact_isql)):
				#self.logger.debug(tact_isql[i])
				self.db.execute(tact_isql[i])
				self.db.commit()
			#全部插入完毕后，执行提交
			#self.db.commit()
		except Exception as inDberr:
			raise inDberr
		#self.logger.debug('done')


#导数据sql备用
#sql = (
#	'select distinct \'insert into tf_f_user values (\'\'\'||PARTITION_ID||\'\'\',\'\'\'||USER_ID||\'\'\',\'\'\'||DUMMY_TAG||\'\'\',\'\'\'||NET_TYPE_CODE||\'\'\',\'\'\'||SERIAL_NUMBER||\'\'\',\'\'\'||EPARCHY_CODE||\'\'\',\'\'\'||CITY_CODE||\'\'\',\'\'\'||CUST_ID||\'\'\',\'\'\'||USECUST_ID||\'\'\',\'\'\'||BRAND_CODE||\'\'\',\'\'\'||PRODUCT_ID||\'\'\',\'\'\'||USER_TYPE_CODE||\'\'\',\'\'\'||PREPAY_TAG||\'\'\',\'\'\'||SERVICE_STATE_CODE||\'\'\',\'\'\'||OPEN_MODE||\'\'\',\'\'\'||ACCT_TAG||\'\'\',\'\'\'||REMOVE_TAG||\'\'\',\'\'\'||IN_DATE||\'\'\',\'\'\'||OPEN_DATE||\'\'\',\'\'\'||PRE_DESTROY_DATE||\'\'\',\'\'\'||DESTROY_DATE||\'\'\',\'\'\'||FIRST_CALL_DATE||\'\'\',\'\'\'||LAST_STOP_DATE||\'\'\',\'\'\'||CREDIT_CLASS||\'\'\',\'\'\'||BASE_CREDIT_VALUE||\'\'\',\'\'\'||CREDIT_VALUE||\'\'\',\'\'\'||CREDIT_CONTROL_ID||\'\'\',\'\'\'||CHANGEUSER_DATE||\'\'\',\'\'\'||SCORE_VALUE||\'\'\',\'\'\'||UPDATE_TIME||\'\'\',\'\'\'||UPDATE_DEPART_ID||\'\'\',\'\'\'||UPDATE_STAFF_ID||\'\'\',\'\'\'||USER_PASSWD||\'\'\',\'\'\'||OPEN_DEPART_ID||\'\'\',\'\'\'||PROVINCE_CODE||\'\'\')\' istsql '
#	'from uop_actself._domain.tf_f_user@toactself._domain where user_id in (self._user_id)'
#	' union all '
#	'select distinct \'insert into tf_f_customer values (\'\'\'||a.PARTITION_ID||\'\'\',\'\'\'||a.CUST_ID||\'\'\',\'\'\'||a.CUST_NAME||\'\'\',\'\'\'||a.CUST_TYPE||\'\'\',\'\'\'||a.CUST_STATE||\'\'\',\'\'\'||a.PSPT_TYPE_CODE||\'\'\',\'\'\'||a.PSPT_ID||\'\'\',\'\'\'||a.EPARCHY_CODE||\'\'\',\'\'\'||a.CITY_CODE||\'\'\',\'\'\'||a.CUST_PASSWD||\'\'\',\'\'\'||a.SCORE_VALUE||\'\'\',\'\'\'||a.CREDIT_CLASS||\'\'\',\'\'\'||a.BASIC_CREDIT_VALUE||\'\'\',\'\'\'||a.CREDIT_VALUE||\'\'\',\'\'\'||a.CREDIT_CONTROL_ID||\'\'\',\'\'\'||a.DEVELOP_DEPART_ID||\'\'\',\'\'\'||a.DEVELOP_STAFF_ID||\'\'\',\'\'\'||a.IN_DEPART_ID||\'\'\',\'\'\'||a.IN_STAFF_ID||\'\'\',\'\'\'||a.IN_DATE||\'\'\',\'\'\'||a.REMOVE_TAG||\'\'\',\'\'\'||a.REMOVE_DATE||\'\'\',\'\'\'||a.REMOVE_STAFF_ID||\'\'\',\'\'\'||a.REMOVE_CHANGE||\'\'\',\'\'\'||a.UPDATE_TIME||\'\'\',\'\'\'||a.UPDATE_DEPART_ID||\'\'\',\'\'\'||a.UPDATE_STAFF_ID||\'\'\',\'\'\'||a.REMARK||\'\'\',\'\'\'||a.CUST_CLASS_TYPE||\'\'\',\'\'\'||a.PROVINCE_CODE||\'\'\',\'\'\'||a.RSRV_TAG1||\'\'\')\' istsql '
#	'from uop_actself._domain.tf_f_customer@toactself._domain a, uop_actself._domain.tf_f_user@toactself._domain b where a.cust_id = b.cust_id and b.user_id in (self._user_id)'
#	' union all '
#	'select distinct \'insert into tf_f_user_param values (\'\'\'||PARTITION_ID||\'\'\',\'\'\'||USER_ID||\'\'\',\'\'\'||PARAM_ID||\'\'\',\'\'\'||PARAM_VALUE||\'\'\',\'\'\'||START_DATE||\'\'\',\'\'\'||END_DATE||\'\'\',\'\'\'||UPDATE_TIME||\'\'\',\'\'\'||UPDATE_DEPART_ID||\'\'\',\'\'\'||UPDATE_STAFF_ID||\'\'\',\'\'\'||PROV_CODE||\'\'\')\' istsql '
#	'from uop_actself._domain.tf_f_user_param@toactself._domain where user_id in (self._user_id)'
#	' union all '
#	'select distinct \'insert into tf_f_user_serv values (\'\'\'||PARTITION_ID||\'\'\',\'\'\'||SERV_INS_ID||\'\'\',\'\'\'||USER_ID||\'\'\',\'\'\'||SERV_ID||\'\'\',\'\'\'||PRIOR_ORDER_TIME||\'\'\',\'\'\'||MAIN_TAG||\'\'\',\'\'\'||PRODUCT_ID||\'\'\',\'\'\'||SERV_BUND_ID||\'\'\',\'\'\'||START_DATE||\'\'\',\'\'\'||END_DATE||\'\'\',\'\'\'||UPDATE_TIME||\'\'\',\'\'\'||UPDATE_DEPART_ID||\'\'\',\'\'\'||UPDATE_STAFF_ID||\'\'\',\'\'\'||PROV_CODE||\'\'\')\' istsql '
#	'from uop_actself._domain.tf_f_user_serv@toactself._domain where user_id in (self._user_id)'
#	' union all '
#	'select distinct \'insert into tf_f_user_servstate values (\'\'\'||PARTITION_ID||\'\'\',\'\'\'||SERV_INS_ID||\'\'\',\'\'\'||USER_ID||\'\'\',\'\'\'||SERV_ID||\'\'\',\'\'\'||MAIN_TAG||\'\'\',\'\'\'||SERV_STATE_CODE||\'\'\',\'\'\'||START_DATE||\'\'\',\'\'\'||END_DATE||\'\'\',\'\'\'||UPDATE_DEPART_ID||\'\'\',\'\'\'||UPDATE_STAFF_ID||\'\'\',\'\'\'||UPDATE_TIME||\'\'\',\'\'\'||PROV_CODE||\'\'\')\' istsql '
#	'from uop_actself._domain.tf_f_user_servstate@toactself._domain where user_id in (self._user_id)'
#	' union all '
#	'select distinct \'insert into tf_f_user_importinfo values (\'\'\'||PARTITION_ID||\'\'\',\'\'\'||USER_ID||\'\'\',\'\'\'||NET_TYPE_CODE||\'\'\',\'\'\'||PRODUCT_ID||\'\'\',\'\'\'||BRAND_CODE||\'\'\',\'\'\'||LOGIC_PHONE||\'\'\',\'\'\'||PHYICAL_PHONE||\'\'\',\'\'\'||START_DATE||\'\'\',\'\'\'||END_DATE||\'\'\',\'\'\'||UPDATE_TIME||\'\'\',\'\'\'||UPDATE_DEPART_ID||\'\'\',\'\'\'||UPDATE_STAFF_ID||\'\'\',\'\'\'||PREPAY_TAG||\'\'\',\'\'\'||PROV_CODE||\'\'\')\' istsql '
#	'from uop_actself._domain.tf_f_user_importinfo@toactself._domain where user_id in (self._user_id)'
#	' union all '
#	'select distinct \'insert into tf_f_feepolicy values (\'\'\'||PARTITION_ID||\'\'\',\'\'\'||FEEPOLICY_INS_ID||\'\'\',\'\'\'||ID_TYPE||\'\'\',\'\'\'||ID||\'\'\',\'\'\'||FEEPOLICY_ID||\'\'\',\'\'\'||RELA_USER_ID||\'\'\',\'\'\'||PRODUCT_ID||\'\'\',\'\'\'||SERV_BUND_ID||\'\'\',\'\'\'||SERV_ID||\'\'\',\'\'\'||FEEPOLICY_BUND_ID||\'\'\',\'\'\'||START_DATE||\'\'\',\'\'\'||END_DATE||\'\'\',\'\'\'||UPDATE_TIME||\'\'\',\'\'\'||UPDATE_DEPART_ID||\'\'\',\'\'\'||UPDATE_STAFF_ID||\'\'\',\'\'\'||PROV_CODE||\'\'\')\' istsql '
#	'from uop_actself._domain.tf_f_feepolicy@toactself._domain where id_type = \'0\' and id in (self._user_id)'
#	' union all '
#	'select distinct \'insert into tf_f_feepolicy_param values (\'\'\'||a.FEEPOLICY_INS_ID||\'\'\',\'\'\'||a.FEEPOLICY_PARAM_ID||\'\'\',\'\'\'||a.FEEPOLICY_PARAM_VALUE||\'\'\',\'\'\'||a.START_DATE||\'\'\',\'\'\'||a.END_DATE||\'\'\',\'\'\'||a.UPDATE_TIME||\'\'\',\'\'\'||a.UPDATE_DEPART_ID||\'\'\',\'\'\'||a.UPDATE_STAFF_ID||\'\'\',\'\'\'||a.PROV_CODE||\'\'\')\' istsql '
#	'from uop_actself._domain.tf_f_feepolicy_param@toactself._domain a, uop_actself._domain.tf_f_feepolicy@toactself._domain b where a.feepolicy_ins_id = b.feepolicy_ins_id and b.id_type = \'0\' and b.id in (self._user_id)'
#	' union all '
#	'select distinct \'insert into tf_f_payrelation values (\'\'\'||PARTITION_ID||\'\'\',\'\'\'||PAYRELATION_ID||\'\'\',\'\'\'||USER_ID||\'\'\',\'\'\'||ITEM_CODE||\'\'\',\'\'\'||PAY_PRIORITY||\'\'\',\'\'\'||ADDUP_METHOD||\'\'\',\'\'\'||ADDUP_MONTHS||\'\'\',\'\'\'||LIMIT_TYPE||\'\'\',\'\'\'||LIMIT_VALUE||\'\'\',\'\'\'||FILL_TAG||\'\'\',\'\'\'||ACCT_ID||\'\'\',\'\'\'||BIND_TYPE||\'\'\',\'\'\'||DISCNT_PRIORITY||\'\'\',\'\'\'||DEFAULT_TAG||\'\'\',\'\'\'||ACT_TAG||\'\'\',\'\'\'||START_CYC_ID||\'\'\',\'\'\'||END_CYC_ID||\'\'\',\'\'\'||UPDATE_TIME||\'\'\',\'\'\'||UPDATE_DEPART_ID||\'\'\',\'\'\'||UPDATE_STAFF_ID||\'\'\',\'\'\'||PROV_CODE||\'\'\')\' istsql '
#	'from uop_actself._domain.tf_f_payrelation@toactself._domain where user_id in (self._user_id)'
#	' union all '
#	'select distinct \'insert into tf_f_account values (\'\'\'||a.PARTITION_ID||\'\'\',\'\'\'||a.ACCT_ID||\'\'\',\'\'\'||a.EPARCHY_CODE||\'\'\',\'\'\'||a.CITY_CODE||\'\'\',\'\'\'||a.CUST_ID||\'\'\',\'\'\'||a.PAY_NAME||\'\'\',\'\'\'||a.PAY_MODE_CODE||\'\'\',\'\'\'||a.CONTRACT_NO||\'\'\',\'\'\'||a.REMOVE_TAG||\'\'\',\'\'\'||a.OPEN_DATE||\'\'\',\'\'\'||a.UPDATE_TIME||\'\'\',\'\'\'||a.UPDATE_DEPART_ID||\'\'\',\'\'\'||a.UPDATE_STAFF_ID||\'\'\',\'\'\'||a.NET_TYPE_CODE||\'\'\',\'\'\'||a.SCORE_VALUE||\'\'\',\'\'\'||a.CREDIT_CLASS_ID||\'\'\',\'\'\'||a.BASIC_CREDIT_VALUE||\'\'\',\'\'\'||a.CREDIT_VALUE||\'\'\',\'\'\'||a.CREDIT_CONTROL_ID||\'\'\',\'\'\'||a.DEBUTY_USER_ID||\'\'\',\'\'\'||a.DEBUTY_CODE||\'\'\',\'\'\'||a.REMOVE_DATE||\'\'\',\'\'\'||a.PROVINCE_CODE||\'\'\')\' istsql '
#	'from uop_actself._domain.tf_f_account@toactself._domain a, uop_actself._domain.tf_f_payrelation@toactself._domain b where TO_CHAR(sysdate,'YYYYMM') between b.start_cyc_id and b.end_cyc_id and a.user_id = b.user_id and b.user_id in (self._user_id)'
#	' union all '
#	'select distinct \'insert into tf_f_user_product values (\'\'\'||PARTITION_ID||\'\'\',\'\'\'||USER_ID||\'\'\',\'\'\'||PRODUCT_MODE||\'\'\',\'\'\'||PRODUCT_ID||\'\'\',\'\'\'||BRAND_CODE||\'\'\',\'\'\'||START_DATE||\'\'\',\'\'\'||END_DATE||\'\'\',\'\'\'||ITEM_ID||\'\'\',\'\'\'||USER_ID_A||\'\'\',\'\'\'||PROV_CODE||\'\'\')\' istsql '
#	'from uop_actself._domain.tf_f_user_product@toactself._domain where user_id in (self._user_id)'
#	' union all '
#	'select distinct \'insert into tf_f_user_member values (\'\'\'||PARTITION_ID||\'\'\',\'\'\'||USER_ID||\'\'\',\'\'\'||MEMBER_ROLE_CODE||\'\'\',\'\'\'||MEMBER_ROLE_TYPE||\'\'\',\'\'\'||MEMBER_ROLE_ID||\'\'\',\'\'\'||MEMBER_ROLE_NUMBER||\'\'\',\'\'\'||MEMBER_ROLE_SHORTNUM||\'\'\',\'\'\'||START_DATE||\'\'\',\'\'\'||END_DATE||\'\'\',\'\'\'||UPDATE_TIME||\'\'\',\'\'\'||UPDATE_DEPART_ID||\'\'\',\'\'\'||UPDATE_STAFF_ID||\'\'\',\'\'\'||DISCNT_PRIORITY||\'\'\',\'\'\'||RELATION_TYPE_CODE||\'\'\',\'\'\'||ITEM_ID||\'\'\',\'\'\'||PROV_CODE||\'\'\')\' istsql '
#	'from uop_actself._domain.tf_f_user_member@toactself._domain where user_id in (self._user_id) or member_role_id in (self._user_id)'
#	)


a=userInfo()
a.setUserId('123123123')
a.setDomain('1')
a.importInfo()
