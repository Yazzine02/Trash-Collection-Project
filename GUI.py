import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from HamiltonianCycle import HamiltonianCycle  # Assuming this is a custom module
from Topography import generate_points_at_distance
import folium
from folium import Icon
import webbrowser
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests

infinity = 99999

# Define bin coordinates and distance matrices for predefined maps
# Change the predefined maps as needed
predefined_maps = {
    "Agdal Secteur 1": {
        "depot": (34.017500, -6.832500),
        "bins": [
            (34.017400, -6.832600),
            (34.017300, -6.832700),
            (34.017200, -6.832800),
            (34.017100, -6.832900),
            (34.017000, -6.833000)
        ],
        "distance_matrix": [
            [infinity, 1, 2, 3, 4],
            [1, infinity, 1, 2, 3],
            [2, 1, infinity, 1, 2],
            [3, 2, 1, infinity, 1],
            [4, 3, 2, 1, infinity]
        ]
    },
    "Agdal Secteur 2": {
        "depot": (34.017600, -6.832400),
        "bins": [
            (34.017500, -6.832500),
            (34.017400, -6.832600),
            (34.017300, -6.832700),
            (34.017200, -6.832800)
        ],
        "distance_matrix": [
            [infinity, 1, 2, 3],
            [1, infinity, 1, 2],
            [2, 1, infinity, 1],
            [3, 2, 1, infinity]
        ]
    }
}


