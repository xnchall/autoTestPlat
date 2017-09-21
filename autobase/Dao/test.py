# -*- coding:utf-8 -*-

"""
this pytext is to test dbPool.py provide API
"""
import datetime
from dbPool import dbPool

db_info3 = {
"dbType" : "pymysql",
"user" : "root",
"passwd" : "123456",
"port" : 3306,
"host" : "10.251.6.62",
"dbName" : "report",
"charset" : "utf8"
}

db_info = {
		'dbType' : "cx_Oracle",
        'host' : "10.124.0.40",
        'user' : "UOP_CRM1",
        'passwd' : "UOP_CRM1",
        'port' : "1521",
        'dbName' : "tcrm1",
        'charset' : "utf-8"
        }
db_info2 = {
		'dbType' : "cx_Oracle",
        'host' : "10.124.0.39",
        'user' : "ubak",
        'passwd' : "ubak_123",
        'port' : "1521",
        'dbName' : "ngact",
        'charset' : "utf-8"
        }

db_info1 = {
        'dbType' : 'cx_Oracle',
        'host' : "10.124.0.42",
        'user' : "UOP_ACT1",
        'passwd' : "UOP_ACT1",
        'port' : "1521",
        'dbName' : "tact1",
    }



def test():
	pool = dbPool.get_instance(db_info)
	print("---------------------")
	#pool = dbPool.setPool(db_info3)
	#pool = dbPool.dbPool(db_info2)
	#print('\n')
	"""
	print("正在测试 13 APIs \n")
	print(u'测试第一个api，设置数据库缓存池')
	pool.setPool(db_info = db_info)
	print('\n')

	print(u'测试第二个api，创建共享链接')
	#pool.shareOrPrivate()
	pool = dbPool.dbPool(db_info)
	print('\n')

	print(u'测试第三个api，创建私有链接')
	pool = dbPool.dbPool(db_info,0)
	print('\n')

	print(u'测试第四个api，创建数据库操作游标构造器')
	pool = dbPool.dbPool(db_info)
	print('\n')
	"""
	#print(u'测试第五、六个api，获取表所有列字段、自动创建参数字典')
	#column = pool.columns("tf_f_user")
	#print(column)
	#dt = pool.create_params('tf_f_user',{'user_id':'b','serial_number1':'a'})
	#print(dt)
	#print('\n')
	#
# 	res = {}
# 	XnUser_id = '3416092924523677'
# 	sql = "select member_role_id, relation_type_code, member_role_code, member_role_number, member_role_type from tf_f_user_member where user_id = :USER_ID and sysdate between start_date and end_date "
# 	param = {":USER_ID":XnUser_id}
# 	result = pool.execQuery(sql, param)
# 	print(result)
# 	if(len(result) == 0):
# 		raise TypeError('在用户资料表中未找到用户(%s)的记录。' %XnUser_id)
# 	else:
# 		res.setdefault(XnUser_id, result)
# 		res.setdefault(XnUser_id, "###########################")
# 		print("load member size:[ %d ] for xnUser:[ %s ] in userMember cache" %(len(result),XnUser_id))
# 		#return res
# 		print(res)

# 		print("##############")
# 		for i in range(len(res[XnUser_id])):
# 			for key, value in res[XnUser_id][i].items():
# 				if(res[XnUser_id][i][key] == '8910'):
# 					print(res[XnUser_id][i]["member_role_number"])
# #for key in v_member[i][key]:
# 		print("##############")
# 		for i in range(len(res[XnUser_id])):
# 			print("##############")
# 			for item in res[XnUser_id][i].items():
# 				print("%s:%s" %(item[0],item[1]))
# 		a(res)
	# sql = "select * from tf_b_trade where user_id = :USER_ID "
	# param = {":USER_ID" : "3415042334960705"}
	# rst = pool.execQuery(sql,param)
	# print("%s\n" %rst)
# """
# 	{'3416092924523677': [{'member_role_type': '0', 'member_role_code': 8004, 'relation_type_code': '8910', 'member_role_id': 3415022732782759, 'member_role_number': '18652933442'}, {'member_role_type': '0', 'member_role_code': 8006, 'relation_type_code': '8910', 'member_role_id': 3416092924523678, 'member_role_number': '02501082872'}, {'member_role_type': '0', 'member_role_code': 8004, 'relation_type_code': '8910', 'member_role_id': 3415033134085812, 'member_role_number': '15651997339'}]}
	
