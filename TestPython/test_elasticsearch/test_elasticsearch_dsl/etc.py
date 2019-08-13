


# The bool query accepts a must parameter (equivalent to AND), a must_not parameter (equivalent to NOT),
#  and a should parameter (equivalent to OR).




# s = Search(using=client, index="book")\
#     .filter("term", category='search')\
#     .query("match", title='python')\
#     .exclude("match", description="beta")
#
# s.aggs.bucket('per_tag', 'terms', field='tags')\
#     .metric('max_lines', 'max', field='lines')
#
# response = s.execute()
#
# for hit in response:
#     print(hit.meta.score, hit.title)
#
# for tag in response.aggregations.per_tag.buckets:
#     print(tag.key, tag.max_lines.value)


# above search is equivalet to :
# response = client.search(
#     index="my-index",
#     body={
#       "query": {
#         "filtered": {
#           "query": {
#             "bool": {
#               "must": [{"match": {"title": "python"}}],
#               "must_not": [{"match": {"description": "beta"}}]
#             }
#           },
#           "filter": {"term": {"category": "search"}}
#         }
#       },
#       "aggs": {
#         "per_tag": {
#           "terms": {"field": "tags"},
#           "aggs": {
#             "max_lines": {"max": {"field": "lines"}}
#           }
#         }
#       }
#     }
# )
#
# for hit in response['hits']['hits']:
#     print(hit['_score'], hit['_source']['title'])
#
# for tag in response['aggregations']['per_tag']['buckets']:
#     print(tag['key'], tag['max_lines']['value'])