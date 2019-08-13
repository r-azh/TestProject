import os
import scipy

import nltk
import sklearn.datasets
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer


data_path = os.path.sep.join(['C:', '_Data_', 'topc', 'ML data', 'ch03'])
all_data = sklearn.datasets.fetch_20newsgroups(subset='all', data_home=data_path)
print("Number of total posts: %i" % len(all_data.filenames))
print(all_data.target_names)

# train_data = sklearn.datasets.fetch_20newsgroups(subset='train', data_home=data_path, download_if_missing=False)
# print("Number of train data: %i" % len(train_data.filenames))
# test_data = sklearn.datasets.fetch_20newsgroups(subset='test', data_home=data_path, download_if_missing=False)
# print("Number of test data: %i" % len(test_data.filenames))

groups = [
    'comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware',
    'comp.sys.mac.hardware', 'comp.windows.x', 'sci.space']

train_data = sklearn.datasets.fetch_20newsgroups(subset='train', categories=groups)
print("Number of train data: %i" % len(train_data.filenames))

test_data = sklearn.datasets.fetch_20newsgroups(subset='test', categories=groups)
print("Number of test data: %i" % len(test_data.filenames))


english_stemmer = nltk.stem.SnowballStemmer('english')


class StemmedTFIDFVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedTFIDFVectorizer, self).build_analyzer()
        return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))


# to prevent UnicodeDecodeError because of noisy data, ignore it
vectorizer = StemmedTFIDFVectorizer(
    min_df=10,
    max_df=0.5,
    stop_words='english',
    decode_error='ignore'
)
vectorized = vectorizer.fit_transform(train_data.data)
num_samples, num_features = vectorized.shape
print(f"#samples: {num_samples}, #features: {num_features}")

num_clusters = 50
k_means = KMeans(
    n_clusters=num_clusters,
    # init='random',
    n_init=1,
    verbose=1,
    random_state=3  # for generating same results, in real uses we don't use this
)
k_means.fit(vectorized)
print("km.labels_=%s" % k_means.labels_)
print("km.labels_.shape=%s" % k_means.labels_.shape)
# print(k_means.cluster_centers_)


new_post = '''Disk drive problems. Hi, I have a problem with my hard disk.
After 1 year it is working only sporadically now.
I tried to format it, but now it doesn't boot any more.
Any ideas? Thanks
'''

new_post_vectorized = vectorizer.transform([new_post])
new_post_label = k_means.predict(new_post_vectorized)[0]
print("prediction: ", new_post_label)
similar_indices = (k_means.labels_ == new_post_label).nonzero()[0]

similar = []
for i in similar_indices:
    distance = scipy.linalg.norm((new_post_vectorized - vectorized[i]).toarray())
    similar.append((distance, train_data.data[i]))

similar = sorted(similar)
print("Count similar: %i" % len(similar))

most_similar_post = similar[0]
less_similar_post = similar[int(len(similar)/10)]
lesser_similar_post = similar[int(len(similar)/2)]

print(most_similar_post)
print(less_similar_post)
print(lesser_similar_post)

print('############## checking noise of data p75 ################')
post_group = zip(train_data.data, train_data.target)
all = [(len(post[0]), post[0], train_data.target_names[post[1]]) for post in post_group]
graphics = sorted([post for post in all if post[2] == 'comp.graphics'])

# real post
print(graphics[5])

# after tokenization, lowercasing, stop word removal
noise_post = graphics[5][1]
analyzer = vectorizer.build_analyzer()
print(list(analyzer(noise_post)))

# after removing words that will be filtered out by min_df and max_df
useful = set(analyzer(noise_post)).intersection(vectorizer.get_feature_names())
print(sorted(useful))

for term in sorted(useful):
    print('IDF(%s)=%.2f' % (
        term,
        vectorizer._tfidf.idf_[vectorizer.vocabulary_[term]]
    ))
