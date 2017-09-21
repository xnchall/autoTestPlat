#coding = utf-8
import subprocess
import time
cmm = "cpth /ngbss/credit2/user/likai/code/data/likai2* /ngbss1/credit/data/alarm/input/17/0"

while(True):
	subprocess.Popen(cmm, shell=True)
	time.sleep(1)
