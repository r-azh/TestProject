import os

import numpy
from gensim import corpora, models, matutils

print('############### loading Associated Press(AP) data ################')
path = os.sep.join(['C:', '_Data_', 'topc', 'ML_data', 'ch04', 'ap'])
# load all text documents
corpus = corpora.BleiCorpus(f'{path}{os.sep}ap.dat', f'{path}{os.sep}vocab.txt')


print('############### Build the topic model from AP ################')
# Build the topic model: this will statistically infer which topics are present in the corpus
model = models.ldamodel.LdaModel(
    corpus,
    num_topics=100,     # number of topics
    id2word=corpus.id2word
)
doc = corpus.docbyoffset(0)     # last document
topics = model[doc]
print(topics)

# What are these topics? Technically, they are multinomial distributions over words, which
# means that they assign a probability to each word in the vocabulary. Words with high
# probability are more associated with that topic than words with lower probability.

print('############### plot number of topics that each document refers to ################')
# import  matplotlib.pyplot as plot
# num_topics_used = [len(model[doc]) for doc in corpus]
# # plot.hist(num_topics_used, numpy.arange(42))
# figure, ax = plot.subplots()
# ax.hist(num_topics_used, numpy.arange(42))
# ax.set_ylabel('Nr of documents')
# ax.set_xlabel('Nr of topics')
# figure.tight_layout()
# plot.show()

print('############### Build the topic model from AP using Alpha ################')
# bigger values for alpha will result in more topics per document.
# default for alpha is 1/num_topics
model = models.ldamodel.LdaModel(
    corpus,
    num_topics=100,
    id2word=corpus.id2word,
    alpha=1
)

print('############### plot number of topics using Alpha ################')
# num_topics_used_using_alpha = [len(model[doc]) for doc in corpus]
# figure, ax = plot.subplots()
# ax.hist([num_topics_used, num_topics_used_using_alpha], numpy.arange(42))
# ax.set_ylabel('Nr of documents')
# ax.set_xlabel('Nr of topics')
#
# # The coordinates below were fit by trial and error to look good
# ax.text(9, 223, r'default alpha')
# ax.text(26, 156, 'alpha=1.0')
# figure.tight_layout()
# figure.show()

print('############### printing top 64 words of all topics ################')

# Iterate over all the topics in the model
for topic_index in range(model.num_topics):
    # Get the top 64 words for this topic
    words = model.show_topic(topic_index, 64)    # 64 is Number of the most significant words that are associated with the topic
    # each item in words is: (word, probability of word in the topic)
    tf = sum(f for _, f in words)   # sum of probabilities for top 64 words in this topic
    for word, f in words:
        print(f'{word}: {int(1000. * f / tf)}')


print('############### WordCloud of topics ################')

# We first identify the most discussed topic, i.e., the one with the
# highest total weight
topics = matutils.corpus2dense(model[corpus], num_terms=model.num_topics)
weight = topics.sum(1)
max_topic = weight.argmax()

# Get the top 64 words for this topic, Without the argument, show_topic would return only 10 words
words = model.show_topic(max_topic, 64)

# generate wordcload

words = [(w, int(v * 10000)) for w, v in words]
try:
    from pytagcloud import create_tag_image, make_tags
except ImportError:
    print("Could not import pytagcloud. Skipping cloud generation")
tags = make_tags(words, maxsize=120)
create_tag_image(tags, 'cloud_blei_lda.png', size=(1800, 1200), fontname='Lobster')

print('############### Comparing documents by topics ################')
# compare two documents by comparing their topic vectors


# create a matrix of topics(project the documents to the topic space)
from gensim import matutils
topics = matutils.corpus2dense(model[corpus], num_terms=model.num_topics)

# compute pairwise distance
from scipy.spatial import distance
pairwise = distance.squareform(distance.pdist(topics))

# set the diagonal elements of the distance matrix to a high value (highest distance + 1)
largest = pairwise.max()
for topic_index in range(len(topics)):
    pairwise[topic_index, topic_index] = largest + 1


# find the closest element (a nearest neighbor classifier)
def closest_to(doc_id):
    return pairwise[doc_id].argmin()

