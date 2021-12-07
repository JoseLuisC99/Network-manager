from scripts.router import send_command

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