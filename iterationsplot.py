import numpy as np
import scipy.sparse as sparse
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale, normalize
import pandas as pd
import networkx as nx
import collections
from kmeans import k_means
import matplotlib.pyplot as plt

path      = 'graphs/'
file      = ['ca-GrQc.txt']
k         = 10

edgelist  = pd.read_csv(path + file[0], delimiter=' ', skiprows=1, header=None)
G         = nx.from_pandas_edgelist(edgelist, source=0, target=1, create_using=nx.Graph())
adj_matr  = nx.to_pandas_adjacency(G, dtype=np.float64)
laplacian = sparse.csgraph.laplacian(adj_matr.values, normed=True)

eigenvalues, eigenvectors = np.linalg.eig(laplacian)
eigenvectors = normalize(eigenvectors.astype(np.float64))

kmeans = KMeans(n_clusters=k, max_iter = 1, n_init=1).fit(eigenvectors)
init_centers = kmeans.cluster_centers_ 

n = 10

phis = np.zeros(n)
best = np.zeros(n)
j = 0
for iterations in range(1, 100, 10):
        kmeans = KMeans(n_clusters=k, max_iter=iterations, init=init_centers).fit(eigenvectors)

        cut_edges = 0
        for i in range(edgelist.shape[0]):
                if (kmeans.labels_[edgelist[0][i]] != kmeans.labels_[edgelist[1][i]]):
                        cut_edges += 1

        counter = collections.Counter(kmeans.labels_)
        smallest = 100000
        for key, value in counter.items():
                if (value < smallest):
                        smallest = value
        phis[j] = cut_edges / smallest
        best[j] = np.amin(phis[:j+1])
        j += 1

print(phis)

plt.plot([1,11,21,31,41,51,61,71,81,91], best,  markerfacecolor='None')
plt.xlabel('Max iterations per single run of k-means algorithm')
plt.ylabel('Objective function')
plt.title('k = 10')
plt.show()
