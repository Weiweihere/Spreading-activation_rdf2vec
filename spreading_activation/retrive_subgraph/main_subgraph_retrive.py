import rdflib
import networkx as nx
import json
from rdflib import Graph, URIRef
from tqdm import tqdm
import time


start_time = time.time()
# Initialize an RDF graph
g = rdflib.Graph()

# Parse the TTL file
g.parse("mappingbased-objects_lang=en.ttl", format="ttl")
# g.parse("testing_coverage/example.ttl", format="ttl")

# Convert RDF graph to a NetworkX graph
G = nx.MultiDiGraph()  # Use DiGraph for directed graph

for s, p, o in g:
    G.add_edge(str(s), str(o), predicate=str(p))

# Check if graph is created successfully
print("the ttl file have been loaded successfully, below is the basic information")
print(nx.info(G))

# print("\nNodes in the ttl graph:")
# for node in G.nodes():
    # print(node)
# 
# print("\nEdges in the graph:")
# for s, o, data in G.edges(data=True):
    # print(f"{s} -> {o}, predicate: {data['predicate']}")

# Load interesting nodes
# with open('testing_coverage/activated_nodes_example.txt', 'r') as file:
    # activated_nodes = json.load(file)

with open("/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/second_round_filter_node/activated_nodes_Album_DBpedia_URI15_20241212_130915_29_1.txt", 'r') as file:
    activated_nodes = json.load(file)
# "/pfs/work7/workspace/scratch/ma_wezhu-spreading/activated_nodes/095_1_nodes/second_round/activated_nodes_20240725_170905_99_1.txt--LP50"
# /pfs/work7/workspace/scratch/ma_wezhu-spreading/activated_nodes/095_1_nodes/second_round/activated_nodes_20240726_175056_99_1.txt KORE
# "/pfs/data5/home/ma/ma_ma/ma_wezhu/jRDF2Vec/examples/jupyter_notebook/walks/testing/newfolder_withisolatednodes/walk_cities_baseline/walk_file_0_unique_rdf_nodes.txt"
# activated_nodes_20240723_111551_99_1.txt --album
# activated_nodes_20240722_110544_27_1.txt --movie
# activated_nodes_20240715_171549_15_1.txt -AAUP
# activated_nodes_20240712_190801_30_1v2.txt --Forbes
# activated_nodes_20240706_000217_14_1.txt KORE
# "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/second_round/activated_nodes_KORE_sorted_20241020_191949.txt"
# old one: /pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/095_1_nodes/activated_nodes_20240706_000217_14_1.txt
# "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/095_1_nodes/second_round/activated_nodes_20240725_170905_99_1.txt"这个是老的，没有包含一些点
# /pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/095_1_nodes/second_round/activated_nodes_KORE_sorted_20241020_191949_70_1.txt"

interesting_nodes = set(activated_nodes.keys())
print(f"Number of activated nodes: {len(interesting_nodes)}")

subG = G.subgraph(interesting_nodes)
print("Subgraph information:")
print(nx.info(subG))

# print("\nNodes in the subgraph:")
# for node in subG.nodes():
    # print(node)
# 
# Print all edges in the subgraph
# print("\nEdges in the subgraph:")
# for s, o, data in subG.edges(data=True):
    # print(f"{s} -> {o}, predicate: {data['predicate']}")

# Verify all interesting nodes are in the subgraph
# missing_nodes = interesting_nodes - set(subG.nodes)
# if missing_nodes:
    # print(f"Missing nodes in the subgraph: {missing_nodes}")
# else:
    # print("All interesting nodes are included in the subgraph.")
# 
# node8 = "http://example.org/node8"
# if node8 in subG.nodes():
    # print(f"{node8} is included in the subgraph.")
# else:
    # print(f"{node8} is not included in the subgraph.")
# 
# Get the first 5 edges in the subgraph
first_5_edges = list(subG.edges())[:5]
# 
# Print the first 5 edges
for s, o in first_5_edges:
    print(f"{s} -> {o}")
# 
# Create an empty rdflib Graph
g_rdf = Graph()

for node in subG.nodes():
    g_rdf.add((URIRef(node), URIRef("rdf:type"), URIRef("owl:Thing")))

# Add all nodes to the rdflib Graph with inferred types
# for node in subG.nodes():
    # node_uri = URIRef(node)
    # node_type = None
    # 
    # Check if the node has a type in the original RDF graph
    # for s, p, o in g.triples((node_uri, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), None)):
        # node_type = o
        # break
    # 
    # if node_type:
        # g_rdf.add((node_uri, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), node_type))
    # else:
        # g_rdf.add((node_uri, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef("foaf:Thing")))  # Default type
# 
# Iterate over the edges in the NetworkX subgraph
for s, o, data in tqdm(subG.edges(data=True), desc="Processing edges"):
    # Add the edge to the rdflib Graph as a triple
    g_rdf.add((URIRef(s), URIRef(data['predicate']), URIRef(o)))
    

# Serialize the rdflib Graph to a TTL file
# g_rdf.serialize(destination='baseline_subgraph/movies_baseline_subgraph.ttl', format='turtle')
g_rdf.serialize(destination='subgraph_withnodes/SA_standard_subgraph/album_0728k.ttl', format='turtle')

total_time = time.time() - start_time
print(f"Total time taken: {total_time:.2f} seconds")



