from Gesture import CGesture

#kolekcia gest daneho typu
class CGestureSet:
    #konstruktor
    def __init__(self,id):        
        #id typu algoritmu, ktoreho vzorky budu nacitane
        self.id = id
        #vzorove gesta
        self.gestures = []
        #cesta adresara, kde su popisy gest
        self.directory = "gestureDefinitions"
        #nacitanie gest do kolekcie
        self.loadGestures()
        
    #nacita gesta daneho algoritmu do pamate
    def loadGestures(self):
        path = ""
        a = CGesture(self.id,path)
        self.gestures.append(a)
        return None
    