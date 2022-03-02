def jaccard_similarity(A, B):
    nominator = A.intersection(B)
    denominator = A.union(B)
    jac_similarity = len(nominator) / len(denominator)
    return jac_similarity


def check_clusters(target_node1, target_node2, modules):
    module_index = 0
    # print(target_node1)
    # print(target_node2)
    # print(modules)
    for module in modules:
        if target_node1 in module or target_node2 in module:
            for k in range(len(modules)):
                if k != module_index:
                    if target_node1 in modules[k] or target_node2 in modules[k]:
                        return True, module_index, k
            return False, module_index, 0
        module_index += 1
    return False, -1, 0


def check_edge_clusters(target_edge1, target_edge2, modules):
    module_index = 0
    for module in modules:
        # print(module)
        for subset in module:
            # print(subset)
            if set(subset) == set(target_edge1) or set(subset) == set(target_edge2):
                return module_index
        module_index += 1
    return -1


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


def join_similar_communities(threshold_similarity, communities, G):
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


def common_edges(set1, set2):
    intersection = 0
    for edge in set1:
        if edge in set2:
            intersection += 2
    return intersection


def total_edges(set1, set2):
    union = len(set1) + len(set2)
    return union


def calculate_similarity(set1, set2):
    similarity = 0
    nominator = common_edges(set1, set2)
    denominator = total_edges(set1, set2)
    if denominator > 0:
        similarity = nominator / denominator
    return similarity


def join_edge_clusters(desired_similarity, clusters, G):
    joined_clusters = list(set(tuple()))
    for e1 in G.edges:
        # print('e1= ', e1)
        for e2 in G.edges:
            if e1 != e2:
                # print('e2= ', e2)
                # print('nbh1')
                # print(clusters[e1])
                # print('nbh2')
                # print(clusters[e2])
                score = calculate_similarity(clusters[e1], clusters[e2])
                # print(score)
                if score >= desired_similarity:
                    # print(score)
                    cluster = check_edge_clusters(e1, e2, joined_clusters)
                    # print('res=', cluster)
                    if cluster == -1:
                        joined_clusters.append({e1, e2})
                        continue
                    joined_clusters[cluster].add(e2)
                # print(joined_clusters)
    return joined_clusters