import numpy
from sklearn.datasets import load_iris

data = load_iris()
features = data.data
feature_names = data.feature_names
target = data.target
target_names = data.target_names

# using NumPY array indexing to get an array of strings
lables = target_names[target]

print('############## finding a threshold for separating iris setosa from others by petal length (as seen in figure)############')
petal_length = features[:, 2]

is_setosa = (lables == 'setosa')

# using NumPY array indexing to get an array and then find max and min in that array for petal length threshold
max_setosa = petal_length[is_setosa].max()
min_non_setosa = petal_length[~is_setosa].min()

print('Maximum of setosa: ', max_setosa)
print('Minimum of others: ', min_non_setosa)


print('############## finding another threshold for separating iris virginca and versicolor ############')
# remove setosa data from features and labels
features = features[~is_setosa]
lables = lables[~is_setosa]

is_virginica = (lables == 'virginica')


class Model:
    def __init__(self, best_threshold, best_feature, best_reverse, best_accuracy):
        self.best_accuracy = best_accuracy
        self.best_feature = best_feature
        self.best_threshold = best_threshold
        self.best_reverse = best_reverse


def fit_threshold_model(features, lables):
    # Initialize best_accuracy to impossible low value
    best_accuracy = -1.0

    # for each data column
    for column in range(features.shape[1]):
        # Test all possible values for threshold
        feature_values = features[:, column].copy()
        for value in feature_values:
            # compute mean of correct answers(comparisons) for this threshold
            prediction = (feature_values > value)
            accuracy = (prediction == lables).mean()
            reverse_accuracy = (prediction != lables).mean()
            if reverse_accuracy > accuracy:
                reverse = True
                accuracy = reverse_accuracy
            else:
                reverse = False

            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_feature = column
                best_threshold = value
                best_reverse = reverse
    # A model is a threshold and an feature_index
    return Model(best_threshold, best_feature, best_reverse, best_accuracy)


model = fit_threshold_model(features, is_virginica)
print('Best threshold is {0} on feature {1} (index {2}), which achieves accuracy of {3:.1%}.'.format(
    model.best_threshold,
    data.feature_names[model.best_feature],
    model.best_feature,
    model.best_accuracy
))

print('############## create a method based on thresholds to do the classification ############')


def is_virginica_test_for_one_row(feature_index, threshold, reverse, example):
    """ Apply threshold model to a new example """
    test = example[feature_index] > threshold
    if reverse:
        test = not test
    return test


def is_virginca_test_for_all_rows(feature_index, threshold, reverse, examples):
    if reverse:
        return examples[:, feature_index] <= threshold
    return examples[:, feature_index] > threshold
# In a threshold model, the decision boundary will always be a line that is parallel to one ot the axes


print('############## heldout data: use train and test data p36 ############')

# Split the data in two: testing and training
# tile Construct an array by repeating first arg the number of times given by second arg.
testing = numpy.tile([True, False], 50)
training = ~testing


def predict(model, data):
    return is_virginca_test_for_all_rows(
        model.best_feature,
        model.best_threshold,
        model.best_reverse,
        data
    )


train_predict = predict(model, features[training])
train_accuracy = numpy.mean(train_predict == is_virginica[training])

test_predict = predict(model, features[testing])
test_accuracy = numpy.mean(test_predict == is_virginica[training])
print('''\
Training accuracy was {0:.1%}.
Testing accuracy was {1:.1%} (N = {2}).
'''.format(train_accuracy, test_accuracy, testing.sum())
      )

print('############## cross-validation: leave-one-out p37 ############')

# for each sample a new model is learned
correct = 0.0
for ei in range(len(features)):
    # select all but the one at position ei
    training = numpy.ones(len(features), bool)
    training[ei] = False
    testing = ~training
    model = fit_threshold_model(features[training], is_virginica[training])

    predictions = predict(model, features[testing])
    correct += numpy.sum(predictions == is_virginica[testing])

accuracy = correct / float(len(features))
print('Accuracy: {0:.1%}'.format(accuracy))

print('############## cross-validation: x-fold p38 ############')


def cross_validate(features, labels, fold_count):
    '''Compute cross-validation errors'''
    error = 0.0
    for fold in range(fold_count):
        training = numpy.ones(len(features), bool)  # convert array of ones to boolean
        training[fold::fold_count] = 0
        testing = ~training
        model = fit_threshold_model(features[training], is_virginica[training])
        predictions = predict(model, features[testing])
        test_error = numpy.mean(predictions == is_virginica[testing])
        error += test_error
    return error/fold_count


error = cross_validate(features, lables, 5)
print('5-fold croos-validation error after z-scoring was: ', error)