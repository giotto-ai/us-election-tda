import sys
sys.path.append('..')
import lmapper as lm
from lmapper.cover import UniformCover
from lmapper.cluster import Linkage


def get_node_size(mapper, offset=50):
    return list(map(lambda x: len(x._labels) + offset,
                    list(dict(mapper._nodes.items()).values())))


def get_mean_node(mapper, df, col):
    return list(map(lambda x: df.iloc[x._labels][col].mean(),
                    list(dict(mapper._nodes.items()).values())))


def get_mapper(filtr, nintervals, overlap, method,
               metric, cutoff, data):
    cover = UniformCover(nintervals=nintervals,
                         overlap=overlap)
    cluster = Linkage(method=method, metric=metric,
                      cutoff=cutoff)
    mapper = lm.Mapper(data=data,
                       filter=filtr,
                       cover=cover, cluster=cluster)
    return mapper
