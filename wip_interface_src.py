"""IMPORTING DEPENDANCIES, DECLARING GLOBAL VARIABLES"""
import tkinter as tk
import math

# Null condition values
target_list = [1, 2.5, 5, 7.5, 10, 15, 20, 25, 30]
#dead_volume is user entry (%)
dead_vol = 30
dead_wt = 5
material_available = 11000
diluent_available = 2000
required_volume = 5
#is stock standard a standard?
stock_binary = 0

null_vp_list = [0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 50, 100]
null_vf_list = [1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000]

#global variables for error. Should be made user configurable. 9
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
    100: 0.08
}
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

#button sizes
b_width = 8
b_height = 2

#global variables for min. and max. glassware sizes
vp_max = 100
vp_min = 0.5
vf_max = 1000
vf_min = 1

#empty input lists
VF = []
VP = []

def VP_button(vol, button):
    global VP #needed to provide update out of scope of function

    if vol in VP:
        VP.remove(vol)
        button.config(relief=tk.RAISED)

    else:
        VP.append(vol)
        button.config(relief=tk.SUNKEN)

    print(VP)

def VF_button(vol, button):
    global VF #needed to provide update out of scope of function

    if vol in VF:
        VF.remove(vol)
        button.config(relief=tk.RAISED)

    else:
        VF.append(vol)
        button.config(relief=tk.SUNKEN)

    print(VF)

"""DECLARING COMPUTATIONAL FUNCTIONS"""

def create_glassware_dictionaries(VP, vp_error, VF, vf_error): 
    vp_dict = {}
    vf_dict = {}

    for vp in VP:

        #checking for valid entries
        if vp < vp_min or vp > vp_max:
            print("gw dict error on creation, vp out of range")
            break

        #finding absolute error for vp 
        if vp in vp_error:
            error = vp_error[vp]
            vp_dict[vp] = error

        #else to estimate error if volume not in error list
        else:
            higher_list = []
            for vol, err in vp_error.items():
                if vol > vp:
                    higher_list.append(vol)
            min_high_vol = min(higher_list)

            vp_dict[vp] = vp_error[min_high_vol]
            print("pipette", vp, "has estimated error")

    for vf in VF:

        #checking for valid entries
        if vf < vf_min or vf > vf_max:
            print("gw_dict error on creation, vf out of range")

        #finding absolute error for vf
        if vf in vf_error:
            error = vf_error[vf]
            vf_dict[vf] = error

        #else to estimate error if volume not in error list
        else:
            higher_list = []
            for vol, err in vf_error.items():
                if vol > vf:
                    higher_list.append(vol)
            min_high_vol = min(higher_list)

            vf_dict[vf] = vf_error[min_high_vol]
            print("flask", vf, "has estimated error")

    #deletes volumes lower than required volume
    vf_check_list = []
    for vf, error in vf_dict.items():
        if vf < required_volume:
            vf_check_list.append(float(vf))

    for v in vf_check_list:
        del vf_dict[v]

    return vp_dict, vf_dict

def create_glassware(vp_dict, vf_dict):
    vp_instances = [VG(volume, 'VP', error) for volume, error in vp_dict.items()]
    vf_instances = [VG(volume, 'VF', error) for volume, error in vf_dict.items()]

    return vp_instances, vf_instances

def create_dilutions(vp_instances, vf_instances):
    dilution_instances = []
    #note to self - does it make sense to organize this
    #nested list another way?
    dil_index = 1
    for vp_instance in vp_instances:
        for vf_instance in vf_instances:
            if vf_instance.volume > vp_instance.volume:
                dilution_factor = vp_instance.volume / vf_instance.volume

                error = dilution_factor * math.sqrt(
                    (vp_instance.error / vp_instance.volume)**2 +
                    (vf_instance.error / vf_instance.volume)**2
                )

                dilution_instance = dilutions(
                    VP_vol=vp_instance.volume,
                    VF_vol=vf_instance.volume,
                    dilution_factor=dilution_factor,
                    error=error
                )

                dilution_instances.append(dilution_instance)

    return dilution_instances

