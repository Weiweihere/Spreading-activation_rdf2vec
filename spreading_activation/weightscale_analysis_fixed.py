import json
import os
import glob

# List of file paths to process
# file_paths = [
    # "fixiteration_round/activated_nodes_Cities_DBpedia_URI15_20241217_000908.txt",
    # "fixiteration_round/activated_nodes_Album_DBpedia_URI15_20241217_000812.txt",
    # "fixiteration_round/activated_nodes_AAUP_DBpedia_URI15_20241217_000839.txt",
    # "second_round/activated_nodes_Album_DBpedia_URI15_20241212_130915.txt",
    # "second_round/activated_nodes_LP50_20241212_171104.txt",
    # "second_round/activated_nodes_20240722_110544_movies.txt",
    # "second_round/activated_nodes_20240715_171549_AAUP.txt",
    # "second_round/activated_nodes_KORE_sorted_20241212_002826.txt"
    # "second_round/activated_nodes_Forbes_DBpedia_URI15_20241024_202438.txt",
    # "second_round/activated_nodes_KORE_sorted_20241212_002826.txt",
    # "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/second_round/activated_nodes_Album_DBpedia_URI15_20241212_130915.txt"
    # "/pfs/work7/workspace/scratch/ma_wezhu-ws_spreading2/old_ws/activated_nodes/second_round/activated_nodes_KORE_sorted_20241212_002826.txt"
# ]

original_folder_path = "fixiteration_round_FT_0.5_2"
file_paths = glob.glob(f'{original_folder_path}/*')
print(file_paths)

folder_path = 'fixiteration_round_FT_0.5_2_filtered_29_1'
# "third_round_filter_node"
fixed_weight_threshold = 0.29


# Create the folder if it does not exist
os.makedirs(folder_path, exist_ok=True)

total_activated_nodes = 0

# Process each file
for file_path in file_paths:
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue
    base_name = os.path.basename(file_path)
    new_file_name = f"{os.path.splitext(base_name)[0]}_29_1.txt"
    new_file_path = os.path.join(folder_path, new_file_name)

    with open(file_path, "r") as file:
        data = file.read()
        node_data = json.loads(data)

    count_above_fixed_weight = 0
    nodes_above_fixed_weight = {}

    for node, weight in node_data.items():
        if weight > 0:
            total_activated_nodes += 1
        if weight >= fixed_weight_threshold:
            count_above_fixed_weight += 1
            nodes_above_fixed_weight[node] = weight

    print(f"Count of nodes with weight above {fixed_weight_threshold} in {file_path}: {count_above_fixed_weight}, Total activated nodes: {total_activated_nodes}")
    
    # Save the filtered nodes to a new text file for each input file
    with open(new_file_path, "w") as new_file:
        json.dump(nodes_above_fixed_weight, new_file, indent=4)
