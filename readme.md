# Welcome to electric.vote!

electric.vote is an open source project under "GNU General Public License v3" that aims to provide liquid democracy to associations / companies / communities /...

The website can be accessed here: https://electric.vote

We're always happy about bug reports / feature requests / constructive feed-back - just leave a message at feedback@electric.vote.

# install instructions

## get python

install anaconda3 and the following packages:

- tornado
- numpy
- Pillow
- pymysql

## get mysql
> sudo apt-get install mysql-server

## set up database:
- login as "debian-sys-maint" ($ mysql -u debian-sys-maint -h localhost -p)
- use password as specified in /etc/mysql/debian.cnf
- create new admin user with passsword (> CREATE USER 'admin'@'localhost' IDENTIFIED BY 'password';)
- grant and flush privileges (> GRANT ALL PRIVILEGES ON * . * TO 'admin'@'localhost';) (> FLUSH PRIVILEGES;)
- create database (> CREATE DATABASE liDem;)
- load database (> USE liDem; ) (> source /database/liDem.sql;)
- set timezone: SET @@global.time_zone = '+xx:00'

## get a signed certificate
1. create a private key and a "certificate signing request" (.csr):
    > openssl req -nodes -new -newkey rsa:2048 -sha256 -out csr.pem
    -> this will create the following files: private key (privkey.pem) and CSR file (csr.pem)
2. let a certificate authority (e.g. namecheap) sign your csr
    -> you'll get a new certificate (.crt) file
3. now, use the .crt file as the certfile and the privkey.pem file as the keyfile

## set up certificates / passwords file
1. create folder /Certificates.
2. copy the certificate file ("mykey.crt") and key file ("mykey.key") into this folder.
3. create a passwords.py file containing the following specifications:  
email_password = "..."  
database_username = "..."  
database_password = "..."  
cookie_secret = "..."

## start the server
the main file for the tornado server is main.py. You can start it in the background by calling:
> nohup sudo ~/anaconda3/envs/env_server/bin/python main.py &

## start poll evaluation service
the evaluation service will regularly keep the results of open / voting polls up to date. You can start it in the background by calling:
> nohup sudo ~/anaconda3/envs/env_server/bin/python evaluation_service.py &

## emails
incoming emails are forwarded to electric.vote@gmail.com
outgoing emails can be sent over the following smtp server:  
smtp_server = "mail.privateemail.com"  
sender_email = "info@electric.vote"  
password = as specified in Certificates/passwords.py

# how to read the code?

Unfortunately, at the moment, the code is documented only very sparsely. However, with a few instructions, I hope you can still find your way through the code:

1. If you want to find a specific python class belonging to a certain URL, you should search for it in main.py.
2. access_database.py builds the interface between the python code and the sql database. Furthermore, it contains the code to evaluate polls (evaluate_poll).
3. The /static folder contains static web content (such as javascript / css files / icons / images)
4. The /template folder contains html templates for the column / center layouts as well as the html structure for all the remaining web-pages / emails.

