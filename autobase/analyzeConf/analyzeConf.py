#! -*-coding:utf-8-*-
from collections import defaultdict
import sys

class ParseConf(object):
	def __init__(self, m_filename='/ngbss/credit/practice/code/etc/autotest.conf'):
		self.m_filename = m_filename
		self.spos = ''

	def getSect(self, m_sectionname):
		s_sectionname = '<'+m_sectionname+'>' #节点开始
		e_sectionname = '</'+m_sectionname+'>' #节点结束
		#content 字符串
		with open(self.m_filename, 'r') as cf:
			content = cf.read()
		if 0 > content.find(m_sectionname):
			print ('cannot find the section')
			return ''
		else:
			self.spos = content.find(s_sectionname)+len(s_sectionname) #获取开始字节位置，不带节点名
			self.epos = content.find(e_sectionname) #获取结束字节位置，不带节点名
			cfcontent = content[self.spos+1:self.epos-1]#.replace('    ','')
			return cfcontent

	def getChildSect(self, m_sectionname, m_childsecname):
		s_childsecname = '<'+m_childsecname+'>' #节点开始
		e_childsecname = '</'+m_childsecname+'>' #节点结束
		ctt = self.getSect(m_sectionname)
		if 0 > ctt.find(m_childsecname):
			print ('cannot find the childsection')
			return ''
		else:
			cpos = ctt.find(s_childsecname)+len(s_childsecname) #获取开始字节位置，不带节点名
			cepos = ctt.find(e_childsecname) #获取结束字节位置，不带节点名
			childctt = ctt[cpos:cepos].replace('    ','')
			return childctt 
		
	def getSectInfo(self, m_sectionname, m_key=None):
		d = {}
		'''
		#判断版本采用不同的分隔符
		if sys.version[:6] < '3.0.0':
			cct = self.getSect(m_sectionname).split('\n')
		else:
			cct = self.getSect(m_sectionname).split('\n')
		'''
		cct = self.getSect(m_sectionname).split('\n')
		for line in cct:
			if 0 > line.find('='):
				continue
			else:
				s = line.replace(' ','').split('=')
				key = s[0]
				value = s[1]
				d[key]=value
		if m_key != None:
			return d.get(m_key,'No such key')
		else:
			return d

	def insertStr(self, m_sectionname, m_tgtstring, m_insertstr):
		ctt = self.getSect(m_sectionname)
		if 0 > ctt.find(m_tgtstring):
			print('cannot find the target string')
			return 0
		else:
			clausepos = ctt.find(m_tgtstring)+len (m_tgtstring)+self.spos
			with open(self.m_filename, 'r') as cf:
				content = cf.read()
			#插入字符串后的新配置文件
			nctt = content[:clausepos] + m_insertstr + ',' + content[clausepos:]
			isExistStr = content[clausepos:clausepos+len(m_insertstr)]
			if ( isExistStr == m_insertstr ):
				print ('This string has already existed!')
				return 0
			else:
				with open(self.m_filename, 'wb') as cf:
					cf.write(bytes(nctt,'utf-8'))
				return 1
