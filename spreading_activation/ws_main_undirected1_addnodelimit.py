import re
import datetime
import json
import time
from collections import deque
import os
# import logging
# import sys

class Node:

    def __init__(self, id, activation=0.0): #initiate instances node which has id, activation level and fire status
        self.id = id
        self.activation = activation
        self.fired = False

    def update_activation(self, additional_activation): #updates node`s activation level based on additional activation(within the bound of 0.0 and 1.0)
        self.activation += additional_activation
        self.activation = min(max(self.activation, 0.0), 1.0)  # Clamp between 0 and 1

class Graph:
    def __init__(self):#initial graph
        self.nodes = {} #dictionary that maps nodes ID to Node objects
        self.edges = {} #dictionary that represents the connection between nodes
        self.predicates = {}  # Store predicates as (source, target): predicate

    def add_edge(self, source, target, weight, predicate): 
        self._add_directed_edge(source, target, weight, predicate)
        # self._add_directed_edge(target, source,weight, predicate)
    
    def _add_directed_edge(self, source, target, weight, predicate):
        """Adds a directed edge to the graph, used internally for undirected edge handling."""
        if source not in self.edges:
            self.edges[source] = []
        if target not in self.edges:  # Ensure target node is initialized in edges dictionary
            self.edges[target] = []
        if not any(e[0] == target for e in self.edges[source]):
            self.edges[source].append((target, weight))
            self.predicates[(source, target)] = predicate
            # print(f"Added edge from {source} to {target} with weight {weight} and predicate {predicate}")
        # else:
            # print(f"Edge already exists: {source} to {target} with predicate {predicate}")
    
    def print_activation_levels(self):
        print("Node activation levels:")
        for node_id, node in self.nodes.items():
            print(f"Node {node_id}: Activation Level = {node.activation}")

    def spread_activation(self, firing_threshold, decay_factor, max_iterations=10):
        activated_edges_with_predicates = set()

        for node in self.nodes.values():
            node.fired = False
            
        iteration = 0
        new_activations = True
        
        while iteration < max_iterations and new_activations:
            new_activations = False
            # activation_updates = {}

            for node in self.nodes.values():
                if node.activation > firing_threshold and not node.fired:
                    node.fired = True
                    new_activations = True
                    # activated_nodes.add(node.id)
                    # print(f"Node {node.id} (Activation: {node.activation}) starts spreading activation")
                    # for neightbor edges
                    for neighbor_id, weight in self.edges.get(node.id, []):
                        neighbor_node = self.nodes[neighbor_id]
                        predicate = self.predicates.get((node.id, neighbor_id))
                        total_activation = node.activation * weight * decay_factor
                        #  the activation value of the node which > 0, the edges should be saved, later, based on the edges recording, then check if 1 and 10 is in the activted subgraph, then check the edgeds on the recording.
                        if total_activation > 0:
                          activated_edges_with_predicates.add((node.id, neighbor_id, predicate))
                          neighbor_node.update_activation(total_activation)
                        # print(f"    -> Spreading {total_activation} to Node {neighbor_id} (Previous Activation: {neighbor_node.activation})")
                        
            
            # if activated_node_count >= min_activated_nodes:
                # break
            iteration += 1
            activated_node_count = sum(1 for node in self.nodes.values() if node.activation > 0)
            print(f"Iteration {iteration}: {activated_node_count} nodes activated.")
            
            if not new_activations:
                print(f"No new activations at iteration {iteration}, stopping...")
                break
            
        print(f"Spreading activation completed in {iteration} iterations with {activated_node_count} activated nodes.")
        return activated_edges_with_predicates
        
