from typing import TypedDict
from sympy import symbols, Matrix, eye

class Node(TypedDict):
    # positive for power generation and negative for power consumption
    name: str
    power: int

    def __init__(self, power):
        self.power = power

class PowerLineOption(TypedDict):
    nodes: frozenset[Node]
    distance: int
    max_power: int

    def __init__(self, node1, node2, distance, max_power):
        self.nodes = frozenset({node1, node2})
        self.distance = distance
        self.max_power = max_power

# Nodes A, B, C, D, E
nodes_array = [Node(name="A", power=50), Node(name="B", power=-30), Node(name="C", power=20), Node(name="D", power=-40), Node(name="E", power=10)]
node_names_array = [node.name for node in nodes_array]

edges_array = [
    PowerLineOption(nodes=frozenset([nodes_array[0], nodes_array[1]]), distance=10, max_power=100),  # AB
    PowerLineOption(nodes=frozenset([nodes_array[1], nodes_array[2]]), distance=20, max_power=150),  # BC
    PowerLineOption(nodes=frozenset([nodes_array[2], nodes_array[3]]), distance=15, max_power=120),  # CD
    PowerLineOption(nodes=frozenset([nodes_array[3], nodes_array[4]]), distance=25, max_power=200),  # DE
    PowerLineOption(nodes=frozenset([nodes_array[0], nodes_array[4]]), distance=30, max_power=180),  # AE
]

def concatenate_names(fset: frozenset) -> str:
    # Extract the objects, sort them by their `name` field, and concatenate the names
    sorted_names = sorted([obj["name"] for obj in fset])
    return "".join(sorted_names)

edge_names = [concatenate_names(pl.nodes) for pl in edges_array]
edge_symbols = symbols(" ".join(edge_names))

COST_PER_DISTANCE = 5
