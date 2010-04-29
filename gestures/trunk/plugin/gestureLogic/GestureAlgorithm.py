class CGestureAlgorithm(object):
    """
    Interface for any recognition algorithm.
    """
    
    def __init__(self):
        """
        Constructor of class CGestureAlgorithm.
        """
        #algorithm name
        self.name = ''
        #algorithm ID
        self.algorithmID = 0
        #current gesture coordinates
        self.coordinates = []
        #well known gestures(CGestureSet)
        self.patternGestures = []
    
    def Recognition(self,type):
        """
        Function which recognize gesture.
        
        @type  type: string
        @param type: gesture type
        """
        pass
    
    def SetCoordinates(self,coor):
        """
        Coordinates setter.
        
        @type  coor: list
        @param coor: gesture coordinates
        """
        self.coordinates = coor
    
    def GetCoordinates(self):
        """
        Coordinates getter
        
        @rtype : list
        @return: gesture coordinates
        """
        return self.coordinates
    
    def DeleteCoordinates(self):
        """
        Delete current coordinates.
        """
        del self.coordinates[:]