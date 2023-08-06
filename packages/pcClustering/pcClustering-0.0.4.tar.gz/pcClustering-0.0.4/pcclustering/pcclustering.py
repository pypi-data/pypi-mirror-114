import pandas as pd
import numpy as np
from numpy import unique
from numpy import where
from sklearn.datasets import make_classification
import csv
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import Birch
from sklearn.cluster import MiniBatchKMeans
from sklearn.mixture import GaussianMixture
from sklearn.cluster import SpectralClustering
from matplotlib import pyplot
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.metrics import calinski_harabasz_score
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN

import warnings
warnings.filterwarnings('ignore')

def agglomerative(st,n_clusters):
    data = pd.read_csv(st,sep = " ")
    X1= data.iloc[:,0:3]
    X=X1.values
    model = AgglomerativeClustering(n_clusters)
    yhat = model.fit_predict(X)
    clusters = unique(yhat)
    fig = plt.figure()
    ax = Axes3D(fig)
    for cluster in clusters:
        row_ix = where(yhat == cluster)
        ax.scatter3D(X[row_ix , 0], X[row_ix , 1],X[row_ix , 2],marker=".")
    ax.view_init(elev = 60,azim = 30)
    ax.set_zlabel('Z')
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    sc_score = silhouette_score(X, yhat, metric='euclidean')
    sc_ch=calinski_harabasz_score(X, yhat)
    print("平均轮廓系数:",sc_score,'\n','CH系数:',sc_ch,'\n')
    return

def brich(st,n_clusters,threshold):
    data = pd.read_csv(st,sep = " ")
    X1= data.iloc[:,0:3]
    X=X1.values
    model = Birch(threshold, n_clusters)
    yhat = model.fit_predict(X)
    clusters = unique(yhat)
    fig = plt.figure()
    ax = Axes3D(fig)
    for cluster in clusters:
        row_ix = where(yhat == cluster)
        ax.scatter3D(X[row_ix , 0], X[row_ix , 1],X[row_ix , 2],marker=".")
    ax.view_init(elev = 60,azim = 30)
    ax.set_zlabel('Z')
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    sc_score = silhouette_score(X, yhat, metric='euclidean')
    sc_ch=calinski_harabasz_score(X, yhat)
    print("平均轮廓系数:",sc_score,'\n','CH系数:',sc_ch,'\n')
    return

def mini_batch_kmeans(st,n_clusters):
    data = pd.read_csv(st,sep = " ")
    X1= data.iloc[:,0:3]
    X=X1.values
    model = MiniBatchKMeans(n_clusters)
    yhat = model.fit_predict(X)
    clusters = unique(yhat)
    fig = plt.figure()
    ax = Axes3D(fig)
    for cluster in clusters:
        row_ix = where(yhat == cluster)
        ax.scatter3D(X[row_ix , 0], X[row_ix , 1],X[row_ix , 2],marker=".")
    ax.view_init(elev = 60,azim = 30)
    ax.set_zlabel('Z')
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    sc_score = silhouette_score(X, yhat, metric='euclidean')
    sc_ch=calinski_harabasz_score(X, yhat)
    print("平均轮廓系数:",sc_score,'\n','CH系数:',sc_ch,'\n')
    return

def spectral_clustering(st,n_clusters):
    data = pd.read_csv(st,sep = " ")
    X1= data.iloc[:,0:3]
    X=X1.values
    model = SpectralClustering(n_clusters)
    yhat = model.fit_predict(X)
    clusters = unique(yhat)
    fig = plt.figure()
    ax = Axes3D(fig)
    for cluster in clusters:
        row_ix = where(yhat == cluster)
        ax.scatter3D(X[row_ix , 0], X[row_ix , 1],X[row_ix , 2],marker=".")
    ax.view_init(elev = 60,azim = 30)
    ax.set_zlabel('Z')
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    sc_score = silhouette_score(X, yhat, metric='euclidean')
    sc_ch=calinski_harabasz_score(X, yhat)
    print("平均轮廓系数:",sc_score,'\n','CH系数:',sc_ch,'\n')
    return

def gaussian_mixture(st,n_components):
    data = pd.read_csv(st,sep = " ")
    X1= data.iloc[:,0:3]
    X=X1.values
    model = GaussianMixture(n_components)
    yhat = model.fit_predict(X)
    clusters = unique(yhat)
    fig = plt.figure()
    ax = Axes3D(fig)
    for cluster in clusters:
        row_ix = where(yhat == cluster)
        ax.scatter3D(X[row_ix , 0], X[row_ix , 1],X[row_ix , 2],marker=".")
    ax.view_init(elev = 60,azim = 30)
    ax.set_zlabel('Z')
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    sc_score = silhouette_score(X, yhat, metric='euclidean')
    sc_ch=calinski_harabasz_score(X, yhat)
    print("平均轮廓系数:",sc_score,'\n','CH系数:',sc_ch,'\n')
    return

def k_means(st,n_clusters):
  data = pd.read_csv(st,sep = " ")
  data1 = data.iloc[:,0:3]
  transfer = StandardScaler()
  data_new = transfer.fit_transform(data1)
  estimator = KMeans(n_clusters)
  estimator.fit(data_new)
  y_pred = estimator.predict(data_new)
  fig = plt.figure()
  ax = Axes3D(fig)
  for i in range(4):
    ax.scatter3D(data_new[y_pred == i,0],data_new[y_pred == i,1],data_new[y_pred == i,2],marker = ".")
  ax.view_init(elev = 60,azim = 30)
  ax.set_zlabel('Z')
  ax.set_ylabel('Y')
  ax.set_xlabel('X')
  sc_score = silhouette_score(data, estimator.labels_, metric='euclidean')
  sc_ch=calinski_harabasz_score(data, estimator.labels_)
  print("平均轮廓系数:",sc_score,'\n','CH系数:',sc_ch,'\n')
  return


def dbscan(str1, eps, min_samples):
    file = open(str1, 'r')
    reader = csv.reader(file)
    reader = list(reader)
    m, n = np.shape(reader)
    data = np.zeros([m, 3], dtype=np.float32)
    for i in range(0, m - 1):
        reader[i] = reader[i][0].split(' ', 3)
        reader[i][0] = float(reader[i][0])
        reader[i][1] = float(reader[i][1])
        reader[i][2] = float(reader[i][2])
        data[i][0] = reader[i][0]
        data[i][1] = reader[i][1]
        data[i][2] = reader[i][2]
    estimator = DBSCAN(eps, min_samples)
    estimator.fit(data)
    y_pred = estimator.labels_
    fig = plt.figure()
    ax = Axes3D(fig)
    for i in range(4):
        ax.scatter3D(data[y_pred == i, 0], data[y_pred == i, 1], data[y_pred == i, 2], marker=".")
    ax.view_init(elev=60, azim=30)
    ax.set_zlabel('Z')
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    sc_score = silhouette_score(data, estimator.labels_, metric='euclidean')
    sc_ch = calinski_harabasz_score(data, estimator.labels_)
    print("平均轮廓系数:", sc_score, '\n', 'CH系数:', sc_ch, '\n')
    plt.show()
    return
