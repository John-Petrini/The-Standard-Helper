dead_vol_default = 30

class VolumetricGlass:
    
    def __init__(self, volume, style, error):
        self.volume = volume
        self.style = style
        self.error = error
        self.deadvol = volume * (dead_vol_default / 100)
        
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