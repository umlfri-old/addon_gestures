from GestureAlgorithm import CGestureAlgorithm
from BoundaryGestureSet import CBoundaryGestureSet

#Boundary Box algoritmus na rozoznavanie gest
class CBoundaryAlgorithm(CGestureAlgorithm):
    #konstruktor
    def __init__(self, size = 5):
        #nazov algoritmu
        self.name = "Boundary Box Algorithm"
        #id algoritmu
        self.algorithmID = 1
        #velkost mriezky
        self.boxsize = size
        #mriezka
        self.box = []
        #Nainicializuj mriezku
        self.BoxInitialization()
        #Nahraj vzorove gesta
        self.patternGestures = CBoundaryGestureSet(self.algorithmID,self.boxsize)

    #Vytvorenie prazdnejmriezky
    def BoxInitialization(self):
        for i in range(self.boxsize):
            row = []
            for j in range(self.boxsize):
                row.append(0)
            self.box.append(row)
    
    #Vycistenie mriezky
    def ClearBox(self):
        for i in range(3):
            for j in range(self.boxsize):
                self.box[i][j] = 0
    
    #algoritmus, ktory vrati rozoznane gesto, diagram je typ diagramu, v ktorom rozoznavame, type je typ gesta, ci sa jedna o spojenie, element... 
    def Recognition(self,diagram,type):
        return None
