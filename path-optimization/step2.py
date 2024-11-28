from sympy import symbols

# Relabeling the edges
edge_labels = {edge: symbols(f"e{i+1}") for i, edge in enumerate(edges.keys())}

#Calculating the cost for each edge
edge_costs = {}
for edge, attrs in edges.items():
    edge_variable = edge_labels[edge]
    distance = attrs['distance']
    cost = COST_PER_DISTANCE * distance
    edge_costs[str(edge_variable)] = cost

#output of the resulting dictionary
print("Edge Costs:")
print(edge_costs)
