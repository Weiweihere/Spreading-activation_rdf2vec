import json
import os

file_path = "second_round/activated_nodes_Album_DBpedia_URI15_20241212_130915.txt"
# activated_nodes_KORE_sorted_20241212_002826.txt"
# second_round/activated_nodes_KORE_sorted_20241020_191949.txt"这个是原来的firing threshold: 0.4， Decay factor: 0.5， uniform_weight: 0.5
# activated_nodes_20240726_175056.txt"

base_name, extension = os.path.splitext(file_path)
folder_path = "095_1_nodes"
new_file_path = f"095_1_nodes/{base_name}_99_1{extension}"

target_count = 36150
# 19300
# count_0_to_025 = 0
# count_025_to_05 = 0
# count_05_to_075 = 0
# count_075_to_085 = 0
# count_085_to_095 = 0
# count_095_to_1 = 0
# 
# nodes_095_to_1 = {}

with open(file_path, "r") as file:
    data = file.read()
    node_data = json.loads(data)

# for node, weight in node_data.items():
    # if 0 <= weight <0.1501:
        # count_0_to_025 +=1
    # elif 0.1501<= weight< 0.1503:
        # count_025_to_05 += 1
    # elif 0.1503 <= weight <0.1505:
        # count_05_to_075 += 1
    # elif 0.1505 <= weight< 0.1507:
        # count_075_to_085 += 1
    # elif 0.1507 <= weight< 0.1508:
        # count_085_to_095 += 1
    # elif 0.1508 <= weight <=1:
        # count_095_to_1 += 1
        # nodes_095_to_1[node] = weight
        # 
# with open(new_file_path, "w") as file:
#    file.write(json.dumps(nodes_095_to_1))
# 
# print("Count of weights from 0 to 0.1501:", count_0_to_025)
# print("Count of weights from 0.1501 to 0.1503:", count_025_to_05)
# print("Count of weights from 0.1503 t 0.1505:", count_05_to_075)
# print("Count of weights from 0.1505 to 0.1507:", count_075_to_085)
# print("Count of weights from 0.1507 to 0.1508:", count_085_to_095)
# print("Count of weights from 0.1508 to 1: ", count_095_to_1)
# 
# print("Nodes with weights from 0.305 to 1 which is saved as interesting node:", len(nodes_095_to_1))
def count_nodes_in_range(node_data, lower_bound, upper_bound):
    count = 0
    nodes_in_range = {}
    for node, weight in node_data.items():
        if lower_bound <= weight < upper_bound or (upper_bound == 1 and weight == 1) :
            count += 1
            nodes_in_range[node] = weight
    return count, nodes_in_range

# Perform binary search to find the range
lower_bound = 0
upper_bound = 1
epsilon = 0.0001  # Small value to adjust the range

while upper_bound - lower_bound > epsilon:
    mid = (lower_bound + upper_bound) / 2
    count, nodes_in_range = count_nodes_in_range(node_data, mid, 1)
    if count < target_count:
        upper_bound = mid
    else:
        lower_bound = mid

# Save the nodes within the found range
# with open(new_file_path, "w") as file:
    # file.write(json.dumps(nodes_in_range))
    
    

print(f"Approximate range to include {target_count} nodes is from {lower_bound} to 1")
print("Count of nodes in this range:", len(nodes_in_range))
# num_nodes_saved = len(nodes_in_range)
# print(f"Saved {num_nodes_saved} nodes in the file: {new_file_path}")