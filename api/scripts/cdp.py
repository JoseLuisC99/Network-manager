from scripts.router import send_command, Router

def show_cdp(ip):
    device = {
        'device_type': 'cisco_ios_telnet',
        'host': ip,
        'password': 'pass1234'
    }
    def router_function(telnet):
        return telnet.send_command('show cdp neighbors detail', use_textfsm=True)
    return send_command(device, router_function)

def get_topology(main_router):
    # nodes = [{'name': 'R1', 'id': 1, 'type': 'router'}, {'name': 'R2', 'id': 2, 'type': 'router'}]
    # links = [{'source': 1, 'target': 2}]
    nodes = []
    links = []
    next_router = [(1, main_router)]
    visited_routers = [main_router.destination_host]
    visited_routers_id = {main_router.destination_host: 1}
    next_id = 2

    while next_router:
        id, router = next_router.pop(0)
        nodes.append({'name': router.destination_host, 'id': id, 'type': 'router'})

        for neighbor in show_cdp(router.management_ip):
            if 'destination_host' not in neighbor:
                continue
            if neighbor['destination_host'] not in visited_routers:
                visited_routers.append(neighbor['destination_host'])
                visited_routers_id[neighbor['destination_host']] = next_id

                next_router.append((next_id, Router(neighbor['destination_host'], neighbor['management_ip'])))
                links.append({'source': id, 'target': next_id})
                next_id += 1
            else:
                link = {'source': visited_routers_id[neighbor['destination_host']], 'target': id}
                alternative = {'source': id, 'target': visited_routers_id[neighbor['destination_host']]}
                if link not in links and alternative not in links:
                    links.append(link)
    return {'nodes': nodes, 'links': links}