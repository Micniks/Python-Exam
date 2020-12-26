import pandas as pd
import networkx as nx
import matplotlib.pyplot as pl


class ClassSynergy:
    
    def __init__(self, dataset = None):
        #Get data from dataset
        if dataset is None:
            self.character_data = pd.read_csv('https://raw.githubusercontent.com/oganm/dndstats/master/docs/charTable.tsv', sep='\t')
        else:
            self.character_data = dataset
        
        
    def getMulticlassGraphically(self):

           # dropping duplicates and getting all unique classes
        class_data = self.character_data[['justClass']]
        drop_class_duplicates = class_data.drop_duplicates()
        unique_classes = [c for c in drop_class_duplicates['justClass'] if "|" not in c]
        unique_classes.sort()

           # getting all characters that have two or more classes
        multiple_classes = [c for c in self.character_data['justClass'] if "|" in c]


           # separating all the classes by splitting strings at "|" and adding to new list
        separated_classes = []
        for i in multiple_classes:
            row = i.split("|")
            for r in row:
                separated_classes.append(r)

           # finding every class occurrence and adding to dictionary with "class" as key and "amount" as value
        class_occurrences = {}
        for occ in separated_classes:
            if occ in class_occurrences:
                class_occurrences[occ] +=1
            else:
                class_occurrences[occ] =1


           # finding all connected classes by separating each connected string and putting them together as dual then adding to new list
        separated_edges = []
        row = []
        for q in multiple_classes:
            row = q.split("|")
            for idx_one in range(len(row)):
                for idx_two in range(idx_one+1,len(row)):
                    separated_edges.append((row[idx_one], row[idx_two]))

           # iterating over connected classes (edges) in the new list and adding them to new dictionary
           # with "class connection" as key and "amount" as value
        edge_occurrences = {}
        for edge in separated_edges:
            if edge in edge_occurrences:
                edge_occurrences[edge] +=1
            else:
                edge_occurrences[edge] =1

           # displaying the nodes and edges (single class occurrence and class connection occurence)
        display(class_occurrences)    
        display(edge_occurrences)



           # Creating the graph and then starting to add data to it
        G = nx.Graph()

           # creating node sizes (10 * number of occurences) and adding to list
        nodes = class_occurrences.values()
        node_sizes = []
        for c in nodes:
            node_size = 10 * c
            node_sizes.append(node_size)

           # adding nodes to graph from dictionary and making pos
        G.add_nodes_from(class_occurrences.keys())
        pos=nx.circular_layout(G)

           # drawing nodes with created sizes, color etc
        nx.draw_networkx_nodes(G, pos, node_color='lime', node_size = node_sizes)

           # creating labels from class_occurrence.keys's names and adding to graph with font size
        labels = {}
        node_list = nodes = class_occurrences.keys()
        for node_name in node_list:
            labels[str(node_name)] = str(node_name)
        nx.draw_networkx_labels(G, pos, labels, font_size=8)

           # iterating over edges from edge_occurrences and adding edges to graph with weights (being number of occurrences * 0.2)
        edges = edge_occurrences.keys()
        for e in edges:
            value = edge_occurrences[e]
            edge_size = 0.2 * value
            G.add_edge(*e, weight=edge_size)

        print(nx.info(G))

           # making list of all weights from edges
        all_weights = []
        for (node1,node2,data) in G.edges(data=True):
                all_weights.append(data['weight'])


        unique_weights = list(set(all_weights))

           # iterating over each weight and making the edges with the weight in question and adding it to the graph
        for weight in unique_weights:
                weighted_edges = [(node1,node2) for (node1,node2,edge_attr) in G.edges(data=True) if edge_attr['weight']==weight]
                   # defining how big every edge should be
                width = weight*25.0/sum(all_weights)
                   # drawing the edges using the edges themselves and the width/weight that belongs to the edge
                nx.draw_networkx_edges(G, pos, edgelist = weighted_edges, width = width, 
                                      edge_color = "red")

        pl.axis('off')
        pl.title('How often each class is played together')
        pl.show()