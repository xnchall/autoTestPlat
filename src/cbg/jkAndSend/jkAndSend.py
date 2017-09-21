#coding = utf-8

import subprocess
import time
import sys
sys.path.append('/ngbss/credit/practice/code')
from autobase.Dao.dbPool import dbPool

from waferslim.converters import convert_arg, convert_result, StrConverter
_STR_CONVERTER = StrConverter()

db_info = {
        'dbType' : "cx_Oracle",
        'host' : "10.124.0.42",
        'user' : "UOP_ACT1",
        'passwd' : "UOP_ACT1",
        'port' : "1521",
        'dbName' : "tact1",
        'charset' : "utf-8"
    }

class jkAndSend(object):

	def __init__(self):
		super(jkAndSend, self).__init__()
		self.pool = dbPool(db_info)
		self._user_id = ''
		self._case_name = ''
		self._is_manual = 0
		self._is_asyn = 0

	@convert_arg(using=_STR_CONVERTER)
	def setUser_id(self, user_id):
		self._user_id = user_id

	@convert_arg(using=_STR_CONVERTER)
	def setCase_name(self, case_name):
		self._case_name = case_name

	@convert_arg(to_type=int)
	def setIs_manual(self, is_hand):
		self._is_manual = is_hand

	@convert_arg(to_type=int)
	def setIs_asyn(self, is_asyn):
		self._is_asyn = is_asyn

	@convert_result(using=_STR_CONVERTER)
	def compare(self):
		# self.insertSql(self._user_id)
		self.isManual()#wiki 设置数据插入方式
		self.isAsyn()#wiki 设置当前case执行方式[串行/异步]
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
			sql = "select process_remark1 from ti_o_jftocredit where user_id=:user_id order by update_time desc"
			param = {":user_id":self._user_id}
			rst = self.pool.execQuery(sql, param)
			return "not fit jkToOpen!",rst[0]["process_remark1"]
		rst = self.getRst()
		if(len(rst) == "0"):
			return "ti_o_credit_work no data"
		elif(rst[0]['process_tag'] == '1'):
			print("this case process successfully,[ti_o_credit_work].process_tag:%s" %(rst[0]['process_tag']))
			return "1"
		elif(rst[0]['process_tag'] == '2'):
			print("this case process false,[ti_o_credit_work].process_tag:%s"  %(rst[0]['process_tag']))
			return "2",rst[0]['process_remark']
		else:
			print("work don't processed,[ti_o_credit_work].process_tag:%s"  %(rst[0]['process_tag']))
			return "1"

	def isManual(self):
		if(self._is_manual == 1):#手工输入
			self.insertSql(self._user_id)
		else:
			pass#调用准备好的sql文件插入oracle

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
		sql1 = "select acct_id,prov_code from tf_f_payrelation where user_id = :user_id and (to_number(to_char(sysdate,'yyyymm')) between start_cyc_id and end_cyc_id) "
		param1 = {":user_id":user_id}
		rst1 = self.pool.execQuery(sql1, param1)
		print("acct_id:%s ,prov_code:%s" %(rst1[0]['acct_id'], rst1[0]['prov_code']))

		sql2 = "insert into TI_O_RECV_CREDIT \
			(TRADE_ID, ACCT_ID, PARTITION_ID, USER_ID, RECOVER_TAG, CANCEL_TAG, BATCH_TAG, WRITEOFF_MODE, RECV_TIME, REMARK, UPDATE_STAFF_ID, UPDATE_DEPART_ID, PROVINCE_CODE, RSRV_STR1, RSRV_STR2, RSRV_STR3) \
			values (f_sys_getseqid(0010,'seq_trade_id'), :acct_id, mod(:acct_id,10000), :user_id, '1', '0', '0', '1', sysdate, '自动化测试数据', 'CREDIT00', 'CREDIT', :pro_code, null, null, null)"
		param2 = {":acct_id":rst1[0]['acct_id'], ":pro_code":rst1[0]['prov_code'], ":user_id":user_id}
		rst2 = self.pool.execInsert(sql2, param2)
		self.pool.commit()
		if(rst2 == 1):
			print("insert [TI_O_RECV_CREDIT] successfully!")

	def getRst(self):
		print("getting [ti_o_credit_work.process_tag]")
		sql = "select process_tag,process_remark from ti_o_credit_work where user_id = :USER_ID order by update_time desc "
		param = {":USER_ID":self._user_id}
		return self.pool.execQuery(sql,param)

	def delete_history(self):
		"""先删除数据，在捞取数据!"""
		sql_d = "delete from ti_o_credit_work WHERE user_id=:USER_ID "
		param_d = {":USER_ID":self._user_id}
		self.pool.commit()
		num = self.pool.executeUD(sql_d,param_d)
		print("delete [ti_o_credit_work] history data successfully: %s" %(num))

	def execute(self):
		print("Execute automatic test system")
		pass
 	
	def reset(self):
		print("Reset automatic test system")
		pass

	def getCur_time(self):
		return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))





		
