cp lcd.service /etc/systemd/system/
cp timer.service /etc/systemd/system/
cp ir.service /etc/systemd/system/
cp systemd/system/* /etc/systemd/system/

sudo systemctl daemon-reload

sudo systemctl enable lcd.service
sudo systemctl start lcd.service

sudo systemctl enable timer.service
sudo systemctl start timer.service

sudo systemctl enable ir.service
sudo systemctl start ir.service

sudo systemctl enable udp.service
sudo systemctl start ir.service

systemctl daemon-reload

sudo systemctl stop lcd.service
sudo systemctl start lcd.service
sudo systemctl restart udp.service
sudo systemctl restart ir.service
sudo systemctl restart net_info.service
