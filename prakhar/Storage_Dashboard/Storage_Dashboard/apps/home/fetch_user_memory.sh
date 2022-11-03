#!/bin/bash
expect -c 'spawn ssh -i id_rsa_TAP.pem root@94.237.49.11 du -d 1 -h /home/ ; expect "Enter passphrase for key 'id_rsa_TAP.pem':"; send "EE2022@\!\r"; interact' > my_file.txt