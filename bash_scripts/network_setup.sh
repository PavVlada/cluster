set -e

create_network_if_not_exist() {
    local network=$1
    if ! sudo virsh net-list --all | grep -wq "$network"; then
        echo "Создание сети $network..."
        sudo virsh net-create "$DATA_DIR/$network.xml"
        echo "Сеть $network создана"
    fi

}

start_network() {
    local network=$1
    if ! sudo virsh net-list | grep -wq "$network"; then
        sudo virsh net-start $network
    fi
    echo "Сеть $network запущена"
}

network=$1

create_network_if_not_exist "$network"
start_network "$network"