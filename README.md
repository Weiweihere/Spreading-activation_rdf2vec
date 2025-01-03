# Spreading Activation on Knowledge Graph for Embedding Generation
This repository contains an application of spreading activation on a knowledge graph to facilitate embedding generation. The process is divided into several key steps, from activation to subgraph retrieval and weight generation.

## Project Overview
Spreading activation is applied to extract meaningful subgraphs and generate embeddings by propagating weights across the knowledge graph. This technique enhances the performance of embedding models like RDF2Vec by refining the structure of the graph before embedding generation.
### Input
- **TTL File:** The knowledge graph.
- **Interesting Node List:** Specifies the nodes of interest.

### Output
- **Subgraph:** The resulting subgraph after processing.

## Requirements

- **Python Version:** 3.8  
Ensure you are using Python 3.8 to run the scripts, as compatibility with other versions is not guaranteed.

## Workflow Breakdown

### 1. Activation Generation
To generate activated nodes, use the following script:

python ws_main_undirected1_addnodelimit.py

Adjustable Parameters:
* Initial Activation: 1
* Firing Threshold: 0.7
* Decay Factor: 0.3
* Unified Weight: 0.3
* Subgraph Retrieval Threshold: 0
* Iteration Limitation: 1
These parameters control the spreading activation dynamics.

Tip:
After running the activation, analyze the scale of the activated nodes using: python weightscale_analysis.py

### 2. Subgraph Retrieval
Once activation is complete, retrieve the subgraph by executing:
python retrive_subgraph/main_subgraph_retrive.py
This script extracts subgraphs based on the activated nodes, facilitating embedding generation on a refined subset of the knowledge graph.

### 3. Weight File Generation for RDF2Vec
To generate weight files for RDF2Vec, use one of the following scripts:
Weight file
   *Direct Proportional Weight:python Direct_Propotional_Weight_list.py
   *Complementary Weight:python Complementary_Weight_list.py
These scripts generate weight configurations essential for enhancing the performance of RDF2Vec embeddings.

### Results
The results of the spreading activation and subgraph retrieval processes are presented in the attached result tables.

Notes
Ensure to fine-tune the parameters according to the knowledge graph's characteristics to achieve optimal performance.
Experimenting with different weight generation methods can provide insight into their impact on embedding quality.

The intergration of weight file with RDF2Vec is saved in https://github.com/Weiweihere/jRDF2Vec/tree/feature-updates
