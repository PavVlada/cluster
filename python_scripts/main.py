from python_scripts.generate_ansible_files import create_ansible_files
from python_scripts.generate_kickstart import create_kickstarts
from python_scripts.generate_vm_creation_command import generate_vm_creation_command
from python_scripts.generate_random_ip import generate_random_ip
from python_scripts.manage_files import read_config
from python_scripts.network_setup import setup_networks_in_linux
from python_scripts.network import Network
from python_scripts.node import Node


def create_networks(config):
    return [Network(net_config['name'], net_config['network_ip'], 
                        net_config['netmask'], net_config['gateway'], net_config['bridge']) 
                        for net_config in config['networks']]


def create_nodes(config):
    node_config = config['nodes']
    count_node = node_config['count_master'] + node_config['count_worker']
    return [Node(node_config['name'] + '-' + str(i + 1), 'node' + str(i + 1) + '.internal',  node_config['conf']) for i in range(count_node)]


def assign_ips_to_nodes(nodes, ip_addresses):
    for i in range(len(nodes)):
        for ip_address in ip_addresses:
            nodes[i].assign_ip(ip_address['network'], ip_address['ips'][i])


def generate_ip_addresses(networks, config):
    count_node = config['nodes']['count_master'] + config['nodes']['count_worker']
    return [generate_random_ip(network, count_node) for network in networks]


if __name__=='__main__':
    config = read_config()

    networks = create_networks(config)
    nodes = create_nodes(config)

    ip_addresses = generate_ip_addresses(networks, config)
    assign_ips_to_nodes(nodes, ip_addresses)

    setup_networks_in_linux(networks)
    create_kickstarts(nodes, networks)
    create_ansible_files(nodes, networks, config)
    generate_vm_creation_command(nodes)


