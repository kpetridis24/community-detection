def jaccard_similarity(A, B):
    nominator = A.intersection(B)
    denominator = A.union(B)
    jac_similarity = len(nominator) / len(denominator)
    return jac_similarity


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


def join_node_clusters(desired_similarity, clusters, G):
    joined_clusters = list(set())
    for i in G.nodes:
        for j in G.nodes:
            if i < j:
                # join, cluster, cluster2 = check_clusters(i, j, joined_clusters)
                # if cluster != -1:
                #     joined_clusters[cluster].add(j)
                #     joined_clusters[cluster].add(i)
                score = jaccard_similarity(clusters[i], clusters[j])
                if score >= desired_similarity:
                    join, cluster, cluster2 = check_clusters(i, j, joined_clusters)
                    if join:
                        print('now')
                        for value in joined_clusters[cluster2]:
                            joined_clusters[cluster].add(value)
                        # joined_clusters[cluster].add(joined_clusters[cluster2])
                        joined_clusters.pop(cluster2)
                        continue
                    print('cluster=', cluster)
                    print('size=', len(joined_clusters))
                    if cluster == -1:
                        joined_clusters.append({i, j})
                        continue
                    joined_clusters[cluster].add(j)
                    joined_clusters[cluster].add(i)
                # else:
                #     joined_clusters.append(clusters[i])
                #     joined_clusters.append(clusters[j])
    # i = 0
    # while True:
    #     for j in

    # for cluster1 in range(len(joined_clusters)):
    #     for cluster2 in range(len(joined_clusters)):
    #         if cluster1 < cluster2:
    #             if joined_clusters[cluster1].intersection(joined_clusters[cluster2]) > 0:


    # print(joined_clusters)
    return joined_clusters


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