import os
import sys
import nltk
import nltk.stem

import scipy
from pprint import pprint

from matplotlib import pylab
from scipy.stats import norm
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

print('##################### Converting raw text into a bag of words ######################')
vectorizer = CountVectorizer(min_df=1)
print(vectorizer)

content = [
    "How to format my hard disk",
    "Hard disk format problems"
]
vectors = vectorizer.fit_transform(content)
feature_names = vectorizer.get_feature_names()  # words in contents
print(feature_names)
print(vectors.toarray().transpose())
print(list(zip(feature_names, vectors.toarray().transpose().tolist())))  # each feature and it's count in content


print('##################### toy data-set ######################')
toy_dir = os.getcwd().replace('mine', os.sep.join(['book', 'data', 'toy']))
posts = []
for file_name in os.listdir(toy_dir):
    with open(os.path.join(toy_dir, file_name)) as file:
        posts.append(file.read())

# posts = [open(os.path.join(dir, f)).read() for f in os.listdir(dir)]
toy_train = vectorizer.fit_transform(posts)
sample_count, feature_count = toy_train.shape
print(f'#samples: {sample_count}, #features: {feature_count}')
feature_names = vectorizer.get_feature_names()
print(feature_names)


new_post = "imaging databases"
new_post_vector = vectorizer.transform([new_post])
pprint(list(zip(feature_names, new_post_vector.toarray().transpose().tolist())))
print(new_post_vector)
print(new_post_vector.toarray())


# Similarity measurement by Euclidean distance between the count vectors of posts
def distance_raw(vector1, vector2):
    delta = vector1 - vector2
    return scipy.linalg.norm(delta.toarray())   # Computes Euclidean norm(shortest distance)


# measure the nearest post
def nearest_sentence(text_list, vector_list, text_item, text_item_vector, distance_function):
    best_distance = sys.maxsize
    best_i = None
    for i, post in enumerate(text_list):
        if post == text_item:
            continue

        post_vector = vector_list.getrow(i)
        distance = distance_function(post_vector, text_item_vector)
        print(f'=== Post {i} with distance={distance} : {post}')
        if distance < best_distance:
            best_distance = distance
            best_i = i
    print(f'Best post is {best_i} with distance = {best_distance}: {text_list[best_i]}')


nearest_sentence(posts, toy_train, new_post, new_post_vector, distance_raw)
# post 3, 4 are similar with different distance
print(toy_train.getrow(3).toarray())
print(toy_train.getrow(4).toarray())

print('##################### normalizing word count vectors ######################')


def distance_normalized(vector1, vector2):
    vector1_normalized = vector1 / scipy.linalg.norm(vector1.toarray())
    vector2_normalized = vector2 / scipy.linalg.norm(vector2.toarray())
    delta = vector1_normalized - vector2_normalized
    return scipy.linalg.norm(delta.toarray())


nearest_sentence(posts, toy_train, new_post, new_post_vector, distance_normalized)

print('##################### removing less important words: stop words ######################')
vectorizer = CountVectorizer(min_df=1, stop_words='english')
print(sorted(vectorizer.get_stop_words())[0:20])

toy_vectors_no_stop_words = vectorizer.fit_transform(posts)
new_post_vector_no_stop_word = vectorizer.transform([new_post])
nearest_sentence(posts, toy_vectors_no_stop_words, new_post, new_post_vector_no_stop_word, distance_normalized)


print('##################### stemming: considering words with same root using NLTK p60 ######################')

english_stemmer = nltk.stem.SnowballStemmer('english')
for word in ['graphics',
             'imaging', 'image', 'imagination', 'imagine',
             'buys', 'buying', 'bought']:
    print(english_stemmer.stem(word))


class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))


stemmed_vectorizer = StemmedCountVectorizer(min_df=1, stop_words='english')
toy_stemmed_vectors = stemmed_vectorizer.fit_transform(posts)
new_post_stemmed_vector = stemmed_vectorizer.transform([new_post])