class SpreadingActivationPipeline:
    def __init__(self, uniform_weight=0.9):
        self.graph = Graph()
        self.node_map = {}
        self.uniform_weight = uniform_weight

    def add_node(self, uri):
        if uri not in self.node_map:
            node_id = len(self.node_map) + 1
            self.node_map[uri] = node_id
            self.graph.nodes[node_id] = Node(node_id)
            print(f"Added node: {uri} with ID: {node_id}")
        else:
            print(f"Node already exists:{uri}")

    def add_edge_from_ttl(self, subject, predicate, object):
        self.add_node(subject)
        self.add_node(object)
        source_id = self.node_map[subject]
        target_id = self.node_map[object]
        self.graph.add_edge(source_id, target_id, self.uniform_weight, predicate)

    def parse_ttl_data(self, ttl_data):
        ttl_pattern = re.compile(r'<(.+?)> <(.+?)> <(.+?)> \.')
        count = 0
        for match in ttl_pattern.finditer(ttl_data):
            subject, predicate, object = match.groups()
            # print(f"Processing triple: {subject}, {predicate}, {object}")
            self.add_edge_from_ttl(subject, predicate, object)
            
            count +=1
            if count%100000 ==0:
                print(f"Processed {count} triples...")
        print("Finished processing all triples.")
            # print(f"processed triple with subject: {subject}")
            
    def save_graph_to_json(self,json_file_path):
        nodes_data = [{"id": uri, "activation": self.graph.nodes[node_id].activation} for uri, node_id in self.node_map.items()]

        edges_data = [{"source": source, "target": target, "weight": weight, "predicate": self.graph.predicates[(source, target)]} for source, edge_list in self.graph.edges.items() for target, weight in edge_list]
         
        graph_data ={
            "nodes": nodes_data,
            "edges": edges_data
        }
        # Serialize and save to file
        with open(json_file_path, 'w') as file:
            json.dump(graph_data, file, indent=4)
            print(f"Graph data saved to {json_file_path}")

    def set_specific_subjects_as_origin(self, subjects, activation_value=1.0):
        activated_count = 0
        not_fount_count = 0
        
        for subject_uri in subjects:
            if subject_uri in self.node_map:
                node_id = self.node_map[subject_uri]
                self.graph.nodes[node_id].activation = activation_value
                activated_count +=1
                # print(f"Initial activation set for {subject_uri}: {self.graph.nodes[node_id].activation}")  # Debugging line
            else:
                not_fount_count +=1
                
                # print(f"Node {subject_uri} not found in node_map.")  # Debugging line
        print(f"Total activated nodes: {activated_count}. Total nodes not found: {not_fount_count}.")


    def run_spreading_activation(self, firing_threshold, decay_factor, max_iterations):
        initial_node_count = sum(1 for node in self.graph.nodes.values() if node.activation > 0)
        # min_activated_nodes = node_limit_factor * initial_node_count
        # print(f"Running spreading activation with min_activated_nodes: {min_activated_nodes}")
        return self.graph.spread_activation(firing_threshold, decay_factor, max_iterations)

    def get_activation_levels(self):
        return {uri: self.graph.nodes[node_id].activation for uri, node_id in self.node_map.items()}
         
    def get_activated_nodes(self, threshold=0.0):
        activation_levels = {}
        for uri, node_id in self.node_map.items():
            node_activation = self.graph.nodes[node_id].activation
            if node_activation >= threshold:
                activation_levels[uri] = node_activation
        return activation_levels
    
    # def get_activated_edges(self, start_nodes, activated_edges_with_predicates):
        # start_time = time.time()
        # update_interval = 300
        # last_update_time = start_time
        # visited = {node_id: False for node_id in start_nodes}
        # queue = deque(start_nodes)
        # activated_edges = []
        # debug_counter = 0

        # while queue:
            # current_node_id = queue.popleft()
            # visited[current_node_id] = True


        # for source_id, target_id, predicate in activated_edges_with_predicates:
            # source_uri = self.get_uri_from_node_id(source_id)
            # target_uri = self.get_uri_from_node_id(target_id)
            # if source_id == current_node_id and not visited.get(target_id,False):
                # visited[target_id] = True
                # queue.append(target_id)
                # activated_edges.append((source_id, predicate, target_id))
            # elif target_id == current_node_id and  not  visited 
            # if debug_counter % 100 == 0:  # Adjust N to the frequency of messages you want
            #    print(f"Debugging: Processing edge {source_uri} --{predicate}--> {target_uri}")
            # 
            # debug_counter += 1

            # current_time = time.time()
            # if current_time - last_update_time >= update_interval:
                # print(f"Processing status: {processed_edges/edge_count} edges checked. Time slapsed: {int(current_time-start_time)} seconds.")
                # last_update_time = current_time

        # start_time = time.time()
        # update_interval = 300
        # last_update_time = start_time
        # for(source, target), predicate in self.graph.predicates.items():
            # source_uri = self.get_uri_from_node_id(source)
            # target_uri = self.get_uri_from_node_id(target)

            # if source_uri in activated_nodes_set and target_uri in activated_nodes_set:
            #    activated_edges.append((source_uri, predicate, target_uri))

            # current_time = time.time()
            # if current_time - last_update_time >= update_interval:
                # print(f"Processing status: {processed_edges/edge_count} edges checked. Time slapsed: {int(current_time-start_time)} seconds.")
                # last_update_time = current_time

        print(f"Total activated edges found:{len(activated_edges)}")
        return activated_edges
    
    # def get_activated_subgraph(self, threshold):
    def get_activated_subgraph(self, threshold):
        print("Starting to retrieve the activated nodes")
        
        activated_nodes = {uri: activation for uri, activation in self.get_activation_levels().items() if activation >= threshold}
        activated_nodes_set = set(activated_nodes.keys())
        # activated_nodes = {uri: activation for uri, activation in self.get_activation_levels().items()}
        node_count = len(self.get_activation_levels().items())
        
        print(f"Total nodes to process: {node_count}")

        print(f"Activated nodes identified: {len(activated_nodes)}")

        # activated_edges = self.get_activated_edges(activated_nodes_set)

        # print(f"Activated edges identified: {len(activated_edges)}")  # Added print statement
        print("Retrieval of activated nodes completed.")
        return activated_nodes
    # activated_edges

    def get_edge_weights(self):
        # Retrieve the weights of the edges
        edge_weights = {}
        for source, edges in self.graph.edges.items():
            for target, weight in edges:
                # Convert node IDs back to URIs for consistency
                source_uri = self.get_uri_from_node_id(source)
                target_uri = self.get_uri_from_node_id(target)
                edge_weights[(source_uri, target_uri)] = weight
        return edge_weights

    def get_uri_from_node_id(self, node_id):
        # Convert a node ID back to its corresponding URI
        for uri, id in self.node_map.items():
            if id == node_id:
                return uri
        return None
        
    def load_and_set_initial_nodes_from_file(self, file_path, activation_value=1.0):
        with open(file_path, 'r') as file:
            for line in file:
                subject_uri = line.strip()
                self.set_specific_subject_as_origin(subject_uri, activation_value)

    def set_specific_subject_as_origin(self, subject_uri, activation_value=1.0):
        if subject_uri in self.node_map:
            self.graph.nodes[self.node_map[subject_uri]].activation = activation_value


