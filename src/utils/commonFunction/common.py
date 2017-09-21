#coding = utf-8

import sys
sys.path.append('/ngbss/credit/practice/code')
import src.utils.creditConstDef.policyDefine as policyDef
import src.utils.creditConstDef.constDef as constDef
import autobase.CATinit.CATinit as actInit
import logging


class commFunc(object):
	"""docstring for ClassName"""

	@staticmethod
	def getpoliceParam(param):
		"""获取策略公共方法policyDefine.py：反射回调机制实现"""
		m_policy = None
		if(param is None or param == ""):
			print("transfer param is abnormal, plz check it!")
			return None
		is_continue = hasattr(policyDef, param)
		if(not is_continue):
			print("param[%s] doesn't set, plz check" %param)
			return None
		else:
			m_policy = getattr(policyDef, param)
		if(m_policy is None):
			print("param[%s] info is None, plz check" %param)
		else:
			print("getted param [%s]:%s sucessfully!" %(param, m_policy["remark"]))
			return m_policy

	@staticmethod
	def getconstParam(param, clause=""):
		"""获取静态常量公共方法constDef.py：反射回调机制实现"""
		m_constDef = None
		if(param is None or param == ""):
			print("transfer param is abnormal, plz check it!")
			return None
		is_continue = hasattr(constDef, param)
		if(not is_continue):
			print("param[%s] doesn't set, plz check" %param)
			return None
		else:
			m_constDef = getattr(constDef, param, clause)
		if(m_constDef is None):
			print("param[%s] info is None, plz check" %param)
		else:
			return m_constDef

	@staticmethod
	def getCATinit(param, clause=""):
		"""获取CATinit.py配置：反射回调机制实现"""
		m_catInit = None
		if(param is None or param == ""):
			print("transfer param is abnormal, plz check it!")
			return None
		is_continue = hasattr(actInit, param)
		if(not is_continue):
			print("param[%s] doesn't set, plz check" %param)
			return None
		else:
			m_catInit = getattr(actInit, param, clause)
		if(m_catInit is None):
			print("param[%s] info is None, plz check" %param)
		else:
			return m_catInit

# comm = commFunc()
# param='sql'
# a = comm.getCATinit(param)
# b=a.replace("uop_actself._domain.", '').replace("@toactself._domain", "").replace("self._user_id","&userid")
# # c=b.replace("@toactself._domain", "")
# # d=c.replace("self._user_id","&userid")
# print(b)