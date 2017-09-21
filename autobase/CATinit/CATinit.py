#-*-coding:utf-8-*-


#initDict.py
#用来存储信控自动化后台，所有用到的初始化值。目的是为了方便后续维护！
#内容包括：
#	1.路径 ，比如：配置文件路径、常用目录路径等
#	2.全局常量，比如：事务控制常量、时间间隔常量等
#	等,可以随时增加。
#增加参数规范：【初始化路径专用字典】
#	1.key:需要初始化文件名_****
#	2.value:string、int等类型变量


#初始化路径专用字典：
path_dict = {
	'analyzeConf_path' : '/ngbss/credit/practice/code/etc/autotest.conf', #解析配置文件类使用初始化值
	'dataDeal_path' : '/ngbss/credit/practice/code/basesql/credit/input/', #信控自动化数据脚本sql文件目录
	'dataStore_outPutPath' : '/ngbss/credit/practice/code/data/credit/output/',#自动化用例导出测试数据存放sql脚本目录
	'log_path' : '/ngbss/credit/practice/log/',#日志文件存储目录
	'logConf_path' : '/ngbss/credit/practice/code/etc/logger.conf' #日志配置文件目录
}
#初始化常量专用字典：
constant_dict = {
	'TRANSACTION_SQL' : 50, #数据库事务控制阀值
	'SUBPROCESS_LIMIT' : 2, #批量导入基础sql文件，动态控制进程池大小，即一个进程执行SUBPROCESS_LIMIT个sql文件
	'PROCESS_SPECIAL' : 3 #特殊处理，当基础数据sql文件少于PROCESS_SPECIAL时没必要创建进程池
} 
#导生产数据sql：
dsql = [
	'delete from TF_F_ACCOUNT where acct_id in (select acct_id from tf_f_payrelation where user_id in (self._user_id))',
	'delete from TF_F_PAYRELATION where user_id in (self._user_id)',
	'delete from TF_F_CUSTOMER where cust_id in (select cust_id from TF_F_USER where user_id in (self._user_id))',
	'delete from TF_F_USER where user_id in (self._user_id)',
	'delete from TF_F_USER_PARAM where user_id in (self._user_id)',
	'delete from TF_F_USER_SERV where user_id in (self._user_id)',
	'delete from TF_F_USER_SERVSTATE where user_id in (self._user_id)',
	'delete from TF_F_USER_IMPORTINFO where user_id in (self._user_id)',
	'delete FROM TF_F_FEEPOLICY_PARAM t where feepolicy_ins_id in (select feepolicy_ins_id from TF_F_FEEPOLICY where id in (self._user_id))',
	'delete from TF_F_FEEPOLICY where id in (self._user_id)',
	'delete from TF_F_USER_PRODUCT where user_id in (self._user_id)',
	'delete from TF_F_USER_MEMBER where (user_id in (self._user_id) or member_role_id in (self._user_id))'
	]
