ret=`gsqlnet billing billing --dsn=QCUBIC213<<EOF
$1
commit;
\q
EOF`