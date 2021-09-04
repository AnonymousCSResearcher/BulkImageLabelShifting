from flask_jsonpify import jsonify
from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation
import hdbscan
import pickle
import json
import numpy as np


def cluster_images(catalogname):
    print("Start...")
    # set clustering algorithm
    algorithm = "kmeans"
    # set number of clusters (kmeans) / min cluster size (hdbscan)
    n_clust = 10

    print("Load pickle...")
    with open("catalogs/"+catalogname + "/img_data_" + catalogname + ".pkl", "rb") as f:
        data = pickle.load(f)
    ########################

    print("Algorithm starts...")
    # execute clustering algorithm
    if algorithm == "kmeans":
        clustering = KMeans(n_clusters=n_clust, random_state=0).fit_predict(data)
    if algorithm == "affinity":
        clustering = AffinityPropagation().fit_predict(data)
    if algorithm == "hdbscan":
        clustering = hdbscan.HDBSCAN(min_cluster_size=n_clust).fit_predict(data)

    # save clustering
    with open("catalogs/"+catalogname + "/clustering_" + catalogname + ".pkl", "wb") as f:
        pickle.dump(clustering, f)

    print("Clustering End...")
    return jsonify({'status': 'success'})

    # args clustering_path,img_path


def create_dict(catalogname):
    # get clustering
    with open("catalogs/"+catalogname + "/clustering_" + catalogname + ".pkl", "rb") as f:
        clustering = pickle.load(f)

    # get filenames
    with open("catalogs/"+catalogname + "/img_files_" + catalogname + ".pkl", "rb") as f:
        files = pickle.load(f)

    # create cluster dictionary
    cluster_dict = {}

    for i in range(0, max(clustering) + 1):
        cluster_dict[i] = []

        # retrieve all filenames of cluster
        cluster_filenames = np.where(clustering == i)[0]

        for item in cluster_filenames:
            cluster_dict[i].append(files[item])

    with open("catalogs/"+catalogname + "/sort_dict_" + catalogname + ".json", "w") as f:
        json.dump(cluster_dict, f)
