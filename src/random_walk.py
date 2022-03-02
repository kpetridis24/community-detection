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


def clusters(G, steps, threshold_similarity):
    communities = list()
    for node in G.nodes:
        community = random_walk(steps, node, G)
        communities.append(community)

    modules = tools.join_similar_communities(threshold_similarity, communities)
    index1, index2 = tools.similar_clusters(threshold_similarity, modules)

    while index1 != -1:
        modules[index1] = modules[index1].union(modules[index2])
        modules.pop(index2)
        index1, index2 = tools.similar_clusters(threshold_similarity, modules)

    return modules


def main():
    steps = 40
    threshold_similarity = 0.1
    G = reader.create_graph('../graphs/soc-sign-bitcoinalpha.csv', True)
    # G = nx.karate_club_graph()

    start = time.time()
    modules = clusters(G, steps, threshold_similarity)
    end = time.time()

    print('Nodes: ', G.number_of_nodes())
    print('Edges: ', G.number_of_edges())
    print('Clustering time: ', end - start)
    print('Number of clusters: ', len(modules))


main()
