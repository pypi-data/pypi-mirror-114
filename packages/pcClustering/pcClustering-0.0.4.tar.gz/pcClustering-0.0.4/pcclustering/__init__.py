"""
Hello from easygui/__init__.py

"""

# __all__ must be defined in order for Sphinx to generate the API automatically.
__all__ = ['agglomerative','brich','mini_batch_kmeans','spectral_clustering','gaussian_mixture','k_means','dbscan']

# Import all functions that form the API
from .pcclustering import agglomerative
from .pcclustering import brich
from .pcclustering import mini_batch_kmeans
from .pcclustering import spectral_clustering
from .pcclustering import gaussian_mixture
from .pcclustering import k_means
from .pcclustering import dbscan
