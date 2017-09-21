#! -*-coding:utf-8-*-
import time,subprocess

class OperateProc(object):
	def __init__(self):
		self._procname = ''
		
	def setProcName(self, _procname):
		self._procname = _procname
	
	def setAction(self,_action):
		self._action = _action
	
	def act(self):
		try:
			pn = self._procname.split(' -')
			pids = 'ps -ef|grep '+pn[0]+'|grep '+pn[1]+'|grep -v grep|cut -b 10-15'
			#pid = bool(os.popen(pids).read()[:-1]) #获取进程pid，转换为boolean，存在为True，不存在为0-False
			pid = bool(subprocess.check_output([pids],shell = True))
			if self._action == 'start':
				if not pid: #未启动
					subprocess.call([self._procname],shell=True)
					print('%s now is running' % self._procname)
				else: #已启动，不再启动
					print('%s is running, do not need to start' % self._procname)
			elif self._action == 'stop':
				if not pid: #未启动
					print('%s is not running, donnot need to stop' % self._procname)
				else: #已启动，kill掉
					kill = pids + '|xargs kill -9'
					subprocess.call([kill],shell = True)
					print('%s stopped' % self._procname)
			elif self._action == 'restart':
				if not pid: #未启动
					print('%s is not running, now starting' % self._procname)
				else: #已启动，先kill掉
					kill = pids + '|xargs kill -9'
					subprocess.call([kill],shell = True)
					time.sleep(10)
				subprocess.call([self._procname],shell=True)
				print('%s now is rerunning' % self._procname)
			else:
				print('Wrong action')
				return 0
			return 1
		except Exception as e:
			print('err: %s' % e)
			return 0