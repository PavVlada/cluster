packages_list=("qemu" "qemu-kvm" "libvirt-daemon" "libvirt-clients" "bridge-utils" "virt-manager" "jq")

for package in "${packages_list[@]}"; do
    if ! dpkg -l | grep -q "^ii  $package"; then
        echo "Установка $package..."
        sudo apt-get install -y "$package 1>/dev/null"
    fi
done

sudo gpasswd -a $USER libvirt
sudo usermod -aG libvirt $USER
echo "Завершена настройка virt"