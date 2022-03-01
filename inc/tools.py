def jaccard_similarity(A, B):
    nominator = A.intersection(B)
    denominator = A.union(B)
    similarity = len(nominator) / len(denominator)
    return similarity


def check_clusters(target_node1, target_node2, modules):
    module_index = 0
    for module in modules:
        if target_node1 in module or target_node2 in module:
            return module_index
        module_index = module_index + 1
    return -1