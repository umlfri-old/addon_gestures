from GestureSet import CGestureSet
from Gesture import CGesture
import os,glob

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
        self.loadGestures()
        
    #nacita gesta daneho algoritmu do pamate
    def loadGestures(self): 
        for path in glob.glob(os.path.join(self.directory, '*.*')):
            a = CGesture(self.id,path)
            for i in range(len(a.description)):
                a.description[i].gestureSize = self.boxsize
                a.FillDescription()
                self.gestures.append(a)
        