def create_dilution_dictionary(dilution_instances):

    # contraint 1 - max available stock conc.
    min_conc = min(target_list)
    max_conc = max(target_list)
    min_df = (min(dilution_instances, key=lambda d: 
                    d.dilution_factor).dilution_factor)
    max_df = (max(dilution_instances, key=lambda d: 
                    d.dilution_factor).dilution_factor)

    max_material = (material_available - 
                (material_available * (dead_wt/100)))
    min_conc = min(target_list)
    min_df = (min(dilution_instances, key=lambda d: 
                d.dilution_factor).dilution_factor)
    upper_stock_conc = (min_conc / min_df)
    max_stock_conc = (min(upper_stock_conc, max_material))
    
    """
    if stock_binary == 1:
        
        #stock conc is max conc by definition
        min_stock_conc = max_conc
    """
    #if stock is only stock
    if stock_binary == 0:
        #x where x*max_df=max_conc
        min_stock_float = (max_conc / max_df)
        min_stock_conc = math.ceil(min_stock_float)

    #dictionary creation
    dilution_dictionary = {}
    top = int(max_stock_conc)
    bottom = int(min_stock_conc)
    for i in range(top, bottom, -1,):

        stock_conc = i
        check_conc_list = []
        check_dilution_list = []

        for dilution in dilution_instances:
            conc = (stock_conc * dilution.dilution_factor)
            vf = dilution.VF_vol

            """and statement exlcludes dilutions at target level using
            VF defined unusuable by exl_dict
            may not need"""
            if conc in target_list:                             
                check_conc_list.append(conc)
                check_dilution_list.append(dilution)

        if all(elem in check_conc_list for elem in target_list):
            dilution_dictionary[stock_conc] = check_dilution_list

    """This shoudl be unit tested
    exclusing some values"""

    #Loop 2 - calculating exlusion list
    exclusion_list = []
    percentage_available = float((100 - dead_wt) / 100)
    usable_material = material_available * percentage_available

    for stock_conc, dilutions in dilution_dictionary.items():
        if stock_conc > usable_material and stock_conc not in exclusion_list:
            exclusion_list.append(stock_conc)

    #Loop 3 - Removing exlusion values from dilution_dictionary
    for exclusion_conc in exclusion_list:
        del dilution_dictionary[exclusion_conc]

    return dilution_dictionary

def create_iteration_dictionary(target_list, dilution_dictionary):
    iteration_dictionary = {}

    #for every stock conc
    for stock_conc, dilution_instances in dilution_dictionary.items():
        all_lists = [[] for _ in range(len(target_list))]

        #for every diluted conc
        count = 0
        for current_target in target_list:
            single_target_list = all_lists[count]

            #confirming if diluted conc matched target
            for dilution_instance in dilution_instances:
                concentration = stock_conc * dilution_instance.dilution_factor

                #INDEX ADDED 01/20/2024
                if concentration == current_target:
                    single_target_list.append(dilution_instance)

            count = count + 1

        iteration_dictionary[stock_conc] = all_lists

    return iteration_dictionary


"DECLARING COMPUTATIONAL CLASSES"

class VG:
    def __init__(self, volume, style, error):
        self.volume = volume
        self.style = style
        self.error = error
        self.deadvol = volume*(dead_vol/100)
        
        if style in ["VF", "VP"]:
            self.style = style
        else:
            raise ValueError("Invalid style. Style must be 'VF' or 'VP'.")
    
    #function to set the volume of an instance
    def set_volume(self, volume):
        self.volume = volume
    
    #validation of style type
    def set_style(self, style):
        if style in ["VF", "VP"]:
            self.style = style
        else:
            raise ValueError("Invalid style. Style must be 'VF' or 'VP'.")
    
    #set error based off volume and type
    def set_errorA(self, errorA):
        self.errorA = errorA
        
class dilutions:
    index_counter = 1 #initiate index counter
    
    def __init__(self, VP_vol, VF_vol, dilution_factor, error):
        self.index = dilutions.index_counter 
        dilutions.index_counter +=1
        
        self.dilution_factor = (VP_vol/VF_vol)
        self.VP_vol = VP_vol
        self.VF_vol = VF_vol
        self.error = error
        
    def __iter__(self):
        # Define the attributes you want to iterate over
        yield self.index
        yield self.VP_vol
        yield self.VF_vol
        yield self.dilution_factor
        yield self.error

