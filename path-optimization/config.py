from typing import TypedDict

class Node(TypedDict):
    # positive for power generation and negative for power consumption
    power: int

class PowerLineOption(TypedDict):
    node1: Node
    node2: Node
    distance: int
    max_power: int

# Nodes A, B, C, D, E
nodes = {
    "A": Node(power=50),
    "B": Node(power=-30),
    "C": Node(power=20),
    "D": Node(power=-40),
    "E": Node(power=10),
}

edges = {
    "AB": PowerLineOption(node1=nodes["A"], node2=nodes["B"], distance=10, max_power=100),
    "BC": PowerLineOption(node1=nodes["B"], node2=nodes["C"], distance=20, max_power=150),
    "CD": PowerLineOption(node1=nodes["C"], node2=nodes["D"], distance=15, max_power=120),
    "DE": PowerLineOption(node1=nodes["D"], node2=nodes["E"], distance=25, max_power=200),
    "AE": PowerLineOption(node1=nodes["A"], node2=nodes["E"], distance=30, max_power=180),
}

COST_PER_DISTANCE = 5