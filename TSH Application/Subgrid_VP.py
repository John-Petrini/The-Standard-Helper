import tkinter as tk
from VolumetricGlass import VolumetricGlass

vp_error = {
    0.5: 0.006,
    1: 0.006,
    1.5: 0.006,
    2: 0.006,
    2.5: 0.006,
    3: 0.01,
    4: 0.01,
    5: 0.01,
    6: 0.02,
    7: 0.02,
    8: 0.02,
    9: 0.02,
    10: 0.02,
    15: 0.03,
    20: 0.03,
    25: 0.03,
    30: 0.04,
    40: 0.05,
    50: 0.08,
    100: 0.08}

# vp_max = 100
# vp_min = 0.5

class VP_subgrid:
    def __init__(self, grid_frame):
        self.values = []
        self._create_header(grid_frame)
        self._create_buttons(grid_frame)

    def _create_header(self, grid_frame):
        header_frame=tk.Frame(grid_frame)
        header_frame.grid(row=0, column=1)

        header_label = tk.Label(header_frame, text="Volumetric Pipettes", 
                                font=('Arial', 12, 'bold'))
        header_label.pack(padx=5, pady=5)

    def _create_buttons(self, grid_frame):
        # initializes grid for buttons in VP_subgrid
        VP_subgrid = tk.Frame(grid_frame, borderwidth=2, relief="solid", 
                              width=200, height=20)
        VP_subgrid.grid(row=1, column = 1, padx=5, pady=5) #formatting grid in grid frame

        # creates each unique button
        self._createButton(VP_subgrid, "0.5", 0, 0, 0.5)
        self._createButton(VP_subgrid, "1", 0, 1, 1)
        self._createButton(VP_subgrid, "1.5", 0, 2, 1.5)
        self._createButton(VP_subgrid, "2", 0, 3, 2)
        self._createButton(VP_subgrid, "2.5", 0, 4, 2.5)
        self._createButton(VP_subgrid, "3", 1, 0, 3)
        self._createButton(VP_subgrid, "4", 1, 1, 4)
        self._createButton(VP_subgrid, "5", 1, 2, 5)
        self._createButton(VP_subgrid, "6", 1, 3, 6)
        self._createButton(VP_subgrid, "7", 1, 4, 7)
        self._createButton(VP_subgrid, "8", 2, 0, 8)
        self._createButton(VP_subgrid, "9", 2, 1, 9)
        self._createButton(VP_subgrid, "10", 2, 2, 10)
        self._createButton(VP_subgrid, "15", 2, 3, 15)
        self._createButton(VP_subgrid, "20", 2, 4, 20)
        self._createButton(VP_subgrid, "25", 4, 0, 25)
        self._createButton(VP_subgrid, "30", 4, 1, 30)
        self._createButton(VP_subgrid, "40", 4, 2, 40)
        self._createButton(VP_subgrid, "50", 4, 3, 50)
        self._createButton(VP_subgrid, "100", 4, 4, 100)

        print(self.getGlassware())

    # defining buttons
    def _createButton(self, VP_subgrid, text, row, col, value):
        button = tk.Button(VP_subgrid, text=text, width=10, height=2)
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
        
        #creating class instances when called
        for volume in self.values:
            glassware.append(VolumetricGlass(volume, 'VP', vp_error[volume]))
        
        return glassware
            
