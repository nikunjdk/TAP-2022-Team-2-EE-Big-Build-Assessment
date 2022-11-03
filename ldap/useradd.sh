#!/bin/sh 

for args; do
	useradd $args

	grep $args /etc/passwd > /root/user
	grep $args /etc/group > /root/group

	/usr/share/migrationtools/migrate_passwd.pl /root/user /root/user.ldif
	/usr/share/migrationtools/migrate_group.pl /root/group /root/group.ldif


	ldapadd -x -D cn=Manager,dc=tap22,dc=ms  -f /root/user.ldif -w 123456
	ldapadd -x -D cn=Manager,dc=tap22,dc=ms  -f /root/group.ldif -w 123456

	echo "$args 123456" > /root/newuser

	awk '{ print "ank -pw", $2, $1 }' < /root/newuser | /usr/sbin/kadmin.local> /dev/null
	
	mkdir /home/$args/.ssh
	cp /root/.ssh/authorized_keys /home/$args/.ssh/
done
