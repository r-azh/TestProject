# page 101
from sklearn import neighbors
knn = neighbors.KNeighborsClassifier(n_neighbors=2)

print(knn)

# train it using fit
knn.fit(
        [[1], [2], [3], [4], [5], [6]],         # features
        [0, 0, 0, 1, 1, 1]                      # classes
        )

# predict new data instance
result = knn.predict([[1.5]])
print('predict for 1.5: ', result)

result = knn.predict([[37]])
print('predict for 37: ', result)

result = knn.predict([[3]])
print('predict for 3: ', result)

result = knn.predict([[3.5]])
print('predict for 3.5: ', result)

# getting class probabilities:
# the result is the probabilities of request value being in each class
result = knn.predict_proba([[1.5]])
print('predict probability for 1.5: ', result)

result = knn.predict_proba([[37]])
print('predict probability for 37: ', result)

result = knn.predict_proba([[3.5]])
print('predict probability for 3.5: ', result)