import json
import os
from operator import itemgetter
from pprint import pprint
from xml.etree import cElementTree

import nltk
import numpy
from matplotlib import pylab
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, precision_recall_curve, auc, classification_report

from TestPython.machine_learning_with_python.ch05_classification_detecting_poor_answers.mine.plot import *

print('############### seeing Posts.xml data ################')
# import TestPython.machine_learning_with_python.ch05_classification_detecting_poor_answers.book.so_xml_to_tsv
# import TestPython.machine_learning_with_python.ch05_classification_detecting_poor_answers.book.chose_instances

# DATA_DIR = os.path.sep.join(['D:', 'fariba', 'r'])
# posts_filename = os.path.join(DATA_DIR, 'Posts.xml')

# # print 3 first elements of xml file
# with open(posts_filename, 'r') as file:
#     print("******** Reading from xml file: %s" % posts_filename)
#     it = map(itemgetter(1),
#              iter(cElementTree.iterparse(posts_filename, events=('start',))))
#
#     root = next(it)
#     print(root)
#
#     counter = 0
#     for element in it:
#         counter += 1
#
#         if counter > 3:
#             break
#         pprint(element.attrib)
#
#
# # print 3 first elements of filtered file
# with open(filename_filtered, 'r') as file:
#     print("\n******** Reading from filtered file: %s" % posts_filename)
#     for i in range(3):
#         print(file.readline())


print('############### fetching posts ################')
DATA_DIR = os.path.sep.join(['C:', '_Data_', 'topc', 'ML_data', 'ch05'])
filename_filtered = os.path.join(DATA_DIR, "filtered.tsv")
chosen = os.path.join(DATA_DIR, "chosen.tsv")
chosen_meta = os.path.join(DATA_DIR, "chosen-meta.json")


def fetch_posts(filename):
    for line in open(filename, "r"):
        post_id, text = line.split("\t")
        yield int(post_id), text.strip()


def fetch_meta(filename):
    meta = json.load(open(filename, 'r'))
    keys = list(meta.keys())    # list of post ids

    # JSON only allows string keys, changing that to int
    for key in keys:
        meta[int(key)] = meta[key]
        del meta[key]

    post_id_to_index = {}
    index_to_post_id = {}

    for post_id, info in meta.items():
        post_id_to_index[post_id] = index = info['idx']
        index_to_post_id[index] = post_id

    return meta, post_id_to_index, index_to_post_id


posts = fetch_posts(chosen)
meta, post_id_to_index, index_to_post_id = fetch_meta(chosen_meta)

print('############### labeling good answers p100 ################')

# ParentId == -1 are questions
all_answers = [q for q, v in meta.items() if v['ParentId'] != -1]

# we take all answers that are scored higher than zero as positive (True)
# and all answers with zero or less points as negative (False)
Y = numpy.asarray([
    meta[answer_id]['Score'] > 0 for answer_id in all_answers
])

print('############### Engineering the features: ################')
print('          ##### feature-1: LinkCount p101 #####')
# This features is already computed in so_xml_to_tsv.filter_html as LinkCount so it exists in meta

# number of hyperlinks in answer's text as feature

import re

# not counting code examples in text
code_match = re.compile('<pre>(.*?)</pre', re.MULTILINE | re.DOTALL)

link_match = re.compile(
    '<a href="http://.*?".*?>(.*?)</a>',
    re.MULTILINE | re.DOTALL
)

tag_match = re.compile('<[^>]*>', re.MULTILINE | re.DOTALL)

# For production systems, we would not want to parse HTML content
# with regular expressions. Instead, we should rely on excellent
# libraries such as BeautifulSoup, which does a marvelous job of
# robustly handling all the weird things that typically occur in
# everyday HTML


def extract_link_count_feature_from_body(text):
    link_count_in_code = 0
    # count links in code to later subtract them
    for match_str in code_match.findall(text):
        link_count_in_code += len(link_match.findall(match_str))

    return len(link_match.findall(text)) - link_count_in_code


