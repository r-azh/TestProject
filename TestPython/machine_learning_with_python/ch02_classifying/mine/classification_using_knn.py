import numpy

print('############## classification using nearest neighbor p44 ############')
# Nearest neighbor classification: when classifying a new element, it looks at the
# training data for the object that is closest to it.

# scikit-learn classification API is organized around 'classifier objects' with two
# essential methods: fit that is learning step, predict

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import KFold, cross_validate


def load_seeds():
    data = []
    labels = []

    with open('../book/data/seeds.tsv') as file:
        for line in file:
            values = line.strip().split('\t')
            data.append([float(v) for v in values[:-1]])
            labels.append(values[-1])
    return numpy.array(data), numpy.array(labels)


features, labels = load_seeds()

classifier = KNeighborsClassifier(n_neighbors=1)    # number of neighbors to consider
kf = KFold(n_splits=5, shuffle=True)
means = []
for training, testing in kf.split(features):
    classifier.fit(features[training], labels[training])
    prediction = classifier.predict(features[testing])

    # numpy.mean on an array of boolean returns fraction of correct decisions for this fold
    correct_mean = numpy.mean(prediction == labels[testing])
    means.append(correct_mean)

print("Mean accuracy: {:.1%}".format(numpy.mean(means)))

# using cross_validate from sklearn
cross_validate_result = cross_validate(classifier, features, labels, cv=kf)
print("Mean accuracy: {:.1%}".format(numpy.mean(cross_validate_result['test_score'])))

print('############## normalize to z-scores p44 ############')
# the z-score of a value is how far away from the mean it is, in units of standard deviation
# normalized_value = (value - mean_of_feature) / standard_deviation
# in sklearn it is StandardScaler

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# we should use a pipeline of transformations: 1-transformation 2-classification
classifier = KNeighborsClassifier(n_neighbors=1)
classifier = make_pipeline([
    ('normalize', StandardScaler()),
    ('knn', classifier)
])

