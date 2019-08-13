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
    context = Text(
        fields={'with_punctuations': Text(analyzer=my_analyzer)}
    )

    class Meta:
        index = 'test_content'


if con.indices.exists(index='test_content'):
    con.indices.delete(index='test_content', ignore_unavailable=True)

text_list = []
for punc in string.punctuation:
    text_list.append(f'text with punctuation: {punc}')
    text_list.append(f'word with punctuation: {punc}text{punc}')
    text_list.append(f'word with punctuation at start: {punc}text')


if con.indices.exists(index='test_content'):
    print('before save there is following contents on db:')
    pprint(Content.search().query(Q('match_all')).execute().hits.hits)
    print('------------------------')


Content.init()
# sleep(10)

for item in text_list:
    content1 = Content(id=text_list.index(item), context=item)
    content1.save()

Index('*').refresh()
print('all saved:')
print('after save there is following contents on db:')
pprint(Content.search().query(Q('match_all')).execute().hits.hits)
print('------------------------')

print('\n *********************** search results for punctuation mark exact match **************************')

for punc in string.punctuation:
    keyword = punc
    result = Content.search().query().filter('match_phrase', context__with_punctuations=keyword).execute()
    print('\nsearch result for "', keyword, '":')
    for hit in result.hits.hits:
        print(hit)


print('\n *********************** search results for punctuation mark in text exact match **************************')
for punc in string.punctuation:
    keyword = f'{punc}text{punc}'
    result = Content.search().query().filter('match_phrase', context__with_punctuations=keyword).execute()
    print('\nsearch result for "', keyword, '":')
    for hit in result.hits.hits:
        print(hit)


print('\n ******************** search results for punctuation mark in text match phrase prefix **********************')
for punc in string.punctuation:
    keyword = f'{punc}'
    result = Content.search().query().filter('match_phrase_prefix', context__with_punctuations=keyword).execute()
    print('\nsearch result for "', keyword, '":')
    for hit in result.hits.hits:
        print(hit)