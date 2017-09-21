#coding = utf-8

import os 
import sys
sys.path.append('/ngbss/credit/practice/code')
from autobase.Dao.dbPool import dbPool
from autobase.baseHelper.baseHelper import baseUtils as utils
from src.utils.userInfo.userMember import userMember
from src.utils.commonFunction.common import commFunc
import logging

common = commFunc()

class dataStore(object):
	"""
	从ooracle捞取数据，存入指定目录下，为dataDeal进程提供输入
	使用这个类必须先要调用setXnUser()方法
	"""
	def __init__(self):
		self._Xn_user = ''#不要被名字欺骗了，不一定是虚拟用户，也可以是单用户
		self.pool = None
		self._m_userMember = None

	def setXnUser(self,user_id, region='1'):
		self._Xn_user = user_id
		if(self.pool is None):
			self.pool = utils.db_getInstance(region)#参数设置域，不填则默认使用一域
		self._m_userMember = userMember()
		self._m_userMember.pool = self.pool

	def loadAllUser(self,user_id):
		all_userList = []
		#判断一下是单用户还是融合用户
		#单用户，直接赋值
		if(self._m_userMember.getRelationType(user_id) is None):
			all_userList.append(user_id)
		else:
			all_userList = self._m_userMember.getAllMember(user_id)
		return all_userList

	def getAllUserInfoSql(self):
		sql_str, formated_sql, rst, user_list = "","",[],[]
		sql_str = common.getCATinit("sql")
		formated_sql = sql_str.replace("uop_actself._domain.", "").replace("@toactself._domain", "").replace("self._user_id",":USER_ID")
		user_list = self.loadAllUser(self._Xn_user)
		for i in range(len(user_list)):
			param = {":USER_ID" : user_list[i]}
			rst.append(self.pool.execQuery(formated_sql, param))
		return rst#[[{},{}],[{},{},{}]......]

	def writeSqlInFile(self, case_name=''):
		#将sql列表存入sql文件，为dataDeal提供输入数据
		file_name, new_fileName, insert_sql, path = '','',[],''#insert_sql这个list有点恶心
		#不用考虑目录是否存在，没必要
		# print(common.getCATinit("path_dict")["dataStore_outPutPath"])
		path = common.getCATinit("path_dict")["dataStore_outPutPath"]
		utils.find_sqlFile(path, case_name)
		file_name = utils.file_result
		if(file_name != ''):
			file_size = os.path.getsize(path + file_name)
			#file_txt = open(os.path.join(path,file_name)).read()
			#if(len(file_txt) == 0):
			if(file_size == 0):
				#空文件,不需要创建新文件
				new_fileName = file_name
			else:
				temp_list = file_name.split('.')
				new_fileName = temp_list[0] +  '_new.' + temp_list[1]
		else:
			new_fileName = case_name + '.sql'
		insert_sql = self.getAllUserInfoSql()
		#创建sql文件
		try:
			os.chdir(path)
			logging.info("file output is [%s], file name is [%s]" %(path, new_fileName))
			file_handle = open(new_fileName, 'w')
			Statistics = 0#统计数据量，后续考虑利用起来，尽量让每个进程导入数据均等
			for i in range(len(insert_sql)):
				for j in range(len(insert_sql[i])):
					file_handle.write(insert_sql[i][j]["istsql"] + '; \n')#一个sql一行
					Statistics += 1
			file_handle.write('commit; \n--writed done, sql_size is [%d].' %(Statistics))#最后事务提交
			print("writed sql into file ,sql_size is [%d]." %(Statistics))
		except IOError as err:
			raise str(err)
		finally:
			file_handle.close()

	def removeBaseData(self):
		print("clean up basedata begin...")
		Delsql_list = []
		clean_number = 0
		Delsql_list = common.getCATinit("dsql")
		for i in range(len(Delsql_list)):
			Delsql_list[i] = Delsql_list[i].replace("self._user_id", ":USER_ID")
		allUser_list = self.loadAllUser(self._Xn_user)
		for m in range(len(allUser_list)):
			param = {":USER_ID" : allUser_list[m]}
			for n in range(len(Delsql_list)):
				self.pool.executeUD(Delsql_list[n], param)
				clean_number += 1
		self.pool.commit()
		logging.info("clean up basedata end [%d]..." %clean_number)


# user_id = "3416031167007155"
# data = dataStore()
# data.setXnUser(user_id)
# case_name1 = 'othertraderelated[ownFee_ZF]'
# data.writeSqlInFile(case_name1)
# data.removeBaseData()
