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

# Sample Data Folder Overview

This repository (saved in [Google Drive](https://drive.google.com/file/d/1vjbcr0uhDjTs5fOZ6e59ObSZNKTvBNXF/view?usp=sharing)) contains two main subfolders within the `sample_data` directory, which are used for the processes of spreading activation and weight adjustments in RDF2Vec transformations.


## Subfolder: `spreading_activation_0.5`

### Files and Usage

- **`Cities_DBpedia_URI15.txt`**
  - **Description**: This file is an example of an interesting list. It contains specific URIs from DBpedia related to cities.

- **`activated_nodes_Cities_DBpedia_URI15_20241227_173421.txt`**
  - **Description**: This file lists nodes that were activated based on the spreading activation algorithm.
  - **Generation**: Can be generated using the Python script `ws_main_undirected1_addnodelimit.py` with an interesting node list and a knowledge graph dataset (ttl file).

- **`activated_nodes_Cities_DBpedia_URI15_20241227_173421_29_1.txt`**
  - **Description**: This file contains activated nodes with a weight greater than 0.29.
  - **Generation**: Use `weightscale_analysis_fixed.py` with `fixed_weight_threshold = 0.29` to obtain this file.

- **`activated_nodes_Cities_DBpedia_URI15_20241227_173421_29_1_subgraph.ttl`**
  - **Description**: This ttl file represents a subgraph for the above-mentioned activated nodes.
  - **Generation**: Generate this file using `main_retrive_inbach.py`.

### Spreading Activation Parameters

- **Initial Activation**: 1
- **Firing Threshold**: 0.5
- **Decay Factor**: 0.3
- **Unified Weight**: 0.3
- **Subgraph Retrieval Threshold**: 0
- **Max Iteration Limitation**: 1

These parameters are crucial for controlling the dynamics of the spreading activation process.

> **Note**: The ttl file used as the knowledge graph dataset is too large to be included here. Please refer to the thesis for instructions on how to download this ttl file.

## Subfolder: `weight_RDF2vec`

### Processing Steps

1. **Generate Weight Files**
   - Use the activated nodes file and the subgraph ttl file to generate weight files. These are utilized in the spreading activation (SA) process.

2. **RDF2Vec Feature Updates**
   - Follow the instructions in `readme_new.md` to generate walks and embeddings using the weight files in RDF2Vec feature updates.
   - vectors.txt in the subfolder is from /pfs/work7/workspace/scratch/ma_wezhu-extended_sa/jRDF2Vec/src/main/java/de/uni_mannheim/informatik/dws/jrdf2vec/testing/SA_0.5_weight_walk_embedding/embedding_city_direct/ so it is the embedding of directed weighted city subgraph

> **Note**: Due to size constraints, the embeddings generated by RDF2Vec are not included in this repository.

