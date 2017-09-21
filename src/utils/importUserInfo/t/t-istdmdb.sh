r=`dsql<<EOF
delete from TF_F_ACCOUNT where acct_id in (select acct_id from tf_f_payrelation where user_id in (1114061524350998));
delete from TF_F_PAYRELATION where user_id in (1114061524350998);
delete from TF_F_CUSTOMER where cust_id in (select cust_id from TF_F_USER where user_id in (1114061524350998));
delete from TF_F_USER where user_id in (1114061524350998);
delete from TF_F_USER_PARAM where user_id in (1114061524350998);
delete from TF_F_USER_SERV where user_id in (1114061524350998);
delete from TF_F_USER_SERVSTATE where user_id in (1114061524350998);
delete from TF_F_USER_IMPORTINFO where user_id in (1114061524350998);
delete from TF_F_FEEPOLICY_PARAM where feepolicy_ins_id in (select feepolicy_ins_id from TF_F_FEEPOLICY where id in (1114061524350998));
delete from TF_F_FEEPOLICY where id_type = 0 and id in (1114061524350998);
delete from TF_F_USER_PRODUCT where user_id in (1114061524350998);
delete from TF_F_USER_MEMBER where (user_id in (1114061524350998) or member_role_id in (1114061524350998));
commit;
quit;
EOF`