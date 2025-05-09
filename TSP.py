#traveling salesman problem

import matplotlib.pyplot as plt
import networkx as nx
import math

cities	= {
'A': (0, 3),
'B': (7, 5),
'C': (1, 0),
'D': (4, 3),
'E': (7, 0),
'F': (5, 3),
'G': (2, 2),
'H': (3, 1)
}

G	= nx.Graph()
for city1	in cities:
    for city2	in cities:
        if city1	!= city2:
            x1, y1	= cities[city1]
            x2, y2	= cities[city2]
            dist = math.hypot(x2	- x1, y2	- y1)
            G.add_edge(city1, city2, weight=dist)
#	Step	1:	Build	MST
mst = nx.minimum_spanning_tree(G)
#	Step	2:	Find	nodes	with	odd	degree
odd_degree_nodes = [v	for v, d	in mst.degree() if d	% 2 == 1]
#	Step	3:	Add	minimum	weight	perfect	matching	on	odd	degree	nodes
matching	= nx.Graph()

for i in range(len(odd_degree_nodes)):
    for j	in range(i + 1, len(odd_degree_nodes)):
        u	= odd_degree_nodes[i]
        v	= odd_degree_nodes[j]
        matching.add_edge(u, v, weight=G[u][v]['weight'])
min_matching = nx.algorithms.matching.min_weight_matching(matching)
multi_graph = nx.MultiGraph(mst)
multi_graph.add_edges_from(min_matching)
#	Step	4:	Eulerian	circuit	and	shortcut	repeated	nodes
euler_circuit = list(nx.eulerian_circuit(multi_graph))
visited	= set()
path	= []
for u, v	in euler_circuit:
    if u	not in visited:
        path.append(u)
        visited.add(u)
    if v	not in visited:
        path.append(v)
        visited.add(v)
#	Return	to	start
path.append(path[0])
#	Calculate	total	distance
total_distance = sum(G[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))
#	Plot	the	result
plt.figure(figsize=(8, 6))
pos	= cities
nx.draw(G, pos, with_labels=True, node_size=700, font_weight='bold')
nx.draw_networkx_edges(G, pos, edgelist=[(path[i], path[i+1]) for i in
range(len(path)-1)], width=2, edge_color='r')
#	Annotate	total	distance
plt.title(f"Christofides Approximate	TSP	Tour\nTotal Distance	≈	{total_distance:.2f}")
plt.grid(True)
plt.show()