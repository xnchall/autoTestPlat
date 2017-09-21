#coding = utf-8

import sys
sys.path.append('/ngbss/credit/practice/code')
from src.utils.workUtility.workUtility import workUtility
import logging

class tradeUtility(workUtility):
	"""继承workUtility"""
	def __init__(self):
		super(tradeUtility, self).__init__()#继承workUtility类属性

	#造欠费
	def setBill(self, user_id):
		self.m_user.loadData(user_id)#调用父类实例方法
		sql = "insert into ts_b_bill \
				(EPARCHY_CODE, NET_TYPE_CODE, SERIAL_NUMBER, BILL_ID, ACCT_ID, USER_ID, PARTITION_ID, CYCLE_ID, INTEGRATE_ITEM_CODE, FEE, BALANCE, PRINT_FEE, B_DISCNT, A_DISCNT, ADJUST_BEFORE, ADJUST_AFTER, LATE_FEE, LATE_BALANCE, LATECAL_DATE, CANPAY_TAG, PAY_TAG, BILL_PAY_TAG, VERSION_NO, UPDATE_TIME, UPDATE_DEPART_ID, UPDATE_STAFF_ID, CHARGE_ID, WRITEOFF_FEE1, WRITEOFF_FEE2, WRITEOFF_FEE3, RSRV_FEE1, RSRV_FEE2, RSRV_FEE3, RSRV_INFO1, RSRV_INFO2, DESC_OWE_TAG, BACKUP_INFO, ROLL_BACK_INFO, CITY_CODE, PROVINCE_CODE) \
				values \
				(:eparchy_code, :net_type_code, :serial_number, f_sys_getseqid(:eparchy_code,'seq_trade_id'), :acct_id, :user_id, mod(:acct_id, 10000), '201701', '24000', '100000000', '88888888', '0', '0', '0', '0', '0', '0', '0', null, '1', '0', '0', '0', to_date('01-05-2015 22:49:36', 'dd-mm-yyyy hh24:mi:ss'), null, null, f_sys_getseqid(:eparchy_code,'seq_trade_id'), null, null, null, null, null, null, null, null, '0', null, null, :city_code, :province_code)"
		param = {
				":eparchy_code":self.m_user.eparchyCode, 
				":net_type_code":self.m_user.netTypeCode, 
				":serial_number":self.m_user.serialNumber, 
				":acct_id":self.m_user.acct_id, 
				":user_id":user_id, 
				":city_code":self.m_user.cityCode, 
				":province_code":self.m_user.provinceCode
				}
		self.pool.execInsert(sql, param)
		self.pool.commit()
		logging.info("[ts_b_bill]:[%s] , set bill successfully!" %user_id)

	#造业务工单
	def setYWtoCredit(self, user_id, tradeTypeCode):
		self.m_user.loadData(user_id)
		sql = "insert into ti_o_ywtocredit ( \
					USER_ID , TRADE_ID , TRADE_TYPE_CODE , PROCESS_TAG , \
					REMARK ,UPDATE_STAFF_ID , UPDATE_DEPART_ID, UPDATE_TIME , \
					PROCESS_TIME , PROCESS_REMARK , PRODUCT_ID , MONEY , \
					ROAM_FLAG , RSRV_STR1 , RSRV_STR2 , RSRV_STR3 , \
					RSRV_STR4 , RSRV_STR5 , PROVINCE_CODE ) \
					values \
					( \
					:USER_ID, f_sys_getseqid(0010,'seq_trade_id'), :TRADETYPECODE, '0', \
					'信用度评估-自动化测试', 'credit', 'credit', sysdate , \
					sysdate , null, :PRODUCT_ID, 0, \
					0, 1, null, null, \
					null, null, :PROVINCE_CODE) "

		param = {
				":USER_ID":user_id, ":TRADETYPECODE":tradeTypeCode, 
				":PRODUCT_ID":self.m_user.productid, ":PROVINCE_CODE":self.m_user.provinceCode
				}
		self.pool.execInsert(sql, param)
		self.pool.commit()
		logging.info("[ti_o_ywtocredit]:[%s] , set yw_creditWork successfully!" %user_id)

	#用户是否有每个属性
	def isOrderUserParam(self, user_id, param_id):
		rst = 0
		sql = "select param_value from tf_f_user_param \
				WHERE user_id=:USER_ID and partition_id=mod(user_id, 10000) \
				and param_id=:PARAM_ID and sysdate between start_date and end_date "
		param = {":USER_ID":user_id, ":PARAM_ID":param_id}
		rst = self.pool.execQuery(sql, param)
		if(len(rst) > 0):
			return rst[0]["param_value"]
		else:
			return None

