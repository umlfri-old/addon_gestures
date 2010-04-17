from lxml import etree
import xml.etree.ElementTree as etree
from BoundaryDescription import CBoundaryDescription

#Gesto zadefinovane lubovolnym algoritmom
class CGesture(object):
    #konstruktor
    def __init__(self,algorithm,path):
        #id pouziteho algoritmu
        self.algorithm = algorithm
        #nazov gesta
        self.name = ""
        #typGesta (element, spojenie, systemove gesto)
        self.gestureType = ""
        #xml s popisomGesta
        self.xmlFile = path
        #akcia spojena s vyskytom gesta
        self.action = ""
        #popisy daneho gesta
        self.description = [] 
        #nacitaj udaje z xml suboru
        self.ParseXMLFromFile(self.xmlFile)
        #self.ParseXMLFromString(path)
              
    #Popise gesto do vytvoreneho popisu
    def FillDescription(self):
        if (self.algorithm == 1):
            for i in range(len(self.description)):
                self.description[i].CreateGestureBox()
                
    #naplni atributy datami o geste parsovanim XML suboru
    def ParseXMLFromFile(self,xmlFile):        
        tree = etree.parse(xmlFile)
        self.ParseXML(tree.getroot())        

    def ParseXMLFromString(self,paStr):
        self.ParseXML(etree.fromstring(paStr))

    def ParseXML(self,root):
        #parsovanie korenoveho elementu
        self.name = root.get("name")
        self.gestureType = root.get("type")                            
        #parsovanie algoritmov    
        for i in range(len(root)):
            if (root[i].get("name")=="Boundary Box Algorithm"):
                for j in range(len(root[i])):
                    lines = []
                    for k in range(len(root[i][j])):
                        coordinate = []
                        coordinate.append(root[i][j][k].get("from"))
                        coordinate.append(root[i][j][k].get("to"))
                        lines.append(coordinate)
                    des = CBoundaryDescription(1,lines)  
                    self.description.append(des)    
                
    def GetName(self):
        return self.name