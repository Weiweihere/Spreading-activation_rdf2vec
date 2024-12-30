import rdflib
import networkx as nx
import json
from rdflib import Graph, URIRef
from tqdm import tqdm
import time
import os

start_time = time.time()

# Initialize an RDF graph
g = rdflib.Graph()

# Parse the TTL file
g.parse("mappingbased-objects_lang=en.ttl", format="ttl")

# Convert RDF graph to a NetworkX graph
G = nx.MultiDiGraph()
for s, p, o in g:
    G.add_edge(str(s), str(o), predicate=str(p))

print("The TTL file has been loaded successfully, below is the basic information")
print(nx.info(G))

# Directory where the activated_nodes files are stored
# activated_nodes_dir = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/second_round_filter_node"

# List of activated nodes files to process
# activated_nodes_files = [
    # "activated_nodes_20240715_171549_AAUP_29_1.txt",
    # "activated_nodes_20240722_110544_movies_29_1.txt",
    # "activated_nodes_Album_DBpedia_URI15_20241212_130915_29_1.txt",
    # "activated_nodes_KORE_sorted_20241212_002826_29_1.txt",
    # "activated_nodes_LP50_20241212_171104_29_1.txt"
# ]

input_dirs = [
    "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/fixiteration_round_FT_0.5_2_filtered_29_1/",
    "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/fixiteration_round_FT_0.7_2_filtered_29_1/"
]

# Output directory
# output_dir = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/SA_standard_0.5_0.7_subgraph"
output_dirs = [
    "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/SA_standard_0.5_subgraph/",
    "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/SA_standard_0.7_subgraph/"
]
# os.makedirs(output_dir, exist_ok=True)

# Process each file


for input_dir, output_dir in zip(input_dirs, output_dirs):
    os.makedirs(output_dir, exist_ok=True)
    activated_nodes_files = [f for f in os.listdir(input_dir) if f.startswith("activated_nodes")]
    
    for file_name in activated_nodes_files:
        file_path = os.path.join(input_dir, file_name)
        
        # Load activated nodes
        with open(file_path, 'r') as file:
            activated_nodes = json.load(file)

        interesting_nodes = set(activated_nodes.keys())
        print(f"\nProcessing {file_name}")
        print(f"Number of activated nodes: {len(interesting_nodes)}")

        subG = G.subgraph(interesting_nodes)
        print("Subgraph information:")
        print(nx.info(subG))

        # Print the first 5 edges in the subgraph
        first_5_edges = list(subG.edges())[:5]
        for s, o in first_5_edges:
            print(f"{s} -> {o}")

        # Create an empty rdflib Graph
        g_rdf = Graph()

        # Assign a generic type to each node
        for node in subG.nodes():
            g_rdf.add((URIRef(node), URIRef("rdf:type"), URIRef("owl:Thing")))

        # Add edges to the RDF graph
        for s, o, data in tqdm(subG.edges(data=True), desc=f"Processing edges for {file_name}"):
            g_rdf.add((URIRef(s), URIRef(data['predicate']), URIRef(o)))

        # Construct output file name
        output_file_name = f"{os.path.splitext(file_name)[0]}_subgraph.ttl"
        output_path = os.path.join(output_dir, output_file_name)

        # Serialize the rdflib Graph to a TTL file
        g_rdf.serialize(destination=output_path, format='turtle')
        print(f"Subgraph saved to {output_path}")

Total_time = time.time() - start_time
print(f"Total time taken: {Total_time:.2f} seconds")

""" for file_name in activated_nodes_files: """
"""     file_path = os.path.join(activated_nodes_dir, file_name) """
"""      """
"""     # Load activated nodes """
"""     with open(file_path, 'r') as file: """
"""         activated_nodes = json.load(file) """
"""  """
"""     interesting_nodes = set(activated_nodes.keys()) """
"""     print(f"\nProcessing {file_name}") """
"""     print(f"Number of activated nodes: {len(interesting_nodes)}") """
"""  """
"""     subG = G.subgraph(interesting_nodes) """
"""     print("Subgraph information:") """
"""     print(nx.info(subG)) """
"""  """
"""     # Print the first 5 edges in the subgraph """
"""     first_5_edges = list(subG.edges())[:5] """
"""     for s, o in first_5_edges: """
"""         print(f"{s} -> {o}") """
"""  """
"""     # Create an empty rdflib Graph """
"""     g_rdf = Graph() """
"""  """
"""     # Assign a generic type to each node """
"""     for node in subG.nodes(): """
"""         g_rdf.add((URIRef(node), URIRef("rdf:type"), URIRef("owl:Thing"))) """
"""  """
"""     # Add edges to the RDF graph """
"""     for s, o, data in tqdm(subG.edges(data=True), desc=f"Processing edges for {file_name}"): """
"""         g_rdf.add((URIRef(s), URIRef(data['predicate']), URIRef(o))) """
"""  """
"""     # Construct output file name """
"""     output_file_name = f"{os.path.splitext(file_name)[0]}_subgraph.ttl" """
"""     output_path = os.path.join(output_dir, output_file_name) """
"""  """
"""     # Serialize the rdflib Graph to a TTL file """
"""     g_rdf.serialize(destination=output_path, format='turtle') """
"""     print(f"Subgraph saved to {output_path}") """

# total_time = time.time() - start_time
# print(f"Total time taken: {total_time:.2f} seconds")