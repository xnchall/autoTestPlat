#-*-coding:utf-8-*-
import os,subprocess,sys

class ConnDB(object):
	global pdmdb

	def __init__(self,dbName):
		self.dbName = dbName

	#def setDB(self,dbName):
	#	self.dbName = dbName

	def __connDB(self,dbName):
		global pdmdb
		if dbName.strip().find("dmdb")!=-1:
			conndmdb="dsql".strip()+os.linesep
			print ("连接数据库命令:"+conndmdb)
			pdmdb=subprocess.Popen(conndmdb,shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
		elif dbName.strip().find("QCUBIC")!=-1:
			conndmdb="gsqlnet billing billing --dsn=QCUBIC213".strip()+os.linesep
			print ("连接数据库命令:"+conndmdb)
			pdmdb=subprocess.Popen(conndmdb,shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)

	def __disconnDB(self,dbName):
		global pdmdb
		if dbName.strip().find("dmdb")!=-1:
			#pdmdb.communicate(("commit;"+os.linesep).encode('utf-8'))
			pdmdb.stdin.write(("exit;"+os.linesep).encode('utf-8'))
			return pdmdb.communicate()

	def execSql(self,ksqls):
		global pdmdb
		self.__connDB(self.dbName)#连接数据库
		#pdmdb.stdin.write()
		for sql in ksqls:#顺序执行sql 取消mdb支持多sql执行在ksqls字典生成时只允许有一对key-value
			if ksqls[sql]:
				print (ksqls[sql])
				#pdmdb.communicate(ksqls[sql].encode('utf-8'))#顺序执行sql
				pdmdb.stdin.write(ksqls[sql].encode('utf-8'))#顺序执行sql
				break
		rdls = self.__disconnDB(self.dbName)
		'''
		if pdmdb.returncode != 0:
			rdls=pdmdb.stdout.read()
			#rdls=pdmdb.communicate()
		
		while True:
			rdl=pdmdb.stdout.read()
			rdls=rdls+rdl
			
			if (not rdl) or rdl.find('Disconnected from Distributed MDB')!=-1:
				if pdmdb.poll() is None:
					pdmdb.kill()
					pdmdb.wait()
					break
		'''
		print (rdls)
		#print (22222222)
		return self.__anaData(rdls,ksqls)

	def __anaData(self,lines,sqls):
		linetag=0    #0初始值 1记录命令开始 2记录查询到数据
		resultV=[]
		data=[]
		data1={}
		errMeg=''
		#mdb只支持单条sql执行，所以只获取一条
		msql=""
		for sql in sqls:
			msql=sqls[sql].strip()
			if msql:
				break
		lines=str(lines).split(os.linesep)
		#log.debug(lines)
		for line in lines:
			#log.debug(line)
			if msql[0:6].lower() != "select":
				if line.find("dMSQL> "+msql)!=-1:
					linetag=1
					resultV=""
					print(1234)
				elif linetag==1:
					if line.find("dMSQL> exit;")!=-1:
						linetag=0
						return resultV
					else:
						resultV=resultV+line.strip()
			elif msql[0:6].lower() == "select":
				if line.find("dMSQL> ")!=-1:#将字段标题存入list
					linetag=1
					tit=line[15:]
					#log.debug(line.index("dMSQL> "))
					tableTitle=tit.split()
				elif linetag!=0:
					if line.find("-------------------------")!=-1 and linetag==1:
						linetag=2
						data1={}
					elif linetag==2 and line.find("--------")==-1:
						tableRes=line.split()
						for i in range(len(tableTitle)):
							data1[tableTitle[i].upper()]=tableRes[i]
						data.append(data1)
						resultV=data
					elif linetag==2 and line.find("--------")!=-1:
						if len(resultV)<1 and len(errMeg)>0:#有错误的情况是:结果集resultV为空,所有信息errMeg不为空
							resultV='error:'+errMeg
							errMeg=''
						linetag=0
						return resultV


a = ConnDB("dmdb")
sql = "select * from tf_f_user where user_id = 1114061524350998;"
ksqls = {"sql":sql}
print(a.execSql(ksqls))