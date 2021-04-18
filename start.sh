#!/bin/bash
apt-get update
apt-get install python3-pip -y
apt-get install mysql-server -y
apt-get install libmysqlclient-dev -y
pip3 install virtualenv

cd /home/ubuntu
git clone https://github.com/odobenuskr/aws-sample-general-app
cd aws-sample-general-app
mkdir uploads

virtualenv venv
. venv/bin/activate
pip3 install -r requirements.txt

cp main.service /etc/systemd/system/
systemctl start main
systemctl enable main
