'''
NOTA BENE: COMMENTING IT FOR NOW AS I HAVEN'T TESTED EVERY LINE SO THE COVERAGE WENT DOWN

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph_without_edge_labels(array_nodes):
    # array_nodes is an array of nodes

    # Initialise the graph G
    G=nx.Graph()
    for n in array_nodes.ravel():
        G.add_node(n)

    nodequeue = list(array_nodes.flatten())
    visited = set()

    while len(nodequeue) > 0:
        node = nodequeue.pop(0)
        visited.add(node)

        for parent, _ in node._d.items():
            # Adding the parent to the graph
            if parent not in G:
                G.add_node(parent)
            # Adding the edge between node and parent
            G.add_edge(node,parent)
            nodequeue.append(parent)
    nx.draw(G, with_labels=True)
    plt.show()
    plt.cla()

def draw_graph(array_nodes):
    # WARNING: STILL NEED TO IMPLEMENT node._operation for overwritten np fcts!!!

    # array_nodes is an array of nodes
    # independent variables in red
    # dependent variables are in blue
    # final node is in orange

    # Color list - has to be a list
    # Annoying if a node is used multiple times
    colours=[]
    node_used=dict()


    # Initialise the graph G
    G=nx.DiGraph()
    for n in array_nodes.ravel():
        G.add_node(n)
        # Terminal node: out-degree is 0
        colours.append('orange')
        node_used[n]=False


    nodequeue = list(array_nodes.flatten())
    visited = set()

    # Dictionary for labels
    edge_labels = dict()

    while len(nodequeue) > 0:
        node = nodequeue.pop(0)
        visited.add(node)

        for parent, _ in node._d.items():
            # Adding the parent to the graph
            if parent not in G:
                G.add_node(parent)
            # Retrieving the operation, which we use as label for the edge
            edge_labels[(node, parent)]=node._operation[parent]
            # Adding the edge between node and parent
            G.add_edge(parent, node)
            nodequeue.append(parent)
            if len(parent._d.items())==0:
                # terminal node: in degree is 0

                if parent in node_used.keys():
                    if not node_used[parent]:
                        colours.append('red')
                        node_used[parent]=True
                else:
                    colours.append('red')
                    node_used[parent]=True
            else:
                if parent in node_used.keys():
                    if not node_used[parent]:
                        colours.append('blue')
                        node_used[parent]=True
                else:
                    colours.append('blue')
                    node_used[parent]=True

    # Drawing the graph
    pos = nx.spring_layout(G)
    plt.figure()
    nx.draw(G, pos, node_color=colours, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()
'''
