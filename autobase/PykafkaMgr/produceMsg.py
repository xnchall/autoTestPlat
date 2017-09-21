#coding=utf-8

import os 
import sys
import time
import json
import etc.config as conf
from PykafkaMgr import kfkProducer

#从json文件获取消息
def getMsgFromJsonfile(filePath):
	if(not os.path.isfile(filePath)):
		print(u"[%s] 输入的json文件路径有误,请检查..." %filePath)
	else:
		with open(filePath) as json_file:
			return json.load(json_file)

def except4v():
	if(len(sys.argv) <= 1):
		print(u"未输入topic和partition！\n你可以--help查看具体使用方法...")
	elif(sys.argv[1].startswith("--")):
		option = sys.argv[1][2:]
		if(option in ("version", "Version")):
			print("Version 1.0 \nPython 2.7.3 (default, Nov  6 2015, 14:11:14) \
					\n[GCC 4.4.7 20120313 (Red Hat 4.4.7-4)] on linux2")
		elif(option in ("help","h")):
			print("*************************************************************")
			print(u"produceMsg.py 接收两个参数, 第一个是topic, 第二个是partition \neg:python produceMsg.py test 0 \n向topic名为test第0分区生产消息 \n消息内容格式json, 输入目录/ngbss/credit2/user/likai/code/data/input/produceMsg.json")
			print("*************************************************************")

def calcMsg(jsonMsg):
	sumMsg, sumAcct = 0, 0
	msgNum = len(jsonMsg)
	print("------------------------------------------")
	for i in range(msgNum):
		acct_num = len(jsonMsg[i]["MSGBODY"])
		print(u"第[%d]条消息，包含ACCT_ID账户数:[%d]个"%(i+1, acct_num))
		sumMsg = i+1
		sumAcct += acct_num
		acct_num = 0
	print(u"本次生产消息总共[%d]条, 总共账户数：[%d]个"%(sumMsg, sumAcct))
	print("------------------------------------------")

if __name__ == '__main__':

	except4v()

	if(len(sys.argv) == 3):
		topic = sys.argv[1]
		partition = int(sys.argv[2])
		produce = kfkProducer(conf.kafka_mgr["broker"])
		produce.__str__()
		jsonMsg = getMsgFromJsonfile(conf.kafka_produce)
		for i in range(len(jsonMsg)):
			produce.produceMsg(topic, ('%s'%jsonMsg[i]).encode('utf-8'), partition)
		print("------------------------------------------")
		print(u"topic:[%s]\npartition:[%d]"%(topic,partition))
		calcMsg(jsonMsg)
		# for i in range(len(jsonMsg)):
		# 	produce.produceMsg('34_ACT_SATRANSFEE_MSG', ('%s'%jsonMsg[i]).encode('utf-8'), 0)
		# print("------------------------------------------")
		# print(u"topic:[%s]\npartition:[%d]"%(topic,partition))
		# calcMsg(jsonMsg)
