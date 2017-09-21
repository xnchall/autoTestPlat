#coding = utf-8
import time
from tradeUtility import tradeUtility

print(type(tradeUtility))
a = tradeUtility()
def log_name():
	base_name = '/ngbss/credit/practice/log/'
	date = time.strftime('%Y%m%d',time.localtime(time.time())) + '.log'
	log_n = base_name + date
	print(log_n)
	return base_name + date

print(log_name())
a.log_name()