nearest_sentence(posts, toy_stemmed_vectors, new_post, new_post_stemmed_vector, distance_normalized)


print('##################### Importance of a word in text: TF-IDF  p63 ######################')
# Term Frequency - Inverse Document Frequency
# counting term frequencies for every post and in addition discount those that appear in many posts
# term that occurs often in that particular post and very seldom anywhere else will have higher value


def tf_idf(term, doc, corpus):
    tf = doc.count(term) / len(doc)
    num_docs_with_term = len([d for d in corpus if term in d])
    idf = scipy.log(len(corpus) / num_docs_with_term)
    return tf * idf


a, abb, abc = ['a'], ['a', 'b', 'b'], ['a', 'b', 'c']
all = [a, abb, abc]
print(tf_idf('a', a, all))
print(tf_idf('a', abb, all))
print(tf_idf('a', abc, all))
print(tf_idf('b', abb, all))
print(tf_idf('b', abc, all))
print(tf_idf('c', abc, all))


class StemmedTFIDFVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedTFIDFVectorizer, self).build_analyzer()
        return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))


tfidf_vectorizer = StemmedTFIDFVectorizer(min_df=1, stop_words='english', decode_error='ignore')
toy_tfidf_vector = tfidf_vectorizer.fit_transform(posts)
new_post_tfidf_vector = tfidf_vectorizer.transform([new_post])
nearest_sentence(posts, toy_tfidf_vector, new_post, new_post_tfidf_vector, distance_normalized)


print('##################### plotting the data p67 ######################')

seed = 2
scipy.random.seed(seed)  # to reproduce the data later on

# generating dummy data for some imaginary posts containing only two words
def generate_dummy_data():
    xw1 = norm(loc=0.3, scale=.15).rvs(20)
    yw1 = norm(loc=0.3, scale=.15).rvs(20)

    xw2 = norm(loc=0.7, scale=.15).rvs(20)
    yw2 = norm(loc=0.7, scale=.15).rvs(20)

    xw3 = norm(loc=0.2, scale=.15).rvs(20)
    yw3 = norm(loc=0.8, scale=.15).rvs(20)

    x = scipy.append(scipy.append(xw1, xw2), xw3)
    y = scipy.append(scipy.append(yw1, yw2), yw3)
    return x, y


class ClusterPlotter:
    def __init__(self, x, y, title, mx=None, y_max=None, x_min=None, kmeans=None):
        pylab.figure(num=None, figsize=(8, 6))
        if kmeans:
            pylab.scatter(x, y, s=50, c=kmeans.predict(list(zip(x, y))))
        else:
            pylab.scatter(x, y, s=50)

        pylab.title(title)
        pylab.xlabel("Occurrence of first word")
        pylab.ylabel("Occurrence of second word")

        pylab.autoscale(tight=True)
        pylab.ylim(bottom=0, top=1)
        pylab.xlim(left=0, right=1)
        self._pylab = pylab

    def show_cluster(self, predictions, meshgrid_x, meshgrid_y, cluster_centers):
        self._pylab.imshow(
            predictions,
            interpolation='nearest',
            extent=(meshgrid_x.min(), meshgrid_x.max(), meshgrid_y.min(), meshgrid_y.max()),
            cmap=self._pylab.cm.get_cmap('Blues'),
            aspect='auto',
            origin='lower'
        )
        self._pylab.scatter(
            cluster_centers[:, 0],
            cluster_centers[:, 1],
            marker='x',
            linewidths=2,
            s=100,
            color='black'
        )
        self.show()

    def show(self):
        self._pylab.show()

    def add_arrow(self, start, end):
        self._pylab.gca().add_patch(
            pylab.Arrow(start[0], start[1], end[0] - start[0], end[1] - start[1], width=0.1)
        )

    def clear(self):
        self._pylab.clf()


x, y = generate_dummy_data()
cluster_plotter = ClusterPlotter(x, y, "Vectors")
# cluster_plotter.show()

print('##################### clustering kmeans p68, p69 ######################')

