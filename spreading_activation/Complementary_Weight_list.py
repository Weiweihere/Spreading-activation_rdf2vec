import json
from rdflib import Graph, URIRef

# activated_nodes_file = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/095_1_nodes/second_round/activated_nodes_20240717_181520_15_1.txt"
# ttl_file = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/city_15K.ttl"
# output_file_path = 'weighted_triples_output_city_com.txt'

# Helper function to normalize URIs
def normalize_uri(uri):
    return uri.strip("<>")

# Dataset configuration: map dataset names to file paths

datasets = {
    "city": {
        "activated_nodes_file": "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/fixiteration_round_FT_0.5_2_filtered_29_1/activated_nodes_Cities_DBpedia_URI15_20241227_173421_29_1.txt",
        "ttl_file": "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/SA_standard_0.5_subgraph/activated_nodes_Cities_DBpedia_URI15_20241227_173421_29_1_subgraph.ttl",
        "output_file_path": "weight_0.5/weighted_triples_output_city_com.txt"
    },
    "movies": {
        # "activated_nodes_file": "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/095_1_nodes/second_round/activated_nodes_20240722_110544_27_1.txt",
        # "activated_nodes_file": "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/second_round_filter_node/activated_nodes_20240722_110544_movies_29_1.txt",
        "activated_nodes_file": "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/fixiteration_round_FT_0.5_2_filtered_29_1/activated_nodes_Movies_DBpedia_URI15_20241227_173616_29_1.txt",
        # "ttl_file": "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/SA_standard_subgraph/activated_nodes_20240722_110544_movies_29_1_subgraph.ttl",
        "ttl_file": "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/SA_standard_0.5_subgraph/activated_nodes_Movies_DBpedia_URI15_20241227_173616_29_1_subgraph.ttl",
        "output_file_path": "weight_0.5/weighted_triples_output_movies_com.txt"
    },
    "albums": {
        "activated_nodes_file": "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/fixiteration_round_FT_0.5_2_filtered_29_1/activated_nodes_Album_DBpedia_URI15_20241227_173208_29_1.txt",
        "ttl_file": "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/SA_standard_0.5_subgraph/activated_nodes_Album_DBpedia_URI15_20241227_173208_29_1_subgraph.ttl",
        # "activated_nodes_file": "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/second_round_filter_node/activated_nodes_Album_DBpedia_URI15_20241212_130915_29_1.txt",
        # "ttl_file": "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/SA_standard_subgraph/album_0728k.ttl",
        "output_file_path": "weight_0.5/weighted_triples_output_albums_com.txt"
    },
    "aaup": {
        "activated_nodes_file": "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/fixiteration_round_FT_0.5_2_filtered_29_1/activated_nodes_AAUP_DBpedia_URI15_20241227_173344_29_1.txt",
        "ttl_file": "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/SA_standard_0.5_subgraph/activated_nodes_AAUP_DBpedia_URI15_20241227_173344_29_1_subgraph.ttl",
        "output_file_path": "weight_0.5/weighted_triples_output_aaup_com.txt"
    },
    "forbes": {
        "activated_nodes_file": "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/fixiteration_round_FT_0.5_2_filtered_29_1/activated_nodes_Forbes_DBpedia_URI15_20241227_173651_29_1.txt",
        "ttl_file": "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/SA_standard_0.5_subgraph/activated_nodes_Forbes_DBpedia_URI15_20241227_173651_29_1_subgraph.ttl",
        "output_file_path": "weight_0.5/weighted_triples_output_forbes_com.txt"
    },
    "lp": {
        "activated_nodes_file": "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/fixiteration_round_FT_0.5_2_filtered_29_1/activated_nodes_LP50_20241227_173541_29_1.txt",
        "ttl_file": "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/SA_standard_0.5_subgraph/activated_nodes_LP50_20241227_173541_29_1_subgraph.ttl",
        "output_file_path": "weight_0.5/weighted_triples_output_lp_com.txt"
    },
    "kore": {
        "activated_nodes_file": "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/fixiteration_round_FT_0.5_2_filtered_29_1/activated_nodes_KORE_sorted_20241227_173458_29_1.txt",
        "ttl_file": "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/SA_standard_0.5_subgraph/activated_nodes_KORE_sorted_20241227_173458_29_1_subgraph.ttl",
        "output_file_path": "weight_0.5/weighted_triples_output_kore_com.txt"
    }
}

