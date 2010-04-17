import os.path
from lxml import etree
import xml.etree.ElementTree as etree
from BoundaryAlgorithm import CBoundaryAlgorithm
import math

class CGestureManager(object):
    def __init__(self):
        self.helpCoord = []
        self.coord = []
        self.alg = CBoundaryAlgorithm()
        self.dic = []        
        self.deleteConnectionCount = 8
        self.deleteConnectionDistance = 10
        self.result = []
        
    #Pomocna metoda pri rozliseni typu gesta
    def FindOutGestureType(self):
        isHigher = False
        pocC = 0
        self.deletePoints = []
        spojenie = False
        for i in self.helpCoord:
            if i[2] == 'AC':
                self.deletePoints.append(i)
        if len(self.deletePoints) >= self.deleteConnectionCount:            
            for i in range(len(self.deletePoints)):
                for j in range(len(self.deletePoints)):
                    roz = math.sqrt(math.fabs(self.deletePoints[i][0]-self.deletePoints[j][0])+
                          math.fabs(self.deletePoints[i][1]-self.deletePoints[j][1]))
                    if roz > self.deleteConnectionDistance:
                        isHigher = True
            if isHigher == False:
                self.result.append('delete connection')
                self.result.append([self.deletePoints[0][0],self.deletePoints[0][1]])
                return        
        for i in self.helpCoord:
            if i[2] == 'V':
                spojenie = True        
        if spojenie == False:
            self.result.append('element')
            return                                                                                         
        for i in self.helpCoord:                    
            if i[2] == 'X':
                self.result.append('connection')                
                self.helpCoord.insert(self.helpCoord.index(i)+1, ['x','x','x'])
                for j in self.helpCoord:                                
                    if j[2] == 'P':
                        self.helpCoord.insert(self.helpCoord.index(j)+1, ['p','p','p'])                                                                
                break                   
                         
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
        self.result = []        
        self.FindOutGestureType()
        print self.result
        if self.result[0] == 'delete connection':
            return self.result
        self.CreateCoordinates()
        a = self.alg.Recognition(self.result)
        if a[0] == 'unknown':
            return a
        if a[0] == 'system':
            return a
        if a[0] == 'delete element':
            if self.helpCoord[0][2] != 'AE':
                a[0] = 'unknown'             
            return a
        if a[0] == 'element':
            bool = False
            for i in self.dic:
                if i[1]==a[1]:
                    bool = True                    
                    a.append(('Element',i[0]))
                    return a
            if bool == False:
                a[0] = 'unknown'             
                return a    
        if a[0] == 'connection':
            bool = False
            for i in self.dic:
                if i[1]==a[1]:
                    bool = True           
                    print a         
                    a.append(('Connection',i[0]))
                    return a
            if bool == False:
                a[0] = 'unknown'             
                return a    