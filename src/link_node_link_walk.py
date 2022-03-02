"""
Large graph clustering using link-node-link walkers
"""
import random
import time
import inc.reader as reader
import inc.tools as tools
import numpy as np
from random import seed
from datetime import datetime


def link_node_link_walk(steps, edge, G):
    community = list()
    for _ in range(steps):
        seed(datetime.now())
        node = random.choice([edge[0], edge[1]])
        neighborhood = set(G.edges(node))
        if node == edge[0]:
            neighborhood.remove(edge)
        else:
            neighborhood.remove((edge[1], edge[0]))
        neighborhood = list(neighborhood)
        if not neighborhood:
            break
        edge = random.choice(list(neighborhood))
        if edge not in community:
            community.append(set(edge))
        # print(community)
    return community


def clusters(G, steps, desired_similarity):
    communities = dict()
    for edge in G.edges:
        community = link_node_link_walk(steps, edge, G)
        communities[edge] = community

    print('Starting joining')
    communities = tools.join_edge_clusters(desired_similarity, communities, G)
    return communities


def main():
    steps = 5
    desired_similarity = 0.0001
    G = reader.create_graph('../graphs/g1.csv', True)

    start = time.time()
    modules = clusters(G, steps, desired_similarity)
    end = time.time()

    print('Nodes: ', G.number_of_nodes())
    print('Edges: ', G.number_of_edges())
    print('Clustering time: ', end - start)
    print('Number of clusters: ', len(modules))


main()