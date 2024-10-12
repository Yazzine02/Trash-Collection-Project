import itertools

infinity = 99999


def HamiltonianCycle(graph, nb_nodes, start):
    nodes = list(range(nb_nodes))
    all_permutations = itertools.permutations(nodes)
    min_cost = infinity
    min_path = tuple()
    for permutation in all_permutations:
        cost = 0
        for i in range(nb_nodes-1):
            node = permutation[i]
            next_node = permutation[(i + 1)]  # Wrap around to the start if at the end
            cost += graph[node][next_node]
        if cost < min_cost:
            min_cost = cost
            min_path = permutation
    return min_path, min_cost
