from collections import defaultdict
from scripts.router import send_command, RouterInfo

def show_connections(ip):
    device = {
        'device_type': 'cisco_ios_telnet',
        'host': ip,
        'password': 'pass1234'
    }
    def router_function(telnet):
        cdp = telnet.send_command('show cdp neighbors detail', use_textfsm=True)
        route = telnet.send_command('show ip route', use_textfsm=True)
        return cdp, route
    return send_command(device, router_function)

def get_topology(main_router):
    nodes = []
    links = []
    connections = defaultdict(list)
    next_router = [(1, main_router)]
    routers = [main_router]
    visited_routers = [main_router.destination_host]
    visited_routers_id = {main_router.destination_host: 1}
    next_id = 2

    while next_router:
        id, router = next_router.pop(0)
        nodes.append({'name': router.destination_host, 'id': id, 'type': 'router'})
        neighbors, routes = show_connections(router.management_ip)

        for route in routes:
            if route['protocol'] == 'C':
                connections[route['network']].append({
                    'router': router.destination_host,
                    'interface': route['nexthop_if']
                })
        for neighbor in neighbors:
            if 'destination_host' not in neighbor:
                continue
            if neighbor['destination_host'] not in visited_routers:
                visited_routers.append(neighbor['destination_host'])
                visited_routers_id[neighbor['destination_host']] = next_id

                routers.append(RouterInfo(neighbor['destination_host'], neighbor['management_ip']))
                next_router.append((next_id, RouterInfo(neighbor['destination_host'], neighbor['management_ip'])))
                links.append({'source': id, 'target': next_id})
                next_id += 1
            else:
                link = {'source': visited_routers_id[neighbor['destination_host']], 'target': id}
                alternative = {'source': id, 'target': visited_routers_id[neighbor['destination_host']]}
                if link not in links and alternative not in links:
                    links.append(link)
    return routers, {'nodes': nodes, 'links': links}, dict(connections)