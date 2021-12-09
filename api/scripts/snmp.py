from collections import defaultdict
from pysnmp.hlapi import *

def getMIB(ip, oid):
    if isinstance(oid, list):
        oids = [ObjectType(ObjectIdentity(c)) for c in oid]
    else:
        oids = [ObjectType(ObjectIdentity(oid))]
    iterator = getCmd(
        SnmpEngine(),
        UsmUserData('admin', 'pass1234', 'seed1234', usmHMACSHAAuthProtocol, usmDESPrivProtocol),
        UdpTransportTarget((ip, 161)),
        ContextData(),
        *oids
    )
    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
    if(errorIndication):
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(), 
            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        data = {}
        for varBind in varBinds:
            varName, varValue = varBind
            data[str(varName)] = varValue
        return dict(data)

def setMIB(ip, oid, value):
    iterator = setCmd(
        SnmpEngine(),
        UsmUserData('admin', 'pass1234', 'seed1234', usmHMACSHAAuthProtocol, usmDESPrivProtocol),
        UdpTransportTarget((ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid), value),
        lookupMib=False
    )
    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
    if(errorIndication):
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(), 
            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))

def ifNumber(ip):
    info = getMIB(ip, '1.3.6.1.2.1.2.1.0')
    return int(info['1.3.6.1.2.1.2.1.0'])

def ifAdminStatus(ip):
    nInterfaces = ifNumber(ip)
    status = []
    for i in range(1, nInterfaces):
        info = getMIB(ip, f'1.3.6.1.2.1.2.2.1.7.{i}')
        if int(info[f'1.3.6.1.2.1.2.2.1.7.{i}']) == 1:
            status.append(True)
        else:
            status.append(False)
    return status

def ifInfo(ip):
    nInterfaces = ifNumber(ip)
    info = defaultdict(list)
    for i in range(1, nInterfaces):
        mib = getMIB(ip, [
            f'1.3.6.1.2.1.2.2.1.2.{i}',
            f'1.3.6.1.2.1.2.2.1.7.{i}',
            f'1.3.6.1.2.1.2.2.1.11.{i}',
            f'1.3.6.1.2.1.2.2.1.17.{i}',
            f'1.3.6.1.2.1.2.2.1.14.{i}',
            f'1.3.6.1.2.1.2.2.1.20.{i}'
        ])
        info['ifDescr'].append(str(mib[f'1.3.6.1.2.1.2.2.1.2.{i}']))
        if int(mib[f'1.3.6.1.2.1.2.2.1.7.{i}']) == 1:
            info['ifAdminStatus'].append(True)
        else:
            info['ifAdminStatus'].append(False)
        info['ifInUcastPkts'].append(int(mib[f'1.3.6.1.2.1.2.2.1.11.{i}']))
        info['ifOutUcastPkts'].append(int(mib[f'1.3.6.1.2.1.2.2.1.17.{i}']))
        info['ifInErrors'].append(int(mib[f'1.3.6.1.2.1.2.2.1.14.{i}']))
        info['ifOutErrors'].append(int(mib[f'1.3.6.1.2.1.2.2.1.20.{i}']))
    return dict(info)

def getSysName(ip):
    name = getMIB(ip, '1.3.6.1.2.1.1.5.0')
    return str(name['1.3.6.1.2.1.1.5.0'])

def getSysContact(ip):
    name = getMIB(ip, '1.3.6.1.2.1.1.4.0')
    return str(name['1.3.6.1.2.1.1.4.0'])

def getSysLocation(ip):
    name = getMIB(ip, '1.3.6.1.2.1.1.6.0')
    return str(name['1.3.6.1.2.1.1.6.0'])

def getSysDescr(ip):
    name = getMIB(ip, '1.3.6.1.2.1.1.1.0')
    return str(name['1.3.6.1.2.1.1.1.0'])