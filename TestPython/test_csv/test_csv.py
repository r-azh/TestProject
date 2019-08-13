import csv

__author__ = 'R.Azh'

file_name = 'device.csv'

with open(file_name, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    read_list = set()
    write_list = set()
    for row in reader:
        read_list.add(row['de_snmprcom'])
        write_list.add(row['de_snmpwcom'])
    print(read_list)
    print(write_list)
