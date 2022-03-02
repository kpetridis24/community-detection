"""
 Helper functions
"""

"""
 Calculates the similarity between to sets, following the formula: |intersection(A, B)| / |union(A, B)|.
"""
def jaccard_similarity(A, B):
    nominator = A.intersection(B)
    denominator = A.union(B)
    jac_similarity = len(nominator) / len(denominator)
    return jac_similarity


"""
 Given a cluster containing sub-clusters, checks if there is a pair of sub-clusters that are similar. If 
 there is one, it returns the corresponding indices, otherwise it returns -1.
"""
def similar_clusters(threshold_similarity, modules):
    for i in range(len(modules)):
        for j in range(len(modules)):
            if i < j:
                if jaccard_similarity(modules[i], modules[j]) >= threshold_similarity:
                    return i, j
    return -1, -1


"""
 Given a cluster containing sub-clusters, joins two similar clusters in the following manner:
    1. If neither of them has already been joined with another sub-cluster in a previous iteration,
       joins the two and appends the new sub-cluster as a separate entry inside the cluster.
    2. If one of them already belongs to another cluster, adds the remaining one to that cluster as
       well.
    3. In both previous cases, the array indicating whether a sub-cluster has been joined with another
       cluster, is updated appropriately.
"""
def join(community_index1, community_index2, community1, community2, cluster_of, modules):
    if cluster_of[community_index1] == -1 and cluster_of[community_index2] == -1:
        new_module = community1.union(community2)
        modules.append(new_module)
        cluster_of[community_index1] = len(modules) - 1
        cluster_of[community_index2] = len(modules) - 1
    elif cluster_of[community_index1] != -1:
        modules[cluster_of[community_index1]].update(community2)
        cluster_of[community_index2] = cluster_of[community_index1]
    else:
        modules[cluster_of[community_index2]].update(community1)
        cluster_of[community_index1] = cluster_of[community_index2]
    return modules, cluster_of


"""
 Given N sets (sets of nodes accessed by the walker, for every node), performs the inital join between sets
 whose similarity exceeds the specified threshold. In the end, sets that were not joined with any other set
 are appended into created structure.
"""
def join_similar_communities(threshold_similarity, communities):
    cluster_of = [-1 for _ in range(len(communities))]
    modules = list(set())
    community_index1 = 0

    for community1 in communities:
        community_index2 = 0
        for community2 in communities:
            if community_index1 < community_index2:
                similarity = jaccard_similarity(community1, community2)
                if similarity >= threshold_similarity:
                    modules, cluster_of = join(community_index1, community_index2,
                                               community1, community2, cluster_of, modules)
            community_index2 += 1
        community_index1 += 1

    for index in range(len(cluster_of)):
        if cluster_of[index] == -1:
            modules.append(communities[index])

    return modules