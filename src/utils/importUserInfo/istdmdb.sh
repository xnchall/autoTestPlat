r=`dsql<<EOF
@$PWD/$1;
commit;
quit;
EOF`