package=vsftpd
vsftpd_conf="/etc/vsftpd.conf"
line="anon_root=$FTP_DIR"

if ! dpkg -l | grep -q "^ii  $package"; then
    echo "Установка $package..."
    sudo apt-get install -y "$package"
fi

sudo sed -i 's/^anonymous_enable=NO$/anonymous_enable=YES/' "$vsftpd_conf"
if [ ! -d "$FTP_DIR" ]; then
    sudo mkdir -p $FTP_DIR
    sudo chown $USER:$USER $FTP_DIR
fi
if ! grep -qF "$line" "$vsftpd_conf"; then
    echo "anon_root=$FTP_DIR" | sudo tee -a "$vsftpd_conf"
fi
sudo systemctl restart vsftpd

echo "Сервер FTP готов к работе"
