from Gesture import CGesture

#kolekcia gest daneho typu
class CGestureSet(object):
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
    def LoadGestures(self):
        pass
    
    def GetGestures(self):
        return self.gestures
    
    def GetGesture(self,ind):
        return self.gestures[ind]
    
    
    
    