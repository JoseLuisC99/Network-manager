from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException


def send_command(device, f):
    try:
        with ConnectHandler(**device) as handler:
            output = f(handler)
        if output is not None:
            return output
        else:
            return {'status': 'ok'}
    except NetmikoAuthenticationException:
        return {'status': 'error', 'info': 'Authentication error'}
    except NetmikoTimeoutException:
        return {'status': 'error', 'info': 'Timeout'}
    except Exception:
        return {'status': 'error', 'info': 'Network error'}

def init_ssh(hostname, ip):
    device = {
        'device_type': 'cisco_ios_telnet',
        'host': ip,
        'password': 'pass1234',
        'secret': 'cisco'
    }
    def router_function(telnet):
        telnet.enable()
        output = telnet.send_command('show ip ssh')
        if 'SSH Enabled - version 2.0' in output:
            return {'status': 'ok'}
        output = telnet.send_command('show ip domain-name')
        if not output:
            telnet.send_config_set([f'ip domain-name {hostname}.manager.com'])
        output = telnet.send_command('show crypto key mypubkey rsa')
        if not output:
            telnet.send_config_set(['crypto key generate rsa', '1024'])
        telnet.send_config_set([
            'ip ssh time-out 30',
            'ip ssh authentication-retries 3',
            'ip ssh version 2'
        ])
        telnet.send_command_timing(
            command_string = """
            configure terminal
            line vty 0 4
            transport input ssh
            login local
            exit
            exit
            """
        )
        return None
    return send_command(device, router_function)

def create_router_user(ip, user_info):
    device = {
        'device_type': 'cisco_ios_telnet',
        'host': ip,
        'password': 'pass1234',
        'secret': 'cisco'
    }
    def router_function(telnet):
        telnet.enable()
        output = telnet.send_command('show ip ssh')
        if 'SSH Enabled - version 2.0' not in output:
            return {'status': 'error', 'info': 'SSH v2 is not enable'}
        telnet.send_config_set([
            f'username {user_info["username"]} privilege {user_info["privilege"]} password {user_info["password"]}'
        ])
        return None
    return send_command(device, router_function)

def delete_router_user(ip, user_info):
    device = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': user_info['username'],
        'password': user_info['password']
    }
    def router_function(ssh):
        ssh.send_config_set([
            f'no username {user_info["username"]} privilege {user_info["privilege"]} password {user_info["password"]}'
        ])
        return None
    return send_command(device, router_function)


def get_interfaces(ip, user_info):
    device = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': user_info['username'],
        'password': user_info['password']
    }
    def router_function(ssh):
        output = ssh.send_command('show ip interface brief', use_textfsm=True)
        return output
    return send_command(device, router_function)

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