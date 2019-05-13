cp lcd.service /etc/systemd/system/
cp timer.service /etc/systemd/system/
cp ir.service /etc/systemd/system/

sudo systemctl daemon-reload

sudo systemctl enable lcd.service
sudo systemctl start lcd.service

sudo systemctl enable timer.service
sudo systemctl start timer.service

sudo systemctl enable ir.service
sudo systemctl start ir.service

