#coding=utf-8


kafka_mgr = {
	"broker" : '10.161.24.240:1092,10.161.24.240:1093,10.161.24.240:1094'
}

kafka_consumerMgr = {
	# "broker" : '10.124.142.46:6667' #0.10集群
	"broker" : '10.161.24.240:1092' #240主机0.9集群
	# "broker" : '10.124.142.46:9092' #0.9集群
}

kafka_logDir = r"/ngbss/credit/practice/log/kafka"

#生产者输入json文件
kafka_produce = r"/ngbss/credit/practice/code/autobase/PykafkaMgr/code_bak/data/input/produceMsg.json"
