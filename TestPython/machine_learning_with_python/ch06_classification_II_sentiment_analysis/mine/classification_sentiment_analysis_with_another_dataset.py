import csv
import os

import numpy

from TestPython.machine_learning_with_python.ch06_classification_II_sentiment_analysis.mine.plot import \
    plot_precision_recall

print('############### Fetch data ################')
DIR_PATH = os.path.sep.join(['C:', '_Data_', 'topc', 'ML_data', 'ch06'])
file_name = os.path.join(DIR_PATH, 'Sentiment_Analysis_Dataset.csv')


def load_data(filename):
    sentences = []
    sentiments = []

    is_first_line = True
    for line in open(filename, 'r', encoding='utf-8', errors='ignore'):
        if is_first_line:
            is_first_line = False
            continue
        line = line.split(',')
        sentences.append(line[3].strip())
        sentiments.append(int(line[1].strip()))

    return numpy.asarray(sentences), numpy.asarray(sentiments)


X, Y = load_data(file_name)

classes = numpy.unique(Y)
class_mapping = {
    0: 'negative',
    1: 'positive'
}
for c in classes:
    print("#%s: %i" % (class_mapping[c], sum(Y == c)))

print('############### solving problem using Multinomial Naive Bayes p135 ################')
# We just said that we will use word occurrence counts as features. We will
# not use them in their raw form, though. Instead, we will use our power horse
# TfidfVectorizer to convert the raw tweet text into TF-IDF feature values, which
# we then use together with the labels to train our first classifier.

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


def create_ngram_model():
    tfidf_ngrams = TfidfVectorizer(
        ngram_range=(1, 3),
        analyzer="word",
        binary=False
    )

    classifier = MultinomialNB()
    return Pipeline([
        ('vect', tfidf_ngrams),
        ('clf', classifier)
    ])


# we keep track of the area under the Precision-Recall curve and for accuracy
from sklearn.metrics import precision_recall_curve, auc
from sklearn.model_selection import ShuffleSplit


def train_model(classifier_factory, x_data, y_data):
    # ShuffleSplit shuffles the data for us, but does not prevent the same data instance to be in multiple folds.
    # setting random state to get deterministic behavior
    cross_validator = ShuffleSplit(n_splits=10, test_size=0.3, random_state=0)

    scores = []
    precision_recall_scores = []

    for train, test in cross_validator.split(x_data):
        x_train, y_train = x_data[train], y_data[train]
        x_test, y_test = x_data[test], y_data[test]

        classifier = classifier_factory()
        classifier.fit(x_train, y_train)

        train_score = classifier.score(x_train, y_train)
        test_score = classifier.score(x_test, y_test)

        scores.append(test_score)

        probability = classifier.predict_proba(x_test)

        precision, recall, pr_threshold = precision_recall_curve(
            y_test,
            probability[:, 1]
        )

        precision_recall_scores.append(auc(recall, precision))

        scores_to_sort = precision_recall_scores
        median = numpy.argsort(scores_to_sort)[int(len(scores_to_sort) / 2)]

        plot_precision_recall(
            auc_score=precision_recall_scores[median],
            name='precision_recall',
            phase='01',
            precision=precision,
            recall=recall,
            label='pos vs neg'
        )

        summary = (
            numpy.mean(scores),
            numpy.std(scores),
            numpy.mean(precision_recall_scores),
            numpy.std(precision_recall_scores)
        )

        print("%.3f\t%.3f\t%.3f\t%.3f" % summary)


# train_model(create_ngram_model, X, Y)

print('############### Tuning classifier parameters p141 ################')
# We can play with TfidfVectorizer parameter first:
# •  Using different settings for NGrams:
#   ° unigrams (1,1)
#   ° unigrams and bigrams (1,2)
#   ° unigrams, bigrams, and trigrams (1,3)
# •  Playing with  min_df : 1 or 2
# •  Exploring the impact of IDF within TF-IDF using  use_idf and  smooth_idf : False or True
# •  Whether to remove stop words or not, by setting  stop_words to  english or  None
# •  Whether to use the logarithm of the word counts ( sublinear_tf )
# •  Whether to track word counts or simply track whether words occur or not, by setting binary to True or False

# We can play the  MultinomialNB classifier parameters too:
# •  Which smoothing method to use by setting  alpha :
#   ° Add-one or Laplace smoothing: 1
#   ° Lidstone smoothing: 0.01, 0.05, 0.1, or 0.5
#   ° No smoothing: 0

# we should train a classifier for every possible combination of all parameter values using GridSearchCV.
# It takes an estimator (instance with a classifier-like interface), which will be the  Pipeline
# instance in our case, and a dictionary of parameters with their potential values.

from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV


def grid_search_model(classifier_factory, x_data, y_data):
    cross_validator = ShuffleSplit(n_splits=10, test_size=0.3, random_state=0)

    # list of potential parameters
    param_grid = dict(
        vect__ngram_range=[(1, 1), (1, 2), (1, 3)],
        vect__min_df=[1, 2],
        vect__stop_words=[None, "english"],
        vect__smooth_idf=[False, True],
        vect__use_idf=[False, True],
        vect__sublinear_tf=[False, True],
        vect__binary=[False, True],
        clf__alpha=[0, 0.01, 0.05, 0.1, 0.5, 1]
    )
    grid_search = GridSearchCV(
        classifier_factory(),
        param_grid=param_grid,
        cv=cross_validator,
        refit=f1_score,
        verbose=10
    )
    grid_search.fit(x_data, y_data)

    return grid_search.best_estimator_


classifier = grid_search_model(create_ngram_model, X, Y)
print(classifier)
