from logCtrl import baseLog


name = "xnchall"
inst = baseLog(name)
log = inst.getLogDefine_instance(name)
log.error(name)
log.info("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
log.debug("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")

def foo():
	trace = "root"
	log1 = baseLog.getLogByconf_instance(trace)
	log1.info("-----------------------------")
	log1.error("***********************")

foo()