from typing import TypedDict

class Node(TypedDict):
    # positive for power generation and negative for power consumption
    power: int
    name: string

class PowerLineOption(TypedDict):
    node1: Node
    node2: Node
    distance: int
    max_power: int

# Nodes A, B, C, D, E
nodes = {
    "A": Node(name="A", power=50),
    "B": Node(name="B",power=-30),
    "C": Node(name="C",power=20),
    "D": Node(name="D",power=-40),
    "E": Node(name="E",power=10),
}

edges ={
    frozenset({nodes["A"],nodes["B"]}): PowerLineOption(nodes=frozenset({nodes["A"],nodes["B"]}),distance=12,max_power=100),
    frozenset({nodes["B"],nodes["C"]}): PowerLineOption(nodes=frozenset({nodes["B"],nodes["C"]}),distance=20,max_power=80),
    frozenset({nodes["C"],nodes["D"]}): PowerLineOption(nodes=frozenset({nodes["C"],nodes["D"]}),distance=15,max_power=60),
    frozenset({nodes["D"],nodes["E"]}): PowerLineOption(nodes=frozenset({nodes["D"],nodes["E"]}),distance=25,max_power=110),
    frozenset({nodes["A"],nodes["E"]}): PowerLineOption(nodes=frozenset({nodes["A"],nodes["E"]}),distance=10,max_power=80),
}

COST_PER_DISTANCE = 5