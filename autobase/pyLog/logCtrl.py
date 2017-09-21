#coding = utg-8

import time
import logging
from logging.config import fileConfig
import sys
sys.path.append('/ngbss/credit/practice/code')
from src.utils.commonFunction.common import commFunc


class baseLog(object):

	logTrace_conf = None
	logTrace = None

	def __init__(self, logFileName):
		self.logFile = baseLog.setLogName(logFileName)
		logging.basicConfig(level = logging.DEBUG,
			format = '%(asctime)s [%(module)s]%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
			datefmt='%Y-%m-%d %H:%M:%S',
			filename=self.logFile,
			filemode = 'a'
			)

	@staticmethod
	def setLogByConf(logtrace):
		common = commFunc()
		path = common.getCATinit("path_dict")
		conf_path = path["logConf_path"]
		fileConfig(conf_path)
		logger = logging.getLogger(logtrace)
		return logger

	def setLogDefine(self,name):
		return logging.getLogger(name)

	@staticmethod
	def getLogByconf_instance(logtrace):
		#配置文件单例模式
		#if(baseLog.logTrace_conf is None):
		baseLog.logTrace_conf = baseLog.setLogByConf(logtrace)
		#else:
			#baseLog.logTrace_conf.info("baseLog could be instantiated only once!")
		return baseLog.logTrace_conf

	@staticmethod
	def getLogDefine_instance(logFileName):
		#默认方式单例模式
		if(baseLog.logTrace is None):
			logger = baseLog(logFileName)
			baseLog.logTrace = logger.setLogDefine(logFileName)
		else:
			baseLog.logTrace.info("baseLog could be instantiated only once!")
		return baseLog.logTrace

	@staticmethod
	def setLogName(logFileName):
		#设置生成日志文件名
		common = commFunc()
		path = common.getCATinit("path_dict")
		base_name = path["log_path"] + logFileName
		date = time.strftime('%Y%m%d',time.localtime(time.time())) + '.log'
		return base_name + date