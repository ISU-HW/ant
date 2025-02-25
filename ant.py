import random
from graph import Graph

class AntOptimizer:
    def __init__(self, graph, n_ants, n_iterations, alpha=1, beta=2, evaporation_rate=0.5, pheromone_init=0.1):
        self.graph = graph
        self.nodes = list(graph.nodes.keys())
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.pheromones = {u: {v: pheromone_init for v in graph.get_neighbors(u)} for u in self.nodes}
        self.best_path = None
        self.best_path_length = float('inf')

    def run(self, start_node=None, hamiltonian=False):
        for iteration in range(self.n_iterations):
            paths, lengths = self._construct_solutions(start_node, hamiltonian)
            self._update_pheromones(paths, lengths)
            iteration_best_length = min(lengths)
            if iteration_best_length < self.best_path_length:
                self.best_path_length = iteration_best_length
                self.best_path = paths[lengths.index(iteration_best_length)]
            print(f"Iteration {iteration + 1}: Best length so far = {self.best_path_length}")
        return self.best_path, self.best_path_length

    def _construct_solutions(self, start_node, hamiltonian):
        paths = []
        lengths = []
        for _ in range(self.n_ants):
            path = self._construct_path(start_node, hamiltonian)
            length = self._calculate_path_length(path)
            paths.append(path)
            lengths.append(length)
        return paths, lengths

    def _construct_path(self, start_node, hamiltonian):
        start_node = start_node if start_node is not None else random.choice(self.nodes)
        path = [start_node]
        while len(path) < len(self.nodes):
            current_node = path[-1]
            next_node = self._choose_next_node(current_node, path)
            path.append(next_node)
        if hamiltonian:
            path.append(path[0])
        return path


    def _choose_next_node(self, current_node, visited):
        probabilities = []
        neighbors = self.graph.get_neighbors(current_node)
        for neighbor, weight in neighbors:
            if neighbor not in visited:
                pheromone = self.pheromones[current_node][(neighbor,weight)] ** self.alpha
                heuristic = (1 / weight) ** self.beta if weight != 0 else 0
                probabilities.append((neighbor, pheromone * heuristic))

        if not probabilities:
            unvisited = [node for node in self.nodes if node not in visited]
            return random.choice(unvisited)

        total = sum(prob for _, prob in probabilities)
        if total == 0:
            return random.choice([neighbor for neighbor, _ in neighbors if neighbor not in visited])

        probabilities = [(node, prob / total) for node, prob in probabilities]
        nodes, weights = zip(*probabilities)
        return random.choices(nodes, weights=weights, k=1)[0]

    def _calculate_path_length(self, path):
        length = 0
        for i in range(len(path) - 1):
            weight = self.graph.get_weight(path[i], path[i + 1])
            if weight is None:
                return float('inf')
            length += weight
        return length

    def _update_pheromones(self, paths, lengths):
        for u in self.pheromones:
            for v in self.pheromones[u]:
                self.pheromones[u][v] *= (1 - self.evaporation_rate)

        for path, length in zip(paths, lengths):
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                if v in self.pheromones[u]:
                    self.pheromones[u][(v, self.graph.get_weight(u, v))] += 1 / length


if __name__ == "__main__":
    gr = Graph()
    file = input("Введите имя файла с графом: ")
    with open(file, "r") as f:
        for line in f:
            u, v, weight = line.strip().split()
            gr.add_edge(u, v, float(weight))

    n_ants = 7
    n_iterations = 10

    print("=== Поиск кратчайшего пути для Коммивояжера ===")
    ant = AntOptimizer(gr, n_ants, n_iterations)
    shortest_path, shortest_length = ant.run(start_node=list(gr.nodes.keys())[0], hamiltonian=False)
    print("\n=== Поиск Гамильтонова цикла ===")
    hamiltonian_cycle, hamiltonian_length = ant.run(start_node=list(gr.nodes.keys())[0], hamiltonian=True)

    print("Кратчайший путь:", shortest_path)
    print("Длина пути:", shortest_length)

    print("Гамильтонов цикл:", hamiltonian_cycle)
    print("Длина цикла:", hamiltonian_length)
