#coding = utf-8

import time
import sys
sys.path.append('/ngbss/credit/practice/code')
from autobase.Dao.dbPool import dbPool
from autobase.baseHelper.baseHelper import baseUtils
from autobase.dataDeal.dataDeal import dataDeal

from waferslim.converters import convert_arg, convert_result, StrConverter
_STR_CONVERTER = StrConverter()


class speedLimit(object):

	def __init__(self):
		super(speedLimit, self).__init__()
		self.pool = None
		self._user_id = ''
		self._case_name = ''
		self._is_manual = 0
		self._is_asyn = 0
		self._policy = '001'
		self._region = '1'

	@convert_arg(using=_STR_CONVERTER)
	def setUser_id(self, user_id):
		self._user_id = user_id

	@convert_arg(using=_STR_CONVERTER)
	def setCase_name(self, case_name):
		self._case_name = case_name

	@convert_arg(to_type=int)
	def setIs_manual(self, is_manual):
		self._is_manual = is_manual

	@convert_arg(to_type=int)
	def setIs_asyn(self, is_asyn):
		self._is_asyn = is_asyn

	@convert_arg(using=_STR_CONVERTER)
	def setPolicy(self, policy):
		if policy:
			self._policy = policy
		else:
			pass

	@convert_arg(to_type=int)
	def setRegion(self, region):
		self._region = region
		if self.pool is None:
			utils = baseUtils()
			self.pool = dbPool.get_instance(utils.set_regionOfDbInfo(region, utils.get_dbInfoByConf()))
		else:
			print("dbPool is instantiated, here passed!")

	@convert_result(using=_STR_CONVERTER)
	def compare(self):
		self.isHand()
		self.isAsyn()
		rst={}
		flag = 0
		while(1==1):
			rst = self.getRst()
			if(len(rst) >= 1):
				break
			time.sleep(1)
			flag = flag + 1
			if(flag > 2):
				break
		if(flag > 2):
			return "the process miss your data!"

		if(rst[0]['process_tag'] == '1'):
			print("this case process successfully,[ti_o_credit_speedlimit_log].process_tag=%s" %(rst[0]['process_tag']))
			return "1"
		elif(rst[0]['process_tag'] == '2'):
			print("this case process false,[ti_o_credit_speedlimit_log].process_tag=%s" %(rst[0]['process_tag']))
			return "2",rst[0]['remark']
		else:
			print("work don't processed,[ti_o_credit_speedlimit_log].process_tag=%s" %(rst[0]['process_tag']))
			return "0"

	def isHand(self):
		if(self._is_manual == 1):#手工输入
			self.insertSql(self._user_id)
		else:#调用准备好的sql文件插入oracle
			exe_sqlScript = dataDeal(self._region, self._case_name)
			exe_sqlScript.execute_single()
			print("insert sql script successfully!")
			

	def isAsyn(self):
		if(self._is_asyn == 1):
			pass#subprocess()调用，多进程并行，实现异步处理
		else:
			pass#串行

	def insertSql(self, user_id, sql_templet=""):
		"""
			放在封装单独的类，提供公共业务方法（根据业务公共方法全放进去，类似于信控utility），两个方法。
			第一个：参数是user_id，和模板sql。
			第二种：参数是user_id和工单类型，根据工单类型自动匹配版本。
		"""
		self.delete_history()
		sql1 = "select eparchy_code,province_code from tf_f_user where user_id = :user_id and remove_tag='0' "
		param1 = {":user_id":user_id}
		rst1 = self.pool.execQuery(sql1, param1)
		if len(rst1):
			print("eparchy_code:%s ,province_code:%s" %(rst1[0]['eparchy_code'], rst1[0]['province_code']))
		else:
			return("user info is null!")

		sql2 = "insert into \
			ti_o_credit_speedlimit_work \
			(TRADE_ID, USER_ID, PARTITION_ID, TRADE_TYPE_CODE, START_DATE, END_DATE, \
			EXEC_TIME, LIMIT_SPEED, CUR_VALUE, LIMIT_VALUE, PROCESS_TAG, UPDATE_TIME, MANAGE_TAG, REMARK, RSRV_STR1, RSRV_STR2, RSRV_STR3, NET_TYPE_CODE, EPARCHY_CODE, PROVINCE_CODE) \
			values \
			(f_sys_getseqid(0010,'seq_trade_id'), :user_id, mod(:user_id,10000), '0', sysdate, TO_DATE( TO_CHAR(last_day(sysdate),'YYYYMMDD') ||'235959' ,'YYYY-MM-DD HH24:MI:SS'), sysdate, :policy, '22548578304', '1073741824', '0', sysdate, null, '', '7151', null, null, '50', :eparchy_code, :province_code)"
		param2 = {":user_id":user_id, ":policy":self._policy,":eparchy_code":rst1[0]['eparchy_code'], ":province_code":rst1[0]['province_code']}
		rst2 = self.pool.execInsert(sql2, param2)
		self.pool.commit()
		if(rst2 == 1):
			print("insert [ti_o_credit_speedlimit_work] successfully!")

	def getRst(self):
		print("getting [ti_oh_credit_speedlimit_work.process_tag]")
		sql = "select process_tag,remark from ti_oh_credit_speedlimit_work where user_id = :USER_ID and (sysdate between start_date and end_date) order by exec_time desc "
		param = {":USER_ID":self._user_id}
		return self.pool.execQuery(sql,param)

	def delete_history(self):
		"""先删除数据，在捞取数据!"""
		sql_d = "delete from ti_oh_credit_speedlimit_work WHERE user_id=:USER_ID and PARTITION_ID=mod(:USER_ID,10000)"
		param_d = {":USER_ID":self._user_id}
		self.pool.commit()
		num = self.pool.executeUD(sql_d,param_d)
		print("delete [ti_oh_credit_speedlimit_work] history data successfully: %s" %num)

	def execute(self):
		print("#########execute##############")

	def reset(self):
		#self.pool = None
		print("**********reset***************")