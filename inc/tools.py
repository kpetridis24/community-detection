def jaccard_similarity(A, B):
    nominator = A.intersection(B)
    denominator = A.union(B)
    jac_similarity = len(nominator) / len(denominator)
    return jac_similarity


def similar_clusters(threshold_similarity, modules):
    for i in range(len(modules)):
        for j in range(len(modules)):
            if i < j:
                if jaccard_similarity(modules[i], modules[j]) >= threshold_similarity:
                    return i, j
    return -1, -1


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