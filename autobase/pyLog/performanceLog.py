#coding=utf-8

import sys
sys.path.append('/ngbss/credit/practice/code')
from autobase.pyLog.logCtrl import baseLog

class perfLog(baseLog):
	"""docstring for perfLog"""
	def __init__(self):
		super(perfLog, self).__init__()

	def exe_time(self, func):
		def time_calc(self,*args, **kargs):
			t0 = time.time()
			#othertradeRelate.logTrace.info("%s, Function[%s] start" %(time.strftime("%X", time.localtime()), func.__name__))
			back = func(self,*args, **kargs)
			#othertradeRelate.logTrace.info("%s, Function[%s] end" % (time.strftime("%X", time.localtime()), func.__name__))
			logging.info("%.5fs taken for Function[%s]" % (time.time() - t0, func.__name__))
			return back
		return time_calc
