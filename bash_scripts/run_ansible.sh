set -e

check_ssh() {
    host=$1
    user=$2
    ssh -o BatchMode=yes -o StrictHostKeyChecking=no "$user@$host" exit
    return $?
}

try_ssh() {
    host=$1
    user=$2
    start_time=$(date +%s)
    while [ $(( $(date +%s) - $start_time )) -lt $TIMEOUT ]; do
        if check_ssh "$host" "$user"; then
            echo "$user@$host доступен"
            return
        else
            echo "Попытка подключения к $user@$host не удалась, ждем 10 секунд и пробуем снова"
            sleep 10
        fi
    done
    echo "Не удалось подключиться по SSH к $user@$host в течение $TIMEOUT секунд, прерываем выполнение"
    exit 1
}

get_host_and_try_ssh() {
    local host_vars_dir=$ANSIBLE_DIR/inventories/$ENVIRONMENT/host_vars
    local key_host=ansible_host
    local key_user=ansible_ssh_user

    for yml_file in "$host_vars_dir"/*/vars.yml; do
        if [[ -f "$yml_file" ]]; then
            values=($(yq -r ".$key_host, .$key_user" "$yml_file"))
            try_ssh ${values[0]} ${values[1]}
        fi
    done
}

run_playbook() {
    get_host_and_try_ssh

    playbook="$1"
    ansible-playbook "$PLAYBOOK_DIR/$1" -i $INVENTORY_DIR/inventory.yml -v
}


PLAYBOOK_DIR="./playbooks"
INVENTORY_DIR="./inventories/$ENVIRONMENT"
cd $ANSIBLE_DIR
run_playbook "preparation.yml"
cd $OLDPWD