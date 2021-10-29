import time
from router import create_router_user, delete_router_user, init_ssh, get_interfaces, set_rip, set_ospf, set_eigrp

# resp = init_ssh('R5', '192.168.0.14')
# print(resp)
# resp = create_router_user('192.168.0.14', {
#     'username': 'test1',
#     'privilege': 15,
#     'password': 'pass1234'
# })

# resp = delete_router_user('192.168.0.14', {
#     'username': 'test1',
#     'privilege': 15,
#     'password': 'pass1234'
# })

# interfaces = get_interfaces('192.168.0.14', {
#     'username': 'test1',
#     'password': 'pass1234'
# })
# for interface in interfaces:
#     print(interface['ipaddr'])

routers = ['192.168.0.22', '192.168.0.14', '192.168.0.10', '192.168.0.6', '192.168.0.2', '192.168.0.1']
# routers = ['192.168.0.1', '192.168.0.2']
for ip in routers:
    output = set_ospf(ip)
    print(f'{ip} said {output["status"]}')