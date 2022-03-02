"""
Large graph clustering using restrained walkers
"""
import networkx as nx
import inc.reader as reader
import inc.tools as tools
import inc.walks as walks
from random import seed
from datetime import datetime
import time
seed(datetime.now())


def clusters(G, steps, window, tolerance, threshold_similarity):
    communities = list()
    for node in G.nodes:
        community = walks.node_node_restrained(steps, window, tolerance, node, G)
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
    steps = 10
    window = 6
    tolerance = 5
    threshold_similarity = 0.1
    G = reader.create_graph('../graphs/soc-sign-bitcoinalpha.csv', True)
    # G = nx.karate_club_graph()

    start = time.time()
    modules = clusters(G, steps, window, tolerance, threshold_similarity)
    end = time.time()

    print('Nodes: ', G.number_of_nodes())
    print('Edges: ', G.number_of_edges())
    print('Clustering time: ', end - start)
    print('Number of clusters: ', len(modules))
    # nx.write_gexf(G, 'test.gexf')


main()
