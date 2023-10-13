#!/bin/bash
set -e

export PROJECT_DIR=$(pwd)
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"

cd "$(dirname "$0")"
source config.sh

log_file="install.log"

log() {
    echo "$(date): $1" >> "$log_file"
}

# log "Starting installation process..."

./install_virt.sh
./create_venv.sh
./start_ftp.sh
./create_dirs.sh
./create_ssh_key.sh
./download_iso.sh
source ../venv/bin/activate
./create_secret.sh
./create_cluster.sh
./run_ansible.sh
deactivate

# log "Installation completed successfully."
