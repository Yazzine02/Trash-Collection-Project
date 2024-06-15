import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_graph_representation_in_window(graph, path, title, toplevel):
    # Create a new figure for the graph
    fig = plt.figure()

    # Create a graph representation of the result of an algorithm
    G = nx.Graph()
    for i in range(len(graph)):
        G.add_node(i)
    for i in range(len(graph)):
        for j in range(i + 1, len(graph)):
            G.add_edge(i, j, weight=graph[i][j])

    pos = nx.spring_layout(G)

    # Draw the nodes with labels
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)

    # Draw the edges representing the path
    for i in range(len(path) - 1):
        start_node = path[i]
        end_node = path[i + 1]
        cost = graph[start_node][end_node]
        nx.draw_networkx_edges(G, pos, edgelist=[(start_node, end_node)], edge_color='r', width=2)
        nx.draw_networkx_edge_labels(G, pos, edge_labels={(start_node, end_node): cost}, font_color='red')

    plt.title(title)

    # Embed the graph in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=toplevel)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Display the Tkinter window
    toplevel.mainloop()