class StandardHelperApp():
    def __init__(self, master):
        self.master = master
        self.master.title("The Standard Helper")
        self.initial_gui()
    
    """ create new class instance for each subgrid element
    class Volumetric_Flasks(): #(0,0)
        def__init__(master, )
    
    class Volumetric_Pipettes(): #(0,1)"""
    
    def initial_gui(self):
        """GRID WITH 4x4 SUBGRID"""
        # Create main grid frame
        grid_frame = tk.Frame(self.master)
        grid_frame.grid(row=0, column=0)
        
        def input_errors(VP, VF, entry_list):

            if VP is None or len(VP)==0:
                print("Null VP list used")
                VP = null_vp_list

            if VF is None or len(VF)==0:
                print("Null VF list used")
                VF = null_vf_list
            """
            for e in entry_list:
                contents = e.get()
                print(contents)"""

        def comp_chain(VP, vp_error, VF, vf_error):

            input_errors(VP, VF, entry_list)

            vp_dict, vf_dict = create_glassware_dictionaries(VP, vp_error, VF, vf_error)
            vp_instances, vf_instances = create_glassware(vp_dict, vf_dict)
            dilution_instances = create_dilutions(vp_instances, vf_instances)
            dilution_dictionary = create_dilution_dictionary(dilution_instances)
            iteration_dictionary = create_iteration_dictionary(target_list, dilution_dictionary)

            return(iteration_dictionary)

        # Create the subgrid frames
        VF_subgrid = tk.Frame(grid_frame, borderwidth=2, relief="solid", width=200, height=200)
        VF_subgrid.grid(row=1, column=0, padx=5, pady=5)
        VP_subgrid = tk.Frame(grid_frame, borderwidth=2, relief="solid", width=200, height=200)
        VP_subgrid.grid(row=1, column=1, padx=5, pady=5)
        user_grid = tk.Frame(grid_frame, borderwidth=2, relief="solid", width=200, height=200)
        user_grid.grid(row=2, column=0, padx=5, pady=5)
        action_grid = tk.Frame(grid_frame, borderwidth=2, relief="solid", width=200, height=200)
        action_grid.grid(row=2, column=1, padx=5, pady=5)

        """HEADERS"""
        # Create header frames
        header_frame1 = tk.Frame(grid_frame)
        header_frame1.grid(row=0, column=0)
        header_frame2 = tk.Frame(grid_frame)
        header_frame2.grid(row=0, column=1)

        # Create header labels
        vf_header_label = tk.Label(header_frame1, text="Volumetric Flasks", font=("Arial", 12, "bold"))
        vf_header_label.pack(pady=5)
        vp_header_label = tk.Label(header_frame2, text="Volumetric Pipettes", font=("Arial", 12, "bold"))
        vp_header_label.pack(pady=5)
        
        """INIT OF USER SUBGRID"""
        # variable assigment - user entries
        entry1 = tk.Entry(user_grid)
        entry2 = tk.Entry(user_grid)
        entry3 = tk.Entry(user_grid)
        entry4 = tk.Entry(user_grid)
        entry5 = tk.Entry(user_grid)
        entry6 = tk.Entry(user_grid)

        # formats user entry points
        entry1.grid(row=0, column=1, padx=5, pady=5)
        entry2.grid(row=1, column=1, padx=5, pady=5)
        entry3.grid(row=2, column=1, padx=5, pady=5)
        entry4.grid(row=3, column=1, padx=5, pady=5)
        entry5.grid(row=4, column=1, padx=5, pady=5)
        entry6.grid(row=5, column=1, padx=5, pady=5)

        global entry_list
        entry_list = [entry1, entry2, entry3, entry4, entry5, entry6]  
        
        # automatically generates & label for user entries
        labels_text = ["Target List (ug/mL)", "Diluent Volume (mL)", "Standard Weight (µg)", 
                       "Standard Volume Required (mL)","Dead Volume (%)", "Dead Weight (%)"]
        
        for i, label_text in enumerate(labels_text):
            label = tk.Label(user_grid, text=label_text, bg='light blue', 
                             font=('Arial', 10, 'bold'))
            label.grid(row=i, column=0, padx=5, pady=5, sticky=tk.E)

            text_box = tk.Entry(user_grid)
            text_box.grid(row=i, column=1, padx=5, pady=5)

        """INIT OFA ACTION SUBGRID"""
        
        compute_stocks = tk.Button(action_grid, text="Find Stock Standard Solutions", 
                                       command=lambda: comp_chain(VP, vp_error, VF, vf_error))
        compute_stocks.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        
            
        #VP Buttons
        vp_b1 = tk.Button(VP_subgrid, text="0.5", width=10, height=2)
        vp_b2 = tk.Button(VP_subgrid, text="1", width=10, height=2)
        vp_b3 = tk.Button(VP_subgrid, text="1.5", width=10, height=2)
        vp_b4 = tk.Button(VP_subgrid, text="2", width=10, height=2)
        vp_b5 = tk.Button(VP_subgrid, text="2.5", width=10, height=2)
        vp_b6 = tk.Button(VP_subgrid, text="3", width=10, height=2)
        vp_b7 = tk.Button(VP_subgrid, text="4", width=10, height=2)
        vp_b8 = tk.Button(VP_subgrid, text="5", width=10, height=2)
        vp_b9 = tk.Button(VP_subgrid, text="6", width=10, height=2)
        vp_b10 = tk.Button(VP_subgrid, text="7", width=10, height=2)
        vp_b11 = tk.Button(VP_subgrid, text="8", width=10, height=2)
        vp_b12 = tk.Button(VP_subgrid, text="9", width=10, height=2)
        vp_b13 = tk.Button(VP_subgrid, text="10", width=10, height=2)
        vp_b14 = tk.Button(VP_subgrid, text="15", width=10, height=2)
        vp_b15 = tk.Button(VP_subgrid, text="20", width=10, height=2)
        vp_b16 = tk.Button(VP_subgrid, text="25", width=10, height=2)
        vp_b17 = tk.Button(VP_subgrid, text="30", width=10, height=2)
        vp_b18 = tk.Button(VP_subgrid, text="40", width=10, height=2)
        vp_b19 = tk.Button(VP_subgrid, text="50", width=10, height=2)
        vp_b20 = tk.Button(VP_subgrid, text="100", width=10, height=2)

        # place all VP buttons in the subframe (4x5 grid)
        vp_b1.grid(row=0, column=0, padx=5, pady=5)
        vp_b2.grid(row=0, column=1, padx=5, pady=5)
        vp_b3.grid(row=0, column=2, padx=5, pady=5)
        vp_b4.grid(row=0, column=3, padx=5, pady=5)
        vp_b5.grid(row=0, column=4, padx=5, pady=5)
        vp_b6.grid(row=1, column=0, padx=5, pady=5)
        vp_b7.grid(row=1, column=1, padx=5, pady=5)
        vp_b8.grid(row=1, column=2, padx=5, pady=5)
        vp_b9.grid(row=1, column=3, padx=5, pady=5)
        vp_b10.grid(row=1, column=4, padx=5, pady=5)
        vp_b11.grid(row=2, column=0, padx=5, pady=5)
        vp_b12.grid(row=2, column=1, padx=5, pady=5)
        vp_b13.grid(row=2, column=2, padx=5, pady=5)
        vp_b14.grid(row=2, column=3, padx=5, pady=5)
        vp_b15.grid(row=2, column=4, padx=5, pady=5)
        vp_b16.grid(row=3, column=0, padx=5, pady=5)
        vp_b17.grid(row=3, column=1, padx=5, pady=5)
        vp_b18.grid(row=3, column=2, padx=5, pady=5)
        vp_b19.grid(row=3, column=3, padx=5, pady=5)
        vp_b20.grid(row=3, column=4, padx=5, pady=5)

            # VF buttons
        vf_b1 = tk.Button(VF_subgrid, text="1", width=10, height=2)
        vf_b2 = tk.Button(VF_subgrid, text="2", width=10, height=2)
        vf_b3 = tk.Button(VF_subgrid, text="5", width=10, height=2)
        vf_b4 = tk.Button(VF_subgrid, text="10", width=10, height=2)
        vf_b5 = tk.Button(VF_subgrid, text="20", width=10, height=2)
        vf_b6 = tk.Button(VF_subgrid, text="25", width=10, height=2)
        vf_b7 = tk.Button(VF_subgrid, text="50", width=10, height=2)
        vf_b8 = tk.Button(VF_subgrid, text="100", width=10, height=2)
        vf_b9 = tk.Button(VF_subgrid, text="200", width=10, height=2)
        vf_b10 = tk.Button(VF_subgrid, text="250", width=10, height=2)
        vf_b11 = tk.Button(VF_subgrid, text="500", width=10, height=2)
        vf_b12 = tk.Button(VF_subgrid, text="1000", width=10, height=2)

        # place all VF buttons in the subframe (4x3 grid)
        vf_b1.grid(row=0, column=0, padx=5, pady=5)
        vf_b2.grid(row=0, column=1, padx=5, pady=5)
        vf_b3.grid(row=0, column=2, padx=5, pady=5)
        vf_b4.grid(row=1, column=0, padx=5, pady=5)
        vf_b5.grid(row=1, column=1, padx=5, pady=5)
        vf_b6.grid(row=1, column=2, padx=5, pady=5)
        vf_b7.grid(row=2, column=0, padx=5, pady=5)
        vf_b8.grid(row=2, column=1, padx=5, pady=5)
        vf_b9.grid(row=2, column=2, padx=5, pady=5)
        vf_b10.grid(row=3, column=0, padx=5, pady=5)
        vf_b11.grid(row=3, column=1, padx=5, pady=5)
        vf_b12.grid(row=3, column=2, padx=5, pady=5)

        vp_b1.configure(command=lambda: VP_button(0.5, vp_b1))
        vp_b2.configure(command=lambda: VP_button(1, vp_b2))
        vp_b3.configure(command=lambda: VP_button(1.5, vp_b3))
        vp_b4.configure(command=lambda: VP_button(2, vp_b4))
        vp_b5.configure(command=lambda: VP_button(2.5, vp_b5))
        vp_b6.configure(command=lambda: VP_button(3, vp_b6))
        vp_b7.configure(command=lambda: VP_button(4, vp_b7))
        vp_b8.configure(command=lambda: VP_button(5, vp_b8))
        vp_b9.configure(command=lambda: VP_button(6, vp_b9))
        vp_b10.configure(command=lambda: VP_button(7, vp_b10))
        vp_b11.configure(command=lambda: VP_button(8, vp_b11))
        vp_b12.configure(command=lambda: VP_button(9, vp_b12))
        vp_b13.configure(command=lambda: VP_button(10, vp_b13))
        vp_b14.configure(command=lambda: VP_button(15, vp_b14))
        vp_b15.configure(command=lambda: VP_button(20, vp_b15))
        vp_b16.configure(command=lambda: VP_button(25, vp_b16))
        vp_b17.configure(command=lambda: VP_button(30, vp_b17))
        vp_b18.configure(command=lambda: VP_button(40, vp_b18))
        vp_b19.configure(command=lambda: VP_button(50, vp_b19))
        vp_b20.configure(command=lambda: VP_button(100, vp_b20))

        vf_b1.configure(command=lambda: VF_button(1, vf_b1))
        vf_b2.configure(command=lambda: VF_button(2, vf_b2))
        vf_b3.configure(command=lambda: VF_button(5, vf_b3))
        vf_b4.configure(command=lambda: VF_button(10, vf_b4))
        vf_b5.configure(command=lambda: VF_button(20, vf_b5))
        vf_b6.configure(command=lambda: VF_button(25, vf_b6))
        vf_b7.configure(command=lambda: VF_button(50, vf_b7))
        vf_b8.configure(command=lambda: VF_button(100, vf_b8))
        vf_b9.configure(command=lambda: VF_button(200, vf_b9))
        vf_b10.configure(command=lambda: VF_button(250, vf_b10))
        vf_b11.configure(command=lambda: VF_button(500, vf_b11))
        vf_b12.configure(command=lambda: VF_button(1000, vf_b12))
    
        # init of GUI - each lime could be independantly called as self. instead of a function on self

root = tk.Tk()
app = StandardHelperApp(root)
root.mainloop()
