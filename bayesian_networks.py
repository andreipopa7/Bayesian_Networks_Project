#aici sunt algoritmii: Kahn, de numerare si greutate


#algoritmul lui Kahn care face sortarea topologica 
#functia asta primeste parametru un dictionar in care cheile sunt noduri si valorile sunt liste denoduri vecine
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

#algoritmul de ENUMERARE -- calculeaza recursiv probabilitati in retele Bayesiene
#are ca date de intrare: lista tuturor var. din retea,val. observate pt. anumite variabile si reteaua B. care e ca un dictionar
#functia returneaza o valoare tip procent
def enumerate_all(vars_list, evidence, network):
    if not vars_list:
        return 1.0

    first, *rest = vars_list
    if first in evidence:
        return probability(first, evidence, network) * enumerate_all(rest, evidence, network)
    else:
        total = 0
        for value in network[first]["values"]:
            extended_evidence = {**evidence, first: value}
            total += probability(first, extended_evidence, network) * enumerate_all(rest, extended_evidence, network)
        return total

#functia asta returneaza probabilitatea unei variabile pe baza evidentei in reteaua Bayesiana
#are ca date de intrare: variabila pt care calc. probailitatea, valorile observate si reteaua B.
#functia returneaza o valoare a probabilitatii
def probability(var, evidence, network):
    parents = network[var]["parents"]
    if not parents:
        return network[var]["probabilities"][evidence[var]]
    parent_values = tuple(evidence[parent] for parent in parents)
    return network[var]["probabilities"][parent_values][evidence[var]]

#functia asta face inferenta prin enumerare
#are ca parametrii: var. interogata, valorile observate, reteaua B.
#returneaza o distributie de probabilitate normalizata pt. variabila interogata
def enumeration_ask(query_var, evidence, network):
    q = {}
    for value in network[query_var]["values"]:
        extended_evidence = {**evidence, query_var: value}
        q[value] = enumerate_all(list(network.keys()), extended_evidence, network)
    total = sum(q.values())
    return {key: prob / total for key, prob in q.items()}



#algoritmul de GREUTATE (Likelihood Weighting) pt retele B.
import random



#functia asta face inferenta aproximativa folosind Greutati (Likelihood Weighting)
#are ca input: var. interogata, valorile observate, reteaua B., nr. de esantioane generate
# functia returneaza o distributie de probabilitate normalizata pentru variabila interogata
def likelihood_weighting(query_var, evidence, network, n_samples):
    weights = {value: 0 for value in network[query_var]["values"]}
    for _ in range(n_samples):
        sample, weight = weighted_sample(network, evidence)
        weights[sample[query_var]] += weight
    total = sum(weights.values())
    return {key: weight / total for key, weight in weights.items()}

#functia asta genereaza un esantion ponderat dintr-o retea B.
#are ca date de intrare: reteaua B. si valorile observate
#functia returneaza un esantion+greutatea corespunzatoare asociata
def weighted_sample(network, evidence):
    sample = {}
    weight = 1.0
    for var in network:
        if var in evidence:
            sample[var] = evidence[var]
            weight *= probability(var, evidence, network)
        else:
            probs = probability(var, sample, network)
            sample[var] = random.choices(list(probs.keys()), weights=list(probs.values()))[0]
    return sample, weight
