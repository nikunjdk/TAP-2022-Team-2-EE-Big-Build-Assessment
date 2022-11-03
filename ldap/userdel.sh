#!/bin/sh 

tar -czf /root/archive/$1.tar.gz /home/$1

userdel -r $1

ldapdelete -x -D cn=Manager,dc=tap22,dc=ms -w 123456 uid=$1,ou=People,dc=tap22,dc=ms
ldapdelete -x -D cn=Manager,dc=tap22,dc=ms -w 123456 cn=$1,ou=Group,dc=tap22,dc=ms
echo "delprinc -force $1" | /usr/sbin/kadmin.local > /dev/null