# 	print(u'测试第七个api，查询功能')
# 	sql = "select member_role_id, relation_type_code, member_role_code, member_role_number, member_role_type from tf_f_user_member where user_id = :USER_ID and sysdate between start_date and end_date "
# 	#param = {"USER_ID":XnUser_id}
# 	#sql = "select * from tf_f_user_member where user_id = :USER_ID "
# 	param = {":USER_ID":'3416092924523677'}
# 	rst = pool.execQuery(sql,param)
# 	print("%s\n" %rst)
# 	print('\n')

# 	print(u'测试第八、九个api，插入功能')
# 	table = 'tf_f_resource'
# 	column_dict = {'resourceinsid': '66666666666688', 'resourcecode': 2001, 'user_id': '1790532750590999', 'totalcount': 8888, 'usedcount': 666, 'totalaccount': 555, 'validtag': 1, 'eparchycode': 999, 'startdate': datetime.datetime(2013, 11, 5, 9, 36, 29), 'enddate': datetime.datetime(2019, 11, 5, 9, 36, 29)}
# 	a = pool.execInsertone(table,column_dict)
# 	pool.commit()
# 	print(u"本次操作成功数: ",a)
# 	print('down!\n')

# 	print(u'测试第十个api，更新功能（自动绑定变量模式）')
# 	set_dict = {'totalaccount':101010,'validtag':0}
# 	where_dict = {'resourceinsid':'1000000000000013'}
# 	a = pool.execUpdate(table,set_dict,where_dict)
# 	pool.commit()
# 	print(u"本次操作成功数: ",a)
# 	print('down!\n')

# 	print(u'测试第十一、十二个api，删除功能（自动绑定变量模式）')
# 	table = 'tf_f_resource'
# 	where_dict = {'resourceinsid':'1000000000000017'}
# 	a = pool.execDelete(table,where_dict)
# 	pool.commit()
# 	print(u"本次操作成功数: ",a)
# 	print('down!\n')

# 	print(u'测试第十三个api，更新和删除功能（手动绑定变量模式）')
# 	sql = 'UPDATE tf_f_resource set validtag=:validtag,totalaccount=:totalaccount where resourceinsid=:resourceinsid'
# 	param = {'resourceinsid': '1000000000000013', 'totalaccount': 101010, 'validtag': 0}
# 	a = pool.executeUD(sql,param)
# 	pool.commit()
# 	print(u"本次操作成功数: ",a)
# 	print('down!\n')


# 	print(u"数据库连接池测试完成!")
# 	pool.close()

# 	print(u"\n关闭了所有资源成功！")

# def insertSql(user_id, sql_templet=""):
# 	pool = dbPool.dbPool(db_info)
# 	sql1 = "select acct_id,prov_code from tf_f_payrelation where user_id = :user_id and (to_number(to_char(sysdate,'yyyymm')) between start_cyc_id and end_cyc_id) "
# 	param1 = {":user_id":user_id}
# 	rst1 = pool.execQuery(sql1, param1)
# 	print(rst1[0]['acct_id'],rst1[0]['prov_code'])

# 	sql2 = "insert into TI_O_RECV_CREDIT \
# 		values (f_sys_getseqid(0010,'seq_trade_id'), :acct_id, mod(:acct_id,10000), :user_id, '1', '0', '0', '1', sysdate, '用户实名认证后做0缴费处理', 'CREDIT00', 'CREDIT', :prov_code, null, null, null)"
# 	param2 = {":acct_id":rst1[0]['acct_id'], "prov_code":rst1[0]['prov_code'], ":user_id":user_id}
# 	rst2 = pool.execInsert(sql2, param2)
# 	if(rst2 == 1):
# 		print("insert [TI_O_RECV_CREDIT] successfully!")
# 	pool.commit()

# def getRst(user_id):
# 	pool = dbPool.dbPool(db_info)
# 	sql_d = "delete from ti_oh_credit_speedlimit_work WHERE user_id = :USER_ID and PARTITION_ID = mod(:USER_ID,10000)"
# 	param_d = {":USER_ID":user_id}
# 	pool.executeUD(sql_d,param_d)
# 	pool.commit()
# 	print("delete [ti_o_credit_speedlimit_work] history data successfully")
# 	sql = "select process_tag,remark from ti_oh_credit_speedlimit_work where user_id = :USER_ID and (sysdate between start_date and end_date) order by exec_time desc "
# 	param = {":USER_ID":user_id}
# 	return pool.execQuery(sql,param)
# """
# def a(memberDcit):
# 	for key in memberDcit:
# 		print("========xn_user[%s] BEGIN========" %key)
# 		for i in range(len(memberDcit[key])):
# 			print("---------------")
# 			for item in memberDcit[key][i].items():
# 				print("%s:%s" %(item[0],item[1]))
# 		print("========xn_user[%s] END=========" %key)

test()
#insertSql('1116010524448934')
#print(getRst('1116010524448934'))