'''
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from NetworkVizExpensive import depth, num_layers
from matplotlib import colors as mcolors


def draw_reverse_graph(array_nodes):
    # array_nodes is an array of nodes
    # independent variables in grey
    # dependent variables are in cyan
    # final node is in purple

    # Color list - has to be a list
    # Annoying if a node is used multiple times
    colours=[]
    node_used=dict()

    # Position dictionary
    position_node=dict()
    counter_initial=0
    counter_final=0

    # Labels dict
    labeldict={}

    # Final postion
    final_position=2*(num_layers(array_nodes)+1)
    layer_position=final_position-1
    counter_layer=0


    # Initialise the graph G
    G=nx.DiGraph()
    for n in array_nodes.ravel():
        G.add_node(n)
        # Terminal node: out-degree is 0
        colours.append('tab:purple')
        node_used[n]=True
        # *final_position/2 to spread things out
        position_node[n]=(final_position, counter_final*final_position/2)
        counter_final+=1
        n._df=1
        print(n._df)
        labeldict[n]='Final node'


    nodequeue = list(array_nodes.flatten())
    visited = set()

    # Dictionary for labels
    edge_labels = dict()

    while len(nodequeue) > 0:
        node = nodequeue.pop(0)
        visited.add(node)

        for parent, derivative in node._d.items():
            # Adding the parent to the graph
            if parent not in G:
                G.add_node(parent)
            # Retrieving the operation, which we use as label for the edge
            edge_labels[(node, parent)]= '+'+str(derivative * node._df)
            try:
                parent._df+=node._df*derivative
            except AttributeError:
                parent._df=node._df*derivative
            # Adding the edge between node and parent
            G.add_edge(node, parent)
            labeldict[parent]=parent._df
            nodequeue.append(parent)

            if len(parent._d.items())==0:
                # terminal node: in degree is 0

                if parent in node_used.keys():
                    if not node_used[parent]:
                        colours.append('tab:grey')
                        node_used[parent]=True
                        # *final_position/2 just to space things out
                        position_node[parent]=(0, (-1)**counter_initial*counter_initial*final_position/2)
                        counter_initial+=1
                else:
                    colours.append('tab:grey')
                    node_used[parent]=True
                    # *final_position/2 just to space things out
                    position_node[parent]=(0, (-1)**counter_initial*counter_initial*final_position/2)
                    counter_initial+=1
            else:
                # not a terminal node
                # in degree is not 0

                if parent in node_used.keys():
                    if not node_used[parent]:
                        colours.append('tab:cyan')
                        node_used[parent]=True
                        # We add to counter_layer as we don't want edges to overlap
                        # multiply by +-1 for same reason
                        position_node[parent]=(layer_position, (-1)**layer_position*(counter_layer+2*layer_position+1/(layer_position+3)))
                        counter_layer+=1
                        layer_position-=1
                else:
                    colours.append('tab:cyan')
                    node_used[parent]=True
                    # We add to counter_layer as we don't want edges to overlap
                    # multiply by +-1 for same reason
                    position_node[parent]=(layer_position, (-1)**layer_position*(counter_layer+2*layer_position+1/(layer_position+3)))
                    counter_layer+=1
                    layer_position-=1


    # Drawing the graph
    pos = nx.spring_layout(G)
    nx.draw(G, position_node, labels=labeldict, node_color=colours, with_labels=True)
    nx.draw_networkx_edge_labels(G, position_node, edge_labels=edge_labels)
    plt.show()
'''
