import tkinter as tk
from Subgrid_VF import VF_subgrid
from Subgrid_VP import VP_subgrid
from Subgrid_contraints import C_subgrid
#from Subgrid_actions
from Dilution import Dilution


class StandardHelperApp():
    def __init__(self):
        # TODO: change master to something that refers to tk
        self.master = tk.Tk()
        self.master.title("The Standard Helper")
        # self.root = tk.Tk()
        self.create_gui()
    
    def run(self):
        self.master.mainloop()

    def create_gui(self):
        """GRID WITH 4x4 SUBGRID"""
        # Create main grid frame
        self.grid_frame = tk.Frame(self.master)
        self.grid_frame.grid(row=0, column=0)

        self.vf_subgrid = VF_subgrid(self.grid_frame)
        self.vp_subgrid = VP_subgrid(self.grid_frame)
        self.C_subgrid = C_subgrid(self.grid_frame)
        #self.A_subgrid = A_subgrid(self.grid_frame)
    
    """
    def compute(self):
        flasks = self.vf_subgrid.getGlassware()
        pipets = []
        dilutions = Dilution.from_glassware_array(pipets, flasks)"""
