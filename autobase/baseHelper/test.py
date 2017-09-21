#conding = utf-8
from baseHelper import baseUtils as utils

#import baseHelper


b = utils.db_getInstance()
print("-----------------------")
sql = "select * from tf_f_user where user_id = :USER_ID "
param = {":USER_ID" : "3417032358442187"}
print(b.execQuery(sql, param))
# a = baseUtils.mysql_getInstance()
# sql = "select * from d_data "
# print(a.execQuery(sql))
# b = utils()
# print(type(b))
# c = b.crmDb_getInstance(3)
# print(type(c))
# sql = "select * from tf_b_trade where user_id = :user_id "
# param = {":user_id" : "3417032358442187"}
# print(c.execQuery(sql, param))