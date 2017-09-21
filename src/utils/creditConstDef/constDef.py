#coding = utf-8

"""
*****************************************业务层静态常量定义*****************************************
注意：增加常量后，注意格式 “,”
"""

#融合关系常量，适用于关联处理
rhRelation = {
	"RELATION_KIND_ISJMRH" : 1, #8800
	"RELATION_KIND_ISRELAXRH" : 2, #8900
	"RELATION_KIND_ISXUSER" : 3, #x3 x5
	"RELATION_KIND_ISZFCARD" : 4, #ZF
	"RELATION_KIND_ISRELAXZF" : 5#8910
}

#特殊产品列表 
special_product = [90265342, 90109906, 90109916, 90171327]

#工单类型
tradeTypeCode = {
	"OWN_STOP" : "7220",
	"HALF_OWN_STOP" : "7210",
	"HIGH_STOP" : "7110",
	"HALF_HIGH_STOP" : "7101",
	"HIGH_OPEN" : "7303",
	"JK_OPEN" : "7304",
	"OPEN_ACCTOUNT" : "10"
}

#融合关系编码
relationCode = {
	"ZHWJ" : "8800",
	"WX" : "4400",
	"ZF" : "ZF",
	"WJZH" : "8900",
	"WJYH" : "8910",
	"GOLD" : "8920",
	"RIO" : "RIO"
}

#关联工单
BKG_RELATE_WORK = "0100000000"
#非关联工单
NOT_RELATE_WORK = "0000000000"
