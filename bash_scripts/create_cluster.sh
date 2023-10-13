start_vm() {
    vm_name=$1
    status=$(sudo virsh domstate "$vm_name")
    if [ "$status" == "shut off" ]; then
        sudo virsh start "$vm_name"
    fi
}

output_lines=$(python ../python_scripts/main.py)

OLD_IFS=$IFS
IFS=$'\n'
output_list=($output_lines)
IFS=$OLD_IFS

for output in "${output_list[@]}"; do
    if [[ $output == "virt-install"* ]]; then
        vm_name=$(echo "$output" | grep -o -- '--name [^ ]*' | awk '{print $2}')
        if ! sudo virsh list --all | grep -q "$vm_name"; then
            echo "Создаю ${vm_name}"
            eval "${output}"
        fi
        # start_vm $vm_name
    else
        echo "${output}"
    fi
done

echo "Все ноды кластера созданы"

