import itertools

infinity = 99999


def HamiltonianCycle(graph, nb_nodes, start):
  nodes = []
  for i in range(nb_nodes):
    if i != start:
      nodes.append(i)
  all_combinations = itertools.permutations(nodes)
  min_cost = infinity
  min_path = ()
  for permutation in all_combinations:
    k = start
    cost = 0
    for node in permutation:
      cost += graph[k][node]
      k = node
    cost += graph[k][start]
    if cost < min_cost:
      min_cost = cost
      min_path =(start,) + permutation
  return min_path

