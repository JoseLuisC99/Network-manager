from scripts.router import send_command

def set_rip(ip, user_info=None):
    if user_info is None:
        device = {
            'device_type': 'cisco_ios_telnet',
            'host': ip,
            'password': 'pass1234',
            'secret': 'cisco'
        }
    else:
        device = {
            'device_type': 'cisco_ios',
            'host': ip,
            'username': user_info['username'],
            'password': user_info['password']
        }
    def router_function(telnet):
        telnet.enable()
        telnet.send_command_timing(
            command_string = """
            configure terminal
            router rip
            version 2
            no auto-summary
            network 192.168.0.0
            network 192.168.1.0
            default-information originate
            redistribute static
            redistribute ospf 1 match internal external 1 external 2
            redistribute eigrp 1
            exit
            no router eigrp 1
            no router ospf 1
            exit
            """
        )
        return None
    return send_command(device, router_function)

def set_ospf(ip, user_info=None):
    if user_info is None:
        device = {
            'device_type': 'cisco_ios_telnet',
            'host': ip,
            'password': 'pass1234',
            'secret': 'cisco'
        }
    else:
        device = {
            'device_type': 'cisco_ios',
            'host': ip,
            'username': user_info['username'],
            'password': user_info['password']
        }
    def router_function(telnet):
        telnet.enable()
        telnet.send_command_timing(
            command_string = """
            configure terminal
            router ospf 1
            network 192.168.0.0 0.0.0.255 area 0
            network 192.168.1.0 0.0.0.255 area 0
            default-information originate
            redistribute static subnets
            redistribute rip subnets
            redistribute eigrp 1 subnets
            exit
            no router rip
            no router eigrp 1
            exit
            """
        )
        return None
    return send_command(device, router_function)

def set_eigrp(ip, user_info=None):
    if user_info is None:
        device = {
            'device_type': 'cisco_ios_telnet',
            'host': ip,
            'password': 'pass1234',
            'secret': 'cisco'
        }
    else:
        device = {
            'device_type': 'cisco_ios',
            'host': ip,
            'username': user_info['username'],
            'password': user_info['password']
        }
    def router_function(telnet):
        telnet.enable()
        telnet.send_command_timing(
            command_string = """
            configure terminal
            router eigrp 1
            network 192.168.0.0
            network 192.168.1.0
            default-information originate
            redistribute static
            redistribute rip
            redistribute ospf 1
            exit
            no router rip
            no router ospf 1
            exit
            """
        )
        return None
    return send_command(device, router_function)