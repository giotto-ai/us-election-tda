from lmapper.filter import Filter
from sklearn.decomposition import PCA
import numpy as np


class SvdFilter(Filter):
    def __init__(self, n_components):
        self.pca = PCA(n_components=n_components)

    def __call__(self, data):
        return self.pca.fit_transform(data).flatten()


class LogSvdFilter(Filter):
    def __init__(self, n_components):
        self.pca = PCA(n_components=n_components)

    def __call__(self, data):
        res = self.pca.fit_transform(data).flatten()
        return np.log(res + abs(np.min(res)) + 1)


class TrafoSvdFilter(Filter):
    def __init__(self, n_components):
        self.pca = PCA(n_components=n_components)

    def __call__(self, data):
        return np.log(np.abs(self.pca.fit_transform(data).flatten()))


class LogProjectionFilter(Filter):
    def __init__(self, ax):
        self.ax = ax

    def __call__(self, data):
        return np.log(data[:, self.ax] + abs(np.min(data[:, self.ax])) + 1)


class LpFilter(Filter):
    def __init__(self, p, k):
        self.p = p
        self.k = k

    def __call__(self, data):
        return np.sum(np.abs(data) ** self.p, axis=1) ** (self.k / self.p)


class LogisticRegressionFilter(Filter):
    def __init__(self, lr):
        self.lr = lr

    def __call__(self, data):
        return self.lr.predict_proba(data)[:, 1]