def save_activated_subgraph_to_ttl(activated_edges, file_path):
    with open(file_path, 'w') as file:
        for source, predicate, target in activated_edges:
            triple = f"<{source}> <{predicate}> <{target}> .\n"
            file.write(triple)


def save_activated_subgraph_with_weights_to_ttl(activated_edges, weights, file_path):
    with open(file_path, 'w') as file:
        for i, (source, predicate, target) in enumerate(activated_edges, start=1):
            # Reified triple
            reified_statement_id = f"_:stmt{i}"
            file.write(f"{reified_statement_id} <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Statement> .\n")
            file.write(f"{reified_statement_id} <http://www.w3.org/1999/02/22-rdf-syntax-ns#subject> <{source}> .\n")
            file.write(f"{reified_statement_id} <http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate> <{predicate}> .\n")
            file.write(f"{reified_statement_id} <http://www.w3.org/1999/02/22-rdf-syntax-ns#object> <{target}> .\n")
            weight = weights.get((source, target), 0)  # Retrieve the weight
            file.write(f"{reified_statement_id} <http://example.com/weight> \"{weight}\"^^<http://www.w3.org/2001/XMLSchema#float> .\n")

def save_subjects_to_file(subjects, file_path):
        with open(file_path, 'w') as file:
            for subject in subjects:
                file.write(subject + '\n')
                
