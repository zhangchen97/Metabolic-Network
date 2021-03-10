from sklearn.model_selection import KFold
import numpy as np
import random
#X = np.array([[1, 2], [1, 3], [1, 4], [3, 4],[5,6],[7,8]])
list=[1, 2, 3, 4,5,6,7,8,9,10,11,12]
random.shuffle(list)
print(list)
X = np.array(list)
print(X)
kf = KFold(n_splits=3)

for train_index, test_index in kf.split(X):
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = X[train_index], X[test_index]
    #y_train, y_test = y[train_index], y[test_index]
    print(X_train)
    print(X_test)
    print("=============")
