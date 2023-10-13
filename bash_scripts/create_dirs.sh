create_dir() {
    local dir=$1
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
    fi
}

create_list_dir() {
    local dir_list=("$@")
    for dir in "${dir_list[@]}"; do
        create_dir "$dir"
    done
}

conf_dirs=("$ANSIBLE_DIR" "$ISO_DIR" "$SECRET_DIR" "$SSH_DIR" "$DATA_DIR")
create_list_dir "${conf_dirs[@]}"

create_dir "$ANSIBLE_DIR/inventories/$ENVIRONMENT/host_vars"