plot_feature_histogram([[int(meta[x]['LinkCount']) for x in meta]], 'LinkCount')
# With the majority of posts having no link at all, we know now that this feature will
# not make a good classifier alone.


print('############### Training the classifier with LinkCount ################')
from sklearn import neighbors

# X = numpy.asarray([[extract_features_from_body(text)] for post_id, text in posts
#                    if post_id in all_answers])
# or
X = numpy.asarray([[int(meta[x]['LinkCount'])] for x in all_answers])
knn_classifier = neighbors.KNeighborsClassifier()
knn_classifier.fit(X, Y)

print('############### Measuring classifier performance for LinkCount ################')
from sklearn.model_selection import KFold, cross_validate


def measure_classifier_performance(classifier, data_x, data_y, print_info=True):
    train_errors = []
    test_scores = []
    test_errors = []

    kfold = KFold(n_splits=10, shuffle=True)

    for train, test in kfold.split(data_x):
        x_train, y_train = data_x[train], data_y[train]
        x_test, y_test = data_x[test], data_y[test]
        classifier.fit(x_train, y_train)
        train_errors.append(1 - classifier.score(x_train, y_train))
        test_score = classifier.score(x_test, y_test)
        test_scores.append(test_score)
        test_errors.append(1 - test_score)

    if print_info:
        print("Mean(scores)=%.5f\tStddev(scores)=%.5f" % (numpy.mean(test_scores), numpy.std(test_scores)))

    return train_errors, test_errors


measure_classifier_performance(knn_classifier, X, Y)
print(" it is not much better than tossing a coin")

# # or using cross_validate from sklearn # problem?
# cross_validate_result = cross_validate(knn_classifier, X, Y, cv=kfold)
# print("Mean accuracy: {:.1%}".format(numpy.mean(cross_validate_result['test_score'])))


print('############### Designing more features: ################')
print('          ##### feature-2: NumTextTokens p104 #####')
print('          ##### feature-3: NumCodeLines p104 #####')


# This features is already computed in so_xml_to_tsv.filter_html as LinkCount so it exists in meta
def extract_link_count_feature_from_body(text):
    num_code_lines = 0
    link_count_in_code = 0
    code_free_text = text

    # remove source code and count how many lines
    for match_str in code_match.findall(text):
        num_code_lines += match_str.count('\n')
        code_free_text = code_match.sub("", code_free_text)

        # Sometimes source code contains links,
        # which we don't want to count
        link_count_in_code += len(link_match.findall(match_str))

    links = link_match.findall(text)
    link_count = len(links)
    link_count -= link_count_in_code
    html_free_text = re.sub(" +", " ",
                            tag_match.sub('', code_free_text)).replace("\n", "")
    link_free_text = html_free_text

    # remove links from text before counting words
    for link in links:
        if link.lower().startswith("http://"):
            link_free_text = link_free_text.replace(link, '')

    num_text_tokens = html_free_text.count(" ")

    return num_text_tokens, num_code_lines, link_count


plot_feature_histogram([[int(meta[x]['NumTextTokens']) for x in meta]], 'NumTextTokens')
plot_feature_histogram([[int(meta[x]['NumCodeLines']) for x in meta]], 'NumCodeLines')


print('############### Measuring classifier performance for new features ################')
X = numpy.asarray([[
    int(meta[x]['NumTextTokens']),
    int(meta[x]['NumCodeLines']),
    int(meta[x]['LinkCount'])
] for x in all_answers])

measure_classifier_performance(knn_classifier, X, Y)

print('          ##### feature-4: AvgSentLen p106 #####')
#  This measures the average number of words in a sentence
print('          ##### feature-5: AvgWordLen p106 #####')
#  This measures the average number of words in a sentence
print('          ##### feature-5: NumAllCaps p106 #####')
# This measures the number of words that are written in uppercase, which is considered bad style
print('          ##### feature-5: NumExclams p106 #####')
# This measures the number of exclamation marks


