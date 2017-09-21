<SISQL>
select 'insert into tf_f_user_param values ('''||PARTITION_ID||''','''||USER_ID||''','''||PARAM_ID||''','''||PARAM_VALUE||''','''||START_DATE||''','''||END_DATE||''','''||UPDATE_TIME||''','''||UPDATE_DEPART_ID||''','''||UPDATE_STAFF_ID||''','''||PROV_CODE||''')' istsql from uop_actself._domain.tf_f_user_param@toactself._domain where user_id in (self._user_id)
</SISQL>

