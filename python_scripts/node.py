class Node:
    def __init__(self, name, host_name, conf):
        self.name = name
        self.host_name = host_name
        self.ips = {}
        self.conf = conf

    def assign_ip(self, network, ip):
        self.ips[network.name] = ip
