from collections import OrderedDict
from functools import reduce
from pprint import pprint

__author__ = 'R.Azh'
import xlsxwriter
import operator
from TestPython.test_excel.data import global_data

workbook = xlsxwriter.Workbook('global_view.xlsx')
data = global_data

# output = BytesIO()
# workbook = xlsxwriter.Workbook(output)
green = workbook.add_format({'bg_color': '#75D175'})
yellow = workbook.add_format({'bg_color': '#FFC667'})
carmine = workbook.add_format({'bg_color': '#8b0000'})
red = workbook.add_format({'bg_color': '#f26c68'})
brown = workbook.add_format({'bg_color': '#6b2607'})

kpi_types = {
    'packet_loss_ratio': {'sheet': workbook.add_worksheet('packet_loss_ratio'),
                          'path': ['qos', 'packet_loss_ratio', 'value']},
    'round_trip_time': {'sheet': workbook.add_worksheet('round_trip_time'),
                        'path': ['qos', 'round_trip_time', 'value']},
    'jitter': {'sheet': workbook.add_worksheet('jitter'),
               'path': ['qos', 'jitter', 'value']},
    'game': {'sheet': workbook.add_worksheet('Game'),
             'path': ['qoe', 'gaming']},
    'live_streaming': {'sheet': workbook.add_worksheet('Live Streaming'),
                       'path': ['qoe', 'live_streaming']},
    'vpn': {'sheet': workbook.add_worksheet('Vpn'),
            'path': ['qoe', 'vpn']},
    'download': {'sheet': workbook.add_worksheet('Download'),
                 'path': ['qoe', 'download']},
    'web_surfing': {'sheet': workbook.add_worksheet('Web Surfing'),
                    'path': ['qoe', 'web_surfing']},
    'web_streaming': {'sheet': workbook.add_worksheet('Web Streaming'),
                      'path': ['qoe', 'web_streaming']},
    'video': {'sheet': workbook.add_worksheet('Video'),
              'path': ['qoe', 'video']},
    'voice': {'sheet': workbook.add_worksheet('Voice'),
              'path': ['qoe', 'voice']},
}
qoe_ranges = {'good': {'value': 'Good', 'format': green},
          'average': {'value': 'Average', 'format': yellow},
          'out_of_scale': {'value': 'Out Of Scale', 'format': red},
          'extreme': {'value': 'Extreme', 'format': carmine},
          'worst_case': {'value': 'Worst Case', 'format': brown}}
for key in qoe_ranges:
    for type in kpi_types:
        kpi_types[type]['sheet'].conditional_format(1, 1, len(data)+1, 100,
                                            {'type': 'text',
                                             'criteria': 'containing',
                                             'value': qoe_ranges[key]['value'],
                                             'format': qoe_ranges[key]['format']})

data.sort(
    key=lambda d: (
    d['destination_location']['continent'],
    d['destination_location']['center'],
    d['source_location']['continent'],
    d['source_location']['center'])
)

row = 2
col = 1
continents = {}
centers = {}
for item in data:
    continent = item['destination_location']['continent']
    center = item['destination_location']['center']
    if continent not in continents:
        continents[continent] = 1
        for kpi, info in kpi_types.items():
            info['sheet'].write(1, col, center)
            info['sheet'].write(col + 1, 0, center)
        centers[center] = col + 1
        col += 1
        row = 2
    if center not in centers:
        for kpi, info in kpi_types.items():
            info['sheet'].write(1, col, center)
            info['sheet'].write(col + 1, 0, center)
        continents[continent] += 1
        centers[center] = col + 1
        col += 1
        row = 2
    if row == col:
        row += 1
    for kpi, info in kpi_types.items():
        value = reduce(operator.getitem, info['path'], item)
        if isinstance(value, str):
            value = qoe_ranges[value]['value']
        info['sheet'].write(row, col - 1, value)
    row += 1

for kpi, info in kpi_types.items():
    info['sheet'].merge_range(0, 0, 1, 0, 'Continent Center')
    col = 1
    sorted_continent = sorted(continents)
    for continent in sorted_continent:
        next_col = col + continents[continent] - 1
        if col == next_col:
            info['sheet'].write(0, col, continent)
            col += 1
        else:
            info['sheet'].merge_range(0, col, 0, next_col, continent)
            col = next_col + 1

workbook.close()
# excel_content = output.getvalue()
# output.close()
# global_view_workbook.close()


