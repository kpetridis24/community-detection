"""
Large graph clustering using restrained walkers
"""
import random
import time
import inc.reader as reader
import inc.tools as tools
import graphs as graphs
from random import seed
from datetime import datetime
seed(datetime.now())


def restrained_walk(steps, window, tolerance, vertex, G):
    community = set()
    accessed_in_steps = [0 for _ in range(steps)]
    accessed_nodes = set()
    for i in range(1, steps):
        neighborhood = list(G.edges(vertex))
        new_edge = random.choice(neighborhood)
        vertex = new_edge[1]
        if vertex not in accessed_in_steps:
            accessed_in_steps[i] = accessed_in_steps[i - 1] + 1
            accessed_nodes.add(vertex)
        else:
            accessed_in_steps[i] = accessed_in_steps[i - 1]
        if i >= window:
            if accessed_in_steps[i] - accessed_in_steps[i - window] <= tolerance:
                break
        community.add(vertex)
    return community


def clusters(G, steps, window, tolerance, threshold_similarity):
    communities = list()
    for node in G.nodes:
        community = restrained_walk(steps, window, tolerance, node, G)
        communities.append(community)

    modules = tools.join_similar_communities(threshold_similarity, communities, G)
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
    G = reader.create_graph('../graphs/g1.csv', True)

    start = time.time()
    modules = clusters(G, steps, window, tolerance, threshold_similarity)
    end = time.time()

    print('Nodes: ', G.number_of_nodes())
    print('Edges: ', G.number_of_edges())
    print('Clustering time: ', end - start)
    print('Number of clusters: ', len(modules))
    # nx.write_gexf(G, 'test.gexf')


main()
