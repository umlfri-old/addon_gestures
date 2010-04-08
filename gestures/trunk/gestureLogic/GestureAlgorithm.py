#interface pre lubovolny algoritmus na rozoznavanie gest polohovacim zariadenim
class CGestureAlgorithm:
    #konstruktor
    def __init__(self):
        #nazov algoritmu
        self.name = ""
        #id algoritmu
        self.algorithmID = 0
        #zoznam suradnic gesta
        self.coordinates = [ () ]
        #zoznam vzorovych gest
        self.patternGestures = []
        
    #algoritmus, ktory vrati rozoznane gesto, diagram je typ diagramu, v ktorom rozoznavame, type je typ gesta, ci sa jedna o spojenie, element... 
    def Recognition(self,diagram,type):
        return None
    