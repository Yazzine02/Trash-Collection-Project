import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from HamiltonianCycle import HamiltonianCycle  # Assuming this is a custom module
from GraphRepresentation import create_graph_representation_in_window  # Assuming this is a custom module
from BruteForcing_TSP import FloydWarshall_BruteForce  # Assuming this is a custom module
import folium
import webbrowser

infinity = 99999

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

        custom_map_radio = tk.Radiobutton(self, text="Custom", variable=self.map_choice_var, value=1, command=lambda: [self.update_image(), self.update_options()])
        custom_map_radio.grid(row=1, column=0, padx=10, pady=5)

        predefined_map_radio1 = tk.Radiobutton(self, text="Agdal Secteur 1", variable=self.map_choice_var, value=2, command=lambda: [self.update_image(), self.update_options()])
        predefined_map_radio1.grid(row=1, column=1, padx=10, pady=5)

        predefined_map_radio2 = tk.Radiobutton(self, text="Agdal Secteur 2", variable=self.map_choice_var, value=3, command=lambda: [self.update_image(), self.update_options()])
        predefined_map_radio2.grid(row=1, column=2, padx=10, pady=5)

        # Map image
        self.map_image_label = tk.Label(self, text="Map")
        self.map_image_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

        # Initial display of the image
        self.update_image()

        self.update_options()

        # Algorithm selection
        algorithm_label = tk.Label(self, text="Select algorithm:")
        algorithm_label.grid(row=19, column=0, padx=10, pady=5, sticky="w")

        algorithm_options = ["Hamiltonian Cycle", "Brute force"]  # Add other algorithms as needed
        algorithm_dropdown = ttk.Combobox(self, textvariable=self.selected_algorithm, values=algorithm_options)
        algorithm_dropdown.grid(row=19, column=1, padx=10, pady=5)
        algorithm_dropdown.bind("<<ComboboxSelected>>", self.update_options)

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

    def run_algorithm_and_display_graph(self):
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

        algorithm = self.selected_algorithm.get()
        print("Algorithm selected: ", algorithm)
        if algorithm == "Hamiltonian Cycle":
            path,cost = HamiltonianCycle(graph, len(graph), 0)
        elif algorithm == "Brute force":
            path,cost = FloydWarshall_BruteForce(graph, len(graph))

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
        self.generate_map(path)
        
        self.quit()

    def generate_map(self, path):
        # Assume we have coordinates for each trash bin
        coordinates = [
            [33.9716, -6.8498],  # Example coordinates (latitude, longitude)
            [33.9731, -6.8471],
            [33.9751, -6.8512],
            # Add more coordinates corresponding to the bins
        ]

        # Create a map centered at the first bin
        map_center = coordinates[0]
        m = folium.Map(location=map_center, zoom_start=15)

        # Add markers for each bin
        for idx in range(len(coordinates)):
            folium.Marker(location=coordinates[idx], popup=f'Bin {idx+1}').add_to(m)

        # Add the path
        path_coords = [coordinates[i] for i in path]
        folium.PolyLine(path_coords, color="blue", weight=2.5, opacity=1).add_to(m)

        # Save the map to an HTML file
        map_filename = "trash_bins_map.html"
        m.save(map_filename)

        # Open the map in a web browser
        webbrowser.open('file://' + os.path.realpath(map_filename))

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

if __name__ == "__main__":
    app = TrashCollectionApp_GUI()
    center_window(app)  # Center the window
    app.mainloop()

