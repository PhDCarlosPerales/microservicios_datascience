#https://conda.io/miniconda.html
#conda install scikit-learn
from sklearn import datasets
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':
    #Load iris dataset form SciKit Learn
    iris = datasets.load_iris()

    #Create a pandas dataframe to show data
    df_iris = pd.DataFrame(iris.data, columns=iris.feature_names)
    df_iris['target'] = pd.Series(iris.target)

    #Species differences
    X = iris.data
    y = iris.target
    colors = [['orange', 'green', 'red'][i] for i in y]

    with plt.rc_context({'axes.edgecolor': 'green', 'xtick.color': 'green',
                         'ytick.color': 'green', 'figure.facecolor': 'green',
                         'axes.labelcolor': 'green', 'axes.labelsize': 'large',
                         'axes.linewidth' : 4, 'xtick.major.width': 4,
                         'axes.labelsize': 20,
                         'xtick.labelsize': 12, 'ytick.labelsize': 12}):



        plt.figure(figsize=(21, 7))

        plt.subplot(1, 2, 1)
        plt.scatter(X[:, 0], X[:, 1], c=colors)
        plt.xlabel('Sepal length')
        plt.ylabel('Sepal width')

        plt.subplot(1, 2, 2)
        plt.scatter(X[:, 2], X[:, 3], c=colors)
        plt.xlabel('Petal length')
        plt.ylabel('Petal width')

    plt.savefig('Iris.png', transparent=True)