sql = (
	'select distinct \'insert into tf_f_user values (\'\'\'||PARTITION_ID||\'\'\',\'\'\'||USER_ID||\'\'\',\'\'\'||DUMMY_TAG||\'\'\',\'\'\'||NET_TYPE_CODE||\'\'\',\'\'\'||SERIAL_NUMBER||\'\'\',\'\'\'||EPARCHY_CODE||\'\'\',\'\'\'||CITY_CODE||\'\'\',\'\'\'||CUST_ID||\'\'\',\'\'\'||USECUST_ID||\'\'\',\'\'\'||BRAND_CODE||\'\'\',\'\'\'||PRODUCT_ID||\'\'\',\'\'\'||USER_TYPE_CODE||\'\'\',\'\'\'||PREPAY_TAG||\'\'\',\'\'\'||SERVICE_STATE_CODE||\'\'\',\'\'\'||OPEN_MODE||\'\'\',\'\'\'||ACCT_TAG||\'\'\',\'\'\'||REMOVE_TAG||\'\'\',to_date(\'\'\'||to_char(IN_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),to_date(\'\'\'||to_char(OPEN_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),to_date(\'\'\'||to_char(PRE_DESTROY_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),to_date(\'\'\'||to_char(DESTROY_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),to_date(\'\'\'||to_char(FIRST_CALL_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),to_date(\'\'\'||to_char(LAST_STOP_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),\'\'\'||CREDIT_CLASS||\'\'\',\'\'\'||BASE_CREDIT_VALUE||\'\'\',\'\'\'||CREDIT_VALUE||\'\'\',\'\'\'||CREDIT_CONTROL_ID||\'\'\',to_date(\'\'\'||to_char(CHANGEUSER_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),\'\'\'||SCORE_VALUE||\'\'\',to_date(\'\'\'||to_char(UPDATE_TIME,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),\'\'\'||UPDATE_DEPART_ID||\'\'\',\'\'\'||UPDATE_STAFF_ID||\'\'\',\'\'\'||USER_PASSWD||\'\'\',\'\'\'||OPEN_DEPART_ID||\'\'\',\'\'\'||PROVINCE_CODE||\'\'\')\' istsql '
	'from uop_actself._domain.tf_f_user@toactself._domain where user_id in (self._user_id)'
	' union all '
	'select distinct \'insert into tf_f_customer values (\'\'\'||a.PARTITION_ID||\'\'\',\'\'\'||a.CUST_ID||\'\'\',\'\'\'||a.CUST_NAME||\'\'\',\'\'\'||a.CUST_TYPE||\'\'\',\'\'\'||a.CUST_STATE||\'\'\',\'\'\'||a.PSPT_TYPE_CODE||\'\'\',\'\'\'||a.PSPT_ID||\'\'\',\'\'\'||a.EPARCHY_CODE||\'\'\',\'\'\'||a.CITY_CODE||\'\'\',\'\'\'||a.CUST_PASSWD||\'\'\',\'\'\'||a.SCORE_VALUE||\'\'\',\'\'\'||a.CREDIT_CLASS||\'\'\',\'\'\'||a.BASIC_CREDIT_VALUE||\'\'\',\'\'\'||a.CREDIT_VALUE||\'\'\',\'\'\'||a.CREDIT_CONTROL_ID||\'\'\',\'\'\'||a.DEVELOP_DEPART_ID||\'\'\',\'\'\'||a.DEVELOP_STAFF_ID||\'\'\',\'\'\'||a.IN_DEPART_ID||\'\'\',\'\'\'||a.IN_STAFF_ID||\'\'\',to_date(\'\'\'||to_char(a.IN_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),\'\'\'||a.REMOVE_TAG||\'\'\',to_date(\'\'\'||to_char(a.REMOVE_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),\'\'\'||a.REMOVE_STAFF_ID||\'\'\',\'\'\'||a.REMOVE_CHANGE||\'\'\',to_date(\'\'\'||to_char(a.UPDATE_TIME,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),\'\'\'||a.UPDATE_DEPART_ID||\'\'\',\'\'\'||a.UPDATE_STAFF_ID||\'\'\',\'\'\'||a.REMARK||\'\'\',\'\'\'||a.CUST_CLASS_TYPE||\'\'\',\'\'\'||a.PROVINCE_CODE||\'\'\',\'\'\'||a.RSRV_TAG1||\'\'\')\' istsql '
	'from uop_actself._domain.tf_f_customer@toactself._domain a, uop_actself._domain.tf_f_user@toactself._domain b where a.cust_id = b.cust_id and b.user_id in (self._user_id)'
	' union all '
	'select distinct \'insert into tf_f_user_param values (\'\'\'||PARTITION_ID||\'\'\',\'\'\'||USER_ID||\'\'\',\'\'\'||PARAM_ID||\'\'\',\'\'\'||PARAM_VALUE||\'\'\',to_date(\'\'\'||to_char(START_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),to_date(\'\'\'||to_char(END_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),to_date(\'\'\'||to_char(UPDATE_TIME,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),\'\'\'||UPDATE_DEPART_ID||\'\'\',\'\'\'||UPDATE_STAFF_ID||\'\'\',\'\'\'||PROV_CODE||\'\'\')\' istsql '
	'from uop_actself._domain.tf_f_user_param@toactself._domain where user_id in (self._user_id)'
	' union all '
	'select distinct \'insert into tf_f_user_serv values (\'\'\'||PARTITION_ID||\'\'\',\'\'\'||SERV_INS_ID||\'\'\',\'\'\'||USER_ID||\'\'\',\'\'\'||SERV_ID||\'\'\',to_date(\'\'\'||to_char(PRIOR_ORDER_TIME,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),\'\'\'||MAIN_TAG||\'\'\',\'\'\'||PRODUCT_ID||\'\'\',\'\'\'||SERV_BUND_ID||\'\'\',to_date(\'\'\'||to_char(START_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),to_date(\'\'\'||to_char(END_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),to_date(\'\'\'||to_char(UPDATE_TIME,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),\'\'\'||UPDATE_DEPART_ID||\'\'\',\'\'\'||UPDATE_STAFF_ID||\'\'\',\'\'\'||PROV_CODE||\'\'\')\' istsql '
	'from uop_actself._domain.tf_f_user_serv@toactself._domain where user_id in (self._user_id)'
	' union all '
	'select distinct \'insert into tf_f_user_servstate values (\'\'\'||PARTITION_ID||\'\'\',\'\'\'||SERV_INS_ID||\'\'\',\'\'\'||USER_ID||\'\'\',\'\'\'||SERV_ID||\'\'\',\'\'\'||MAIN_TAG||\'\'\',\'\'\'||SERV_STATE_CODE||\'\'\',to_date(\'\'\'||to_char(START_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),to_date(\'\'\'||to_char(END_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),\'\'\'||UPDATE_DEPART_ID||\'\'\',\'\'\'||UPDATE_STAFF_ID||\'\'\',to_date(\'\'\'||to_char(UPDATE_TIME,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),\'\'\'||PROV_CODE||\'\'\')\' istsql '
	'from uop_actself._domain.tf_f_user_servstate@toactself._domain where user_id in (self._user_id)'
	' union all '
	'select distinct \'insert into tf_f_user_importinfo values (\'\'\'||PARTITION_ID||\'\'\',\'\'\'||USER_ID||\'\'\',\'\'\'||NET_TYPE_CODE||\'\'\',\'\'\'||PRODUCT_ID||\'\'\',\'\'\'||BRAND_CODE||\'\'\',\'\'\'||LOGIC_PHONE||\'\'\',\'\'\'||PHYICAL_PHONE||\'\'\',to_date(\'\'\'||to_char(START_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),to_date(\'\'\'||to_char(END_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),to_date(\'\'\'||to_char(UPDATE_TIME,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),\'\'\'||UPDATE_DEPART_ID||\'\'\',\'\'\'||UPDATE_STAFF_ID||\'\'\',\'\'\'||PREPAY_TAG||\'\'\',\'\'\'||PROV_CODE||\'\'\')\' istsql '
	'from uop_actself._domain.tf_f_user_importinfo@toactself._domain where user_id in (self._user_id)'
	' union all '
	'select distinct \'insert into tf_f_feepolicy values (\'\'\'||PARTITION_ID||\'\'\',\'\'\'||FEEPOLICY_INS_ID||\'\'\',\'\'\'||ID_TYPE||\'\'\',\'\'\'||ID||\'\'\',\'\'\'||FEEPOLICY_ID||\'\'\',\'\'\'||RELA_USER_ID||\'\'\',\'\'\'||PRODUCT_ID||\'\'\',\'\'\'||SERV_BUND_ID||\'\'\',\'\'\'||SERV_ID||\'\'\',\'\'\'||FEEPOLICY_BUND_ID||\'\'\',to_date(\'\'\'||to_char(START_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),to_date(\'\'\'||to_char(END_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),to_date(\'\'\'||to_char(UPDATE_TIME,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),\'\'\'||UPDATE_DEPART_ID||\'\'\',\'\'\'||UPDATE_STAFF_ID||\'\'\',\'\'\'||PROV_CODE||\'\'\')\' istsql '
	'from uop_actself._domain.tf_f_feepolicy@toactself._domain where id_type = \'0\' and id in (self._user_id)'
	' union all '
	'select distinct \'insert into tf_f_feepolicy_param values (\'\'\'||a.FEEPOLICY_INS_ID||\'\'\',\'\'\'||a.FEEPOLICY_PARAM_ID||\'\'\',\'\'\'||a.FEEPOLICY_PARAM_VALUE||\'\'\',to_date(\'\'\'||to_char(a.START_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),to_date(\'\'\'||to_char(a.END_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),to_date(\'\'\'||to_char(a.UPDATE_TIME,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),\'\'\'||a.UPDATE_DEPART_ID||\'\'\',\'\'\'||a.UPDATE_STAFF_ID||\'\'\',\'\'\'||a.PROV_CODE||\'\'\')\' istsql '
	'from uop_actself._domain.tf_f_feepolicy_param@toactself._domain a, uop_actself._domain.tf_f_feepolicy@toactself._domain b where a.feepolicy_ins_id = b.feepolicy_ins_id and b.id_type = \'0\' and b.id in (self._user_id)'
	' union all '
	'select distinct \'insert into tf_f_payrelation values (\'\'\'||PARTITION_ID||\'\'\',\'\'\'||PAYRELATION_ID||\'\'\',\'\'\'||USER_ID||\'\'\',\'\'\'||ITEM_CODE||\'\'\',\'\'\'||PAY_PRIORITY||\'\'\',\'\'\'||ADDUP_METHOD||\'\'\',\'\'\'||ADDUP_MONTHS||\'\'\',\'\'\'||LIMIT_TYPE||\'\'\',\'\'\'||LIMIT_VALUE||\'\'\',\'\'\'||FILL_TAG||\'\'\',\'\'\'||ACCT_ID||\'\'\',\'\'\'||BIND_TYPE||\'\'\',\'\'\'||DISCNT_PRIORITY||\'\'\',\'\'\'||DEFAULT_TAG||\'\'\',\'\'\'||ACT_TAG||\'\'\',\'\'\'||START_CYC_ID||\'\'\',\'\'\'||END_CYC_ID||\'\'\',to_date(\'\'\'||to_char(UPDATE_TIME,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),\'\'\'||UPDATE_DEPART_ID||\'\'\',\'\'\'||UPDATE_STAFF_ID||\'\'\',\'\'\'||PROV_CODE||\'\'\')\' istsql '
	'from uop_actself._domain.tf_f_payrelation@toactself._domain where user_id in (self._user_id)'
	' union all '
	'select distinct \'insert into tf_f_account values (\'\'\'||a.PARTITION_ID||\'\'\',\'\'\'||a.ACCT_ID||\'\'\',\'\'\'||a.EPARCHY_CODE||\'\'\',\'\'\'||a.CITY_CODE||\'\'\',\'\'\'||a.CUST_ID||\'\'\',\'\'\'||a.PAY_NAME||\'\'\',\'\'\'||a.PAY_MODE_CODE||\'\'\',\'\'\'||a.CONTRACT_NO||\'\'\',\'\'\'||a.REMOVE_TAG||\'\'\',to_date(\'\'\'||to_char(a.OPEN_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),to_date(\'\'\'||to_char(a.UPDATE_TIME,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),\'\'\'||a.UPDATE_DEPART_ID||\'\'\',\'\'\'||a.UPDATE_STAFF_ID||\'\'\',\'\'\'||a.NET_TYPE_CODE||\'\'\',\'\'\'||a.SCORE_VALUE||\'\'\',\'\'\'||a.CREDIT_CLASS_ID||\'\'\',\'\'\'||a.BASIC_CREDIT_VALUE||\'\'\',\'\'\'||a.CREDIT_VALUE||\'\'\',\'\'\'||a.CREDIT_CONTROL_ID||\'\'\',\'\'\'||a.DEBUTY_USER_ID||\'\'\',\'\'\'||a.DEBUTY_CODE||\'\'\',to_date(\'\'\'||to_char(a.REMOVE_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),\'\'\'||a.PROVINCE_CODE||\'\'\')\' istsql '
	'from uop_actself._domain.tf_f_account@toactself._domain a, uop_actself._domain.tf_f_payrelation@toactself._domain b where TO_CHAR(sysdate,\'YYYYMM\') between b.start_cyc_id and b.end_cyc_id and a.acct_id = b.acct_id and b.user_id in (self._user_id)'
	' union all '
	'select distinct \'insert into tf_f_user_product values (\'\'\'||PARTITION_ID||\'\'\',\'\'\'||USER_ID||\'\'\',\'\'\'||PRODUCT_MODE||\'\'\',\'\'\'||PRODUCT_ID||\'\'\',\'\'\'||BRAND_CODE||\'\'\',to_date(\'\'\'||to_char(START_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),to_date(\'\'\'||to_char(END_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),\'\'\'||ITEM_ID||\'\'\',\'\'\'||USER_ID_A||\'\'\',\'\'\'||PROV_CODE||\'\'\')\' istsql '
	'from uop_actself._domain.tf_f_user_product@toactself._domain where user_id in (self._user_id)'
	' union all '
	'select distinct \'insert into tf_f_user_member values (\'\'\'||PARTITION_ID||\'\'\',\'\'\'||USER_ID||\'\'\',\'\'\'||MEMBER_ROLE_CODE||\'\'\',\'\'\'||MEMBER_ROLE_TYPE||\'\'\',\'\'\'||MEMBER_ROLE_ID||\'\'\',\'\'\'||MEMBER_ROLE_NUMBER||\'\'\',\'\'\'||MEMBER_ROLE_SHORTNUM||\'\'\',to_date(\'\'\'||to_char(START_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),to_date(\'\'\'||to_char(END_DATE,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),to_date(\'\'\'||to_char(UPDATE_TIME,\'yyyymmddhh24miss\')||\'\'\',\'\'YYYYMMDDHH24MISS\'\'),\'\'\'||UPDATE_DEPART_ID||\'\'\',\'\'\'||UPDATE_STAFF_ID||\'\'\',\'\'\'||DISCNT_PRIORITY||\'\'\',\'\'\'||RELATION_TYPE_CODE||\'\'\',\'\'\'||ITEM_ID||\'\'\',\'\'\'||PROV_CODE||\'\'\')\' istsql '
	'from uop_actself._domain.tf_f_user_member@toactself._domain where user_id in (self._user_id) or member_role_id in (self._user_id) and sysdate between start_date and end_date '
	)

