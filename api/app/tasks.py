from scripts.snmp import ifInfo, getSysName, getSysLocation, getSysContact, getSysDescr
from scripts.cdp import get_topology
from app.models import Router, Interface
import json
import datetime

def getTopology(main_router):
    print('Getting topology...')
    routers, topology, connections = get_topology(main_router)
    
    with open('topology.json', 'w') as f:
        json.dump(topology, f)
    with open('connections.json', 'w') as f:
        json.dump(connections, f)
    
    routers_name = list()
    for router in routers:
        routers_name.append(router.destination_host)
        db_router = Router.objects(hostname=router.destination_host)
        if db_router.count() > 0:
            db_router = db_router.first()
            db_router = db_router.modify(set__ip=router.management_ip)
        else:
            db_router = Router(hostname=router.destination_host, ip=router.management_ip)
            db_router.save()  
    routers = Router.objects()
    for router in routers:
        if router.hostname not in routers_name:
            router.delete()
    print('Topology updated.')

def getInterfacesInfoByRouter(router):
    info = ifInfo(router.ip)
    descr = info['ifDescr']
    status = info['ifAdminStatus']
    in_pkgs = info['ifInUcastPkts']
    out_pkgs = info['ifOutUcastPkts']
    in_err_pkgs = info['ifInErrors']
    out_err_pkgs = info['ifOutErrors']
    date = datetime.datetime.utcnow

    for d, s, in_p, out_p, ine_p, oute_p in zip(descr, status, in_pkgs, out_pkgs, in_err_pkgs, out_err_pkgs):
        Interface.objects(
            description=d, status=s, router=router.id
        ).modify(
            upsert=True, new=True,
            push__inPkgs=in_p,
            push__outPkgs=out_p,
            push__inErrPkgs=ine_p,
            push__outErrPkgs=oute_p,
            push__time=date
        )

def getInterfacesInfo():
    routers = Router.objects()
    for router in routers:
        print(f'Getting interfaces info: Router {router.hostname}')
        getInterfacesInfoByRouter(router)
    print('Interfaces info updated.')

def updateSystemInfoByRouter(router):
    name = getSysName(router.ip)
    descr = getSysDescr(router.ip)
    contact = getSysContact(router.ip)
    location = getSysLocation(router.ip)
    router.modify(set__hostname=name, set__description=descr, set__contact=contact, set__location=location)

def updateSystemInfo():
    routers = Router.objects()
    for router in routers:
        print(f'Updating system info: Router {router.hostname}')
        updateSystemInfoByRouter(router)
    print('System info updated.')

def updateNetworkInfo(main_router):
    print(f'[{datetime.datetime.now(): %Y-%m-%d %H:%M:%S}] Updating network information...')
    getTopology(main_router)
    getInterfacesInfo()
    updateSystemInfo()
    print(f'[{datetime.datetime.now(): %Y-%m-d %H:%M:%S}] Network information updated.')