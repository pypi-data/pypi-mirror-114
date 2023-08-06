"""
Hashing-based clustering method
"""

import random
import time
import matplotlib.pyplot as plt
import numpy as np

# Global constants
EPISILON = (0.0001, 0.0002)
COLORS = ('b', 'g', 'r', 'c', 'm', 'y', 'k', 'w')


### Instrastructure

def gen_cluster_centers(num_clusters):
    """
    Input: int num_clusters
    
    Output: numpy array of cluster centers in the square [-1, 1]^2
    """
    
    return np.array([(random.uniform(-1, 1), random.uniform(-1, 1)) for dummy in range(num_clusters)])


def gen_cluster_points(cluster_centers, points_in_cluster):
    """
    Input: numpy array cluster_centers, int points_in_cluster
    
    Output: numpy array points to be clustered
    """
    
    return np.array([ (x_center + random.uniform(-EPISILON[0] / 2, EPISILON[0] / 2),
              y_center + random.uniform(-EPISILON[1] / 2, EPISILON[1] / 2))
             for (x_center, y_center) in cluster_centers for dummy in range(points_in_cluster) ])


def gen_default_clustering(cluster_centers, points_in_cluster):
    """
    Input: numpy array cluster_centers, int points_in_cluster
    
    Output: set of tuples of integers indices for clustering associated with point creation
    """
    
    return set([tuple(range(points_in_cluster * idx, points_in_cluster * (idx + 1))) for idx in range(len(cluster_centers))])



def get_box(point):
    """
    Input: tuple point of floats
    
    Output: list of vertices of box centered at point with size EPISILON
    """
    
    return np.array(
        [(point[0] - EPISILON[0] / 2, point[1] - EPISILON[1] / 2),
         (point[0] - EPISILON[0] / 2, point[1] + EPISILON[1] / 2),
         (point[0] + EPISILON[0] / 2, point[1] + EPISILON[1] / 2),
         (point[0] + EPISILON[0] / 2, point[1] - EPISILON[1] / 2),
         (point[0] - EPISILON[0] / 2, point[1] - EPISILON[1] / 2)])

def plot_clusters(points, clusters):
    """
    Input: numpy array of points, list clusters of sets of indices
    
    Actions: Plots points and 
    """
    
    color = 0
    for cluster in clusters:
        for idx in cluster:
            point = points[idx]
            box = get_box(point)
            plt.plot(box[:, 0], box[:, 1], c=COLORS[color])
        color = (color +1 ) % len(COLORS)
        
    plt.show()
    
    
### Functions for hashing-based clustering
    
    
def hash_point(point):
    """
    Input: Tuple point of floats
    
    Output: Tuple of ints suitable for hashing
    """
    
    return (int(round(point[0] / EPISILON[0])),
            int(round(point[1] / EPISILON[1])))


def get_neighbors(bin_idx):
    """
    Input: tuple bin_idx of integers
    
    Output: set of eight integer tuples
    """
    
    return {(bin_idx[0] - 1, bin_idx[1] - 1),
            (bin_idx[0] - 1, bin_idx[1]),
            (bin_idx[0] - 1, bin_idx[1] + 1),
            (bin_idx[0], bin_idx[1] - 1),
            (bin_idx[0], bin_idx[1] + 1),
            (bin_idx[0] + 1, bin_idx[1] - 1),
            (bin_idx[0] + 1, bin_idx[1]),
            (bin_idx[0] + 1, bin_idx[1] + 1)}

        
def merge_clusters(points, bins, bin_idx, neighbor_idx):
    """
    Input: list points, hash table bins, keys bin_idx, neighbor_idx
    
    Action: update hash table bins with clusters for bin_idx and neighbor_idx merged
    
    NOTE: maintains the invariant that the bins for a current cluster always point 
    to the SAME set of points indices (no copies are made)
    """
    
    if neighbor_idx not in bins:
        return
    
    bin_cluster = bins[bin_idx]
    neighbor_cluster = bins[neighbor_idx]
        
    # Always mutate the bigger cluster and iterative update the smaller cluster    
    if len(neighbor_cluster) > len(bin_cluster):
        neighbor_cluster.update(bin_cluster)
        for pt_idx in bin_cluster:
            bin_pt_idx = hash_point(points[pt_idx])
            bins[bin_pt_idx] = neighbor_cluster  
    else:
        bin_cluster.update(neighbor_cluster)       
        for pt_idx in neighbor_cluster:
            neighbor_pt_idx = hash_point(points[pt_idx])
            bins[neighbor_pt_idx] = bin_cluster
            

def gen_hash_clustering(points):
    """
    Input: list, points of tuples
    
    Output: list, sets of integers
    """
    
    # Assign point indices to bins
    bins = {}
    for point, pt_idx in zip(points, range(len(points))):
        bin_idx = hash_point(point)
        if bin_idx in bins:
            bins[bin_idx].add(pt_idx)
        else:
            bins[bin_idx] = {pt_idx}
    
    # Merge clusters for adjacent bins
    for bin_idx in bins:
        for neighbor_idx in get_neighbors(bin_idx):
            merge_clusters(points, bins, bin_idx, neighbor_idx)
    
    # Extract unique clustering
    clustering = set()
    for idx in bins:
        clustering.add(tuple(sorted(bins[idx])))
    
    return clustering
        
        
    
def test_hash_clustering():
    """ Test out hashing-based clustering """
    
    random.seed(1)
    num_clusters = 10
    points_in_clusters = 6
    
    cluster_centers = gen_cluster_centers(num_clusters)
    points = gen_cluster_points(cluster_centers, points_in_clusters)
    
    print(points)
    
    default_clusters = gen_default_clustering(cluster_centers, points_in_clusters)
    print(default_clusters)
    plot_clusters(points, default_clusters)
    
    start_time = time.perf_counter()
    print("Start hash clustering")
    hash_clusters = gen_hash_clustering(points)
    print("Done hash clustering")
    stop_time = time.perf_counter()
    print("Took", stop_time - start_time, "seconds for", num_clusters * points_in_clusters, "points")
    print(hash_clusters)
    plot_clusters(points, hash_clusters)
    
# test_hash_clustering()

