import socket
import struct
import random


def ip_to_int(ip):
    return struct.unpack('!I', socket.inet_aton(ip))[0]


def int_to_ip(ip_int):
    return socket.inet_ntoa(struct.pack('!I', ip_int))


def available_hosts_count(net):
    netmask_int = ip_to_int(net.netmask)
    return (netmask_int ^ 0xFFFFFFFF) - 1


def generate_random_ip(net, count):
    network_int = ip_to_int(net.network_ip)
    available_hosts = available_hosts_count(net)

    
    if count > available_hosts:
        raise ValueError("Недостаточно доступных IP адресов в заданной сети.")
    
    generated_ips = set()
    while len(generated_ips) < count:
        random_host_int = random.randint(1, available_hosts)
        ip_int = network_int + random_host_int
        generated_ips.add(int_to_ip(ip_int))

    return {
        'network': net,
        'ips': list(generated_ips)
    }
