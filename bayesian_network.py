import json

"""
Clasa BayesianNetwork se ocupa ce gestionarea unei retele
bayesiene incarcata dintr-un fisier JSON
"""
class BayesianNetwork:
    def __init__(self, filename):
        """
        Constructorul clasei BayesianNetwork
        Functie care incarca reteaua beyesiana dintr-un fisier JSON
        :param filename: numele fisierului JSON
        """
        self.evidence = {}
        with open(filename, 'r') as file:
            self.network = json.load(file)["nodes"]

    def set_evidence(self, evidence):
        """
        Functie care seteaza evidentele (nodurile observate) pentru calcul
        :param evidence: un dictionar de perechi nod:valoare
        """
        self.evidence = evidence

    def get_possible_values(self, node):
        """
        Functie care preia valorile posibile pentru un nod din retea, pe baza tabelelor de probabilitate
        :param node: numele nodului din retea
        :return: returneaza o lista de valori posibile pentru un nod din retea
        """
        probabilities = self.network[node]["probabilities"]
        # se verifica structura tabelelor de probabilitate:
        # daca sunt probabilitati conditionate, se extrag cheile
        # daca sunt marginale, se extrag direct cheile
        if isinstance(next(iter(probabilities.values())), dict):
            return list(next(iter(probabilities.values())).keys())
        else:
            return list(probabilities.keys())

    def enumeration_ask(self, query_node):
        """
        Functie care se ocupa de inferenta prin enumerare
        :param query_node: nodul interogat
        :return: o distributie de probabilitate normalizata pt. variabila interogata
        """
        # o lista a tuturor variabilelelor din retea
        variables = list(self.network.keys())
        query_probs = {}

        # se obtin toate valorile pentru nodul interogat si se calculeaza probabilitatile acestora
        possible_values = self.get_possible_values(query_node)
        for value in possible_values:
            query_probs[value] = self.enumerate_all(variables, {**self.evidence, query_node: value})

        # se normalizeaza probabilitatile pentru a asigura ca au suma 1
        alpha = sum(query_probs.values())
        for k in query_probs:
            query_probs[k] /= alpha

        # se rotunjesc rezultatele la 4 zecimale
        query_probs = {k: round(v, 4) for k, v in query_probs.items()}

        return query_probs

    # Algoritmul de Enumerare pentru Retele Bayesiene
    def enumerate_all(self, nodes_list, evidence):
        """
        Functie care calculeaza recursiv probabilitati in retele Bayesiene
        :param: nodes_list: lista tuturor nodurilor din retea
                evidence: nodurile observate
        :return: o valoare tip procent
        """
        if not nodes_list:
            # daca nu exista noduri in retea se returneaza 1
            return 1.0

        # se ia primul nod din lista
        first, *rest = nodes_list

        if first in evidence:
            # daca nodul este cunoscut, se calculeaza probabilitatea pentru aceasta
            prob = self.probability(first, evidence)
            # apoi se continua procesarea urmatoarelor variabile recursiv
            return prob * self.enumerate_all(rest, evidence)
        else:
            # daca nodul nu este cunoscut, se calculeaza suma probabilitatilor
            total = 0
            possible_values = self.get_possible_values(first)
            for value in possible_values:
                # se aduna probabilitateaa pentru fiecare nod posibil
                total += self.probability(first, {**evidence, first: value}) * self.enumerate_all(
                    rest, {**evidence, first: value})
            return total

    def probability(self, node, evidence):
        """
        Functie care calculeaza probabilitatea unei variabile pe baza evidentei in reteaua Bayesiana
        :param: variabila pt care calc. probailitatea, valorile observate si reteaua B.
        :return: o valoare a probabilitatii
        """
        node_data = self.network[node]
        parents = node_data["parents"]

        if not parents:
            # daca nodul nu are parinti se folosesc direct cheile
            return node_data["probabilities"][evidence[node]]

        # daca nodul are parinti se folosesc valorile conditionate
        parent_values = ",".join(evidence[parent] for parent in parents)
        return node_data["probabilities"][parent_values][evidence[node]]

    def p_e_query(self, evidence):
        """
        Functie care calculeaza probabilitatea evidentelor P(E=e) pe baza retelei bayesiene.
        :param evidence: nodurile observate
        :return: probabilitatea evidentelor curente
        """
        all_variables = list(self.network.keys())
        return self.enumerate_all(all_variables, evidence)


#algoritmul lui Kahn care face sortarea topologica
#functie care  primeste parametru un dictionar in care cheile sunt noduri si valorile sunt liste denoduri vecine
#functia asta returneaza o lista cu noduri sortate topologic sau valoarea"none" daca am ciclu in graf
def kahn_topological_sort(graph):
    #initializez SD
    in_degree = {node: 0 for node in graph}
    for neighbors in graph.values():
        for neighbor in neighbors:
            in_degree[neighbor] += 1

    #incep cu nodurile care nu au muchii de intrare
    s = [node for node, degree in in_degree.items() if degree == 0]
    l = []

    while s:
        n = s.pop(0)
        l.append(n)
        for m in graph.get(n, []):
            in_degree[m] -= 1
            if in_degree[m] == 0:
                s.append(m)

    #cazul cand graful are mai are muchii => are un ciclu
    if any(degree > 0 for degree in in_degree.values()):
        return None
    return l