# Add a method in SpreadingActivationPipeline class to get the weights
def get_edge_weights(self):
    return {(self.node_map.inverse[source_id], self.node_map.inverse[target_id]): weight
            for (source_id, target_id), weight in self.graph.edges.items()}


def load_graph_from_json(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    print(f"Loaded graph from: {json_file_path}")

    graph = Graph()
    node_map = {}  # Maps URIs to node IDs for quick lookup
    id_to_uri = {}  # Reverse map: from numeric ID back to URI

    # Reconstruct nodes and map URIs to node IDs
    for node_data in data['nodes']:
        uri = node_data['id']
        activation = node_data.get('activation', 0.0)
        node_id = len(graph.nodes) + 1
        graph.nodes[node_id] = Node(node_id, activation)
        node_map[uri] = node_id
        id_to_uri[node_id] = uri  # Store the reverse mapping

    # Reconstruct edges using the reverse mapping
    for edge_data in data['edges']:
        # Use the reverse mapping to get URIs for source and target
        source_uri = id_to_uri[edge_data['source']]
        target_uri = id_to_uri[edge_data['target']]
        source_id = node_map[source_uri]
        target_id = node_map[target_uri]
        weight = edge_data['weight']
        predicate = edge_data['predicate']
        
        graph.add_edge(source_id, target_id, weight, predicate)

    return graph, node_map

def save_as_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Usage:
start_time = time.time()


print("-----------program start-----------------")
file_paths = [
    "/pfs/data5/home/ma/ma_ma/ma_wezhu/jRDF2Vec/examples/jupyter_notebook/interesting_nodes/new_interesting_node/Album_DBpedia_URI15.txt",
    "/pfs/data5/home/ma/ma_ma/ma_wezhu/jRDF2Vec/examples/jupyter_notebook/interesting_nodes/new_interesting_node/AAUP_DBpedia_URI15.txt",
    "/pfs/data5/home/ma/ma_ma/ma_wezhu/jRDF2Vec/examples/jupyter_notebook/interesting_nodes/new_interesting_node/Cities_DBpedia_URI15.txt",
    "/pfs/data5/home/ma/ma_ma/ma_wezhu/jRDF2Vec/examples/jupyter_notebook/interesting_nodes/KORE_sorted.txt",
    "/pfs/data5/home/ma/ma_ma/ma_wezhu/jRDF2Vec/examples/jupyter_notebook/interesting_nodes/LP50.txt",
    "/pfs/data5/home/ma/ma_ma/ma_wezhu/jRDF2Vec/examples/jupyter_notebook/interesting_nodes/new_interesting_node/Movies_DBpedia_URI15.txt",
    "/pfs/data5/home/ma/ma_ma/ma_wezhu/jRDF2Vec/examples/jupyter_notebook/interesting_nodes/new_interesting_node/Forbes_DBpedia_URI15.txt"
    
]

output_folder = "activated_nodes/fixiteration_round_FT_0.7_2"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)
#1-loading the graph

# Load the graph from the saved JSON file

loading_graph_start_time = time.time()
graph, node_map = load_graph_from_json('parsed_graph1.json')
print("Graph loaded successfully.")
loading_graph_elapsed_time = time.time() - loading_graph_start_time
print(f"Loading the graph took: {loading_graph_elapsed_time:.2f} seconds")

print("-----------Json data loaded-----------------")

pipeline = SpreadingActivationPipeline(uniform_weight=0.3) 
print(f"create pipeline with uniform weight: {pipeline.uniform_weight}")
 
pipeline.graph = graph  # Set the loaded graph
pipeline.node_map = node_map  # Set the loaded node_map
print("Pipeline initialized.")


# with open("one_city.txt","r") as file:
    # initial_nodes = [line.strip() for line in file.readlines()]
# print(f"initial notes read:{len(initial_nodes)}nodes.") 
# "/pfs/data5/home/ma/ma_ma/ma_wezhu/jRDF2Vec/examples/jupyter_notebook/interesting_nodes/KORE_sorted.txt"
# 

# 2-Load initial nodes



