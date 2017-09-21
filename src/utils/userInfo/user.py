#conding = utf-8
import sys
sys.path.append('/ngbss/credit/practice/code')
from autobase.Dao.dbPool import dbPool
from autobase.baseHelper.baseHelper import baseUtils as utils
import logging

class User(object):
	"""用户信息基类"""

	swich_flag = True#保证单用户资料日志输出只打一次

	def __init__(self):
		# self.region = (lambda region: '1' if region == '' else region)('1')#测试
		# self.pool = dbPool.get_instance(utils.set_regionOfDbInfo(self.region, utils.get_dbInfoByConf()))
		self.pool = None #数据库操作句柄
		self.user_id = ''
		self.acct_id = ''
		self.cityCode = ''
		self.dummyTag = '' #虚拟用户标识 
		self.custid = ''
		self.serialNumber = ''
		self.brandCode = '' #品牌
		self.netTypeCode = ''
		self.creditValue = 0
		self.creditClass = 0
		self.userTypeCode = ''
		self.productid = 0#产品标识
		self.serviceStateCode = ''
		self.removeTag = ''
		self.stopedDays =0#已停机天数
		self.provinceCode = ''
		self.eparchyCode = ''
		self.openDate = ''
		self.lastStopedDays = ''

	def loadData(self, user_id):
		self.clear()
		self.user_id = user_id
		self.queryData()

	def queryData(self):
		sql = "Select dummy_tag,Cust_Id, Serial_Number, NET_TYPE_CODE, Brand_Code, User_Type_Code, Base_Credit_Value, Credit_Value, Credit_Class,Credit_Control_Id, Product_Id, Service_State_Code, Remove_Tag, Eparchy_Code, City_Code, \
                      Nvl(to_date(to_char(sysdate, 'YYYYMMDD'), 'YYYYMMDD') - to_date(to_char(last_stop_date, 'YYYYMMDD'), 'YYYYMMDD'),0), \
                      Nvl(Round(Sysdate - Pre_Destroy_Date), 0),To_Char(Open_Date, 'YYYYMMDDHH24MISS'), Prepay_Tag, Open_Mode, Province_Code, nvl(to_char(last_stop_date, 'YYYYMMDD'),0),To_Char(Pre_Destroy_Date, 'YYYYMMDDHH24MISS') \
                      From Tf_f_User Where User_Id = :user_id And Partition_Id = Mod(:user_id, 10000) "
		param = {":user_id" : self.user_id}
		reslut = self.pool.execQuery(sql, param)
		if(len(reslut) == 0):
			logging.info('在用户资料表中未找到用户(%s)的记录。' %self.user_id)
			pass
		else:
			self.custid = reslut[0]['cust_id']
			self.dummyTag = reslut[0]['dummy_tag']
			self.serialNumber = reslut[0]['serial_number']
			self.netTypeCode = reslut[0]['net_type_code']
			self.brandCode = reslut[0]['brand_code']
			self.userTypeCode = reslut[0]['user_type_code']
			self.creditValue = reslut[0]['credit_value']
			self.creditClass = reslut[0]['credit_class']
			self.productid = reslut[0]['product_id']
			self.serviceStateCode = reslut[0]['service_state_code']
			self.removeTag = reslut[0]['remove_tag']
			self.eparchyCode = reslut[0]['eparchy_code']
			self.cityCode = reslut[0]['city_code']
			self.provinceCode = reslut[0]['province_code']

		sql_acct = " select acct_id  from tf_f_payrelation where user_id = :user_id and start_cyc_id <= to_number(to_char(sysdate, 'YYYYMM') )  and end_cyc_id >= to_number(to_char(sysdate, 'YYYYMM') ) and default_tag = '1' and act_tag = '1' "
		reslut1 = self.pool.execQuery(sql_acct, param)
		if(len(reslut1) == 0):
			raise TypeError('用户(%s)不存在有效的付费关系。' %self.user_id)
		else:
			self.acct_id = reslut1[0]['acct_id']

		self.printUserInfo()

	def clear(self):
		self.user_id = ''
		self.acct_id = ''
		self.dummyTag = '' #虚拟用户标识 
		self.custid = ''
		self.serialNumber = ''
		self.brandCode = '' #品牌
		self.netTypeCode = ''
		self.creditValue = 0
		self.creditClass = 0
		self.userTypeCode = ''
		self.productid = 0#产品标识
		self.serviceStateCode = ''
		self.removeTag = ''
		self.stopedDays =0#已停机天数
		self.provinceCode = ''
		self.eparchyCode = ''
		self.openDate = ''
		self.lastStopedDays = ''

	def printUserInfo(self):
		if(self.swich_flag):
			logging.info("================")
			logging.info("user_id:%s " %self.user_id)
			logging.info("acct_id:%s " %self.acct_id)
			logging.info("serial_number:%s" %self.serialNumber)
			logging.info("custid:%s " %self.custid)
			logging.info("brand_code:%s" %self.brandCode)
			logging.info("eparchyCode:%s" %self.eparchyCode)
			logging.info("dummytag:%s " %self.dummyTag)
			logging.info("netTypeCode:%s " %self.netTypeCode)
			logging.info("creditValue:%s " %self.creditValue)
			logging.info("creditClass:%s " %self.creditClass)
			logging.info("removeTag:%s " %self.removeTag)
			logging.info("provinceCode:%s " %self.provinceCode)
			logging.info("serviceStateCode:%s " %self.serviceStateCode)
			logging.info("================")
			self.swich_flag = False#精髓