#导DMDB sql
dsql_dmdb = (
	#'delete from tf_f_account where acct_id in (select acct_id from tf_f_payrelation where sysdate between start_date and end_date and user_id in (self._user_id));'
	#'delete from tf_f_user_servstate where user_id in (self._user_id);\n'
	#'delete from tf_f_user_param where user_id in (self._user_id);\n'
	#'delete from tf_f_feepolicy where id_type = 0 and id in (self._user_id);\n'
	#'delete from tf_f_user_importinfo where user_id in (self._user_id);\n'
	#'delete from tf_f_user_product where user_id in (self._user_id);\n'
	#'delete from tf_f_user_serv where user_id in (self._user_id);\n'
	'delete from TF_F_ACCOUNT where acct_id in (select acct_id from tf_f_payrelation where user_id in (self._user_id));\n'
	'delete from TF_F_PAYRELATION where user_id in (self._user_id);\n'
	'delete from TF_F_CUSTOMER where cust_id in (select cust_id from TF_F_USER where user_id in (self._user_id));\n'
	'delete from TF_F_USER where user_id in (self._user_id);\n'
	'delete from TF_F_USER_PARAM where user_id in (self._user_id);\n'
	'delete from TF_F_USER_SERV where user_id in (self._user_id);\n'
	'delete from TF_F_USER_SERVSTATE where user_id in (self._user_id);\n'
	'delete from TF_F_USER_IMPORTINFO where user_id in (self._user_id);\n'
	'delete from TF_F_FEEPOLICY_PARAM where feepolicy_ins_id in (select feepolicy_ins_id from TF_F_FEEPOLICY where id in (self._user_id));\n'
	'delete from TF_F_FEEPOLICY where id_type = 0 and id in (self._user_id);\n'
	'delete from TF_F_USER_PRODUCT where user_id in (self._user_id);\n'
	'delete from TF_F_USER_MEMBER where (user_id in (self._user_id) or member_role_id in (self._user_id));\n'
	)
