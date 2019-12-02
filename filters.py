from lmapper.filter import Filter
from sklearn.decomposition import PCA
import numpy as np


class SvdFilter(Filter):
    def __init__(self, n_components):
        self.pca = PCA(n_components=n_components)

    def __call__(self, data):
        return self.pca.fit_transform(data).flatten()


class LpFilter(Filter):
    def __init__(self, p, k):
        self.p = p
        self.k = k

    def __call__(self, data):
        return np.sum(np.abs(data) ** self.p, axis=1) ** (self.k / self.p)
