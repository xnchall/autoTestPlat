#coding = utf-8
#
#baseHelper.py是辅助baseauto底层功能实现的方法集合

import os
import subprocess
import time
import sys
sys.path.append('/ngbss/credit/practice/code')
from autobase.analyzeConf.analyzeConf import ParseConf
from autobase.Dao.dbPool import dbPool
from src.utils.commonFunction.common import commFunc
parseConf = ParseConf()
common = commFunc()
import logging

class baseUtils():

	file_result = ''

	@staticmethod
	def get_infoFromConf(node, subNode):
		#解析拥有子节点配置
		try:
			return parseConf.getSectInfo(node, subNode)
		except Exception as e:
			logging.error("get conf is error!")
			raise e

	@staticmethod
	def get_singleFactorFromConf(node):
		#解析没有子节点配置
		try:
			return parseConf.getSectInfo(node)
		except Exception as e:
			logging.error("get conf is error!")
			raise e
#-------------------------------act库------------------------------------
	@staticmethod
	def get_dbInfoByConf():
		#获取一个默认节点，作为数据库默认链接库
		return parseConf.getSectInfo('TACT1')

	@staticmethod
	def set_regionOfDbInfo(region, db_info):
		if(region == ''):
			logging.info("使用默认数据库act1!")
		else:
			db_info['user'] = "UOP_ACT" + str(region)
			db_info['passwd'] = "UOP_ACT" + str(region)
			db_info['dbName'] = "tact" + str(region)
		return db_info

	@staticmethod
	def db_getInstance(region='1'):
		#oracle 数据库操作接口
		pool_oracle = dbPool.get_instance(baseUtils.set_regionOfDbInfo(region, baseUtils.get_dbInfoByConf()))
		return pool_oracle
#-------------------------------------------------------------------

#--------------------------mysql------------------------------------
	@staticmethod
	def mysql_getInstance(dbType='MYSQL'):#参数默认值设置为mysql
		#mysql 数据库操作接口
		# db_info = baseUtils.get_singleFactorFromConf(dbType)
		# pool_mysql = dbPool(db_info).setPool(db_info)
		pool_mysql = dbPool.get_instance(baseUtils.get_singleFactorFromConf(dbType))
		return pool_mysql

	@staticmethod
	def createReport(param):
		sql = ""
		pool = baseUtils.mysql_getInstance()
		row_number = pool.execInsert(sql,param)
		if(row_number > 0):
			logging.info("create report successfully!")
		else:
			logging.error("Unknow error")
#-------------------------------------------------------------------


#-------------------------------crm库-------------------------------
#---------为crm库封装，之所以copy，调用地方太多，麻烦一次-----------
	@staticmethod
	def get_crmDBInfoByConf():
		return parseConf.getSectInfo('CRM1')

	@staticmethod
	def set_regionForCrm(region, db_info):
		if(str(region) == '' ):
			logging.info("使用默认数据库crm1!")
		else:
			db_info['user'] = "UOP_CRM" + str(region)
			db_info['passwd'] = "UOP_CRM" + str(region)
			db_info['dbName'] = "tcrm" + str(region)
			return db_info

	@staticmethod
	def crmDb_getInstance(region = '1'):
		pool_crm = dbPool.get_instance(baseUtils.set_regionForCrm(region, baseUtils.get_crmDBInfoByConf()))
		return pool_crm
#-------------------------------------------------------------------
#-------------------------------------------------------------------其他方法
	@staticmethod
	def getClass(Class):
		return Class.__class__.__name__

	@staticmethod
	def find_sqlFile(path, fileCase):
		"""递归模糊查找目标文件"""
		#os.chdir(path)
		dir_dict = []
		is_continue = False #是否继续查找
		for fileName in os.listdir(path):
			filePath = os.path.join(path, fileName)
			if(os.path.isfile(filePath) and fileCase in fileName):
				baseUtils.file_result = fileName
				is_continue = False
				break
			elif(os.path.isdir(filePath)):
				is_continue = True
				dir_dict.append(filePath)
		if(is_continue):
			for i in range(len(dir_dict)):
				if(baseUtils.file_result == ''):
					baseUtils.find_sqlFile(dir_dict[i], fileCase)
				else:
					break

	@staticmethod
	def reflashTimestamp(interval):
		#刷新时间戳
		start_time = time.time()
		cmd = "stouch /ngbss1/credit/data/etc/lock/PARA_NOTIFY_FILE"
		logging.info("---------------------------------------")
		while True:
			end_time = time.time()
			if((end_time - start_time) % interval == 0):
				subprocess.Popen(cmd, cwd="/ngbss/credit/", shell=True)
				logging.info("reflash timestamp successfully!")
				logging.info("---------------------------------------")

	@staticmethod
	def setLogName(logFileName):
		#设置生成日志文件名
		path = common.getCATinit("path_dict")
		base_name = path["log_path"] + logFileName
		date = time.strftime('%Y%m%d',time.localtime(time.time())) + '.log'
		return base_name + date
