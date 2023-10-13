import os
import subprocess
from python_scripts.manage_files import create_template


def create_network_template(network):
    data_dir = os.environ.get('DATA_DIR')
    context = {
        'internal_net': network.name,
        'bridge_name': network.bridge,
        'ip_address': network.network_ip,
        'netmask': network.netmask
    }
    create_template(data_dir, network.name + '.xml', 'internet_template.xml', context)


def run_bash_script(script, args=[]):
    bash_script_dir = os.environ.get('BASH_SCRIPT_DIR')
    bash_script_path = os.path.join(bash_script_dir, script)
    try:
        subprocess.run(['bash', bash_script_path] + args, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Ошибка выполнения скрипта {script}: {e}')


def setup_network_in_linux(network):
    create_network_template(network)
    run_bash_script('network_setup.sh', [network.name])


def setup_networks_in_linux(networks):
    for network in networks:
        setup_network_in_linux(network)