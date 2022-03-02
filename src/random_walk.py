"""
Large graph clustering using random walkers
"""
import inc.reader as reader
import networkx as nx
import inc.tools as tools
import random
import time
from random import seed
from datetime import datetime
seed(datetime.now())


def random_walk(steps, vertex, G):
    community = set()
    for _ in range(steps):
        neighborhood = list(G.edges(vertex))
        new_edge = random.choice(neighborhood)
        vertex = new_edge[1]
        community.add(vertex)
    return community


def similar_clusters(threshold_similarity, modules):
    for i in range(len(modules)):
        for j in range(len(modules)):
            if i < j:
                if tools.jaccard_similarity(modules[i], modules[j]) >= threshold_similarity:
                    return i, j
    return -1, -1


def join(community_index1, community_index2, community1, community2, cluster_of, modules):
    if cluster_of[community_index1] == -1 and cluster_of[community_index2] == -1:
        new_module = community1.union(community2)
        modules.append(new_module)
        cluster_of[community_index1] = len(modules) - 1
        cluster_of[community_index2] = len(modules) - 1
    elif cluster_of[community_index1] != -1:
        modules[cluster_of[community_index1]].update(community2)
        cluster_of[community_index2] = cluster_of[community_index1]
    else:
        modules[cluster_of[community_index2]].update(community1)
        cluster_of[community_index1] = cluster_of[community_index2]
    return modules, cluster_of


def join_similar_communities(threshold_similarity, communities, G):
    cluster_of = [-1 for _ in range(len(communities))]
    modules = list(set())
    community_index1 = 0

    for community1 in communities:
        community_index2 = 0
        for community2 in communities:
            if community_index1 < community_index2:
                similarity = tools.jaccard_similarity(community1, community2)
                if similarity >= threshold_similarity:
                    modules, cluster_of = join(community_index1, community_index2,
                                               community1, community2, cluster_of, modules)
            community_index2 += 1
        community_index1 += 1

    for index in range(len(cluster_of)):
        if cluster_of[index] == -1:
            modules.append(communities[index])

    return modules


def clusters(G, steps, threshold_similarity):
    communities = list()
    for node in G.nodes:
        community = random_walk(steps, node, G)
        communities.append(community)

    modules = join_similar_communities(threshold_similarity, communities, G)
    index1, index2 = similar_clusters(threshold_similarity, modules)

    while index1 != -1:
        modules[index1] = modules[index1].union(modules[index2])
        modules.pop(index2)
        index1, index2 = similar_clusters(threshold_similarity, modules)

    return modules


def main():
    steps = 50
    threshold_similarity = 0.1
    G = reader.create_graph('../graphs/g1.csv', True)
    # G = nx.karate_club_graph()

    start = time.time()
    modules = clusters(G, steps, threshold_similarity)
    end = time.time()

    print('Nodes: ', G.number_of_nodes())
    print('Edges: ', G.number_of_edges())
    print('Clustering time: ', end - start)
    print('Number of clusters: ', len(modules))


main()
