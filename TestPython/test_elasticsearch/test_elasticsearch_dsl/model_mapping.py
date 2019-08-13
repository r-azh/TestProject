# Define a default Elasticsearch client
from elasticsearch_dsl import connections, DocType, Text, Keyword, Date, Integer, datetime, Search

# Define a default Elasticsearch client
con = connections.create_connection(hosts=['localhost'])


class Article(DocType):
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    body = Text(analyzer='snowball')
    tags = Keyword()
    published_from = Date()
    lines = Integer()

    class Meta:
        index = 'blog'

    def save(self, **kwargs):
        self.lines = len(self.body.split())
        return super(Article, self).save(**kwargs)

    def is_published(self):
        return datetime.today() >= self.published_from

# create the mappings in elasticsearch
Article.init()

# create and save and article
article = Article(meta={'id': 1001}, title='Hello World!', tags=['test'])
article.body = ''' looong text '''
article.published_from = datetime.today()
article.save()

article = Article.get(id=1001)
print(article.is_published())

search_all = Search(using=con, index=('blog'))
print("result count %s" % search_all.count())
articles = search_all.execute()
print("results: \n %s" % a for a in articles)

# Display cluster health
print(connections.get_connection().cluster.health())

