#!/bin/bash

cd  /home/ubuntu/SKN04-4th-3Team

echo "> 🔵 Stop & Remove docker services."
sudo docker-compose down

echo "> 🟢 Run new docker services."
sudo docker-compose up -d --build >> /var/log/deploy.log 2>&1