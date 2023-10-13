import os
from python_scripts.manage_files import create_template, read_secret


def get_ks_name(node_name):
    return 'ks-' + node_name + '.cfg'


def create_kickstart(node, networks):
    ftp_dir = os.environ.get('FTP_DIR')
    secret = read_secret()
    ks_name = get_ks_name(node.name)

    net_info_list = [
        {'gateway': network.gateway, 
         'node_ip': node.ips[network.name], 
         'netmask': network.netmask} 
         for network in networks]

    context = {
        'admin_name': node.conf['admin_name'],
        'timezone': node.conf['timezone'],
        'host_name': node.host_name,

        'adminpw': secret['adminpw'],
        'rootpw': secret['rootpw'],
        'ssh_key': secret['ssh_key'],

        'net_info_list': net_info_list
    }
    create_template(ftp_dir, ks_name, 'ks_template.cfg', context)


def create_kickstarts(nodes, networks):
    for node in nodes:
        create_kickstart(node, networks)