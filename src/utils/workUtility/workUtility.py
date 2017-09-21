#coding=utf-8

import time
import sys
#import cx_Oracle
sys.path.append('/ngbss/credit/practice/code')
from autobase.Dao.dbPool import dbPool
from src.utils.userInfo.userMember import userMember
from src.utils.commonFunction.common import commFunc
import logging

class workUtility():
	"""工单表操作类"""

	#logTrace = None

	def __init__(self):
		print("#########BEGIN##########")
		self.pool = None #数据库操作句柄
		self.m_user = None #用户基础数据操作句柄
		self.commonF = commFunc()#实例化操作接口

	def insertCreditwork(self, user_id, trade_type_code, is_relation=0):

		logging.info("FUNCTION INSERTCREDITWORK BEGIN !")
		if(trade_type_code == '' and user_id == ''):
			logging.error("function param is NULL, plz check!")
			return False
		self.m_user.loadData(user_id)
		sql = "insert into ti_o_credit_work values (f_sys_getseqid(:EPARCHY_CODE,'seq_trade_id'), f_sys_getseqid(:EPARCHY_CODE,'seq_trade_id'), :TRADE_TYPE_CODE,:USER_ID, '1' ,'0' ,'0' ,sysdate,sysdate ,'0' ,:MANAGE_TAG, '0' ,'0' ,'20000',NULL ,sysdate ,'CREDIT00' , 'CREDI', NULL, '0', '0', '0', NULL, :EPARCHY_CODE, :NET_TYPE_CODE, NULL, :PROVINCE_CODE, '0')"
		#MANAGE_TAG_0 = "0000000000" #生成不关联工单
		#MANAGE_TAG_1 = "0100000000" #生成关联工单
		param = {":EPARCHY_CODE":self.m_user.eparchyCode, ":TRADE_TYPE_CODE":trade_type_code, 
				":USER_ID":self.m_user.user_id, ":NET_TYPE_CODE":self.m_user.netTypeCode, ":PROVINCE_CODE":self.m_user.provinceCode, ":MANAGE_TAG":self.commonF.getconstParam("NOT_RELATE_WORK")}
		if(is_relation == 1):#产生关联工单
			param[":MANAGE_TAG"] = self.commonF.getconstParam("BKG_RELATE_WORK")
			try:
				logging.debug("SQL : %s" %(sql % locals()))
				num = self.pool.execInsert(sql, param)
			except cx_Oracle.Error as e:
				self.pool.rollback()
				logging.error("cx_Oracle.Error:%s" %e)
				raise TypeError("insert ti_o_credit_work error!")
		else:
			num = self.pool.execInsert(sql, param)
			logging.info("insert [ti_o_credit_work] successfully")
		self.pool.commit()
		logging.debug("insert [ti_o_credit_work] data successfully: %s" %num)
		logging.info("FUNCTION INSERTCREDITWORK END !")

	def getCreditwork(self, user_id, trade_type_code):
		v_list = []
		#self.m_user.loadData(clause["user_id"])
		#if(clause["trade_type_code"] == self.commonF.getconstParam(tradeType[])
		sql = "select user_id, process_tag, process_remark, manage_tag from ti_o_credit_work a WHERE user_id=:USER_ID and trade_type_code=:TRADE_TYPE_CODE order by exec_time desc"
		param = {":USER_ID":user_id, ":TRADE_TYPE_CODE":trade_type_code}
		try:
			logging.debug("SQL : %s" %(sql % locals()))
			v_list = self.pool.execQuery(sql, param)
		except cx_Oracle.Error as e:
			logging.error("cx_Oracle.Error:%s" %e)
			raise
		logging.info("FUNCTION GETCREDITWORK END !")
		return v_list

	def deleteCreditwork(self, user_id, trade_type_code):
		sql = "delete from ti_o_credit_work where user_id=:USER_ID and trade_type_code=:TRADE_TYPE_CODE "
		param = {":USER_ID":user_id, ":TRADE_TYPE_CODE":trade_type_code}
		try:
			logging.debug("SQL : %s" %(sql % locals()))
			num = self.pool.executeUD(sql, param)
		except cx_Oracle.Error as e:
			self.pool.rollback()
			logging.error("cx_Oracle.Error:%s" %e)
			raise
		self.pool.commit()
		logging.debug("delete [ti_o_credit_work] history data successfully: %s" %num)

	def getAuditWork(self, user_id):
		param = {":USER_ID" : user_id}
		sql = "select user_id, rsrv_str1 FROM tf_o_credit_audit WHERE user_id=:USER_ID and process_type=1"
		return self.pool.execQuery(sql, param)

	def getUserCredit(self, user_id, credit_type_code, provinceCode, trade_type_code):
		sql = "select credit_value from tf_f_user_credit \
				WHERE user_id=:USER_ID and partition_id=mod(user_id, 10000) \
				and credit_type_code=:CREDIT_TYPE_CODE and province_code=:PROVINCECODE \
				and trade_type_code=:TRADE_TYPE_CODE"
		param = {
				":USER_ID":user_id, ":CREDIT_TYPE_CODE":credit_type_code, 
				":PROVINCECODE":provinceCode, ":TRADE_TYPE_CODE":trade_type_code
				}

		creditValue = self.pool.execQuery(sql, param)
		if(creditValue is not None):
			return creditValue
		else:
			logging.error("get user creditValue error, because of creditValue is None")
			return None
#utility = workUtility()
# utility.deleteCreditwork('1114082824660388', '7301')
# utility.insertCreditwork('1114082824660388', '7301')
# print(utility.getCreditwork('1114082824660388', '7301'))
#print(utility.log_name())
# print("over!")