class CDescription(object):
    """
    Interface for gesture description.
    """

    def __init__(self,id):
        """
        Constructor of class CDescription.
        
        @type  id: int
        @param id: algorithm id
        """
        self.id = id
    
    #naplni atributy datami o geste
    def ParseXML(self):
        """
        Fill attributes from XML file.
        """
        pass