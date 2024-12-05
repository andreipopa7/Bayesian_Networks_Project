from bayesian_network import BayesianNetwork, kahn_topological_sort

def main():
    filename = "test1_network.json"
    bayesian_network = BayesianNetwork(filename)

    graph = {node: bayesian_network.network[node]["parents"] for node in bayesian_network.network.keys()}

    sorted_nodes = kahn_topological_sort(graph)
    if sorted_nodes is None:
        print("Graful are un ciclu, sortarea topologică nu este posibilă!")
        return

    sorted_nodes.reverse()
    print(f"Ordinea topologică a nodurilor: {sorted_nodes}")

    evidence = {
        "Gripa": "Nu",
        "Abces": "Nu",
        "Anorexie": "Nu"
    }
    bayesian_network.set_evidence(evidence)

    print("\nNodurile retelei:")
    for node in bayesian_network.network.keys():
        print(f"  - {node}")

    query_node = "Oboseala"
    possible_values = bayesian_network.get_possible_values(query_node)
    print(f"\nValori posibile pentru '{query_node}': {possible_values}")

    print(f"\nInferenta pentru nodul '{query_node}':")
    query_result = bayesian_network.enumeration_ask(query_node)
    for value, probability in query_result.items():
        print(f"  {value}: {probability}")

if __name__ == "__main__":
    main()
