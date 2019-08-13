import collections
from pprint import pprint
import xlsxwriter
import operator
from functools import reduce
from  TestPython.test_excel.data import vps_gateway_provider_data, vps_gateway_tic_data

__author__ = 'R.Azh'
# data = vps_gateway_provider_data
data = vps_gateway_tic_data


def get(obj, path, default=None):
    if isinstance(path, str):
        path = path.split('.')
    for item in path:
        try:
            obj = obj[item]
        except (KeyError, TypeError):
            return default
    return obj


from ast import literal_eval
workbook = xlsxwriter.Workbook('VPS-Gateway.xlsx')
qoe_ranges = {}
color_mapping = {
    'good': "rgb(117, 209, 117)",
    'average': "rgb(255, 198, 103)",
    'extreme': "rgb(139, 0, 0)",
    'worst_case': "rgb(242, 108, 104)",
    'out_of_scale': "rgb(107, 38, 7)",
    'unavailable': "rgb(183, 183, 183)",
}
for key, value in color_mapping.items():
    color = literal_eval(value.lstrip('rgb'))
    color = "#{0:02x}{1:02x}{2:02x}".format(*color)
    qoe_ranges[key] = {'value': key.replace('_', ' ').title(),
                       'format': workbook.add_format({'bg_color': color})}

# kpi_types = {
#     'packet_loss_ratio': {
#         'sheet': workbook.add_worksheet('packet_loss_ratio'),
#         'path': 'qos.packet_loss_ratio.value'},
#     'round_trip_time': {'sheet': workbook.add_worksheet('round_trip_time'),
#                         'path': 'qos.round_trip_time.value'},
#     'jitter': {'sheet': workbook.add_worksheet('jitter'),
#                'path': 'qos.jitter.value'},
#     'game': {'sheet': workbook.add_worksheet('Game'),
#              'path': 'qoe.gaming'},
#     'live_streaming': {'sheet': workbook.add_worksheet('Live Streaming'),
#                        'path': 'qoe.live_streaming'},
#     'vpn': {'sheet': workbook.add_worksheet('Vpn'),
#             'path': 'qoe.vpn'},
#     'download': {'sheet': workbook.add_worksheet('Download'),
#                  'path': 'qoe.download'},
#     'web_surfing': {'sheet': workbook.add_worksheet('Web Surfing'),
#                     'path': 'qoe.web_surfing'},
#     'web_streaming': {'sheet': workbook.add_worksheet('Web Streaming'),
#                       'path': 'qoe.web_streaming'},
#     'video': {'sheet': workbook.add_worksheet('Video'),
#               'path': 'qoe.video'},
#     'voice': {'sheet': workbook.add_worksheet('Voice'),
#               'path': 'qoe.voice'},
# }

kpi_types = {
    'packet_loss_ratio': {
        'sheet': workbook.add_worksheet('packet_loss_ratio'),
        'path': 'qos.packet_loss_ratio.value'},
    'round_trip_time': {'sheet': workbook.add_worksheet('round_trip_time'),
                        'path': 'qos.round_trip_time.value'},
    'jitter': {'sheet': workbook.add_worksheet('jitter'),
               'path': 'qos.jitter.value'},
    'game': {'sheet': workbook.add_worksheet('Game'),
             'path': 'qoe.gaming.case'},
    'live_streaming': {'sheet': workbook.add_worksheet('Live Streaming'),
                       'path': 'qoe.live_streaming.case'},
    'vpn': {'sheet': workbook.add_worksheet('Vpn'),
            'path': 'qoe.vpn.case'},
    'download': {'sheet': workbook.add_worksheet('Download'),
                 'path': 'qoe.download.case'},
    'web_surfing': {'sheet': workbook.add_worksheet('Web Surfing'),
                    'path': 'qoe.web_surfing.case'},
    'web_streaming': {'sheet': workbook.add_worksheet('Web Streaming'),
                      'path': 'qoe.web_streaming.case'},
    'video': {'sheet': workbook.add_worksheet('Video'),
              'path': 'qoe.video.case'},
    'voice': {'sheet': workbook.add_worksheet('Voice'),
              'path': 'qoe.voice.case'},
}
for key in qoe_ranges:
    for kpi_type in kpi_types:
        kpi_types[kpi_type]['sheet'].conditional_format(
            1, 1, len(data) + 1, 100, {'type': 'text',
                                       'criteria': 'containing',
                                       'value': qoe_ranges[key]['value'],
                                       'format': qoe_ranges[key]['format']}
        )

