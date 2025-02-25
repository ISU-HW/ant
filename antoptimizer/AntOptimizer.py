import random


class AntOptimizer:
    def __init__(
        self,
        graph,
        n_ants,
        n_iterations,
        alpha=1,
        beta=2,
        evaporation_rate=0.5,
        pheromone_init=0.1,
    ):
        self.graph = graph
        self.nodes = list(graph.nodes.keys())
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.pheromones = {
            u: {(v, weight): pheromone_init for v, weight in graph.get_neighbors(u)}
            for u in self.nodes
        }
        self.best_path = None
        self.best_path_length = float("inf")

    """Искать кратчайший гамильтонов цикл в графе от стартовой вершины."""

    def find_hamiltonian_cycle(self, start_node=None):
        # sourcery skip: use-named-expression
        self.best_path = None
        self.best_path_length = float("inf")

        valid_cycle_found = False

        for iteration in range(self.n_iterations):
            paths, lengths = self._construct_solutions(start_node, is_cycle=True)

            valid_paths = [
                (path, length)
                for path, length in zip(paths, lengths)
                if path is not None and length < float("inf")
            ]

            if valid_paths:
                valid_cycle_found = True
                valid_paths.sort(key=lambda x: x[1])  # Сортировка по длине
                current_best_path, current_best_length = valid_paths[0]

                if current_best_length < self.best_path_length:
                    self.best_path_length = current_best_length
                    self.best_path = current_best_path

                self._update_pheromones(
                    [path for path, _ in valid_paths],
                    [length for _, length in valid_paths],
                )

                print(
                    f"Итерация {iteration + 1}: Лучшая длина = {self.best_path_length}"
                )
            else:
                print(f"Итерация {iteration + 1}: Гамильтонов цикл не найден")

        if not valid_cycle_found:
            print("Не удалось найти гамильтонов цикл в этом графе.")
            return None, float("inf")

        return self.best_path, self.best_path_length

    def _construct_solutions(self, start_node, is_cycle):
        paths = []
        lengths = []
        for _ in range(self.n_ants):
            path = self._construct_path(start_node, is_cycle)
            length = self._calculate_path_length(path)
            paths.append(path)
            lengths.append(length)
        return paths, lengths

    """Построить путь через все вершины от стартовой вершины."""

    def _construct_path(self, start_node, is_cycle):
        start_node = start_node if start_node is not None else random.choice(self.nodes)
        path = [start_node]
        visited = set(start_node)

        while len(visited) < len(self.nodes):
            current_node = path[-1]
            next_node = self._choose_next_node(current_node, visited)

            if next_node is None:
                return None

            path.append(next_node)
            visited.add(next_node)

        if is_cycle:
            if self.graph.is_adjacent(path[-1], path[0]):
                path.append(path[0])
            else:
                # Нельзя замкнуть цикл - недопустимый путь
                return None

        return path

    def _choose_next_node(self, current_node, visited):
        probabilities = []
        neighbors = self.graph.get_neighbors(current_node)

        # Собирать только непосещенные соседние вершины
        for neighbor, weight in neighbors:
            if neighbor not in visited:
                key = (neighbor, weight)
                if key in self.pheromones[current_node]:
                    pheromone = self.pheromones[current_node][key] ** self.alpha
                    heuristic = (1 / weight) ** self.beta if weight != 0 else 0
                    probabilities.append((neighbor, pheromone * heuristic))

        # Если нет соседних непосещенных вершин нельзя продолжить путь
        if not probabilities:
            return None

        total = sum(prob for _, prob in probabilities)
        if total == 0:
            # Выбрать случайную непосещенную соседнюю вершину
            unvisited_neighbors = [
                neighbor for neighbor, _ in neighbors if neighbor not in visited
            ]
            return random.choice(unvisited_neighbors) if unvisited_neighbors else None

        # Выбирать вершину на основе вероятностей
        probabilities = [(node, prob / total) for node, prob in probabilities]
        nodes, weights = zip(*probabilities)
        return random.choices(nodes, weights=weights, k=1)[0]

    def _calculate_path_length(self, path):
        if path is None:
            return float("inf")  # Недопустимый путь имеет бесконечную длину

        length = 0
        for i in range(len(path) - 1):
            weight = self.graph.get_weight(path[i], path[i + 1])
            if weight is None:
                return float("inf")  # Ребро не существует
            length += weight
        return length

    def _update_pheromones(self, paths, lengths):
        # Испарение феромонов на всех рёбрах
        for u in self.pheromones:
            for v in self.pheromones[u]:
                self.pheromones[u][v] *= 1 - self.evaporation_rate

        # Добавление феромонов на пройденные рёбра
        for path, length in zip(paths, lengths):
            if length == float("inf"):
                continue

            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                weight = self.graph.get_weight(u, v)
                if weight is not None:
                    key = (v, weight)
                    if key in self.pheromones[u]:
                        self.pheromones[u][key] += 1 / length
