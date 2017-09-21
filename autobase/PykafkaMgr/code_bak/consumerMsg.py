#coding=utf-8

import os 
import sys
# import json
import etc.config as conf
from PykafkaMgr import kfkConsumer


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
			print(u"consumerMsg.py 接收2个参数, 即topic \neg:python consumerMsg.py test 0\n消费topic名为test的第0分区消息[从开始消费]")
			print("*************************************************************")


if __name__ == '__main__':

	except4v()

	if(len(sys.argv) == 3):
		topic = sys.argv[1]
		partition = int(sys.argv[2])
		consumer = kfkConsumer(conf.kafka_consumerMgr["broker"])
		consumer.__str__()
		consumer.consumerMsg(topic,partition)
