class Network:
    def __init__(self, name, network_ip, netmask, gateway, bridge):
        self.name = name
        self.network_ip = network_ip
        self.netmask = netmask
        self.gateway = gateway
        self.bridge = bridge
