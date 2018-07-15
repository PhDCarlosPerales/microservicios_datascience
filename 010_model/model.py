import numpy as np
from sklearn import datasets, metrics
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


iris = datasets.load_iris()

############################################################################################
# Fit
############################################################################################
X_train,X_test,Y_train,Y_test = train_test_split(iris.data, iris.target, test_size=0.2,
                                                 random_state=42)

# fit a logistic regression model to the data
model = LogisticRegression()
model.fit(X_train, Y_train)
print(model)
# make predictions
expected = iris.target
predicted = model.predict(iris.data)
# summarize the fit of the model
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))


# Printing decision regions
plt.figure(figsize=(10, 10))


def plot_decision_regions(X, y, classifier, test_idx):
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                         np.arange(y_min, y_max, 0.1))
    Z = classifier.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.contourf(xx, yy, Z, alpha=0.4)
    plt.scatter(X[:, 0], X[:, 1], c=y,
                                  s=20, edgecolor='k')


plot_decision_regions(X = iris.data[:,[2,3]]
                  , y = iris.target
                  , classifier = LogisticRegression().fit(X_train[:,[2,3]], Y_train) # Fit 2d to plot 2d
                  , test_idx = range(105,150))
plt.xlabel('Petal length')
plt.ylabel('Petal width')
plt.show()



############################################################################################
# Predict
############################################################################################
print("Last row sp {}".format(iris.target[-1:]))
print("Prediction for last row: {}".format(model.predict_proba(iris.data[-1:])))


############################################################################################
# Persist
############################################################################################
import pickle
# save the model to disk
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = dir_path+'/iris_model.pkl'
print("Saving to {}".format(filename))
pickle.dump(model, open(filename, 'wb'))

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.predict_proba(iris.data[-1:])
print("Prediction from pickle for last row: {}".format(result))
