packages_list=("qemu" "qemu-kvm" "libvirt-daemon" "libvirt-clients" "bridge-utils" "virt-manager" "jq")

for package in "${packages_list[@]}"; do
    if ! dpkg -l | grep -q "^ii  $package"; then
        echo "Установка $package..."
        sudo apt-get install -y "$package"
    fi
done

sudo modprobe kvm
sudo gpasswd -a $USER libvirt
sudo gpasswd -a root libvirt
sudo usermod -aG libvirt $USER
sudo usermod -aG libvirt root
sudo usermod -aG kvm $USER
sudo usermod -aG kvm root
sudo usermod -aG users libvirt-qemu
echo "Завершена настройка virt"
