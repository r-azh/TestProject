from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch()
# es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}

res = es.index(index="test_index", doc_type="tweet", id=1, body=doc)
print(res['result'])

res = es.get(index="test_index", doc_type="tweet", id=1)
print(res['_source'])

es.indices.refresh(index='test_index')

res = es.search(index="test_index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])