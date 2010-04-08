class CSettings:

    def __init__(self):
        self.LineColor = "#00FF00"
        self.LineSize = 3
    
    def setValues(self,color,size):
        self.LineColor = color        
        self.LineSize = size
    
    def setDefaultValues(self):
        self.LineColor = "#00FF00"
        self.LineSize = 3
    
        