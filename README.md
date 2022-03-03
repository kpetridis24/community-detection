# network-clustering

Undirected network community detection via optimization of the modularity quality function. We provide three (3) separate methods for network clustering. The clusters are
created such that, they contain vertices with high connectivity between each other, but less connectivity between them and the vertices located in another cluster. The 
quality of the partitions detected, is determined by the [modularity quality function](https://en.wikipedia.org/wiki/Modularity_(networks)). The implementation utilizes
walkers in order to optimize the modularity of each cluster, based on its definition.

**Random walkers**

The first method uses random walkers to access a set of vertices, during a m-step walk, starting from an initial vertex. At step k, the walker is located at vertex v(k)
and arbitrarily picks one of its neighbors as the next vertex. Each possible choice has the probability of 1/d(k), where d(k) is the degree of vertex v(k).


**Restrained walkers**

The second method emerges from an observation on method-1. Each walk can be divided in three separate stages. During the first stage, almost every node the walker accesses,
hasn't already been accessed, which both makes theoretical sense and agrees with the practical analysis and testing. The second stage is when most of the nodes inside the
initial community have been accessed, so now the walker re-iterates over the same set of nodes for a second time. Eventually, the walker starts moving towards a different 
community, during the third and final stage. After producing a mathematical representation of the above mentioned behavior, we are able to terminate each walk, before entering
the third stage, entraping it inside the two initial stages, which results is optimal clustering effect.


**Link-node-link walk**

In the third and final version, we form cluster containing edges instead of nodes. In order to accomplish that, a m-step link-node-link walk is performed in the following
manner. Given a starting edge e, the walker randomly picks one of its two incident nodes (extremities of the edge). After that, the next edge is arbitrarily picked from the 
node's neighboring edges. Repeating this process, we get a set of edges for every edge of the graph.


**Joining of clusters**

The output of all methods, is N sets of elements (nodes or edges), where N is the number of graph's nodes or edges, depending on the method used. Considering the [Jaccard Similarity](https://en.wikipedia.org/wiki/Jaccard_index) as the metric of comparing the similarity between any pair of communities, we join every pair of communities A, B
if SIMILARITY(A, B) > t, where t is a pre-defined similarity threshold. This joining is done recursively until there is no pair of clusters, whose similarity exceeds the 
required threshold.


