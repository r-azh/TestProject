import re
from pprint import pprint
from time import sleep

from elasticsearch_dsl import connections, DocType, Text, Long, Search, Q, Index
from elasticsearch_dsl.query import SimpleQueryString, MatchPhrase

con = connections.create_connection(hosts=['localhost'], port=9200)


class Content(DocType):
    id = Long()
    context = Text()

    class Meta:
        index = 'test_content'


# con.delete_by_query(index='content',doc_type='content', q={})
if con.indices.exists(index='test_content'):
    con.indices.delete(index='test_content', ignore_unavailable=True)

text_list = [
    'اکران فیلم‌های جـــار به کارگردانی حسین شمس (رییس جار) هر شب از صدا و سیما',
    '… 🔸برخی منتقد این حجم از افزایش عوارض خروج از کشور هستند، اما در این باره نکاتی قابل تامل وجود دارد که شاید در اظهارنظرها موثر باشد. 🔸در سال 95 بیش از 9 میلیون نفر/سفر خارجی توسط ایرانیان انجام شده که بر اساس برخی برآوردها، بالغ بر 7 میلیارد دلار خروج ارز در پی داشته است. 🔸طبیعتا بخشی از هزینه های تحمیل شده به کشور از ناحیه خروج ارز، باید از محل عوارض جبران شود و تعرفه کنونی، در مقایسه با هزینه‌ها قابل مقایسه نیست.…',
    'صدا و سیمای آزادی',
    'کلاس های جبرانی پایه هفتم'
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


def get_keyword_regex(keyword):
    def _convert_keyword_to_list(keyword):
        result = list()
        prev_char = ""
        characters = list(keyword)
        for character in characters:
            if character == "\\" and prev_char == "":
                prev_char = character
                continue

            result.append(prev_char + character)
            prev_char = ""

        return result

    separators1 = [u'\u200c', 'ـ']
    # separators2 = [r'\s']
    separators_pattern1 = "[%s]*" % ("".join(separators1))
    # separators_pattern2 = "[%s]*" % ("".join(separators2))
    sub = re.sub(re.compile(separators_pattern1), r'', keyword)
    # sub = re.sub(re.compile(separators_pattern2), r' ', sub)
    # normalized_keyword = re.escape(sub)
    # pattern = separators_pattern.join(_convert_keyword_to_list(normalized_keyword))
    return sub #'.*'+sub+'.*'


# kwargs1 = Q('bool', **{'must': [Q('regexp', context=regex1)]})
# kwargs1 = Q('regexp', context=regex1)

search = Content.search()

print('\n *************************** \nsearch results:')

keywords = [
    '     صدا  و   سیما',
    '   قابل    مقــــایسه',
    'جبران',
    'عوارض'
    ]
regex_list = []
kwargs_list = []
for i in range(0, len(keywords)):
    regex_list.append(get_keyword_regex(keywords[i]))
    kwargs_list.append(SimpleQueryString(query=regex_list[i], fields=['context'], default_operator='and'))
    result = search.query(kwargs_list[i]).execute()
    print('\n' + keywords[i] + ':')
    for hit in result.hits.hits:
        print(hit)

# result = search.query(Q('constant_score', filter=kwargs1)).execute()

# kwargs_exclude = SimpleQueryString(query=regex_list[1], fields=['context'], default_operator='not')

result3 = search.query().exclude(kwargs_list[1]).execute()
result4 = search.query().filter('match_phrase_prefix', context=regex_list[0]).execute()
result5 = search.query().filter('match_phrase', context=regex_list[0]).execute()
result6 = search.query().filter('match_phrase', context=regex_list[2]).execute()
# result7 = search.query().filter('match_phrase', context=regex_list[2]).filter('match_phrase', context=regex_list[3]).execute()  #works
# result7 = search.query().filter(Q("match_phrase",  context=regex_list[2]) & Q("match_phrase", context=regex_list[3])).execute()
result7 = search.query().filter(Q('bool', **{'must': [MatchPhrase(context=regex_list[2]), MatchPhrase(context=regex_list[3])]})).execute()


print('\n exclude' + keywords[2] + ':')
for hit in result3.hits.hits:
    print(hit)

print('\n match phrase prefix' + keywords[0] + ':')
for hit in result4.hits.hits:
    print(hit)

print('\n match phrase' + keywords[0] + ':')
for hit in result5.hits.hits:
    print(hit)

print('\n match phrase' + keywords[2] + ':')
for hit in result6.hits.hits:
    print(hit)

print('\n match phrase' + keywords[2] + ' ' + keywords[3] + ':')
for hit in result7.hits.hits:
    print(hit)

# test all scenario combinations
# normalize keyword for assertion first