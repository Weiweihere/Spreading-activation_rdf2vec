import re
import datetime
import json

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
        self._add_directed_edge(source, target, weight,predicate)
        self._add_directed_edge(target, source,weight, predicate)
    
    def _add_directed_edge(self, source, target, weight, predicate):
        """Adds a directed edge to the graph, used internally for undirected edge handling."""
        if source not in self.edges:
            self.edges[source] = []
        if target not in self.edges:  # Ensure target node is initialized in edges dictionary
            self.edges[target] = []
        if not any(e[0] == target for e in self.edges[source]):
            self.edges[source].append((target, weight))
            self.predicates[(source, target)] = predicate
            print(f"Added edge from {source} to {target} with weight {weight} and predicate {predicate}")
        else:
            print(f"Edge already exists: {source} to {target} with predicate {predicate}")
        
    def print_activation_levels(self):
        print("Node activation levels:")
        for node_id, node in self.nodes.items():
            print(f"Node {node_id}: Activation Level = {node.activation}")

    def spread_activation(self, firing_threshold, decay_factor, max_iterations=10):
        for node in self.nodes.values():
            node.fired = False
            
        iteration = 0
        new_activations = True
        
        while iteration < max_iterations and new_activations:
            new_activations = False

            for node in self.nodes.values():
                if node.activation > firing_threshold and not node.fired:
                    node.fired = True
                    new_activations = True
                    print(f"Node {node.id} (Activation: {node.activation}) starts spreading activation")
                    # for neightbor edges
                    for neighbor_id, weight in self.edges.get(node.id, []):
                        neighbor_node = self.nodes[neighbor_id]
                        total_activation = node.activation * weight * decay_factor
                        print(f"    -> Spreading {total_activation} to Node {neighbor_id} (Previous Activation: {neighbor_node.activation})")
                        neighbor_node.update_activation(total_activation)
            iteration += 1 
        print(f"Spreading activation completed in {iteration} iterations.")
        
class SpreadingActivationPipeline:
    def __init__(self, uniform_weight=0.5):
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
        
        for match in ttl_pattern.finditer(ttl_data):
            subject, predicate, object = match.groups()
            print(f"Processing triple: {subject}, {predicate}, {object}")
            self.add_edge_from_ttl(subject, predicate, object)
            print(f"processed triple with subject: {subject}")

    def load_ttl_file(self, file_path):
        with open(file_path, 'r') as file:
            ttl_data = file.read()
            self.parse_ttl_data(ttl_data)
        self.save_graph_to_json("parsed_graph1.json")
        
    
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
        for subject_uri in subjects:
            if subject_uri in self.node_map:
                node_id = self.node_map[subject_uri]
                self.graph.nodes[node_id].activation = activation_value
                print(f"Initial activation set for {subject_uri}: {self.graph.nodes[node_id].activation}")  # Debugging line
            else:
                print(f"Node {subject_uri} not found in node_map.")  # Debugging line

    def run_spreading_activation(self, firing_threshold, decay_factor):
        # No origin_uri argument needed; we set activation for all subjects beforehand
        # for node in self.graph.nodes.values():
            # node.fired = False
            # Run the spreading activation
            self.graph.spread_activation(firing_threshold, decay_factor)

    def get_activation_levels(self):
        return {uri: self.graph.nodes[node_id].activation for uri, node_id in self.node_map.items()}
         
    def get_activated_nodes(self, threshold=0.0):
        activation_levels = {}
        for uri, node_id in self.node_map.items():
            node_activation = self.graph.nodes[node_id].activation
            if node_activation >= threshold:
                activation_levels[uri] = node_activation
        return activation_levels

    def get_activated_subgraph(self, threshold):
        activated_nodes = {uri: activation for uri, activation in self.get_activation_levels().items() if
                           activation >= threshold}
        activated_edges = []

        for (source, target), predicate in self.graph.predicates.items():
            source_uri = None
            target_uri = None
            for uri, id in self.node_map.items():
                if id == source:
                    source_uri = uri
                if id == target:
                    target_uri = uri

            if source_uri in activated_nodes and target_uri in activated_nodes:
                activated_edges.append((source_uri, predicate, target_uri))

        return activated_nodes, activated_edges

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

# Usage:

pipeline = SpreadingActivationPipeline(uniform_weight=0.5)

# Load TTL data from file
print("Loading TTL data...")
# pipeline.load_ttl_file("example_graph.ttl")
pipeline.load_ttl_file("mappingbased-objects_lang=en.ttl")
print("ttl data loaded")




