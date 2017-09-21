#coding = utf-8

#datadeal自动化测试数据初始化类
#1.前端wiki字段is_sync控制：
#	1  ：程序插入sql文件脚本数据
#	0  ：手工插入wiki输入数据
#2.插入自动化测试基础数据
#3.数据销毁
#4.数据脚本名称命名规则：
#	进程名_通道_省份_自动化用例名.sql
#	举例：cbg_c220_p34_speedLimit.sql

import os
import datetime
import sys
import subprocess
import multiprocessing

sys.path.append('/ngbss/credit/practice/code')
from autobase.baseHelper.baseHelper import baseUtils as utils
import autobase.CATinit.CATinit as CAT_init
# from src.utils.commonFunction.common import commFunc

class dataDeal(object):
	"""批量执行sql文件时候用例名称可以为空，单个导入sql文件不能为空"""
	def __init__(self, caseName='', region='1'):
		self.caseName = caseName
		self.region = region
		self.file_result = ''#记录文件查找返回值（值是文件名）

	def get_caseName(self):
		"""获取自动化用例名称"""
		return self.caseName

	def find_sqlFile(self, path, fileCase):
		"""递归模糊查找目标文件"""
		#os.chdir(path)
		dir_dict = []
		is_continue = False #是否继续查找
		for fileName in os.listdir(path):
			filePath = os.path.join(path, fileName)
			if(os.path.isfile(filePath) and fileCase in fileName):
				self.file_result = fileName
				is_continue = False
				break
			elif os.path.isdir(filePath):
				is_continue = True
				dir_dict.append(filePath)
		if(is_continue):
			for i in range(len(dir_dict)):
				if(self.file_result == ''):
					self.find_sqlFile(dir_dict[i], fileCase)
				else:
					break

	def get_allFiles(self, node, subNode):
		dataDir = utils.get_infoFromConf(node, subNode)
		return dataDir, os.listdir(dataDir)

	def stat_info():
		"""
		三个维度：时间 +　数量　+ 循环次数
		1.统计执行一个sql文件需要时间
		2.统计执行完成所有sql文件需要时间
		3.统计执行sql文件成功数量与失败数量
		后续考虑封装一个性能分析类。
		"""
		pass

	#方式一：采用shell命令执行
	#方式二：采用cx_oracle驱动执行
	def execute_single(self):
		try:
			dataDir = self.get_allFiles('dataDealDir','practice_dataDir')
			self.find_sqlFile(dataDir[0], self.caseName)
			if(self.file_result == ''):
				raise TypeError("there don't have such file!")
			else:
				sqlplus = 'sqlplus uop_act1/uop_act1@tact1'.replace('act1', 'act'+str(self.region))
				pre_echo = 'echo \'@' + CAT_init.path_dict['dataDeal_path'] + '/' + self.file_result + '\'| '
				cammand = pre_echo + sqlplus
				subprocess.Popen(cammand, shell=True)
				return True
		except Exception as e:
			raise TypeError('function[execute_single] is error!')

	def execute_batch(self, file_list):
		try:
			for i in range(len(file_list)):
				sqlplus = 'sqlplus uop_act1/uop_act1@tact1'.replace('act1', 'act'+str(self.region))
				pre_echo = 'echo \'@' + CAT_init.path_dict['dataDeal_path'] + file_list[i] + '\'| '
				cammand = pre_echo + sqlplus
				subprocess.Popen(cammand, shell=True)
			return True
		except Exception as e:
			raise TypeError('function[execute_batch] is error!')

	def execute_batchByProcesses(self):
		"""
		批量导入所有自动化用例需要的基础用户资料
		一个用例一个sql文件脚本，那基础数据文件很多。将所有脚本分为n部分，分别采用n个进程并行执行插入。
		进程池计算原理：（3 ，2都是可配置的ACTinit.py）
		1.sql文件总数小于3时，依然采用单进程导入数据。
		2.sql文件总数大于5时，[总数/5]向上取整得到进程池大小n，然后前n-1个进程都是插入500条sql，最后一个进程插入剩余sql文件。
		"""
		file_list = self.get_allFiles('dataDealDir','practice_dataDir')[1]
		is_len = len(file_list)
		if(is_len < CAT_init.constant_dict['PROCESS_SPECIAL']):
			self.execute_batch(file_list)
		else:
			process_tool = CAT_init.constant_dict['SUBPROCESS_LIMIT']
			step = is_len/process_tool
			if(isinstance(step, float)):
				step = int(step) + 1
			batch_sql = []
			for i in range(0, is_len, process_tool):#0到is_len,每次间隔process_tool
				batch_sql.append(file_list[i:i+process_tool])
			#创建动态进程池
			multi_pool = multiprocessing.Pool(processes=step)
			#并发执行
			for i in range(step):
				result = multi_pool.apply_async(self.execute_batch, (batch_sql[i], ))
			multi_pool.close()
			multi_pool.join()
			if(result.successful()):
				print('sucessful!')


# c = dataDeal('othertraderelated')
# # a = c.get_allFiles('dataDealDir', 'practice_dataDir')
# # c.find_sqlFile(a[0],'QQQQQQQQ')
# # print('&&&&&&&&&&7'+c.file_result)
# # print(c.get_allFiles('dataDealDir','practice_dataDir'))
# c.execute_single()
