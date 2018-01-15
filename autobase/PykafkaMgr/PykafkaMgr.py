#coding=utf-8

import time
import logging
import sys
import json
import etc.config as conf
sys.path.append('/ngbss/credit/practice/tool/kafka-python-1.3.4')
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from kafka import TopicPartition


def log_name():
	base_name = conf.kafka_logDir
	date = time.strftime('%Y%m%d',time.localtime(time.time())) + '.log'
	return base_name + date

logging.basicConfig(level=logging.INFO,
		format='%(asctime)-15s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
		datefmt='%Y-%m-%d %H:%M:%S',
		filename=log_name(),
		filemode='a'
		)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)


class kfkProducer(object):

	# producer = None

	def __init__(self, broker_list):
		# self._broker = broker
		# self._kafkaPort = kafkaPort
		# self._kafkaTopic = kafkaTopic
		self._brokerList = broker_list

	def __str__(self):
		logging.info("--------------------------------")
		logging.info("kafka-producer params ...")
		logging.info("[KAFKA-BROKER]:%s" %self._brokerList)
		# logging.info("[KAFKA-PORT]:%s" %self._kafkaPort)
		# logging.info("[KAFKA-TOPIC]:%s" %self._kafkaTopic)
		logging.info("--------------------------------")

	def registerKfkProducer(self):
		try:
			# producer = KafkaProducer(bootstrap_servers = '{kafka_host}:{kafka_port}'.format(
			# 	kafka_host=self._broker,
			# 	kafka_port=self._kafkaPort
			# 	))        #注册单机链接实例
			producer = KafkaProducer(bootstrap_servers = self._brokerList)#注册集群链接实例
		except KafkaError as e:
			logging.info(e)
		return producer

	def produceMsg(self, topic, msg, partition=0):
		# 自动将输入字符串转化为json格式，产出消息
		if(topic in ('', None)):
			logging.error("topic is None, plz check!")
		else:
			try:
				# parmas_message = json.dumps(msg)#转化为json格式
				producer = self.registerKfkProducer()
				producer.send(topic, value=msg, partition=partition)
				producer.flush()
				# time.sleep(1)
			except KafkaError as e:
				logging.info(e)



class kfkConsumer(object):

	# consumer = None

	def __init__(self, zookeeperList):
		# self._broker = broker
		# self._kafkaPort = kafkaPort
		self._zookeeperList = zookeeperList
		# self._topic = topic

	def __str__(self):
		logging.info("--------------------------------")
		logging.info("kafka-consumer params ...")
		logging.info("[KAFKABROKER_LIST]:%s" %self._zookeeperList)
		logging.info("--------------------------------")

	def registerConsumer(self):
		try:
			consumer = KafkaConsumer(
				bootstrap_servers=[self._zookeeperList], request_timeout_ms = 30001,
				auto_offset_reset='earliest')
		except KafkaError as e:
			logging.info(e)
		return consumer

	def consumerMsg(self, topic, partition=0):
		if(topic in ('', None)):
			logging.error("topic is None, plz check!")
		else:
			try:
				v_consumer = self.registerConsumer()
				v_consumer.assign([TopicPartition(topic,partition)])
				# self.registerConsumer.subscribe([self._kafkaTopic])
				for message in v_consumer:
					# message value and key are raw bytes -- decode if necessary!
					# e.g., for unicode: `message.value.decode('utf-8')
					logging.info("%s:%d:%d: msg=%s" % (message.topic, message.partition,
								message.offset, message.value.decode('utf-8')))
					#print("%s:%d:%d: msg=%s" % (message.topic, message.partition,
								#message.offset, message.value.decode('utf-8')))#for sss
			except KafkaError as e:
				logging.info(e)
