#coding = utf-8
#
#常驻进程方法集合
#新增进程需要重启
#
#----------------------------import
from baseHelper import baseUtils as utils

def reflashTimestamp():
	#时间戳刷新，间隔时间interval，单位秒
	interval = 90
	utils.reflashTimestamp(interval)

if __name__ == '__main__':
	reflashTimestamp()