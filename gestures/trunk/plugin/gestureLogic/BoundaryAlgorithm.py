from GestureAlgorithm import CGestureAlgorithm
from BoundaryGestureSet import CBoundaryGestureSet
import math

class CBoundaryAlgorithm(CGestureAlgorithm):
    """
    Boundary box algorithm for gesture recognition
    """
    
    def __init__(self, size = 5):
        """
        Constructor of class CBoundaryGestureSet.
        
        @type  size: int
        @param size: gesture box size
        """
        #algorithm name
        self.name = 'Boundary Box Algorithm'
        #algorithm ID
        self.algorithmID = 1
        #gesture box size
        self.boxSize = size
        #gesture box
        self.box = []
        #box initialization
        self.BoxInitialization()
        #loaded known gestures
        self.patternGestures = CBoundaryGestureSet(self.algorithmID,self.boxSize)
        
        #the maximum distance from line considered as same direction
        self.lineDeviation = 20
        #the maximum distance connection gesture from end or beginning of connection
        self.connectionDistance = 40
        #the maximum wrong pixels in element gesture
        self.elementRecognitionDeviation = 1
        #the maximum wrong pixels in connection gesture
        self.connectionRecognitionDeviation = 2
        #the maximum wrong pixels in delete gesture
        self.deleteDeviation = 7
        #gesture coordinates
        self.coordinates = []

    def BoxInitialization(self):
        """
        Create empty box with size:boxsize
        """
        for i in range(self.boxSize):
            row = []
            for j in range(self.boxSize):
                row.append(0)
            self.box.append(row)
    
    def ClearBox(self):
        """
        Clear box.
        """
        for i in range(self.boxSize):
            for j in range(self.boxSize):
                self.box[i][j] = 0
    
    def MakeBinaryBox(self):
        """
        From box make binary box(box contains only 0,1).
        """
        for i in range(self.boxSize):
            for j in range(self.boxSize):
                if self.box[i][j] >= 1:
                    self.box[i][j] = 1
    
    def Boundaries(self):
        """
        Find out gestures edges.
        """
        self.minz = 9999
        self.maxv = 0
        self.mins = 9999
        self.maxj = 0
        for x in self.coordinates:
            if x[0] > self.maxv: self.maxv = x[0]
            if x[0] < self.minz: self.minz = x[0]
            if x[1] > self.maxj: self.maxj = x[1]
            if x[1] < self.mins: self.mins = x[1]
    
    def SystemGesture(self):
        """
        Check if the gesture is system(from one line).
        
        @rtype :string
        @return: system gesture name or direction error
        """
        bool = True
        if (self.maxj-self.mins) <= self.lineDeviation:
            #line from right to left
            if self.coordinates[0][0]-self.coordinates[len(self.coordinates)-1][0] >= 0:
                for i in range(len(self.coordinates)-1):
                    if self.coordinates[i][0] >= self.coordinates[i+1][0] and math.fabs(self.coordinates[i][1]-self.coordinates[0][1]) <= self.lineDeviation:
                        pass
                    else:
                        bool = False
                if bool == False:
                    return 'direction error'
                else:
                    return 'from right to left'
            #line from left to right
            if self.coordinates[0][0]-self.coordinates[len(self.coordinates)-1][0] <= 0:
                for i in range(len(self.coordinates)-1):
                    if self.coordinates[i][0] <= self.coordinates[i+1][0] and math.fabs(self.coordinates[i][1]-self.coordinates[0][1]) <= self.lineDeviation:
                        pass
                    else:
                        bool = False
                if bool == False:
                    return 'direction error'
                else:
                    return 'from left to right'
        if (self.maxv - self.minz) <= self.lineDeviation:
            #line from down to up
            if self.coordinates[0][1]-self.coordinates[len(self.coordinates)-1][1] >= 0:
                for i in range(len(self.coordinates)-1):
                    if self.coordinates[i][1] >= self.coordinates[i+1][1] and math.fabs(self.coordinates[i][0]-self.coordinates[0][0]) <= self.lineDeviation:
                        pass
                    else:
                        bool = False
                if bool == False:
                    return 'direction error'
                else:
                    return 'from down to up'
            #line from up to down
            if self.coordinates[0][1]-self.coordinates[len(self.coordinates)-1][1] <= 0:
                for i in range(len(self.coordinates)-1):
                    if self.coordinates[i][1] <= self.coordinates[i+1][1] and math.fabs(self.coordinates[i][0]-self.coordinates[0][0]) <= 20:
                        pass
                    else:
                        bool = False
                if bool == False:
                    return 'direction error'
                else:
                    return 'from up to down'
        return 'direction error'
    
    #naplnenie mriezky hodnotami z programu
    def FillBox(self):
        """
        Fill box with coordinates from picDrawingArea.
        """
        #set width and height of box
        sir = (self.maxv-self.minz)/self.boxSize
        vys = (self.maxj-self.mins)/self.boxSize
        
        #fill box
        for x in self.coordinates:
            pozx = int(((x[0]-self.minz)/sir))
            if x[0] == self.maxv: pozx = self.boxSize-1
            pozy = int(((x[1]-self.mins)/vys))
            if x[1] == self.maxj: pozy = self.boxSize-1
            self.box[pozy][pozx] +=1
    
    def ElementComparation(self):
        """
        Compare painted gesture with element gestures in algorithm's gesture set.
        
        @rtype : string
        @return: recognized element name or delete element or unknown 
        """
        zh = self.boxSize*self.boxSize
        ind = 0
        odch = 0
        for x in range(len(self.patternGestures.GetGestures())):
            if self.patternGestures.GetGesture(x).gestureType == 'element':
                for k in range(len(self.patternGestures.GetGesture(x).description)):
                    a = 0
                    for i in range(self.boxSize):
                        for j in range(self.boxSize):
                            if self.box[i][j] == self.patternGestures.GetGesture(x).description[k].gestureBox[i][j]:
                                a = a+1
                    #sample same as the gesture
                    if a == zh:
                        return self.patternGestures.GetGesture(x).GetName()
                    #deviation from sample
                    if a > odch:
                        odch = a
                        ind = x
        
        if zh-odch <= self.elementRecognitionDeviation:
            return self.patternGestures.GetGesture(ind).GetName()
        a = 0
        for i in range(self.boxSize):
            for j in range(self.boxSize):
                if self.box[i][j] == 1:
                    a = a+1
        if a+self.deleteDeviation >= zh:
            return 'delete element'
        return 'unknown'
    
    def ConnectionComparation(self):
        """
        Compare painted gesture with connection gestures in algorithm's gesture set.
        
        @rtype: string
        @return: recognized connection name or unknown
        """
        zh = self.boxSize*self.boxSize
        ind = 0
        odch = 0
        for x in range(len(self.patternGestures.GetGestures())):
            if self.patternGestures.GetGesture(x).gestureType == 'connection':
                for k in range(len(self.patternGestures.GetGesture(x).description)):
                    a = 0
                    for i in range(self.boxSize):
                        for j in range(self.boxSize):
                            if self.box[i][j] == self.patternGestures.GetGesture(x).description[k].gestureBox[i][j]:
                                a = a+1
                    #sample same as the gesture
                    if a==zh:
                        return self.patternGestures.GetGesture(x).GetName()
                    #deviation from sample
                    if a>odch:
                        odch = a
                        ind = x
        if zh-odch <= self.connectionRecognitionDeviation:
            return self.patternGestures.GetGesture(ind).GetName()
        return 'unknown'
    
    #algoritmus, ktory vrati rozoznane gesto, type je typ gesta, ci sa jedna o spojenie, element.
    def Recognition(self,type):
        """
        Algoritmus which recognize gesture and send result to gesture manager.
        
        #@type type: string
        @param type: type of gesture
        @rtype: list
        @return: list with parameters of recognition
        """
        result = []
        #if gesture type is element
        if type[0] == 'element':
            self.Boundaries()
            res = self.SystemGesture()
            #system gesture
            if res != 'direction error':
                result.append('system')
                result.append(res)
                return result
            else:
                #element gesture
                self.FillBox()
                self.MakeBinaryBox()
                ele = self.ElementComparation()
                if ele != 'unknown':
                    #delete element gesture
                    if ele == 'delete element':
                        result.append('delete element')
                        result.append(self.coordinates[0])
                        return result
                    else:
                        #element gesture
                        result.append('element')
                        result.append(ele)
                        return result
                else:
                    del result[:]
                    result.append('unknown')
                    return result
        #connection gesture
        if type[0] == 'connection':
            bendPoints = []
            for i in self.coordinates:
                if i == ('x','x'):
                    poz = self.coordinates.index(i)
            #set connection bend points
            for i in range(poz):
                if self.coordinates[i] == ('p','p'):
                    bendPoints.append(self.coordinates[i-1])
            #clean connection
            if self.coordinates[len(self.coordinates)-1][0] =='x':
                self.MakeBinaryBox()
                ele = self.ConnectionComparation()
                if ele !='unknown':
                    result.append('connection')
                    result.append(ele)
                    result.append(bendPoints)
                    result.append(self.coordinates[0])
                    result.append(self.coordinates[len(self.coordinates)-2])
                else:
                    del result[:]
                    result.append('unknown')
                return result
            #other than connection
            if self.coordinates[len(self.coordinates)-1][0] != 'x':
                result.append('connection')
                result.append(bendPoints)
                poc = 0
                roz = 0
                prv = 0.0
                posl = 0.0
                #gesture distance from beginning
                for i in self.coordinates[poz+1:len(self.coordinates)+1]:
                    if i != ('p','p'):
                        poc = poc+1
                        roz = roz+ math.sqrt(math.fabs(i[0]-self.coordinates[0][0])*math.fabs(i[0]-self.coordinates[0][0])+
                                    math.fabs(i[1]-self.coordinates[0][1])*math.fabs(i[1]-self.coordinates[0][1]))
                prv = roz/poc
                poc = 0
                roz = 0
                #gesture distance from end
                for i in self.coordinates[poz+1:len(self.coordinates)+1]:
                    if i != ('p','p'):
                        poc = poc+1
                        roz = roz+ math.sqrt(math.fabs(i[0]-self.coordinates[poz-1][0])*math.fabs(i[0]-self.coordinates[poz-1][0])+
                                    math.fabs(i[1]-self.coordinates[poz-1][1])*math.fabs(i[1]-self.coordinates[poz-1][1]))
                posl = roz/poc
                #compare distances
                if prv >= posl:
                    if posl <= self.connectionDistance:
                        result.append(self.coordinates[0])
                        result.append(self.coordinates[poz-1])
                    else:
                        del result[:]
                        result.append('unknown')
                        return result
                if prv < posl:
                    if prv <= self.connectionDistance:
                        result.append(self.coordinates[poz-1])
                        result.append(self.coordinates[0])
                    else:
                        del result[:]
                        result.append('unknown')
                        return result
                new = []
                for i in self.coordinates[poz+1:len(self.coordinates)+1]:
                    if i != ('p','p'):
                        new.append(i)
                self.coordinates = new
                self.Boundaries()
                self.FillBox()
                self.MakeBinaryBox()
                ele = self.ConnectionComparation()
                if ele != 'unknown':
                    result.insert(1, ele)
                else:
                    del result[:]
                    result.append('unknown')
                return result