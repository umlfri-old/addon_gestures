from GestureSet import CGestureSet
from Gesture import CGesture
import os

class CBoundaryGestureSet(CGestureSet):
    """
    Collection of gestures specified with Boundary Box algorithm.
    """
    
    #konstruktor
    def __init__(self,id,boxsize):
        """
        Constructor of class CBoundaryGestureSet.
        
        @type  id: int
        @param id: algorithm id
        @type  boxsize: int
        @param boxsize: size of gesture box
        """
        #algorithm id
        self.id = id
        #gesture box size
        self.boxsize = boxsize
        #collection of gestures
        self.gestures = []
    
    def LoadGesturesFromDirectory(self):
        """
        Load gestures from directory.
        """
        ces = os.path.join(os.path.dirname(__file__), 'gestureDefinitions')+'\\'
        for path in os.listdir(ces):
            if path[0] != '.':
                a = CGesture(self.id,ces+path)
                for i in range(len(a.description)):
                    a.description[i].gestureSize = self.boxsize
                a.FillDescription()
                self.gestures.append(a)
    
    def LoadGesturesFromMetamodel(self,xmlFiles,bool):
        """
        Load gestures from metamodel.
        """
        if bool == False:
             del self.gestures[:]
             return
        for j in xmlFiles:
            a = CGesture(self.id,j)
            a.ParseXMLFromString(j)
            for i in range(len(a.description)):
                a.description[i].gestureSize = self.boxsize
            a.FillDescription()
            self.gestures.append(a)
    
    def GetId(self):
        """
        Algorithm ID getter.
        
        @rtype : int
        @return: algorithm ID
        """
        return self.id
    
    def GetBoxsize(self):
        """
        Box size getter.
        
        @rtype : int
        @return: box size
        """
        return self.boxsize