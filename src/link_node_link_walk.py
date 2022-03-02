"""
Large graph clustering using link-node-link walkers
"""
import random
import time
import inc.reader as reader
import inc.tools as tools
import networkx as nx
from random import seed
from datetime import datetime
seed(datetime.now())


def link_node_link_walk(steps, edge, G):
    community = set()
    for _ in range(steps):
        node = random.choice([edge[0], edge[1]])
        neighborhood = set(G.edges(node))
        if node == edge[0]:
            neighborhood.remove(edge)
        else:
            neighborhood.remove((edge[1], edge[0]))
        neighborhood = list(neighborhood)
        if not neighborhood:
            return community
        edge = random.choice(neighborhood)
        community.add(edge)
    return community


def clusters(G, steps, threshold_similarity):
    communities = list()
    for edge in G.edges:
        community = link_node_link_walk(steps, edge, G)
        if community:
            communities.append(community)

    modules = tools.join_similar_communities(threshold_similarity, communities)
    index1, index2 = tools.similar_clusters(threshold_similarity, modules)

    while index1 != -1:
        modules[index1] = modules[index1].union(modules[index2])
        modules.pop(index2)
        index1, index2 = tools.similar_clusters(threshold_similarity, modules)

    return modules


def main():
    steps = 20
    threshold_similarity = 0.15
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