from pprint import pprint

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, DocType, Text, Long, connections, Q

client = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200}])
connections.create_connection(hosts=['localhost'], port=9200, timeout=20)


class Book(DocType):
    id = Long()
    title = Text()
    description = Text()

    class Meta:
        index = 'book'


if client.indices.exists(index='books'):
    s0 = Book.search().delete()

books = {'titles': ['python', 'java', 'c#', 'javascript', 'golang', 'scala', 'androidjava', 'core_java'],
         'descritions': ['alpha', '0', 'beta', 'alpha_0', '2nd ed', '1st ed', '3st ed', 'draft']}

for i in range(len(books['titles'])):
    book = Book(id=1000+i, title=books['titles'][i],
                description=books['descritions'][i])
    book.save()


s1 = Book.search()
r1 = s1.execute()

s2 = Search()
s2.doc_type(Book)
r2 = s2.execute()

s3 = Search(index='book')
r3 = s3.execute()

s1 = s1.filter('terms', title=['python', 'c#'])
r_1 = s1.execute()

s2 = s2.filter('term', title='python')
r_2 = s2.execute()

s3 = s3.query('match', title='python')
r_3 = s3.execute()

s4 = Book.search().query('match_phrase_prefix', title='java')
r_4 = s4.execute()

kwargs = {'must': [Q('match_phrase_prefix', title='java')]}
s5 = Book.search().query(Q('bool', **kwargs))
r_5 = s5.execute()
for hit in r_5.hits.hits:
    print(hit)


# all items in an index
index_name = 'book'
s = Search(index=index_name).execute().hits.hits
pprint(s)
