from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from collections import namedtuple

RouterInfo = namedtuple('Router', ['destination_host', 'management_ip'])

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

def get_interfaces(ip):
    device = {
        'device_type': 'cisco_ios_telnet',
        'host': ip,
        'password': 'pass1234'
    }
    def router_function(telnet):
        output = telnet.send_command('show ip interface brief', use_textfsm=True)
        return output
    return send_command(device, router_function)