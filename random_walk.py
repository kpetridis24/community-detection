"""
Large graph clustering using random walkers
"""
import inc.reader as reader
import random
import time
from random import seed
from datetime import datetime
seed(datetime.now())


def jaccard_similarity(A, B):
    nominator = A.intersection(B)
    denominator = A.union(B)
    similarity = len(nominator) / len(denominator)
    return similarity


def random_walk(steps, vertex, G):
    community = set()
    for _ in range(steps):
        neighborhood = list(G.edges(vertex))
        new_edge = random.choice(neighborhood)
        vertex = new_edge[1]
        community.add(vertex)
    return community


def check_clusters(target_node1, target_node2, modules):
    module_index = 0
    for module in modules:
        if target_node1 in module or target_node2 in module:
            return module_index
        module_index = module_index + 1
    return -1


def clusters(G, steps, desired_similarity):
    communities = dict()
    for node in G.nodes:
        community = random_walk(steps, node, G)
        communities[node] = community

    C = list(set())
    for i in G.nodes:
        for j in G.nodes:
            if i < j:
                score = jaccard_similarity(communities[i], communities[j])
                if score >= desired_similarity:
                    cluster = check_clusters(i, j, C)
                    if cluster == -1:
                        C.append({i, j})
                        continue
                    C[cluster].add(j)
    return C


def main():
    steps = 50
    desired_similarity = 0.03
    G = reader.create_graph('g1.csv', True)

    start = time.time()
    modules = clusters(G, steps, desired_similarity)
    end = time.time()

    print('Nodes: ', G.number_of_nodes())
    print('Edges: ', G.number_of_edges())
    print('Clustering time: ', end - start)
    print('Number of clusters: ', len(modules))

    # nx.write_gexf(G, 'test.gexf')


main()