number_of_clusters = 3
meshgrid_x, meshgrid_y = scipy.meshgrid(
    scipy.arange(0, 1, 0.001),
    scipy.arange(0, 1, 0.001)
)

# 1 iteration
k_mean = KMeans(
    init='random',
    n_clusters=number_of_clusters,
    verbose=1,
    n_init=1,
    max_iter=1,
    random_state=seed
)

k_mean.fit(scipy.array(list(zip(x, y))))

predictions = k_mean.predict(
    scipy.c_[meshgrid_x.ravel(), meshgrid_y.ravel()]
).reshape(meshgrid_x.shape)

cluster_plotter_1 = ClusterPlotter(x, y, "Clustering with 1 iteration", kmeans=k_mean)
cluster_1a, cluster_1b, cluster_1c = k_mean.cluster_centers_

cluster_plotter_1.show_cluster(predictions, meshgrid_x, meshgrid_y, k_mean.cluster_centers_)
# cluster_plotter.clear()

# 2 iterations
k_mean = KMeans(
    init='random',
    n_clusters=number_of_clusters,
    verbose=1,
    n_init=1,
    max_iter=2,
    random_state=seed
)

k_mean.fit(scipy.array(list(zip(x, y))))

predictions = k_mean.predict(
    scipy.c_[meshgrid_x.ravel(), meshgrid_y.ravel()]
).reshape(meshgrid_x.shape)

cluster_plotter_3 = ClusterPlotter(x, y, "Clustering with 1 iteration", kmeans=k_mean)
cluster_2a, cluster_2b, cluster_2c = k_mean.cluster_centers_

cluster_plotter_3.add_arrow(cluster_1a, cluster_2a)
cluster_plotter_3.add_arrow(cluster_1b, cluster_2b)
cluster_plotter_3.add_arrow(cluster_1c, cluster_2c)
cluster_plotter_3.show_cluster(predictions, meshgrid_x, meshgrid_y, k_mean.cluster_centers_)
# cluster_plotter.clear()


# 2 iterations
k_mean = KMeans(
    init='random',
    n_clusters=number_of_clusters,
    verbose=1,
    n_init=1,
    max_iter=2,
    random_state=seed
)

k_mean.fit(scipy.array(list(zip(x, y))))

predictions = k_mean.predict(
    scipy.c_[meshgrid_x.ravel(), meshgrid_y.ravel()]
).reshape(meshgrid_x.shape)

cluster_plotter_3 = ClusterPlotter(x, y, "Clustering with 1 iteration", kmeans=k_mean)
cluster_2a, cluster_2b, cluster_2c = k_mean.cluster_centers_

cluster_plotter_3.add_arrow(cluster_1a, cluster_2a)
cluster_plotter_3.add_arrow(cluster_1b, cluster_2b)
cluster_plotter_3.add_arrow(cluster_1c, cluster_2c)
cluster_plotter_3.show_cluster(predictions, meshgrid_x, meshgrid_y, k_mean.cluster_centers_)
# cluster_plotter.clear()

# 3 iterations
k_mean = KMeans(
    init='random',
    n_clusters=number_of_clusters,
    verbose=1,
    n_init=1,
    max_iter=3,
    random_state=seed
)

k_mean.fit(scipy.array(list(zip(x, y))))

predictions = k_mean.predict(
    scipy.c_[meshgrid_x.ravel(), meshgrid_y.ravel()]
).reshape(meshgrid_x.shape)

cluster_plotter_3 = ClusterPlotter(x, y, "Clustering with 1 iteration", kmeans=k_mean)
cluster_3a, cluster_3b, cluster_3c = k_mean.cluster_centers_

cluster_plotter_3.add_arrow(cluster_2a, cluster_3a)
cluster_plotter_3.add_arrow(cluster_2b, cluster_3b)
cluster_plotter_3.add_arrow(cluster_2c, cluster_3c)
cluster_plotter_3.show_cluster(predictions, meshgrid_x, meshgrid_y, k_mean.cluster_centers_)
# cluster_plotter.clear()