class TrashCollectionApp_GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg="#a2bffe")
        self.title("Trash Collection App")
        self.geometry("1000x800")

        # Variables needed for the GUI
        self.entries_matrix = []
        self.selected_algorithm = tk.StringVar(value="Hamiltonian Cycle")

        # Map choice
        map_label = tk.Label(self, text="Map choice:")
        map_label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="w")
        self.map_choice_var = tk.IntVar(value=1)

        custom_map_radio = tk.Radiobutton(self, text="Custom", variable=self.map_choice_var, value=1,
                                          command=lambda: [self.update_image(), self.update_options()])
        custom_map_radio.grid(row=1, column=0, padx=10, pady=5)

        predefined_map_radio1 = tk.Radiobutton(self, text="Agdal Secteur 1", variable=self.map_choice_var, value=2,
                                               command=lambda: [self.update_image(), self.update_options()])
        predefined_map_radio1.grid(row=1, column=1, padx=10, pady=5)

        predefined_map_radio2 = tk.Radiobutton(self, text="Agdal Secteur 2", variable=self.map_choice_var, value=3,
                                               command=lambda: [self.update_image(), self.update_options()])
        predefined_map_radio2.grid(row=1, column=2, padx=10, pady=5)

        # Map image
        self.map_image_label = tk.Label(self, text="Map")
        self.map_image_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

        # Initial display of the image
        self.update_image()

        self.update_options()

        # Algorithm selection (only Hamiltonian Cycle)
        algorithm_label = tk.Label(self, text="Select algorithm:")
        algorithm_label.grid(row=19, column=0, padx=10, pady=5, sticky="w")

        algorithm_options = ["Hamiltonian Cycle"]
        algorithm_dropdown = ttk.Combobox(self, textvariable=self.selected_algorithm, values=algorithm_options)
        algorithm_dropdown.grid(row=19, column=1, padx=10, pady=5)

        # Run button
        run_button = tk.Button(self, text="Run", command=self.run_algorithm_and_display_graph)
        run_button.grid(row=20, column=0, columnspan=3, padx=10, pady=5)

        # Centering widgets
        self.center_widgets()

    def center_widgets(self):
        # Center the Run button
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Center the map image label
        self.map_image_label.grid(sticky="nsew")

    def update_image(self):
        folder_path = "map_images"  # Folder containing the images
        image_filename = "placeholder.png"  # Image filename
        map_choice_var_value = self.map_choice_var.get()
        if map_choice_var_value == 1:
            image_filename = "placeholder.png"
        elif map_choice_var_value == 2:
            image_filename = "Agdal_Secteur1.jpg"
        elif map_choice_var_value == 3:
            image_filename = "Agdal_Secteur2.jpg"

        image_path = os.path.join(folder_path, image_filename)
        map_image_pil = Image.open(image_path).resize((1000, 400))

        map_image_tk = ImageTk.PhotoImage(map_image_pil)
        self.map_image_label.config(image=map_image_tk)
        self.map_image_label.image = map_image_tk  # Keep a reference to prevent garbage collection

    def validate_number_of_bins(self, event):
        num_bins = int(self.number_of_bins_entry.get())
        print(f"Selected number of bins: {num_bins}")
        self.clear_entries()
        self.create_entries(num_bins)

    def clear_entries(self):
        for row in self.entries_matrix:
            for entry in row:
                entry.destroy()
        self.entries_matrix = []

    def create_entries(self, num_bins):
        for i in range(num_bins):
            entries_row = []
            for j in range(num_bins):
                entry = tk.Entry(self, width=5)
                entry.grid(row=5 + i, column=j, padx=5, pady=5)
                entries_row.append(entry)
            self.entries_matrix.append(entries_row)

    def update_options(self, event=None):
        if self.map_choice_var.get() == 1:  # Custom map selected
            # Options of custom map (hidden when not selected)
            vlist = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
            self.number_of_bins_label = tk.Label(self, text="Number of bins:")
            self.number_of_bins_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

            self.number_of_bins_var = tk.StringVar(value="Pick an Option")
            self.number_of_bins_entry = ttk.Combobox(self, textvariable=self.number_of_bins_var, values=vlist)
            self.number_of_bins_entry.grid(row=3, column=1, padx=5, pady=5)
            self.number_of_bins_entry.bind("<<ComboboxSelected>>", self.validate_number_of_bins)

            self.distance_matrix_label = tk.Label(self, text="Distance matrix:")
            self.distance_matrix_label.grid(row=4, column=0, padx=10, pady=5, columnspan=2, sticky="w")
        else:
            self.number_of_bins_label.grid_forget()
            self.number_of_bins_entry.grid_forget()
            self.distance_matrix_label.grid_forget()
            self.clear_entries()

    def run_algorithm_and_display_graph(self):
        map_choice = self.map_choice_var.get()
        if map_choice== 1:
            graph = []
            for row in self.entries_matrix:
                graph_row = []
                for entry in row:
                    value = entry.get()
                    if value.isdigit():
                        graph_row.append(int(value))
                    elif value == "inf":
                        graph_row.append(infinity)
                    else:
                        print("Invalid input")
                graph.append(graph_row)
        else:
            selected_map = "Agdal Secteur 1" if map_choice == 2 else "Agdal Secteur 2"
            graph = predefined_maps[selected_map]["distance_matrix"]
            self.bin_coordinates = [predefined_maps[selected_map]["depot"]] + predefined_maps[selected_map]["bins"]

        algorithm = self.selected_algorithm.get()
        print("Algorithm selected: ", algorithm)
        if algorithm == "Hamiltonian Cycle":
            path, cost = HamiltonianCycle(graph, len(graph), 0)

        if not path:
            print("No path found")
            return
        print("Path found")
        print("Path: ", path)
        print("Cost: ", cost)

        # Open a new window to display the graph
        graph_window = tk.Toplevel(self)
        graph_window.title("Algorithm Representation")

        # Call the function to create the graph representation in the new window
        create_graph_representation_in_window(graph, path, algorithm, graph_window)

        # Generate and display the map
        self.generate_map(path,graph,map_choice)

        # Quit GUI
        self.quit()

    def generate_map(self, path, graph, map_choice):
        if map_choice == 1:
            bin_coordinates = [(38.9001, -77.0365)]
            print("Number of bins:", len(path))
            print("Path followed:", path)
            for i in range(1, len(path)):
                print(path[i-1])
                print(len(bin_coordinates))
                if path[i - 1] >= len(path):
                    print(f"Invalid path index: path[{i - 1}] = {path[i - 1]}")
                    return

                prev_bin = bin_coordinates[i - 1]
                distance_km = graph[path[i - 1]][path[i]]
                new_bin = generate_points_at_distance(prev_bin[0], prev_bin[1], distance_km)
                bin_coordinates.append(new_bin)
                print(f"Added new_bin: {new_bin} at index: {len(bin_coordinates) - 1}")
        else:
            bin_coordinates = self.bin_coordinates

        # Query OSRM API to get the route
        route = get_osrm_route([bin_coordinates[i] for i in path])

        if route is None:
            print("Failed to generate route")
            return

        map_center = bin_coordinates[0]
        m = folium.Map(location=map_center, zoom_start=17)

        # Define paths to the icons
        depot_icon_path = "C:/Users/user/Desktop/PFA/display_map/icons/facility.png"
        bin_icon_path = "C:/Users/user/Desktop/PFA/display_map/icons/trash-bin.png"

        # Add a marker for the trash depot with a custom icon
        folium.Marker(
            location=bin_coordinates[0],
            popup="Trash Depot",
            icon=folium.CustomIcon(depot_icon_path, icon_size=(60, 60))
        ).add_to(m)

        # Add bin locations to the map
        for i in path:
            if i != 0:
                folium.Marker(
                    location=bin_coordinates[i],
                    popup=f"Bin {i}",
                    icon=folium.CustomIcon(bin_icon_path, icon_size=(60, 60))
                ).add_to(m)

        # Add the route to the map
        folium.PolyLine(route, color="red", weight=2.5, opacity=1).add_to(m)

        # Save map to an HTML file and open it in the default web browser
        map_path = "trash_bins_map.html"
        m.save(map_path)
        webbrowser.open(map_path)


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

    pos = nx.spring_layout(G, seed=42)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Draw the edges representing the path with red arrows
    for i in range(len(path) - 1):
        start_node = path[i]
        end_node = path[i + 1]
        cost = graph[start_node][end_node]
        nx.draw_networkx_edges(G, pos, edgelist=[(start_node, end_node)], edge_color='r', width=2, arrows=True)
        nx.draw_networkx_edge_labels(G, pos, edge_labels={(start_node, end_node): cost}, font_color='red')

    plt.title(title)

    # Embed the graph in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=toplevel)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Display the Tkinter window
    toplevel.mainloop()


def get_osrm_route(coordinates):
    base_url = "http://router.project-osrm.org/route/v1/driving/"
    coords = ";".join([f"{lon},{lat}" for lat, lon in coordinates])
    url = f"{base_url}{coords}?overview=full&geometries=geojson"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        route = data['routes'][0]['geometry']['coordinates']
        # Convert the route to folium-compatible (lat, lon) format
        route = [(coord[1], coord[0]) for coord in route]
        return route
    else:
        print(f"Error fetching route: {response.status_code}")
        return None


if __name__ == "__main__":
    app = TrashCollectionApp_GUI()
    app.mainloop()
