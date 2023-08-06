'''
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Needed for the graph (positions of the nodes)
def depth(node):
    if len(node._d.items())==0:
        return 1
    else:
        # recursive
        return max(depth(parent) for parent, _ in node._d.items())+1

# Needed for the graph (positions of the nodes)
def num_layers(array_nodes):
    return max(depth(node) for node in array_nodes.ravel())

def draw_graph_expensive(array_nodes):
    # array_nodes is an array of nodes
    # independent variables in red
    # dependent variables are in blue
    # final node is in orange

    # Color list - has to be a list
    # Annoying if a node is used multiple times
    colours=[]
    node_used=dict()

    # Position dictionary
    position_node=dict()
    counter_initial=0
    counter_final=0

    # Final postion
    final_position=2*(num_layers(array_nodes)+1)
    layer_position=final_position-1
    counter_layer=0


    # Initialise the graph G
    G=nx.DiGraph()
    for n in array_nodes.ravel():
        G.add_node(n)
        # Terminal node: out-degree is 0
        colours.append('orange')
        node_used[n]=True
        # *final_position/2 to spread things out
        position_node[n]=(final_position, counter_final*final_position/2)
        counter_final+=1


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
                        # *final_position/2 just to space things out
                        position_node[parent]=(0, (-1)**counter_initial*counter_initial*final_position/2)
                        counter_initial+=1
                else:
                    colours.append('red')
                    node_used[parent]=True
                    # *final_position/2 just to space things out
                    position_node[parent]=(0, (-1)**counter_initial*counter_initial*final_position/2)
                    counter_initial+=1
            else:
                # not a terminal node
                # in degree is not 0

                if parent in node_used.keys():
                    if not node_used[parent]:
                        colours.append('blue')
                        node_used[parent]=True
                        # We add to counter_layer as we don't want edges to overlap
                        # multiply by +-1 for same reason
                        position_node[parent]=(layer_position, (-1)**layer_position*(counter_layer+2*layer_position+1/(layer_position+3)))
                        counter_layer+=1
                        layer_position-=1
                else:
                    colours.append('blue')
                    node_used[parent]=True
                    # We add to counter_layer as we don't want edges to overlap
                    # multiply by +-1 for same reason
                    position_node[parent]=(layer_position, (-1)**layer_position*(counter_layer+2*layer_position+1/(layer_position+3)))
                    counter_layer+=1
                    layer_position-=1


    # Drawing the graph
    pos = nx.spring_layout(G)
    nx.draw(G, position_node, node_color=colours, with_labels=True)
    nx.draw_networkx_edge_labels(G, position_node, edge_labels=edge_labels)
    plt.show()
'''
