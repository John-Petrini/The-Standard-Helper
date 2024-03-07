import tkinter as tk

# default values
target_list = [1, 2.5, 5, 7.5, 10, 15, 20, 25, 30]
dead_vol = 20 # assumes 20% dead volume of all flasks
dead_wt = 10 # assumes 10% available material is lost
default_material_amount = 10000000 # assumes (10^6ug = 10g) material 

class C_subgrid:
    def __init__(self, grid_frame):
        self.constraint_list = []
        self._create_entry_widgets(grid_frame)

    def _create_entry_widgets(self, grid_frame):
        # initializing grid layout
        C_subgrid = tk.Frame(grid_frame, borderwidth=2, relief='solid',
                              width=200, height=200)
        C_subgrid.grid(row=2, column=0, padx=5, pady=5) # formatting grid in grid frame

        # defining label text characters 
        label_list = [
            "Target Concentrations (x, y, z):" ,
            "Standard Material Available(µg):",
            "Dead Volume (%):" ,
            "Dead Weight (%):" 
        ]

        constraint_list = []

        # creates labels and entries, adds entries to list for accessability
        for i, label_text in enumerate(label_list):
            # label creation to right of entry field
            label = tk.Label(C_subgrid, text=label_text, font=('Arial', 8, 'bold'))
            label.grid(row=i, column=0, padx=5, pady=5, sticky=tk.E)

            # entry field creation
            entry_field = tk.Entry(C_subgrid)
            entry_field.grid(row=i, column=1, padx=5, pady=5)

            #stores values of entry widget in dictionary, callable by label text
            constraint_list.append(entry_field)
    
    """
    def getConstraints(self):
        print(constraint_list)"""

    

