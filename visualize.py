import networkx as nx 
import matplotlib.pyplot as plt 
   
# Defining a Class 
class GraphVisualization: 
   
    def __init__(self): 
          
        # visual is a list which stores all  
        # the set of edges that constitutes a 
        # graph 
        self.visual = [] 
          
    # addEdge function inputs the vertices of an 
    # edge and appends it to the visual list 
    def addEdge(self, a, b): 
        temp = [a, b] 
        self.visual.append(temp) 
          
    # In visualize function G is an object of 
    # class Graph given by networkx G.add_edges_from(visual) 
    # creates a graph with a given list 
    # nx.draw_networkx(G) - plots the graph 
    # plt.show() - displays the graph 
    def visualize(self): 
        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G) 
        plt.show() 
  
# Driver code 
G = GraphVisualization() 
 
for index, row in data.iterrows():
    if(index < 1000):
        G.addEdge(row[0], row[1])
    else:
        break

G.visualize() 