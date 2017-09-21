#coding = utf-8

import time
import sys
sys.path.append('/ngbss/credit/practice/code')
from autobase.Dao.dbPool import dbPool
from autobase.baseHelper.baseHelper import baseUtils as utils
from autobase.pyLog.performanceLog import perfLog as perfLog
from src.utils.workUtility.tradeUtility import tradeUtility
from src.utils.userInfo.userMember import userMember
from src.utils.commonFunction.common import commFunc
from waferslim.converters import convert_arg, convert_result, StrConverter
_STR_CONVERTER = StrConverter()

common = commFunc()

#性能日志统计
def exe_time(func):
	def time_calc(self,*args, **kargs):
		t0 = time.time()
		#othertradeRelate.logTrace.info("%s, Function[%s] start" %(time.strftime("%X", time.localtime()), func.__name__))
		back = func(self,*args, **kargs)
		#othertradeRelate.logTrace.info("%s, Function[%s] end" % (time.strftime("%X", time.localtime()), func.__name__))
		othertradeRelate.logTrace.info("%.5fs taken for Function[%s]" % (time.time() - t0, func.__name__))
		return back
	return time_calc

class creditValueEval(object):

	is_firstExe = True

	def __init__(self):
		self.user_id = ''
		self.region = '1'
		self.logOn = None
		self.pool = None
		self._m_userMember = None
		self._tradeUtility = None
		self.is_manual = 1
		self.is_asyn = 0
		self.ywTradecode = ''

	def setCase_name(self, case_name):
		pass

	def setRegion(self, region):
		self.region = region
		if self.pool is None:
			self._m_userMember = userMember()
			self._tradeUtility = tradeUtility()
			self.logOn = perfLog.getLogByconf_instance("cbg")
			self._tradeUtility.logTrace = dbPool.logTrace = self.logOn
			self.pool = utils.db_getInstance(region)
			self._m_userMember.pool = self._tradeUtility.pool = self.pool
			self._tradeUtility.m_user = self._m_userMember
		else:
			self.logOn.info("dbPool is instantiated, here passed!")

	def setUser_id(self, user_id):
		self.user_id = user_id

	def setIs_manual(self, is_manual):
		self.is_manual = is_manual

	def setIs_asyn(self, is_asyn):
		self.is_asyn = is_asyn

	def data_preparation(self):
		if(self.is_manual == '0'):
			pass
		else:
			#清理数据
			param = {"user_id":self.user_id}
			self.pool.execDelete("ti_o_ywtocredit", param)
			self.pool.execDelete("tf_f_user_credit", param)
			self.pool.commit()
			#插入数据
			self.ywTradecode = common.getconstParam("tradeTypeCode")["OPEN_ACCTOUNT"]
			self._tradeUtility.setYWtoCredit(self.user_id, self.ywTradecode)
			self.pool.commit()
			self.logOn.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

	def getResult(self):
		rst_userCredit, rst_ywNorm, special_pro = [], [], []
		#获取特殊产品列表
		special_pro = common.getconstParam("special_product")
		self._m_userMember.loadData(self.user_id)
		creditValueEval.validation()
		rst_userCredit = self._tradeUtility.getUserCredit(self.user_id, 1, self._m_userMember.provinceCode, self.ywTradecode)
		if(len(rst_userCredit) == 0):
			return 0,"tf_f_user_credit is null"
		self.logOn.info("[%s] in [tf_f_user_credit], credit_value : %s" %(self.user_id, rst_userCredit[0]["credit_value"]))
		#用户是否订购特殊属性
		param_creditValue = self._tradeUtility.isOrderUserParam(self.user_id, '31110012')
		self.logOn.info("[%s] in [tf_f_user_param] param_id [31110012] ,param_value : %s" %(self.user_id, param_creditValue))
		#如果是继承芝麻信用的2i产品需要特殊处理
		if(self._m_userMember.productid in special_pro 
			and 
			param_creditValue is not None):
			if(rst_userCredit[0]["credit_value"] == int(param_creditValue)):
				return "1"
			else:
				return "0"
		else:
			if(rst_userCredit[0]["credit_value"] == 0):
				return "1"
			else:
				return "0"

	@staticmethod
	def validation():
		if(creditValueEval.is_firstExe):
			interval = 5
			creditValueEval.is_firstExe = False
		else:
			interval = 5
		time.sleep(interval)

	def compare(self):
		self.data_preparation()
		return self.getResult()
