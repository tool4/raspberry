#!/bin/sh
systemctl daemon-reload

sudo systemctl stop lcd.service
sudo systemctl start lcd.service
sudo systemctl restart udp.service
sudo systemctl restart ir.service
sudo systemctl restart net_info.service
