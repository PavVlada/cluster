import os
from python_scripts.manage_files import create_template


def count_mask_bits(netmask):
    octets = map(int, netmask.split('.'))
    bit_netmask = sum(bin(octet).count('1') for octet in octets)
    return bit_netmask


def create_dir(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def get_inventory_dir():
    ansible_dir = os.environ.get('ANSIBLE_DIR')
    environment = os.environ.get('ENVIRONMENT')
    return os.path.join(ansible_dir, 'inventories', environment)


def create_cluster_vars(networks):
    environment = get_inventory_dir()
    cluster_vars_dir = os.path.join(environment, 'group_vars', 'cluster')
    create_dir(cluster_vars_dir)

    context = {
        'nameserver': networks[1].gateway
    }

    create_template(cluster_vars_dir, 'main.yml', 'cluster_vars_template.yml', context)


def create_inventory(config):
    inventory_dir = get_inventory_dir()
    count_master = config['nodes']['count_master']
    count_worker = config['nodes']['count_worker']
    count_node = count_master + count_worker

    master_host = f'node[1:{count_master}]' if count_master != 1 else 'node1'
    worker_host = f'node[{count_master + 1}:{count_node}]' if count_worker != 1 else f'node{count_master + 1}'

    context = {
        'master_host': master_host + '.internal',
        'worker_host': worker_host + '.internal'
    }

    create_template(inventory_dir, 'inventory.yml', 'inventory_template.yml', context)


def create_host_vars(nodes, networks):
    for node in nodes:
        invenvtory_dir = get_inventory_dir()
        host_vars_dir = os.path.join(invenvtory_dir, 'host_vars', node.host_name)

        context = {
            'ansible_host': node.ips['default'],
            'ansible_ssh_user': node.conf['admin_name'],
            'internal_ip': node.ips['intnet'],
            'network_ip': networks[1].network_ip,
            'netmask': count_mask_bits(networks[1].netmask)
        }

        create_dir(host_vars_dir)
        create_template(host_vars_dir, 'vars.yml', 'host_vars_template.yml', context)


def create_ansible_files(nodes, networks, config):
    create_host_vars(nodes, networks)
    create_cluster_vars(networks)
    create_inventory(config)
    print("Ansible файлы созданы")