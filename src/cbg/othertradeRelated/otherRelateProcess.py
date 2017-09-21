#coding = utf-8

import time
import inspect
import sys
sys.path.append('/ngbss/credit/practice/code')
from autobase.Dao.dbPool import dbPool
from autobase.baseHelper.baseHelper import baseUtils as utils
from autobase.dataDeal.dataDeal import dataDeal
from autobase.pyLog.logCtrl import baseLog
from src.utils.workUtility.tradeUtility import tradeUtility
from src.utils.userInfo.userMember import userMember
from src.utils.commonFunction.common import commFunc
from src.utils.dataStore.dataStore import dataStore
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

class othertradeRelate(object):
	logTrace = None#baseLog.getLogByconf_instance("root")
	is_firstExe = True
	"""docstring for othertradeRelate"""
	def __init__(self):
		self.pool = None#act库数据库连接池
		self.pool_crm = None#crm库数据链接池
		self._dataStore = None#基础数据类，这里用到了数据清理
		self._m_userMember = None
		self._workUtility = None
		self._user_id = ''
		self._trade_type_code = ''
		self._case_name = ''
		self._is_manual = 1
		self._is_asyn = 0
		self._region = '1'
		self._user_list = []#所有成员用户列表--成员类型全是int
		self.work_number = 0

	@staticmethod
	def get_current_function_name():
		return inspect.stack()[1][3]
		# print("%s.%s"%(utils.getClass(self), self.get_current_function_name()))

	def setCase_name(self, case_name):
		self._case_name = case_name

	def setRegion(self, region):
		self._region = region
		if self.pool is None:
			self._m_userMember = userMember()
			self._workUtility = tradeUtility()
			othertradeRelate.logTrace = baseLog.getLogByconf_instance(self._case_name)
			self._workUtility.logTrace = dbPool.logTrace = othertradeRelate.logTrace
			self.pool = utils.db_getInstance(region)
			self.pool_crm = utils.crmDb_getInstance(region)
			self._m_userMember.pool = self._workUtility.pool = self.pool
			self._workUtility.m_user = self._m_userMember
			#封装一个公共基类，给所有测试用例继承
		else:
			othertradeRelate.logTrace.info("dbPool is instantiated, here passed!")

	def setUser_id(self, user_id):
		self._user_id = user_id
		self._dataStore = dataStore()
		self._dataStore.pool = self.pool
		self._dataStore.setXnUser(self._user_id, self._region)

	def setTrade_type_code(self, trade_type_code):
		self._trade_type_code = trade_type_code

	def setIs_manual(self, is_manual):
		self._is_manual = is_manual

	def setIs_asyn(self, is_asyn):
		self._is_asyn = is_asyn

	@exe_time
	def data_preparation(self):
		#如果是冒烟测试需要清理数据，导入sql脚本
		if(self._is_manual == '0'):
			self._dataStore.removeBaseData()
			exe_sqlScript = dataDeal(self._case_name, self._region)#在sql脚本中清理历史数据
			exe_sqlScript.exe_sqlScript()
			othertradeRelate.logTrace.info("insert sql script successfully!")
		else:
			#fitnesse数据传输格式被waferslim解析出来类型是string，容易出错
			if(self._m_userMember.isZFCardMinor(self._user_id) is None):#如果是触发用户不是ZF副卡
				user_list = self._m_userMember.getAllMember(self._user_id)
			else:
				user_list = self._m_userMember.getAllMemberByZFminor(self._user_id)
			self._user_list = user_list
			othertradeRelate.logTrace.info(str(user_list))
			for i in range(len(user_list)):
				param = {"user_id":user_list[i]}
				self._workUtility.deleteCreditwork(user_list[i], self._trade_type_code) #清理work表历史数据
				self.pool.execDelete("ts_b_bill", param)#删除历史账单
				self.pool_crm.execDelete("tf_b_trade", param)#删除营业库台账表未竣工工单
			self.pool.commit()#提交删除事务，必须两次，因为删除和插入同一数据会违反事务一致性
			self.pool_crm.commit()
			self._workUtility.insertCreditwork(self._user_id, self._trade_type_code, 0)#0--造非关联工单
			#如果是欠费停机或欠费半停,需要为触发用户造欠费
			tradeTypeCode_map = common.getconstParam("tradeTypeCode")
			if(self._trade_type_code in [tradeTypeCode_map["OWN_STOP"], tradeTypeCode_map["HALF_OWN_STOP"]]):
				self._workUtility.setBill(self._user_id)
				othertradeRelate.logTrace.info("set user bill successfully!")
			#如果是高额停机或高额半停
			if(self._trade_type_code in [tradeTypeCode_map["HIGH_STOP"], tradeTypeCode_map["HALF_HIGH_STOP"]]):
				pass
				#对于紧密融合用户只用造一个用户符合条件，松散融合的所有成员需要满足条件
			self.pool.commit()#提交插入事务
			othertradeRelate.logTrace.info("insert user Info successfully!")
	def isAsyn(self):
		if(self._is_asyn == 1):
			pass#subprocess()调用，多进程并行，实现异步处理
		else:
			pass#串行

	@exe_time
	def getResult(self):
		rst_audit,audit_info,rst_work,work_info,t_user = [],[],[],[],[]
		t_user = self._user_list[:]#不能直接操作原来列表,不存在嵌套列表所以可以这样使用
		userTypeCode = self._m_userMember.getAllRelation(self._user_id)
		m_tradetype = common.getconstParam("tradeTypeCode")
		other_tradeType = [m_tradetype["OWN_STOP"],m_tradetype["HALF_OWN_STOP"],m_tradetype["HIGH_STOP"],m_tradetype["HALF_HIGH_STOP"]]
		#这个校验逻辑确实有点复杂！
		if(self._trade_type_code in other_tradeType):
			if(
				(self._m_userMember.netTypeCode not in ['40','30']) 
				or 
				(common.getconstParam("relationCode")["GOLD"] in userTypeCode)
				):
				othertradeRelate.validation()
				for m in range(len(t_user)):
					work_info = self._workUtility.getCreditwork(t_user[m], self._trade_type_code)#[[{}],[{}]]
					if(len(work_info) == 0):
						continue
					rst_work.append(work_info[0])#{}
				#如若触发用户是50，且关系不是8920，只关心work表的校验
				if(len(rst_work) == 0):
					#按照逻辑应该不会走这里的
					return "[ti_o_credit_work] doesn't exist successful work"
				for n in range(len(rst_work)):
					#判断触发用户，manage_tag是0000000000
					if(
						(str(rst_work[n]["user_id"]) == self._user_id)
						and 
						(rst_work[n]["manage_tag"] == common.getconstParam("NOT_RELATE_WORK"))
						and
						(rst_work[n]["process_tag"] == '1')
						):
						self.work_number += 1
					else:
						if(rst_work[n]["manage_tag"] == common.getconstParam("BKG_RELATE_WORK")):
							self.work_number += 1
				# print("-----------%s.%s-----------"%(utils.getClass(self), self.get_current_function_name()))
				othertradeRelate.logTrace.info("[ti_o_credit_work] : %s"%str(rst_work))
				othertradeRelate.logTrace.info("ti_o_credit_work:%d, user_list_number:%d"%(self.work_number, len(self._user_list)))
				if(self.work_number == len(self._user_list)):
					return 1
				else:
					return 0
			else:
				#触发用户是30和40，并且融合关系不是8920
				#先查询ti_o_credit_work,只有触发用户
				othertradeRelate.validation()
				rst_work = self._workUtility.getCreditwork(self._user_id, self._trade_type_code)
				if((str(rst_work[0]["user_id"]) == self._user_id)
					and
					(rst_work[0]["manage_tag"] == common.getconstParam("NOT_RELATE_WORK"))
					and
					(rst_work[0]["process_tag"] == '1')
					):
					self.work_number += 1
				#再查询tf_o_credit_audit
				t_user.remove(int(self._user_id))#过滤触发用户，因为触发用户工单在ti_o_credit_work
				for x in range(len(t_user)):
					audit_info = self._workUtility.getAuditWork(t_user[x])
					if(len(audit_info) == 0):
						continue
					rst_audit.append(audit_info[0])
				if(len(rst_audit) == 0):
					return 0,"[tf_o_credit_audit] doesn't exist any work"
				othertradeRelate.logTrace.info("[ti_o_credit_work] : %s" %str(rst_work))
				othertradeRelate.logTrace.info("[ti_o_credit_audit] : %s" %str(rst_audit))
				othertradeRelate.logTrace.info("tf_o_credit_audit:%d ,ti_o_credit_work:%d, user_list_number:%d" %(len(rst_audit),self.work_number,len(self._user_list)))
				if(len(rst_audit) + self.work_number == len(self._user_list)):
					return 1
				else:
					return 0
		else:
			othertradeRelate.logTrace.info("TradeTypeCode[%s] doesn't meet the requirement!" %self._trade_type_code)
		return 0

	@staticmethod
	def validation():
		if(othertradeRelate.is_firstExe):
			interval = 10
			othertradeRelate.is_firstExe = False
		else:
			interval = 3
		time.sleep(interval)

	def compare(self):
		self.data_preparation()
		self.isAsyn()
		# param = {}
		# utils.createReport(param)#生成测试报告
		return self.getResult()

	def reset(self):
		#精髓点
		self.work_number = 0
