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


def clusters(G, steps, window, tolerance, desired_similarity):
    communities = dict()
    for node in G.nodes:
        community = restrained_walk(steps, window, tolerance, node, G)
        communities[node] = community

    communities = tools.join_node_clusters(desired_similarity, communities, G)
    return communities


def main():
    steps = 50
    window = 6
    tolerance = 5
    desired_similarity = 0.03
    G = reader.create_graph('../graphs/g1.csv', True)

    start = time.time()
    modules = clusters(G, steps, window, tolerance, desired_similarity)
    end = time.time()

    print('Nodes: ', G.number_of_nodes())
    print('Edges: ', G.number_of_edges())
    print('Clustering time: ', end - start)
    print('Number of clusters: ', len(modules))

    # nx.write_gexf(G, 'test.gexf')


main()