# initial_nodes_file_path = "/pfs/data5/home/ma/ma_ma/ma_wezhu/jRDF2Vec/examples/jupyter_notebook/interesting_nodes/new_interesting_node/Cities_DBpedia_URI15.txt"
# "/pfs/data5/home/ma/ma_ma/ma_wezhu/jRDF2Vec/examples/jupyter_notebook/interesting_nodes/LP50.txt"
# "/pfs/data5/home/ma/ma_ma/ma_wezhu/jRDF2Vec/examples/jupyter_notebook/interesting_nodes/new_interesting_node/Album_DBpedia_URI15.txt"
# initial_nodes_file_path = "/pfs/data5/home/ma/ma_ma/ma_wezhu/jRDF2Vec/examples/jupyter_notebook/interesting_nodes/KORE_sorted.txt"

    
for input_file_path in file_paths:
    start_time = time.time()
    base_file_name = os.path.basename(input_file_path).split('.')[0]
    print(f"Processing file: {input_file_path}")
    initial_nodes_start_time = time.time()
    with open(input_file_path,"r", encoding="utf-8", errors="ignore") as file:
        initial_nodes = [line.strip() for line in file.readlines()]
        initial_nodes_elapsed_time = time.time() - initial_nodes_start_time
    print(f"Initial {len(initial_nodes)} nodes from {base_file_name}, Loading initial nodes took: {initial_nodes_elapsed_time:.2f} seconds")    
    
    for node in pipeline.graph.nodes.values():
        node.activation = 0.0
        node.fired = False
        
    set_activation_start_time = time.time()
    print("Setting initial activation for nodes..")
    pipeline.set_specific_subjects_as_origin(initial_nodes,activation_value=1.0)
    set_activation_elapsed_time = time.time() - set_activation_start_time
    print(f"Setting initial activation took: {set_activation_elapsed_time:.2f} seconds")
    print(f"initial activation set with activation value 1.0")
    print("Setting initial activation for nodes..finished")
    
    spreading_activation_start_time = time.time()
    pipeline.run_spreading_activation(firing_threshold=0.7,decay_factor=0.3,max_iterations=1)
    print(f"Running spreading activation with firing threshold: 0.7, dacay factor:0.3,max iterations:1...")
    print("Retrieve activated nodes")
    # activated_nodes, activated_edges = pipeline.get_activated_subgraph(threshold=0)
    activated_nodes = pipeline.get_activated_subgraph(threshold=0)

    # print(f"Activated subgraph retrieved. {len(activated_nodes)} nodes and {len(activated_edges)} edges activated.")
    print(f"Activated node retrieved. {len(activated_nodes)} nodes ")
    spreading_activation_elapsed_time = time.time() - spreading_activation_start_time
    print(f"Spreading activation took: {spreading_activation_elapsed_time:.2f} seconds")

    saving_start_time = time.time()
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # output_file_name = f"activated_nodes/second_round/activated_nodes_{base_file_name}_{current_time}.txt"

    
    txt_output_file =os.path.join(output_folder, f"activated_nodes_{base_file_name}_{current_time}.txt")
    with open(txt_output_file, 'w') as txt_file:
        json.dump(activated_nodes, txt_file, indent=4)
        saving_elapsed_time = time.time() - saving_start_time
        print(f"Saving results took: {saving_elapsed_time:.2f} seconds")
        print(f"Successfully saved activated nodes to activated_nodes list")
        
        # Total execution time
        total_elapsed_time = time.time() - start_time
        print(f"Total script execution time: {total_elapsed_time:.2f} seconds")
        print(f"""
              Execution Summary:
              1. Graph Loading: {loading_graph_elapsed_time:.2f} seconds
              2. Initial Nodes Loading: {initial_nodes_elapsed_time:.2f} seconds
              3. Activation Setting: {set_activation_elapsed_time:.2f} seconds
              4. Spreading Activation: {spreading_activation_elapsed_time:.2f} seconds
              5. Saving Results: {saving_elapsed_time:.2f} seconds
              -------------------------------------
              Total Execution Time: {total_elapsed_time:.2f} seconds
              """)

