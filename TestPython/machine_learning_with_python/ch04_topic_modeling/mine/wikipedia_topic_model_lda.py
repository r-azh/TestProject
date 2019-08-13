import logging
import os

import gensim
import numpy
from gensim import matutils

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

print('############### load preprocessed data ################')
path = os.sep.join(['C:', '_Data_', 'topc', 'ML_data', 'ch04', 'wiki'])

id2word = gensim.corpora.Dictionary.load_from_text(f'{path}{os.sep}wiki_en_output_wordids.txt.bz2')
mm = gensim.corpora.MmCorpus(f'{path}{os.sep}wiki_en_output_tfidf.mm')


print('############### build LDA model ################')
# model = gensim.models.ldamodel.LdaModel(
#     corpus=mm,
#     id2word=id2word,
#     num_topics=100,
#     update_every=1,
#     chunksize=10000,
#     passes=1
# )
#
# model.save('C:\\_Data_\\topc\ML_data\\ch04\\wiki\\wiki_lda.pkl')

model = gensim.models.ldamodel.LdaModel.load('C:\\_Data_\\topc\ML_data\\ch04\\wiki\\wiki_lda.pkl')


print('############### create topics ################')
# topics = numpy.zeros((len(mm), model.num_topics))
# for document_index, document in enumerate(mm):
#     doc_topic = model[document]
#     for topic_index, topic_vector in doc_topic:
#         topics[document_index, topic_index] += topic_vector
# numpy.save(f'{path}{os.sep}topics.npy', topics)

topics = numpy.load(f'{path}{os.sep}topics.npy')


print('############### create topics ################')
lens = (topics > 0).sum(axis=0)
print('the average of document mentions ', numpy.mean(lens), ' topics')
print(numpy.mean(lens <= 1000), ' percent of them mentioned 1000 or fewer topics')

print('############### WordCloud of topics ################')


def create_word_claod(words, output_file_name, maxsize, fontname='Lobster'):
    words = [(w, int(v * 10000)) for w, v in words]
    try:
        from pytagcloud import create_tag_image, make_tags
    except ImportError:
        print("Could not import pytagcloud. Skipping cloud generation")
    tags = make_tags(words, maxsize=maxsize)
    create_tag_image(tags, output_file_name, size=(1800, 1200), fontname=fontname)


weights = topics.sum(axis=0)
words = model.show_topic(weights.argmax(), 64)
create_word_claod(words, 'wiki_word_cloud_most_talked_aboud_lda.png', 120, fontname='Cardo')
words = model.show_topic(weights.argmin(), 64)
create_word_claod(words, 'wiki_word_cloud_least_talked_aboud_lda.png', 200)
