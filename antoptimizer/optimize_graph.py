from graph import Graph
import antoptimizer

def optimize(graph_file, n_ants=1, n_iterations=9):
    gr = Graph()

    with open(graph_file, "r") as f:
        f.readline()
        for line in f:
            u, v, weight = line.strip().split()
            gr.add_edge(u, v, float(weight))

    ant = antoptimizer.AntOptimizer(gr, n_ants, n_iterations)

    print("\n=== Поиск кратчайшего гамильтонова цикла ===")
    hamiltonian_cycle, hamiltonian_length = ant.find_hamiltonian_cycle(
        start_node=list(gr.nodes.keys())[0]
    )

    print("Гамильтонов цикл:", hamiltonian_cycle)
    print("Длина цикла:", hamiltonian_length)


if __name__ == "__main__":
    optimize(input("Введите имя файла с графом: "))
