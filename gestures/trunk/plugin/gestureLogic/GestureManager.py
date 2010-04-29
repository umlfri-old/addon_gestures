from lxml import etree
import math
import os.path

from BoundaryAlgorithm import CBoundaryAlgorithm

class CGestureManager(object):
    """
    Gesture manager takes care about choosing recognition algorithm and
    provides coordinates this algorithm.
    """
    
    def __init__(self):
        """
        Constructor of class CGestureManager.
        """
        #help coordinates with symptom
        self.helpCoord = []
        #coordinates send to recognition algorithm
        self.coord = []
        #recognition algorithm
        self.alg = CBoundaryAlgorithm()
        #dictionary (element and connection name : gesture name)
        self.dic = []
        #minimum symptoms for deleting connection
        self.deleteConnectionCount = 8
        #maximum gesture distance when deleting connection
        self.deleteConnectionDistance = 10
        #result of recognition
        self.result = []
    
    #Pomocna metoda pri rozliseni typu gesta
    def FindOutGestureType(self):
        """
        Help method for dividing gesture to group(element,connection,delete connection)
        """
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
                return
        del self.result[:]
        self.result.append('unknown')
        return
    
    def SetCoord(self,pix):
        """
        Coordinates setter.
        
        @type  pix: list
        @param pix: list of coordinates
        """
        self.helpCoord = pix
    
    def CreateCoordinates(self):
        """
        Create coordinates from help coordinates, remove symptoms.
        """
        for i in self.helpCoord:
            self.coord.append((i[0],i[1]))
        self.alg.SetCoordinates(self.coord)
    
    def DeleteCoordinates(self):
        """
        Clear list with coordinates.
        """
        self.helpCoord = []
        self.coord = []
    
    def CreateDictionary(self,paStr):
        """
        Create dictionary from gestures and their actions.
        [element and connection name : gesture name]
        """
        del self.dic[:]
        if paStr == "":
            return
        if len(paStr[0])>0:
            for i in range(len(paStr[0])):
                self.dic.append([paStr[0][i].get('objectId'),paStr[0][i].get('gestureName')])
        if len(paStr[1])>0:
            for i in range(len(paStr[1])):
                self.dic.append([paStr[1][i].get('objectId'),paStr[1][i].get('gestureName')])
    
    def Recognize(self):
        """
        Recognize gesture. Sent coordinates to algorithm for recognition and get
        the message about recognition. Result sent to plugin.
        
        @rtype  : list
        @return: list with parameters about recognition
        """
        self.result = []
        self.FindOutGestureType()
        if self.result[0] == 'delete connection':
            return self.result
        if self.result[0] == 'unknown':
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
                if i[1] == a[1]:
                    bool = True
                    a.append(('Element',i[0]))
                    return a
            if bool == False:
                a[0] = 'unknown'
                return a
        if a[0] == 'connection':
            bool = False
            pom = []
            for i in self.dic:
                if i[1] == a[1]:
                    bool = True
                    pom.append(i[0])
            a.append(('Connection',pom))
            return a
            if bool == False:
                a[0] = 'unknown'
                return a