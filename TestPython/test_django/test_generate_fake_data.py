import datetime

__author__ = 'R.Azh'

import random

# create monitoring result

kpis = Kpi.objects.all()
for i in range(1, 1000000):
    for k in kpis:
        MonitoringResult.objects.create(timestamp=datetime.datetime.now(),
        kpi=k,
        value=random.random()*100)


# create kpi for links
links = Link.objects.filter(link_type=Link.TYPE_CUSTOMER)
kpis = []
for l in links:
    for kt in [Kpi.PACKET_LOSS_RATIO, Kpi.ROUND_TRIP_TIME, Kpi.JITTER]:
        attributes = {'authtype': '0',
              'data_type': '0',
              'delay': '90',
              'delay_flex': '',
              'delta': '2',
              'description': '',
              'error': '',
              'evaltype': '0',
              'flags': '0',
              'formula': '',
              'history': '90',
              'hostid': '10437',
              'interfaceid': '291',
              'inventory_link': '0',
              'ipmi_sensor': '',
              'key_': 'jitter',
              'lastclock': '1507742453',
              'lastlogsize': '0',
              'lastns': '620518479',
              'lastvalue': '3.0460',
              'lifetime': '0',
              'logtimefmt': '',
              'mtime': '0',
              'multiplier': '0',
              'name': '11993',
              'params': 'last("icmppingsec[,10,,56,,avg]")',
              'password': '{$TELNET_PASSWORD}',
              'port': '',
              'prevvalue': '0.0590',
              'privatekey': '',
              'publickey': '',
              'snmp_community': '{$SNMP_READ_COMMUNITY}',
              'snmp_oid': '',
              'snmpv3_authpassphrase': '{$SNMP3_AUTHPASS}',
              'snmpv3_authprotocol': '0',
              'snmpv3_contextname': '',
              'snmpv3_privpassphrase': '{$SNMP3_PRIVPASS}',
              'snmpv3_privprotocol': '0',
              'snmpv3_securitylevel': '0',
              'snmpv3_securityname': '{$SNMP3_SECNAME}',
              'state': '0',
              'status': '0',
              'templateid': '0',
              'trapper_hosts': '',
              'trends': '365',
              'type': '15',
              'units': '',
              'username': '{$TELNET_USERNAME}',
              'value_type': '0',
              'valuemapid': '0'}
        kpi = {'link': l, 'gateway': Kpi.NMF, 'kpi_type': kt,
         'gateway_kpi_id': random.random()*100, 'attributes': attributes}
        kpis.append(kpi)

        kpi = {'link': l, 'gateway': Kpi.CEM, 'kpi_type': kt,
         'gateway_kpi_id': abs(random.random()*10000),
               'attributes': attributes}
        kpis.append(kpi)

# kpis_ = Kpi.objects.bulk_create(kpis)

for k in kpis:
    print(k)
    try:
        kp = Kpi.objects.create(**k)
    except:
        pass
    print(kp)
    MonitoringResult.objects.create(timestamp=datetime.datetime.now(),
    kpi=kp,
    value=random.random()*100)


    # PACKET_LOSS_RATIO = 1
    # ROUND_TRIP_TIME = 2
    # JITTER = 3
    # TRACE_ROUTE = 4

