import string
from pprint import pprint

from elasticsearch_dsl import connections, DocType, Long, Text, Q, Index, Mapping, Field
from elasticsearch_dsl import analyzer, tokenizer

my_analyzer = analyzer('my_analyzer',
                       tokenizer=tokenizer('whitespace'),
                       filter=['lowercase']
                       )


con = connections.create_connection(hosts=['localhost'], port=9200)


class Content(DocType):

    id = Long()
    # context = Text(analyzer=my_analyzer)     # works
    context = Text(
        # fields={'with_punctuations': Field(type=Text, analyzer=my_analyzer)}
        fields={'with_punctuations': Text(analyzer=my_analyzer)}
    )
    # context = Text()

    class Meta:
        index = 'test_content'


if con.indices.exists(index='test_content'):
    con.indices.delete(index='test_content', ignore_unavailable=True)

text_list = [
    "من خیلی چیزها را می فهمم ؛ اما به روی خودم نمی آورم ... نه اینکه برایم مهم نباشد ! فقط حوصله ی جار و جنجال ندارم",
    "_**⚡ ️**_قیمت #طلا و #سکه همگام با #دلار ریزش کرد _ **🔸**_ ",
    f'word word2',
    'کسی اطلاع داره هزینه "مواد" لازم برای پر کردن دندون چقدره؟'

]


if con.indices.exists(index='test_content'):
    print('before save:')
    pprint(Content.search().query(Q('match_all')).execute().hits.hits)
    print('------------------------')


Content.init()
# sleep(10)

for item in text_list:
    content1 = Content(id=text_list.index(item), context=item)
    content1.save()

Index('*').refresh()
print('all saved:')
pprint(Content.search().query(Q('match_all')).execute().hits.hits)

print(string.punctuation)

def has_punctuation(keyword):
    for i in string.punctuation:
        if i in keyword:
            print(keyword, 'has punctuation')

# print(query.to_dict())

print('\n *************************** search results ******************************')
# i = Index('test_content')
# i.analyzer(my_analyzer)
# Index('test_content').refresh()

keyword = '#جار'
has_punctuation(keyword)
# result = Content.search().query('nested', path='context', query=Q('match_phrase', context__with_punctuations=keyword)).execute
result = Content.search().query().filter('match_phrase', context__with_punctuations=keyword).execute()
print('\nsearch result for ', keyword, ' (should be empty):')
for hit in result.hits.hits:
    print(hit)

keyword = "جار"
has_punctuation(keyword)
result = Content.search().query().filter('match_phrase', context=keyword).execute()
print('search result for ', keyword, ' (should find one):')
for hit in result.hits.hits:
    print(hit)

keyword = "جار"
has_punctuation(keyword)
result = Content.search().query().filter('match_phrase', context__with_punctuations=keyword).execute()
print('search result for ', keyword, ' (should find one):')
for hit in result.hits.hits:
    print(hit)

keyword = "دلار"
has_punctuation(keyword)
result = Content.search().query().filter('match_phrase', context=keyword).execute()
print('search result for ', keyword, ' (should find one):')
for hit in result.hits.hits:
    print(hit)

keyword = "دلار"
has_punctuation(keyword)
result = Content.search().query().filter('match_phrase', context__with_punctuations=keyword).execute()
print('search result for ', keyword, ' (should find one):')
for hit in result.hits.hits:
    print(hit)

keyword = 'wordw'
result = Content.search().query().filter('match_phrase_prefix', context__with_punctuations=keyword).execute()
print('\nsearch result for "', keyword, '":')
for hit in result.hits.hits:
    print(hit)

result = Content.search().query().filter('match_phrase_prefix', context=keyword).execute()
print('\nsearch result for "', keyword, '":')
for hit in result.hits.hits:
    print(hit)

keyword = "مواد لازم"
result = Content.search().query().filter('match_phrase_prefix', context__with_punctuations=keyword).execute()
print('\nsearch result for context__with_punctuations"', keyword, '":')
for hit in result.hits.hits:
    print(hit)

result = Content.search().query().filter('match_phrase_prefix', context=keyword).execute()
print('\nsearch result for "', keyword, '":')
for hit in result.hits.hits:
    print(hit)

# from elasticsearch_dsl import analyzer, tokenizer
#
# my_analyzer = analyzer('my_analyzer',
#     # tokenizer=tokenizer('trigram', 'nGram', min_gram=3, max_gram=3),
#     tokenizer=tokenizer('whitespace'),
#     filter=['lowercase']
# )
#
# i = Index('test_content')
# i.analyzer(my_analyzer)
#
# m = Mapping('')
# m.field('context', 'text')
# m.save('test_content')