def prepare_sent_features(post_texts, post_infos):
    for pid, text in post_texts:
        if not text:
            post_infos[pid]['AvgSentLen'] = post_infos[pid]['AvgWordLen'] = 0
        else:
            from platform import python_version
            if python_version().startswith('2'):
                text = text.decode('utf-8')
            sent_lens = [len(nltk.word_tokenize(
                sent)) for sent in nltk.sent_tokenize(text)]
            post_infos[pid]['AvgSentLen'] = numpy.mean(sent_lens)
            post_infos[pid]['AvgWordLen'] = numpy.mean(
                [len(w) for w in nltk.word_tokenize(text)])

        post_infos[pid]['NumAllCaps'] = numpy.sum(
            [word.isupper() for word in nltk.word_tokenize(text)])

        post_infos[pid]['NumExclams'] = text.count('!')
    return post_infos


meta = prepare_sent_features(posts, meta)
plot_feature_histogram([[int(meta[x]['AvgSentLen']) for x in meta]], 'AvgSentLen')
plot_feature_histogram([[int(meta[x]['AvgWordLen']) for x in meta]], 'AvgWordLen')
plot_feature_histogram([[int(meta[x]['NumAllCaps']) for x in meta]], 'NumAllCaps')
plot_feature_histogram([[int(meta[x]['NumExclams']) for x in meta]], 'NumExclams')


print('############### Measuring classifier performance for new features ################')
X = numpy.asarray([[
    int(meta[x]['NumTextTokens']),
    int(meta[x]['NumCodeLines']),
    int(meta[x]['LinkCount']),
    int(meta[x]['AvgSentLen']),
    int(meta[x]['AvgWordLen']),
    int(meta[x]['NumAllCaps']),
    int(meta[x]['NumExclams'])
] for x in all_answers])

measure_classifier_performance(knn_classifier, X, Y)

print('############### Bias-Variance trade-off p108 ################')


def bias_variance_analysis(classifier, x_data, y_data, name):
    data_sizes = numpy.arange(60, 2000, 4)

    train_errors = []
    test_errors = []

    for data_size in data_sizes:
        step_train_errors, step_test_errors = measure_classifier_performance(
            classifier, x_data[:data_size], y_data[:data_size], False
        )
        train_errors. append(numpy.mean(step_train_errors))
        test_errors. append(numpy.mean(step_test_errors))

    plot_bias_variance(
        data_sizes,
        train_errors,
        test_errors,
        name,
        "Bias-Variance for '%s'" % name
    )


bias_variance_analysis(knn_classifier, X, Y, "5NN")


print('############### Model Complexity for different k values in kNN p 112 ################')
# try reducing model complexity by increasing k


def k_complexity_analysis_for_knn(x_data, y_data):
    # creates a range of k values for testing
    k_values = numpy.hstack((
        (numpy.arange(1, 20)),
        (numpy.arange(21, 100, 5))
    ))

    train_errors = []
    test_errors = []

    for k in k_values:
        step_train_errors, step_test_errors = measure_classifier_performance(
            neighbors.KNeighborsClassifier(n_neighbors=k), x_data, y_data, False
        )
        train_errors.append(numpy.mean(step_train_errors))
        test_errors.append(numpy.mean(step_test_errors))

    plot_k_complexity(k_values, train_errors, test_errors)


for k in [5, 10, 40]:
    print(f"kNN for k={k}")
    measure_classifier_performance(
        neighbors.KNeighborsClassifier(n_neighbors=k),
        data_x=X,
        data_y=Y
    )
k_complexity_analysis_for_knn(x_data=X[:2000], y_data=Y[:2000])


print('############### Classifying by Logistic Regression ################')
# by regularization parameter C we can control the model complexity, similar to the parameter k for the nearest neighbor
# method. Smaller values for C result in more penalization of the model complexity.

