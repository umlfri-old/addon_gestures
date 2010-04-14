import os.path
from lxml import etree
import xml.etree.ElementTree as etree
from BoundaryAlgorithm import CBoundaryAlgorithm

class CGestureManager(object):
    def __init__(self):
        self.helpCoord = []
        self.coord = []
        self.alg = CBoundaryAlgorithm()
        self.dic = []        
        
    def FindOutGestureType(self):
        self.type = ""
        pocet = 0
        pocNE = 0
        pocC = 0
        self.coordinatesC = []
        print self.helpCoord
        for i in self.helpCoord:                        
            if i[2] != 'N':
                pocet = pocet+1
            if i[2] != 'AE':
                pocNE = pocNE+1
            if i[2] == 'AC':
                self.coordinatesC.append(i);
                pocC = pocC + 1
            
        if pocet == len(self.helpCoord):            
            self.type = 'delete element'        
                
        if pocNE == len(self.helpCoord) and pocC >=2:
            self.type = 'delete connection'
            return
        
        if self.type !='delete element':
            for i in self.helpCoord:                    
                if i[2] == 'X':
                    self.type = 'connection'                
                    self.helpCoord.insert(self.helpCoord.index(i)+1, ['x','x','x'])
                    for j in self.helpCoord:                                
                        if j[2] == 'P':
                            self.helpCoord.insert(self.helpCoord.index(j)+1, ['p','p','p'])                                                                
                    break                   
            if self.type !='connection':
                self.type = 'element or system'
        print self.type
                         
    def SetCoord(self,pix):
        self.helpCoord = pix
    
    def CreateCoordinates(self):
        for i in self.helpCoord:
            self.coord.append((i[0],i[1]))
        self.alg.SetCoordinates(self.coord)        
    
    def DeleteCoordinates(self):
        self.helpCoord = []
        self.coord = []        
        
    def CreateDictionary(self,ele,con):
        del self.dic[:]
        if len(ele)>0:        
            for i in ele:
                self.dic.append([i,''])
        if len(con)>0:        
            for i in con:
                self.dic.append([i,''])
                
        ces = os.path.join(os.path.dirname(__file__), "gestures")+"//"                                                
        for path in os.listdir(ces):
            if path[0]!= '.':
                tree = etree.parse(ces+path)
                root = tree.getroot()
                ele = root.get("objectID")
                gest = root[0].get("name")
                for i in self.dic:
                    if i[0] == ele:
                        i[1] = gest    
    
    def Recognize(self):
        self.FindOutGestureType()
        self.CreateCoordinates()
       # print self.dic                
        a = self.alg.Recognition(self.type)
        if a[0] == 'delete element':
            return a        
        if a[0] == 'delete connection':
            a.append(self.coordinatesC[0])
            return a
        if a[0] == 'element':
            bool = False
            for i in self.dic:
                if i[1]==a[1]:
                    bool = True                    
                    a.append(('Element',i[0]))
                    return a
            if bool == False:
                del a[:]
                a.append('error')
                return a            
        if a[0] == 'connection':
            bool = False
            for i in self.dic:
                if i[1]==a[1]:
                    bool = True                    
                    a.append(('Connection',i[0]))
                    return a
            if bool == False:
                del a[:]
                a.append('error')
                return a            
        #del a[:]                 
        #a.append('error')
        return a
    