data.sort(
    key=lambda d: (
        # d['supplier'],
        # d['name'],
        d['source_location']['continent'],
        d['source_location']['center'],
        # d['source_location']['continent'],
        # d['source_location']['center']
        )
)
for kpi_type in kpi_types:
    row = 0
    col = 0
    gateway_info = collections.OrderedDict([('Name', 'name'), ('Supplier', 'supplier'), ('IP Port', 'ip_port'),
                                           ('Capacity', 'capacity'), ('Source', 'reference.source_location.center'),
                                           ('Destination', 'reference.destination_location.center')])
    for title in gateway_info:
        kpi_types[kpi_type]['sheet'].merge_range(row, col, row + 1, col, title)
        col += 1
row = 2
col = len(gateway_info)
continents = {}
centers = {}
locations = {}
suppliers = {}
for item in data:
    continent = item['source_location']['continent']
    center = item['source_location']['center']
    if continent not in locations:
        locations[continent] = {'center_count': 1, 'centers': {center: col}}
        for kpi, info in kpi_types.items():
            info['sheet'].write(1, col, center)
        print(1, col, center)
        col += 1
        row = 2
    if center not in locations[continent]['centers']:
        for kpi, info in kpi_types.items():
            info['sheet'].write(1, col, center)
        print(1, col, center)
        locations[continent]['center_count'] += 1
        locations[continent]['centers'][center] = col
        col += 1
        row = 2
print(locations)
print(suppliers)
# print(continents)
# print(centers)

for kpi, info in kpi_types.items():
    col = len(gateway_info)
    sorted_continent = collections.OrderedDict(sorted(locations.items()))
    for continent in sorted_continent:
        next_col = col + sorted_continent[continent]['center_count'] - 1
        if col == next_col:
            info['sheet'].write(0, col, continent)
            col += 1
        else:
            info['sheet'].merge_range(0, col, 0, next_col, continent)
            col = next_col + 1

data.sort(
    key=lambda d: (
        d['name'],
        d['supplier'],
        # d['reference']['destination_location']['continent'],
        # d['reference']['destination_location']['center'],
        # d['source_location']['continent'],
        # d['source_location']['center']
        )
)
center_format = workbook.add_format({'align': 'center_across'})
    # 'align': 'center',
    # 'valign': 'vcenter'
# max_col = col
row = 1
count = 1
link_names = set()
for item in data:
    if item['name'] not in link_names:
        link_names.add(item['name'])
        row += 1
    # supplier = item['supplier']
    # if supplier not in suppliers:
    #     suppliers[supplier] = 1
    #     for kpi, info in kpi_types.items():
    #         info['sheet'].merge_range(row, 0, row, max_col, supplier, center_format)
    #     row += 1
    # else:
    #     suppliers[supplier] += 1

    # if row == col:
    #     row += 1
    print('---------------------')
    pprint(item)
    print('item: ', count)
    col = locations[item['source_location']['continent']]['centers'][item['source_location']['center']]
    print(row, col)
    for info in kpi_types.values():
        gw_col = 0
        for gwi in gateway_info:
            info['sheet'].write(row, gw_col, get(item, gateway_info[gwi]))
            gw_col += 1
        print(info['sheet'].name)
        print(row, col)


        # print(info['path'])
        # print(value)
        value = get(item, info['path'])
        if isinstance(value, str):
            value = qoe_ranges[value]['value']
        # print(row, col)
        # print(item['source_location']['continent'], item['source_location']['center'])
        info['sheet'].write(row, col, value)
        print(value)
    count += 1
pprint(locations)
workbook.close()

