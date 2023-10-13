import os
from generate_kickstart import get_ks_name


def get_iso_path():
    iso_dir = os.environ.get('ISO_DIR')
    iso_name = os.environ.get('ISO_NAME')
    return os.path.join(iso_dir, iso_name)


def get_vm_options(node):
    iso_path = get_iso_path()
    return [
        '--name', node.name,
        '--ram', str(node.conf['ram']),
        '--vcpus', str(node.conf['vcpus']),
        '--disk', 'size=' + str(node.conf['disk_size']),
        '--os-variant', node.conf['os_variant'],
        '--location', iso_path,
        '--graphics', 'none',
        '--noreboot'
    ]


def get_network_options(node):
    network_options = list()
    for network in node.ips.keys():
        network_options.extend(['--network', 'network=' + network + ',model=virtio'])
    return network_options


def get_extra_options(node):
    ks_name = get_ks_name(node.name)
    return ['--extra-args="ks=ftp://'+ node.conf['ftp_ip'] +'/' + ks_name + ' console=ttyS0,115200n8"']


def creation_command(node):
    vm_options = get_vm_options(node)
    network_options = get_network_options(node)
    extra_options = get_extra_options(node)

    command = ['virt-install'] + vm_options + network_options + extra_options
    return ' '.join(command)


def generate_vm_creation_command(nodes):
    for node in nodes:
        print(creation_command(node))