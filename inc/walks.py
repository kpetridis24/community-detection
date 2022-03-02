from random import seed
from datetime import datetime
import random
seed(datetime.now())

"""
 Performs a m-step walk starting from the specified vertex and returns the set of nodes accessed during 
 the walk. The walk is performed in a node-node fashion. Each next node is selected arbitrarily from the
 neighborhood of the previous node.
"""
def node_node(steps, vertex, G):
    community = set()
    for _ in range(steps):
        neighborhood = list(G.edges(vertex))
        new_edge = random.choice(neighborhood)
        vertex = new_edge[1]
        community.add(vertex)
    return community


"""
 Performs a m-step walk starting from the specified vertex and returns the set of nodes accessed during 
 the walk. The walk is performed in a node-node fashion but this time it is restrained. Each next node is 
 selected arbitrarily from the neighborhood of the previous node. The process terminates when the walker
 has already accessed most of the nodes inside the initial community, and starts moving towards another one.
"""
def node_node_restrained(steps, window, tolerance, vertex, G):
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


"""
 Performs a m-step walk starting from the specified edge and returns the set of edges accessed during 
 the walk. The walk is performed in a node-link-node fashion. Starting from the initial edge, one of 
 its two extremities (two nodes per edge) is picked arbitrarily. After this, we pick one of the edges, 
 incident to this node and continue the same process.
"""
def link_node_link(steps, edge, G):
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