for c in [0.01, 0.1, 1.0, 10.0]:
    name = f"LogReg C={c}"
    print(name)
    logistic_regression_classifier = LogisticRegression(penalty='l2', C=c)
    bias_variance_analysis(
        logistic_regression_classifier, X, Y, name
    )
    measure_classifier_performance(logistic_regression_classifier, X, Y)


print('############### accuracy: precision / recall p116 ################')
# precision = True Positive(TP) / (True Positive(TP) + False Positive(FP)
# recall = True Positive(TP) / (True Positive(TP) + False Negative(FN)

# roc: Receiver operating characteristic
# auc: area under curve


def measure_classifier_performance_with_precision_recall(classifier, data_x, data_y, print_info=True, name=""):
    train_errors = []
    test_scores = []
    test_errors = []

    precisions = []
    recalls = []
    pr_scores = []
    fp_rates = []
    tp_rates = []
    roc_scores = []
    thresholds = []

    kfold = KFold(n_splits=10, shuffle=True)

    for train, test in kfold.split(data_x):
        x_train, y_train = data_x[train], data_y[train]
        x_test, y_test = data_x[test], data_y[test]
        classifier.fit(x_train, y_train)
        train_errors.append(1 - classifier.score(x_train, y_train))
        test_score = classifier.score(x_test, y_test)
        test_scores.append(test_score)
        test_errors.append(1 - test_score)

        probability = classifier.predict_proba(x_test)[:, 1]    # 1 because there is 2 class for classification

        fp_rate, tp_rate, roc_threshold = roc_curve(y_test, probability)

        precision, recall, pr_thresholds = precision_recall_curve(y_test, probability)

        roc_scores.append(auc(fp_rate, tp_rate))
        fp_rates.append(fp_rate)
        tp_rates.append(tp_rate)
        thresholds.append(pr_thresholds)

        pr_scores.append(auc(recall, precision))
        precisions.append(precision)
        recalls.append(recall)

    # sort scores and find the medium to use in plot p118
    scores_to_sort = pr_scores
    medium = numpy.argsort(scores_to_sort)[int(len(scores_to_sort) / 2)]

    plot_roc(roc_scores[medium], name, fp_rates[medium], tp_rates[medium])
    plot_precision_recall(
        pr_scores[medium],
        name,
        precisions[medium],
        recalls[medium],
        "good answers"
    )

    if print_info:
        idx80 = precisions[medium] >= 0.8
        print(f"Precision={precisions[medium][idx80][0]}")
        print(f"Recall={recalls[medium][idx80][0]}")
        thresholds = numpy.hstack(([0], thresholds[medium]))[idx80][0]
        print(f"Thresholds={thresholds}")

        probability_for_good = classifier.predict_proba(x_test)[:, 1]
        print(classification_report(
            y_test,
            probability_for_good > 0.63,
            target_names=['not accepted', 'accepted']
        ))

        # the way to use achieved threshold in prediction process p119
        # answer_class = probability_for_good > thresholds

    return classifier


knn_classifier = measure_classifier_performance_with_precision_recall(
    knn_classifier,
    X,
    Y,
    name="knn classifier"
)
logistic_regression_classifier = measure_classifier_performance_with_precision_recall(
    LogisticRegression(penalty='l2', C=0.1),
    X,
    Y,
    name="LogReg classifier"
)

print('############### plot feature importance p120 ################')
feature_names = numpy.array((
    'NumTextTokens',
    'NumCodeLines',
    'LinkCount',
    'AvgSentLen',
    'AvgWordLen',
    'NumAllCaps',
    'NumExclams',
    'NumImages'
))
plot_feature_importance(feature_names, logistic_regression_classifier, "LogReg C=0.10")


print('############### ship it p121 ################')
import pickle
pickle.dump(logistic_regression_classifier, open("logistic_regression_classifier.dat", "wb"))
logistic_regression_classifier = pickle.load(open("logistic_regression_classifier.dat", "rb"))
