__author__ = 'R.Azh'


def func1(arg):
    print('func1: ', str(arg))
    return 'func1'


def func2(arg):
    print('func2: ', str(arg))
    return 'func2'

search_query = "filter=sdate[int]>=160619,sdate[int]=160620,sdate[int]<=160621, network_element_id=5732c8111401003a045006d4"


filter_query_string = {"province_id": "province_id={}",
                       "city_id": "city_id={}",
                       "exchange_id": "exchange_id={}",
                       "site_id": "site_id={}",
                       "network_element_id": "_id[oid]={}",
                       "network_element_port_id": "_id[oid]={}"}


queries = search_query.replace('filter=', '').split(',')
date_queries = 'filter='
select_queries = ''
for i in queries:
    print(i)
    if 'sdate' in i:
        date_queries = ''.join([date_queries, i, ','])
    else:
        field, value = i.split('=')
        if field.strip() in ["province_id", "city_id", 'exchange_id', 'site_id', 'network_element_id']:
            result = func1(filter_query_string[field.strip()].format(value))
        elif "network_element_port_id" in field:
            result = func2(filter_query_string[field.strip()].format(value))

print('date_queries:', date_queries)

print(queries)

