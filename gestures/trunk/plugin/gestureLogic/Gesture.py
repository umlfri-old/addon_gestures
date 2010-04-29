from lxml import etree
from BoundaryDescription import CBoundaryDescription

class CGesture(object):
    """
    Class gesture it can be used with any recognition algorithm.
    """
    
    def __init__(self,algorithm,path):
        """
        Constructor of class CGesture.
        
        @type  algorithm: int
        @param algorithm: algorithm id
        @type  path: string
        @param path: path to XML file
        """
        #algorithm id
        self.algorithm = algorithm
        #gesture name
        self.name = ""
        #gesture type(element, connection, system)
        self.gestureType = ""
        #path to XML file
        self.xmlFile = path
        #gesture descriptions(CDescription), one gesture can have more than one description
        self.description = []
              
    #Popise gesto do vytvoreneho popisu
    def FillDescription(self):
        """
        Create gesture box from loaded XML file in descriptions.
        """
        if (self.algorithm == 1):
            for i in range(len(self.description)):
                self.description[i].CreateGestureBox()
    
    #naplni atributy datami o geste parsovanim XML suboru
    def ParseXMLFromFile(self,xmlFile):
        """
        Fill attributes by parsing from XML file.
        """
        tree = etree.parse(xmlFile)
        self.ParseXML(tree.getroot())

    def ParseXMLFromString(self,paStr):
        """
        Fill attributes by parsing from metamodel.
        """
        self.ParseXML(etree.fromstring(paStr))

    def ParseXML(self,root):
        """
        Parse from root element.
        
        @type  root: Element
        @param root: root element
        """
        self.name = root.get('name')
        self.gestureType = root.get('type')
        #recognition algorithm parsing
        for i in range(len(root)):
            if (root[i].get('name') == 'Boundary Box Algorithm'):
                for j in range(len(root[i])):
                    lines = []
                    for k in range(len(root[i][j])):
                        coordinate = []
                        coordinate.append(root[i][j][k].get('from'))
                        coordinate.append(root[i][j][k].get('to'))
                        lines.append(coordinate)
                    des = CBoundaryDescription(1,lines)
                    self.description.append(des)
    
    def GetName(self):
        """
        Gesture name getter.
        
        @rtype : string
        @return: gesture name
        """
        return self.name
    
    def GetDescriptions(self):
        """
        Gesture descriptions getter.
        
        @rtype : list
        @return: gesture descriptions(CDescription)
        """
        return self.description