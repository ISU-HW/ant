from graph.node import Node


class Graph:
    def __init__(self, is_oriented=False):
        self.nodes = {}
        self.is_oriented = is_oriented

    def add_vertex(self, name):
        if name not in self.nodes:
            self.nodes[name] = Node(name)

    def remove_vertex(self, name):
        if name in self.nodes:
            for node in self.nodes.values():
                node.remove_edge(name)
            del self.nodes[name]

    def add_edge(self, u, v, weight=1):
        self.add_vertex(u)
        self.add_vertex(v)
        self.nodes[u].add_edge(v, weight)
        if not self.is_oriented:
            self.nodes[v].add_edge(u, weight)

    def remove_edge(self, u, v):
        if u in self.nodes:
            self.nodes[u].remove_edge(v)
        if not self.is_oriented and v in self.nodes:
            self.nodes[v].remove_edge(u)

    def get_neighbors(self, name):
        if name in self.nodes:
            return self.nodes[name].get_neighbors()
        return []

    def get_weight(self, u, v):
        if u in self.nodes:
            return self.nodes[u].get_weight(v)
        return None

    def is_adjacent(self, u, v):
        for neigbor, weight in self.get_neighbors(u):
            if neigbor == v:
                return True
        return False

    def __str__(self):
        result = ""
        for node in self.nodes.values():
            result += f"{node}\n"
        return result