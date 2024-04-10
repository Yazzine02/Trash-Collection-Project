import itertools

infinity=99999


def FloydWarshall(nb_nodes,graph):
    distance_matrix=list(graph)
    for k in range(nb_nodes):
        for i in range(nb_nodes):
            for j in range(nb_nodes):
                distance_matrix[i][j]=min(distance_matrix[i][j],distance_matrix[i][k]+distance_matrix[k][j])
    return distance_matrix


def BruteForce(nb_nodes,graph):
    combinations = itertools.permutations(range(nb_nodes))
    final_cost = infinity
    final_path = ()
    shortest_distance_matrix=FloydWarshall(4,graph)
    for combination in combinations:
        cost=0
        previous_node=combination[0]
        for node in combination:
            cost+=shortest_distance_matrix[previous_node][node]
            previous_node=node
        if cost<final_cost:
            final_cost=cost
            final_path=combination
    return final_path

def FloydWarshall_BruteForce(graph,nb_nodes):
    distance_matrix=FloydWarshall(nb_nodes,graph)
    path=BruteForce(nb_nodes,distance_matrix)
    return path