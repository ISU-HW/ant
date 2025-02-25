
class Node:
    def __init__(self, name):
        self.name = name
        self.edges = []

    def add_edge(self, neighbor, weight=1):
        if (neighbor, weight) not in self.edges:
            self.edges.append((neighbor, weight))

    def remove_edge(self, neighbor):
        self.edges = [edge for edge in self.edges if edge[0] != neighbor]

    def get_neighbors(self):
        return [(neighbor, weight) for neighbor, weight in self.edges]

    def get_weight(self, neighbor):
        for n, weight in self.edges:
            if n == neighbor:
                return weight
        return None

    def __str__(self):
        return f"Node({self.name}, Edges: {self.edges})"