# activated nodes file
# city: /pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/095_1_nodes/second_round/activated_nodes_20240717_181520_15_1.txt
# activated_nodes_file = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/generate_edge_list/activated_nodes_test.txt"this is according to the miro

# movies: "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/095_1_nodes/second_round/activated_nodes_20240722_110544_27_1.txt"
# albums: "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/095_1_nodes/second_round/activated_nodes_20240723_111551_99_1.txt"
# aaup: "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/095_1_nodes/second_round/activated_nodes_20240715_171549_15_1.txt"
# forbes: "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/095_1_nodes/activated_nodes_20240712_190801_30_1v2.txt"

# Lp: "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/095_1_nodes/second_round/activated_nodes_20240726_175056_99_1.txt"

# kore /pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/095_1_nodes/activated_nodes_20240706_000217_14_1.txt
# testing file:activated_nodes_file = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/jRDF2Vec/src/main/java/de/uni_mannheim/informatik/dws/jrdf2vec/testing/weight_testing.txt"
# ttl_file = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/jRDF2Vec/src/main/java/de/uni_mannheim/informatik/dws/jrdf2vec/testing/graph.ttl"
    

# ttl file
# city: /pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/city_15K.ttl
# ttl_file = "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/generate_edge_list/city_test.ttl"
# rest ttl file

# "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/movies_41K.ttl"
# "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/Album2_61K.ttl"
# "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/AAUP_95K.ttl"
# "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/Forbes_119K.ttl"
# "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/LP50_48K.ttl"
# "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/retrive_subgraph/subgraph_withnodes/kore_171K.ttl"
# 
# 


for dataset_name, files in datasets.items():
    print(f"Processing dataset: {dataset_name}")
    
    try:
        with open(files["activated_nodes_file"], 'r') as file:
            node_weights_data = json.load(file)
            node_weights = {normalize_uri(key): value for key, value in node_weights_data.items()}
        print("Node weights loaded successfully.")
    except Exception as e:
        print(f"Error loading node weights for {dataset_name}: {e}")
        continue
    
    g = Graph()
    try:
        g.parse(files["ttl_file"], format="ttl")
        print(f"Graph loaded successfully. contains {len(g)} triples")
    except Exception as e:
        print(f"An error occurred loading graph for {dataset_name}: {e}")
        continue
    missing_nodes =  set()
    for subj, _, obj in g:
        if normalize_uri(str(subj)) not in node_weights:
            missing_nodes.add(str(subj))
        if normalize_uri(str(obj)) not in node_weights:
            missing_nodes.add(str(obj))
    if missing_nodes:
        print(f"Nodes not found in the node weights dictionary for {dataset_name}:")
        for node in missing_nodes:
            print(node)
    else:
        print(f"All nodes found in the node weights dictionary for {dataset_name}.")
        
    edge_weights = []
    
    for subj, pred, obj in g:
        subj_uri = normalize_uri(str(subj))
        obj_uri = normalize_uri(str(obj))
        if subj_uri in node_weights and obj_uri in node_weights:
            subj_weight = node_weights[subj_uri]
            obj_weight = node_weights[obj_uri]
            
            connected_objects = [
                normalize_uri(str(o)) for _, _, o in g.triples((subj, pred, None))
            ]
            connected_weights = [
                node_weights.get(o, 0) for o in connected_objects
            ]
            sum_weights = sum(connected_weights)
            
            if sum_weights > 0:
                edge_weight = 1-obj_weight / sum_weights
                edge_weights.append((subj_uri, str(pred), obj_uri, edge_weight))
            else:
                print(f"Skipping edge {subj} -> {obj} via predicate {pred}: sum of connected weights is 0.")
        else:
            print(f"Node {subj} or {obj} not in node weights dictionary.")
    
    try:
        with open(files["output_file_path"], 'w') as f:
            for subj, pred, obj, weight in edge_weights:
                f.write(f"{subj}|{pred}|{obj}|{weight:.4f}\n")
        print(f"Output written to {files['output_file_path']}")
    except IOError as e:
        print(f"Error writing to file {files['output_file_path']}: {e}")
    
    print(f"completed processing dataset: {dataset_name}\n")