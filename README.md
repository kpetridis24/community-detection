# network-clustering

Undirected network community detection via optimization of the modularity quality function. We provide three (3) separate methods for network clustering. The clusters are
created such that, they contain vertices with high connectivity between each other, but less connectivity between them and the vertices located in another cluster. The 
quality of the partitions detected, is determined by the (modularity quality function)[https://en.wikipedia.org/wiki/Modularity_(networks)]. The implementation utilizes
walkers in order to optimize the modularity of each cluster, based on its definition.

**Random walkers**

The first method uses random walkers to access a set of vertices, during a m-step walk, starting from an initial vertex. At step k, the walker is located in vertex v_k
