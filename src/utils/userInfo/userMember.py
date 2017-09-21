#coding = utf-8

# from userInfo import User 
import sys
sys.path.append('/ngbss/credit/practice/code')
from autobase.Dao.dbPool import dbPool
from autobase.baseHelper.baseHelper import baseUtils as utils
from src.utils.userInfo import user
from src.utils.commonFunction.common import commFunc
import logging

#继承User类
class userMember(user.User):
	"""docstring for userMember"""

	#switch_on = True#类属性
	commonF = commFunc()

	def __init__(self):
		super(userMember, self).__init__()#继承user类属性
		self.last_xnUser = ''

	def printMemberInfo(self, memberList, xn_user):
		number = 0
		flag = 0
		if(self.last_xnUser != xn_user):
			self.last_xnUser = xn_user
			number = len(memberList)
			logging.info("========xn_user[%s] BEGIN========" %xn_user)
			for i in range(len(memberList)):
				if(i > 0):
					logging.info("---------------")
				for item in memberList[i].items():
					logging.info("%s:%s" %(item[0],item[1]))
				flag = i
			logging.info("========xn_user[%s] END=======" %xn_user)
			if(flag >= number-1):
				logging.info("load member size [ %d ] for xnUser [%s] in userMember cache" %(number, xn_user))
		#self.switch_on = False

	def getBaseMemmber(self, user_id):
		"""根据虚拟用户获取当前群组成员基础信息"""
		param = {":USER_ID" : user_id}
		mySql = "select member_role_id, relation_type_code, member_role_code, member_role_number, member_role_type \
				from tf_f_user_member where user_id = :USER_ID and sysdate between start_date and end_date "
		v_list = self.pool.execQuery(mySql, param)
		self.printMemberInfo(v_list, user_id)
		if(len(v_list) == 0):
			logging.info('there\'s nothing or not xn_user in tf_f_user_member about User[%s]!' %param[":USER_ID"])
			return None
		else:
			return v_list

	
	def isXnUser(self, user_id):
		"""判断是否为虚拟用户"""
		self.loadData(user_id)
		if(self.dummyTag == '1'):
			return True
		elif(self.dummyTag == '0'):
			#print("input user_id:[%s] is not XnUser" %user_id)
			return False
		else:
			return None

	def getUserMemberByUser(self, user_id):
		"""8910获取到除ZF副卡外的成员"""
		member_list,user_list,str_user = [], [], ""
		if(self.isXnUser(user_id)):
			member_list = self.getBaseMemmber(user_id)
		else:
			#是成员先获取虚拟user_id，排除ZF关系
			if(self.isZFCard(user_id) is None):
				member_list = self.getBaseMemmber(self.getXnUser(user_id)[0]["user_id"])
			else:
				#若是ZF，需要先暂时排除
				user_list = self.getXnUser(user_id)
				for i in range(len(user_list)):
					if(user_list[i]["relation_type_code"] == "ZF"):
						pass
					else:
						str_user = user_list[i]["user_id"]
				member_list = self.getBaseMemmber(str_user)
		return member_list

	def getZFmember(self, user):
		str_Master = self.isZFCard(user)
		if(str_Master is None):
			return None
		else:
			return self.getBaseMemmber(str_Master)
	
	def getAllMember(self, user):
		"""正向查找遍历,非8910中zf副卡以外触发业务使用"""
		total_member, father_member, sub_member = [],[],[]
		relation_list = self.getAllRelation(user)
		#处理单纯的ZF关系
		if(len(relation_list) == 1 and relation_list[0] == "ZF"):
			master_card = self.isZFCardMaster(user)
			mem_dict = self.getBaseMemmber(master_card)
			for i in range(len(mem_dict)):
				total_member.append(mem_dict[i]["member_role_id"])
		#非ZF或者复合关系
		else:
			father_member = self.getUserMemberByUser(user)
			if(father_member is not None):
				for j in range(len(father_member)):
					mem_str = father_member[j]["member_role_id"]
					if(self.isZFCard(mem_str) is not None):
						sub_member = self.getZFmember(mem_str)
						for i in range(len(sub_member)):
							total_member.append(sub_member[i]["member_role_id"])
					total_member.append(mem_str)
			#print(["userMember.getAllMember:"]+list(set(total_member)))
		return list(set(total_member))#排重

	def getAllMemberByZFminor(self, user):
		"""逆向查找遍历,8910中zf副卡触发业务使用"""
		total_mem = []
		minor_card = self.isZFCardMinor(user)#返回值是副卡
		if(minor_card is not None):
			master_card = self.isZFCard(minor_card)#获取主卡
			total_mem = self.getAllMember(master_card)
			total_mem.append(minor_card)
		return list(set(total_mem))#排重

	def getAllRelation(self, user):
		"""返回list,['8900','ZF',...]"""
		m_relationList = []
		v_list = []
		dummyTag = self.isXnUser(user)
		if(dummyTag is None):
			logging.info("user[%s] information is abnormal, plz check [tf_f_user]." %user)
			m_relationList = None
		elif(dummyTag):
			v_list = self.getBaseMemmber(user)
			if(v_list is None):
				#讲道理走不到这里
				logging.info("user[%s] doesn't have relation!" %user)
				m_relationList = None
			else:
				m_relationList.append(v_list[0]['relation_type_code'])#解析字典
				#根据虚拟用户遍历成员是否存在其他子组合(ZF)
				for m in range(len(v_list)):
					if(self.isZFCard(v_list[m]["member_role_id"]) is None):
						continue
					else:
						m_relationList.append('ZF')
		else:
			#如果是主副卡副卡
			minor_card = self.isZFCardMinor(user)
			if(minor_card is not None):
				temp_list = self.getXnUser(self.isZFCard(minor_card))#根据ZF主卡获取所有关系
				for n in range(len(temp_list)):
					m_relationList.append(temp_list[n]["relation_type_code"])
			else:
				v_list = self.getXnUser(user)
				if(v_list is None):
					#讲道理也走不到这里
					print("user[%s] hasn't relation!" %user)
					m_relationList = None
				else:
					temp = []
					for j in range(len(v_list)):
						temp.extend(self.getBaseMemmber(v_list[j]["user_id"]))
					for i in range(len(temp)):
						if(self.isZFCard(temp[i]["member_role_id"]) is not None):
							m_relationList.append('ZF')
							continue
						m_relationList.append(temp[i]['relation_type_code'])
		return list(set(m_relationList))#统一排重(异常处理)

	def getXnUser(self, user_id):
		"""获取虚拟用户和融合关系"""
		xn_list = []
		sql = "select user_id, relation_type_code from tf_f_user_member \
			where member_role_id = :member_role_id and sysdate between start_date and end_date "
		param = {":member_role_id" : user_id}
		xn_list = self.pool.execQuery(sql, param)
		if(len(xn_list) == 0):
			logging.info("plz check userInfo in [tf_f_user_member]")
			return None
		else:
			return xn_list

	def getRelationType(self, user_id):
		"""获取虚拟用户或者成员的融合关系"""
		sql_xn = "select relation_type_code from tf_f_user_member \
		where user_id = :user_id and sysdate between start_date and end_date "
		sql_member = "select relation_type_code from tf_f_user_member \
		where member_role_id = :user_id and sysdate between start_date and end_date "
		relation_list = []
		param = {":user_id" : user_id}

		is_dummyTag = self.isXnUser(user_id)
		if(not is_dummyTag):
			relation_list = self.pool.execQuery(sql_member, param)
		elif(is_dummyTag):
			relation_list = self.pool.execQuery(sql_xn, param)

		if(len(relation_list) == 0):
			return None
		else:
			return relation_list

	def isZFCard(self, user_id):
		"""是主副卡主卡返回主卡，不是返回None"""
		sql = "select a.user_id from tf_f_user_member a, td_o_credit_rhrelation b where a.member_role_id = :user_id \
				and a.partition_id = mod(:user_id, 10000) \
				and (sysdate between a.start_date and a.end_date) \
				and a.relation_type_code = b.relation_type_code \
				and b.rsrv_str1 = '4' "
		param = {":user_id" : user_id}
		rst = self.pool.execQuery(sql, param)
		if(len(rst) > 0):
			#print("user [%s] match relation_type_code is [%s]." %(user_id, "ZF"))
			return rst[0]["user_id"]
		else:
			return None

	def isZFCardMaster(self, user_id):
		"""是主副卡主卡返回主卡，不是返回None"""
		#非主副卡直接返回
		if(not self.isZFCard(user_id)):
			return None

		sql_zf = "select user_id from tf_f_user_member where member_role_id = user_id \
				and member_role_id = :user_id and relation_type_code = 'ZF' \
				and sysdate between start_date and end_date "
		param = {":user_id" : user_id}
		rst_list = self.pool.execQuery(sql_zf, param)
		if(len(rst_list) > 0):
			return rst_list[0]["user_id"]
		else:
			return None

	def isZFCardMinor(self, user_id):
		"""是主副卡副卡返回副卡，不是返回None"""
		if(self.isZFCard(user_id) is None):
			return None

		sql_zf = "select member_role_id from tf_f_user_member where member_role_id <> user_id \
				and member_role_id = :user_id and relation_type_code = 'ZF' \
				and sysdate between start_date and end_date "
		param = {":user_id" : user_id}
		rst_list = self.pool.execQuery(sql_zf, param)
		if(len(rst_list) > 0):
			return rst_list[0]["member_role_id"]
		else:
			return None
