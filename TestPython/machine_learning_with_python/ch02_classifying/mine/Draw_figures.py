import numpy
from matplotlib import pyplot
import numpy as np
from matplotlib.colors import ListedColormap

from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier

print('############## figure1 p38 ############')

data = load_iris()
# load_iris returns an object with several fields
iris_features = data.data
feature_names = data.feature_names
target = data.target
target_names = data.target_names

for t in range(3):
    if t == 0:
        c = 'r'
        marker = '>'
    elif t == 1:
        c = 'g'
        marker = 'o'
    elif t == 2:
        c = 'b'
        marker = 'x'
    pyplot.scatter(
        iris_features[target == t, 0],
        iris_features[target == t, 1],
        marker=marker,
        c=c
    )
# pyplot.show()

print('############## figure5 p47 ############')


def load_seeds():
    data = []
    labels = []

    with open('../book/data/seeds.tsv') as file:
        for line in file:
            values = line.strip().split('\t')
            data.append([float(v) for v in values[:-1]])
            labels.append(values[-1])
    return numpy.array(data), numpy.array(labels)


def plot_predictions(features, labels):
    x_start, x_end = features[:, 0].min() * .9, features[:, 0].max() * 1.1
    y_start, y_end = features[:, 2].min() * .9, features[:, 2].max() * 1.1
    x_values = numpy.linspace(x_start, x_end, 1000)
    y_values = numpy.linspace(y_start, y_end, 1000)
    #   Return coordinate matrices from coordinate vectors.
    x_values, y_values = numpy.meshgrid(x_values, y_values)

    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(features[:, (0, 2)], labels)
    # vstack: Stack arrays in sequence vertically (row wise)
    # ravel: Returns a 1D version of self, as a view.
    predictions = model.predict(
        numpy.vstack([x_values.ravel(), y_values.ravel()]).T
    ).reshape(x_values.shape)

    color_map = ListedColormap([(1., .7, .7), (.7, 1., .7), (.7, .7, 1.)])
    dot_color_map = ListedColormap([(1., .0, .0), (.1, .6, .1), (.0, .0, 1.)])

    figure, axes = pyplot.subplots()
    axes.set_xlim(x_start, x_end)
    axes.set_ylim(y_start, y_end)
    axes.set_xlabel(feature_names[0])
    axes.set_ylabel(feature_names[2])
    axes.pcolormesh(x_values, y_values, predictions, cmap=color_map)
    axes.scatter(
            features[:, 0],
            features[:, 2],
            c=labels,
            cmap=dot_color_map
        )
    return figure, axes


seed_data, labels = load_seeds()
names = sorted(set(labels))
# replace str label with index of label
labels = numpy.array([names.index(label) for label in labels])

normalized_data = (seed_data - seed_data.mean(0)) / seed_data.std(0)
figure, axes = plot_predictions(normalized_data, labels)
figure.tight_layout()
pyplot.show()