from GestureSet import CGestureSet
from Gesture import CGesture
import os

#kolekcia gest daneho typu
class CBoundaryGestureSet(CGestureSet):
    #konstruktor
    def __init__(self,id,boxsize):
        #id typu algoritmu, ktoreho vzorky budu nacitane
        self.id = id
        #velkost mriezky
        self.boxsize = boxsize
        #vzorove gesta        
        self.gestures = []
        self.directory = "gestureDefinitions"
        self.loadGesturesFromDirectory()
        
    #nacita gesta daneho algoritmu do pamate
    def loadGesturesFromDirectory(self):      
        ces = os.path.join(os.path.dirname(__file__), "gestureDefinitions")+"//"
        for path in os.listdir(ces):
            if path[0]!='.':
                a = CGesture(self.id,ces+path)
                for i in range(len(a.description)):
                    a.description[i].gestureSize = self.boxsize
                a.FillDescription()
                self.gestures.append(a)
                
    def loadGesturesFromMetamodel(self,xmlFiles):
        for j in xmlFiles:
            a = CGesture(self.id,j)
            a.ParseXMLFromString(j)
            for i in range(len(a.description)):
                a.description[i].gestureSize = self.boxsize
            a.FillDescription()
            self.gestures.append(a)
                