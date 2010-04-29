from Gesture import CGesture

class CGestureSet(object):
    """
    Collection of gestures.
    """
    
    #konstruktor
    def __init__(self,id):
        """
        Constructor of class CGestureSet.
        
        @type  id: int
        @param id: algorithm id
        """
        #algorithm id
        self.id = id
        #collection of gestures
        self.gestures = []
        #directory in which are XML files
        self.directory = 'gestureDefinitions'
        #loading gestures to collection
        self.loadGestures()
    
    def LoadGestures(self):
        """
        Load gestures to collection.
        """
        pass
    
    def GetGestures(self):
        """
        Gestures getter.
        
        @rtype : list
        @return: returns list of gestures(CGestures)
        """
        return self.gestures
    
    def GetGesture(self,ind):
        """
        Returns specific gesture.
        
        @type ind: int
        @param ind: index in list
        @rtype : CGesture
        @return: return gesture with specified id
        """
        return self.gestures[ind]