sql_dmdb = (
	'select \'insert into tf_f_user (user_id,dummy_tag,net_type_code,serial_number,eparchy_code,city_code,cust_id,usecust_id,brand_code,product_id,user_type_code,prepay_tag,service_state_code,open_mode,acct_tag,remove_tag,in_date,open_date,pre_destroy_date,destroy_date,first_call_date,last_stop_date,credit_class,base_credit_value,credit_value,credit_control_id,changeuser_date,score_value,update_time,province_code) values (\'\'\'||a.USER_ID||\'\'\',\'\'\'||a.DUMMY_TAG||\'\'\',\'\'\'||a.NET_TYPE_CODE||\'\'\',\'\'\'||a.SERIAL_NUMBER||\'\'\',\'\'\'||a.EPARCHY_CODE||\'\'\',\'\'\'||a.CITY_CODE||\'\'\',\'\'\'||a.CUST_ID||\'\'\',\'\'\'||a.USECUST_ID||\'\'\',\'\'\'||a.BRAND_CODE||\'\'\',\'\'\'||a.PRODUCT_ID||\'\'\',\'\'\'||a.USER_TYPE_CODE||\'\'\',\'\'\'||a.PREPAY_TAG||\'\'\',\'\'\'||a.SERVICE_STATE_CODE||\'\'\',\'\'\'||a.OPEN_MODE||\'\'\',\'\'\'||a.ACCT_TAG||\'\'\',\'\'\'||a.REMOVE_TAG||\'\'\',\'\'\'||to_char(a.IN_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||to_char(a.IN_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||a.PRE_DESTROY_DATE||\'\'\',\'\'\'||to_char(a.DESTROY_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||to_char(a.FIRST_CALL_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||to_char(a.LAST_STOP_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||a.CREDIT_CLASS||\'\'\',\'\'\'||a.BASE_CREDIT_VALUE||\'\'\',\'\'\'||a.CREDIT_VALUE||\'\'\',\'\'\'||a.CREDIT_CONTROL_ID||\'\'\',\'\'\'||to_char(a.CHANGEUSER_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||a.SCORE_VALUE||\'\'\',\'\'\'||to_char(a.UPDATE_TIME,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||a.PROVINCE_CODE||\'\'\');\' istsql'
	' from tf_f_user a where a.user_id in (self._user_id)'
	' union all '
	'select \'insert into tf_f_user_serv (serv_ins_id,user_id,serv_id,prior_order_time,main_tag,product_id,serv_bund_id,start_date,end_date) values (\'\'\'||a.SERV_INS_ID||\'\'\',\'\'\'||a.USER_ID||\'\'\',\'\'\'||a.SERV_ID||\'\'\',\'\'\'||a.PRIOR_ORDER_TIME||\'\'\',\'\'\'||a.MAIN_TAG||\'\'\',\'\'\'||a.PRODUCT_ID||\'\'\',\'\'\'||a.SERV_BUND_ID||\'\'\',\'\'\'||to_char(a.START_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||to_char(a.END_DATE,\'YYYYMMDDHH24MISS\')||\'\'\');\' istsql'
	' from tf_f_user_serv a where a.user_id in (self._user_id) and sysdate between a.start_date and a.end_date'
	' union all '
	'select \'insert into tf_f_user_servstate (user_id,serv_id,serv_ins_id,main_tag,serv_state_code,start_date,end_date) values (\'\'\'||a.USER_ID||\'\'\',\'\'\'||a.SERV_ID||\'\'\',\'\'\'||a.SERV_INS_ID||\'\'\',\'\'\'||a.MAIN_TAG||\'\'\',\'\'\'||a.SERV_STATE_CODE||\'\'\',\'\'\'||to_char(a.START_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||to_char(a.END_DATE,\'YYYYMMDDHH24MISS\')||\'\'\');\' istsql'
	' from tf_f_user_servstate a where a.user_id in (self._user_id) and sysdate between a.start_date and a.end_date'
	' union all '
	'select \'insert into tf_f_user_param(USER_ID,PARAM_ID,PARAM_VALUE,START_DATE,END_DATE) values (\'\'\'||user_id||\'\'\',\'\'\'||param_id||\'\'\',\'\'\'||param_value||\'\'\',\'\'\'||to_char(start_date,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||to_char(end_date,\'YYYYMMDDHH24MISS\')||\'\'\');\' istsql'
	' from tf_f_user_param a where user_id in (self._user_id) and sysdate between a.start_date and a.end_date'
	' union all '
	'select \'insert into tf_f_feepolicy (FEEPOLICY_INS_ID,ID_TYPE,ID,FEEPOLICY_ID,RELA_USER_ID,PRODUCT_ID,SERV_BUND_ID,SERV_ID,FEEPOLICY_BUND_ID,START_DATE,END_DATE) values (\'\'\'||FEEPOLICY_INS_ID||\'\'\',\'\'\'||ID_TYPE||\'\'\',\'\'\'||ID||\'\'\',\'\'\'||FEEPOLICY_ID||\'\'\',\'\'\'||RELA_USER_ID||\'\'\',\'\'\'||PRODUCT_ID||\'\'\',\'\'\'||SERV_BUND_ID||\'\'\',\'\'\'||SERV_ID||\'\'\',\'\'\'||FEEPOLICY_BUND_ID||\'\'\',\'\'\'||to_char(START_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||to_char(END_DATE,\'YYYYMMDDHH24MISS\')||\'\'\');\' istsql'
	' from tf_f_feepolicy a where a.id_type = 0 and a.id in (self._user_id) and sysdate between a.start_date and a.end_date'
	' union all '
	'select \'insert into tf_f_user_importinfo (USER_ID,NET_TYPE_CODE,PREPAY_TAG,PRODUCT_ID,BRAND_CODE,LOGIC_PHONE,PHYICAL_PHONE,START_DATE,END_DATE) values (\'\'\'||USER_ID||\'\'\',\'\'\'||NET_TYPE_CODE||\'\'\',\'\'\'||PREPAY_TAG||\'\'\',\'\'\'||PRODUCT_ID||\'\'\',\'\'\'||BRAND_CODE||\'\'\',\'\'\'||LOGIC_PHONE||\'\'\',\'\'\'||PHYICAL_PHONE||\'\'\',\'\'\'||to_char(START_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||to_char(END_DATE,\'YYYYMMDDHH24MISS\')||\'\'\');\' istsql'
	' from tf_f_user_importinfo a where user_id in (self._user_id) and sysdate between a.start_date and a.end_date'
	' union all '
	'select \'insert into tf_f_user_product (USER_ID,PRODUCT_MODE,PRODUCT_ID,BRAND_CODE,START_DATE,END_DATE,ITEM_ID,USER_ID_A) values (\'\'\' || a.USER_ID || \'\'\',\'\'\' || a.PRODUCT_MODE || \'\'\',\'\'\' || a.PRODUCT_ID || \'\'\',\'\'\' ||a.BRAND_CODE|| \'\'\',\'\'\' || to_char(a.START_DATE, \'YYYYMMDDHH24MISS\') || \'\'\',\'\'\' || to_char(a.END_DATE, \'YYYYMMDDHH24MISS\') || \'\'\',\'\'\' ||a.ITEM_ID|| \'\'\',\'\'\' ||a.USER_ID_A|| \'\'\');\' istsql'
	' from tf_f_user_product a where a.user_id in (self._user_id) and sysdate between a.start_date and a.end_date'
	' union all '
	'select \'insert into tf_f_payrelation (payrelation_id,user_id,item_code,pay_priority,addup_method,addup_months,limit_type,limit_value,fill_tag,acct_id,bind_type,discnt_priority,default_tag,act_tag,start_cyc_id,end_cyc_id) values (\'\'\'||a.PAYRELATION_ID||\'\'\',\'\'\'||a.USER_ID||\'\'\',\'\'\'||a.ITEM_CODE||\'\'\',\'\'\'||a.PAY_PRIORITY||\'\'\',\'\'\'||a.ADDUP_METHOD||\'\'\',\'\'\'||a.ADDUP_MONTHS||\'\'\',\'\'\'||a.LIMIT_TYPE||\'\'\',\'\'\'||a.LIMIT_VALUE||\'\'\',\'\'\'||a.FILL_TAG||\'\'\',\'\'\'||a.ACCT_ID||\'\'\',\'\'\'||a.BIND_TYPE||\'\'\',\'\'\'||a.DISCNT_PRIORITY||\'\'\',\'\'\'||a.DEFAULT_TAG||\'\'\',\'\'\'||a.ACT_TAG||\'\'\',\'\'\'||a.START_CYC_ID||\'\'\',\'\'\'||a.END_CYC_ID||\'\'\');\' istsql'
	' from tf_f_payrelation a where a.user_id in (self._user_id) and to_char(sysdate, \'YYYYMM\') between a.start_cyc_id and a.end_cyc_id'
	' union all '
	'select \'insert into tf_f_account (acct_id,eparchy_code,city_code,cust_id,pay_mode_code,score_value,credit_value,credit_control_id,remove_tag,open_date,remove_date,province_code) values (\'\'\'||a.ACCT_ID||\'\'\',\'\'\'||a.EPARCHY_CODE||\'\'\',\'\'\'||a.CITY_CODE||\'\'\',\'\'\'||a.CUST_ID||\'\'\',\'\'\'||a.PAY_MODE_CODE||\'\'\',\'\'\'||a.SCORE_VALUE||\'\'\',\'\'\'||a.CREDIT_VALUE||\'\'\',\'\'\'||a.CREDIT_CONTROL_ID||\'\'\',\'\'\'||a.REMOVE_TAG||\'\'\',\'\'\'||to_char(a.OPEN_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||to_char(a.REMOVE_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||a.PROVINCE_CODE||\'\'\');\' istsql'
	' from tf_f_account a, tf_f_payrelation b where TO_CHAR(sysdate,\'YYYYMM\') between b.start_cyc_id and b.end_cyc_id and a.acct_id = b.acct_id and b.user_id in (self._user_id)'
	' union all '
	'select \'insert into tf_f_user_member(USER_ID,MEMBER_ROLE_CODE,MEMBER_ROLE_TYPE,MEMBER_ROLE_ID,MEMBER_ROLE_NUMBER,MEMBER_ROLE_SHORTNUM,DISCNT_PRIORITY,RELATION_TYPE_CODE,ITEM_ID,START_DATE,END_DATE) values (\'\'\'||USER_ID||\'\'\',\'\'\'||MEMBER_ROLE_CODE||\'\'\',\'\'\'||MEMBER_ROLE_TYPE||\'\'\',\'\'\'||MEMBER_ROLE_ID||\'\'\',\'\'\'||MEMBER_ROLE_NUMBER||\'\'\',\'\'\'||MEMBER_ROLE_SHORTNUM||\'\'\',\'\'\'||DISCNT_PRIORITY||\'\'\',\'\'\'||RELATION_TYPE_CODE||\'\'\',\'\'\'||ITEM_ID||\'\'\',\'\'\'||to_char(START_DATE,\'YYYYMMDDHH24MISS\')||\'\'\',\'\'\'||to_char(END_DATE,\'YYYYMMDDHH24MISS\')||\'\'\');\' istsql'
	' from tf_f_user_member where user_id in (self._user_id) or member_role_id in (self._user_id) and sysdate between start_date and end_date'
	)