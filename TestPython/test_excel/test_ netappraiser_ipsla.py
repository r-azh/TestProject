from ast import literal_eval
from TestPython.test_excel.test_netappraiser_vps_gateway_provider import get

__author__ = 'R.Azh'

from TestPython.test_excel.data import ipsla_data
import xlsxwriter

color_mapping = {
    'good': "rgb(117, 209, 117)",
    'average': "rgb(255, 198, 103)",
    'extreme': "rgb(139, 0, 0)",
    'worst_case': "rgb(242, 108, 104)",
    'out_of_scale': "rgb(107, 38, 7)",
    'unavailable': "rgb(183, 183, 183)",
}

data = ipsla_data
workbook = xlsxwriter.Workbook('ip_sla.xlsx')
worksheet = workbook.add_worksheet('ip_sla')
qoe_ranges = {}
for key, value in color_mapping.items():
    color = literal_eval(value.lstrip('rgb'))
    color = "#{0:02x}{1:02x}{2:02x}".format(*color)
    qoe_ranges[key] = {'value': key.replace('_', ' ').title(),
                       'format': workbook.add_format({'bg_color': color})}
# print(qoe_ranges)
for key in qoe_ranges:
    worksheet.conditional_format(
        1, 1, len(data) + 1, 15, {'type': 'text',
                                  'criteria': 'containing',
                                  'value': qoe_ranges[key]['value'],
                                  'format': qoe_ranges[key]['format']}
    )
    row = 0
    col = 0
    first_title_list = [
        'Name', 'Supplier', 'Location', 'Capacity', 'IP Port'
    ]
for title in first_title_list:
    worksheet.merge_range(row, col, row + 1, col, title)
    col += 1

worksheet.merge_range(row, col, row, col + 2, 'Qos')
worksheet.merge_range(row, col + 3, row, col + 9, 'Qoe')
row += 1
title_list = ['Round Trip Time', 'Packet Loss Ratio', 'Jitter', 'Vpn',
              'Web Stream', 'Download', 'Web Surfing', 'Gaming', 'Video',
              'Voice']
for title in title_list:
    worksheet.write(row, col, title)
    col += 1

for item in data:
    col = 0
    row += 1
    # keys = [item['name'], item['supplier'], '{}, {}, {}- {}, {}, {}'.format(item['source_location']['continent'],
    #                                                                         item['source_location']['country'],
    #                                                                         item['source_location']['center'],
    #                                                                         item['destination_location'][
    #                                                                             'continent'],
    #                                                                         item['destination_location'][
    #                                                                             'country'],
    #                                                                         item['destination_location'][
    #                                                                             'center']),
    #         item['capacity'], '',
    #         item['qos']['round_trip_time']['value'] if item['qos']['round_trip_time'] else '',
    #         item['qos']['packet_loss_ratio']['value'] if item['qos']['packet_loss_ratio'] else '',
    #         item['qos']['jitter']['value'] if item['qos']['jitter'] else '',
    #         print_itmes[item['qoe']['vpn']] if item['qoe']['vpn'] else '',
    #         print_itmes[item['qoe']['web_streaming']] if item['qoe']['web_streaming'] else '',
    #         print_itmes[item['qoe']['download']] if item['qoe']['download'] else '',
    #         print_itmes[item['qoe']['web_surfing']] if item['qoe']['web_surfing'] else '',
    #         print_itmes[item['qoe']['gaming']] if item['qoe']['gaming'] else '',
    #         print_itmes[item['qoe']['video']] if item['qoe']['video'] else '',
    #         print_itmes[item['qoe']['voice']] if item['qoe']['voice'] else '']
    # for i in keys:
    #     ip_sla_worksheet.write(row, col, i)
    #     col += 1
    keys = ['name', 'supplier', 'location', 'capacity', 'ip_port', 'qos.round_trip_time.value',
            'qos.packet_loss_ratio.value', 'qos.jitter.value',
            'qoe.vpn.case', 'qoe.web_streaming.case',
            'qoe.download.case', 'qoe.web_surfing.case',
            'qoe.gaming.case', 'qoe.video', 'qoe.voice']
    for i in keys:
        value = qoe_ranges[get(item, i)]['value'] \
            if get(item, i) in qoe_ranges else get(item, i)
        if i == 'location':
            value = '{}, {}, {}- {}, {}, {}'.format(
                item['source_location']['continent'],
                item['source_location']['country'],
                item['source_location']['center'],
                item['destination_location']['continent'],
                item['destination_location']['country'],
                item['destination_location']['center']
            )
        if i == 'ip_port':
            value = ''
        worksheet.write(row, col, value)
        col += 1
# print(row, col)

# format1 = ip_sla_workbook.add_format({'bold': 1, 'italic': 1, 'font_color': '#000000'})
#worksheet.conditional_format('A1:A4', {'type':     'cell',
                                    # 'criteria': '>',
                                    # 'value':    5,
                                    # 'format':   format1})

workbook.close()












