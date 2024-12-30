import rdflib
import networkx as nx
from collections import defaultdict
import pandas as pd
import os
import glob

# Load the TTL file into an RDFLib graph
# ttl_file = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/movies_41K.ttl"
# ttl_file = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/baseline_subgraph/movies_baseline_subgraph.ttl"
# ttl_file = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/baseline_subgraph/AAUP_baseline_subgraph.ttl"
# ttl_file = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/AAUP_95K.ttl"
# ttl_file = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/baseline_subgraph/Forbes_baseline_subgraph.ttl"
# ttl_file = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/Forbes_119K.ttl"
# ttl_file = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/baseline_subgraph/album_baseline_subgraph.ttl"
# ttl_file = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/Album2_61K.ttl"
# ttl_file = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/baseline_subgraph/LP50_baseline_subgraph.ttl"
# ttl_file = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/LP50_48K.ttl"
# ttl_file = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/baseline_subgraph/KORE_baseline_subgraph.ttl"
# ttl_file = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/kore_171K.ttl"
# ttl_file = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/city_15K.ttl"
# ttl_file = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/testing_forstatistic.ttl"
# ttl_file = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/SA_standard_subgraph/album_0728k.ttl"album已经分析完了
# activated_nodes_20240715_171549_AAUP_29_1_subgraph.ttl
# activated_nodes_20240722_110544_movies_29_1_subgraph.ttl
# activated_nodes_Album_DBpedia_URI15_20241212_130915_29_1_subgraph.ttl
# activated_nodes_KORE_sorted_20241212_002826_29_1_subgraph.ttl
# activated_nodes_LP50_20241212_171104_29_1_subgraph.ttl

# List of TTL files to process
# ttl_files = [
    # "activated_nodes_20240715_171549_AAUP_29_1_subgraph.ttl",
    # "activated_nodes_20240722_110544_movies_29_1_subgraph.ttl",
    # "activated_nodes_KORE_sorted_20241212_002826_29_1_subgraph.ttl",
    # "activated_nodes_LP50_20241212_171104_29_1_subgraph.ttl"
# ]

base_directory = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/SA_standard_0.7_subgraph/"
output_folder = "statistic_sa_standard_subgraph/SA_0.7"

os.makedirs(output_folder, exist_ok=True)

ttl_files = [f for f in os.listdir(base_directory) if f.endswith(".ttl")]

for ttl_filename in ttl_files:
    full_path = os.path.join(base_directory, ttl_filename)
    g = rdflib.Graph()
    g.parse(full_path, format="ttl")
    
    # Creating a NetworkX directed graph
    nx_graph = nx.DiGraph()
    
    # Collecting node degree information
    node_degrees = defaultdict(int)
    literal_count = 0
    namespaces = defaultdict(int)
    
    subjects = set()
    predicates = set()
    objects = set()
    
    # Iterate over triples in the graph
    for s, p, o in g:
        subjects.add(s)
        predicates.add(p)
        objects.add(o)
        nx_graph.add_edge(s, o, predicate=p)
        node_degrees[s] += 1
        if isinstance(o, rdflib.Literal):
            literal_count += 1
        else:
            node_degrees[o] += 1
        namespace_uri = p.toPython().split('/')[0] + '/'
        namespaces[namespace_uri] += 1

    num_nodes = len(set(nx_graph.nodes))
    num_edges = nx_graph.number_of_edges()

    # Graph density calculation for a directed graph
    density = num_edges / (num_nodes * (num_nodes - 1)) if num_nodes > 1 else 0
    
    # Create a dictionary to store the statistics
    stats = {
        "Statistic": [
            "Number of Triples",
            "Number of Unique Subjects",
            "Number of Unique Predicates",
            "Number of Unique Objects",
            "Number of Nodes",
            "Number of Edges",
            "Average Node Degree",
            "Maximum Node Degree",
            "Minimum Node Degree",
            "Number of Literals",
            "Number of Namespaces",
            "Graph Density"
        ],
        "Value": [
            len(g),
            len(subjects),
            len(predicates),
            len(objects),
            num_nodes,
            num_edges,
            sum(node_degrees.values()) / len(node_degrees),
            max(node_degrees.values()),
            min(node_degrees.values()),
            literal_count,
            len(namespaces),
            density
        ]
    }
    
    # Convert the dictionary to a pandas DataFrame
    df = pd.DataFrame(stats)

    base_name = os.path.splitext(os.path.basename(ttl_filename))[0]
    output_file = f"{base_name}_statistics.xlsx"
    output_path = os.path.join(output_folder, output_file)
    
    # Save the DataFrame to an Excel file
    df.to_excel(output_path, index=False)

    print(f"Processed and saved statistics for {ttl_filename} to {output_path}")