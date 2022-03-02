import csv
import networkx as nx
import numpy as np


def get_nodes_edges_txt(file):
    edges = list()
    nodes = set()
    f = open(file, 'r')
    for line in f:
        token = line.split()
        nodes.add(token[0])
        nodes.add(token[1])
        edges.append((token[0], token[1]))
    nodes = list(nodes)
    return nodes, edges


def get_nodes_edges_csv(file):
    edges = list()
    with open(file, 'r') as csv_file:
        vertices = set()
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            vertices.add(int(line[0]))
            vertices.add(int(line[1]))
            edges.append((int(line[0]), int(line[1])))
    nodes = list(vertices)
    return nodes, edges


def create_graph(file, is_csv):
    if is_csv is True:
        nodes, edges = get_nodes_edges_csv(file)
    else:
        nodes, edges = get_nodes_edges_txt(file)
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G

