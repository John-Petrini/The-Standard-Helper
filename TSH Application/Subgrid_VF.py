import tkinter as tk
from VolumetricGlass import VolumetricGlass
vf_error = {
    1: 0.006,
    2: 0.006,
    5: 0.01,
    10: 0.02,
    20: 0.03,
    25: 0.03,
    30: 0.04,
    50: 0.05,
    100: 0.08,
    200: 0.10,
    250: 0.12,
    500: 0.20,
    1000: 0.30
}

# vf_max = 1000
# vf_min = 1

class VF_subgrid:
    def __init__(self, grid_frame):
        self.values = []
        self._create_header(grid_frame)
        self._create_buttons(grid_frame)

    # creates header in row above VF_subgrid (0,0)
    def _create_header(self, grid_frame):
        header_frame = tk.Frame(grid_frame)
        header_frame.grid(row=0, column=0)

        header_label = tk.Label(header_frame, text="Volumetric Flasks", 
                                font=("Arial", 12, 'bold'))
        header_label.pack(pady=5, padx=5)

    # creating buttons in VF_subgrid (1,0)
    def _create_buttons(self, grid_frame):
        # initializes grid layout
        VF_subgrid = tk.Frame(grid_frame, borderwidth=2, relief="solid", 
                              width=200, height=200)
        VF_subgrid.grid(row=1, column=0, padx=5, pady=5) #formatting grid in grid frame

        # creates each unique button
        self._createButton(VF_subgrid, "1", 0, 0, 1)
        self._createButton(VF_subgrid, "2", 0, 1, 2)
        self._createButton(VF_subgrid, "5", 0, 2, 5)
        self._createButton(VF_subgrid, "10", 1, 0, 10)
        self._createButton(VF_subgrid, "20", 1, 1, 20)
        self._createButton(VF_subgrid, "25", 1, 2, 25)
        self._createButton(VF_subgrid, "50", 2, 0, 50)
        self._createButton(VF_subgrid, "100", 2, 1, 100)
        self._createButton(VF_subgrid, "200", 2, 2, 200)
        self._createButton(VF_subgrid, "250", 3, 0, 250)
        self._createButton(VF_subgrid, "500", 3, 1, 500)
        self._createButton(VF_subgrid, "1000", 3, 2, 1000)

        print(self.getGlassware())
    
    # defining buttons
    def _createButton(self, VF_subgrid, text, row, col, value):
        button = tk.Button(VF_subgrid, text=text, width=10, height=2)
        button.grid(row=row, column=col, padx=5, pady=5)
        button.configure(command=lambda: self._onPress(value, button))

    # defining button press
    def _onPress(self, value, button):
        if value in self.values:
            self.values.remove(value)
            button.config(relief=tk.RAISED)
        else:
            self.values.append(value)
            button.config(relief=tk.SUNKEN)
        
        print(self.getGlassware())
    
    def getGlassware(self):
        glassware = []
        for volume in self.values:
            glassware.append(VolumetricGlass(volume, 'VF', vf_error[volume]))
        return glassware

