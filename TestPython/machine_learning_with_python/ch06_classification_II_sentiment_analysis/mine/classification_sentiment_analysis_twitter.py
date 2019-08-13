import numpy

from TestPython.machine_learning_with_python.ch06_classification_II_sentiment_analysis.book.utils import \
    load_sanders_data

print('############### Fetch twitter data ################')
X, Y = load_sanders_data()

classes = numpy.unique(Y)
for c in classes:
    print("#%s: %i" % (c, sum(Y == c)))
