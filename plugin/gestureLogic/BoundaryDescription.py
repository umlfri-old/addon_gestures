from Description import CDescription

class CBoundaryDescription(CDescription):
    """
    Gesture description for Boundary Box algorithm.
    """
    
    #konstruktor
    def __init__(self,id,lines):
        """
        Constructor of class CBoundaryDescription.
        
        @type  id: int
        @param id: algorithm id
        @type  lines: list
        @param id: list of vectors
        """
        #help lines indicates vectors from XML file
        self.helpLines = lines
        #algorithm id
        self.id = id
        #gesture size
        self.gestureSize = 5
        #gesture box
        self.gestureBox = []
        #size of one pixel of box
        self.pixelSize = 0.0
        #final coordinates
        self.coordinates = []
    
    def GetHelpLines(self):
        """
        Help lines getter.
        
        @rtype: list
        @return: list of vectors
        """
        return self.helpLines
    
    def GetGestureBox(self):
        """
        Gesture box getter.
        
        @rtype: list
        @return: gesture box
        """
        return self.gestureBox
    
    def ReverseGestureBox(self):
        """
        Turn gesture box upside down.
        """
        p = int(self.gestureSize/2)
        for i in range(p):
            pom = self.gestureBox[i]
            self.gestureBox[i] = self.gestureBox[len(self.gestureBox)-i-1]
            self.gestureBox[len(self.gestureBox)-i-1] = pom
        
    def CreateGestureBox(self):
        """
        Create gesture box from coordinates. Assign area for every coordinate.
        """
        self.BoxInitialization()
        self.ParseCoordinations()
        for x in self.coordinates:
            pozx = int(((x[0]-0)/self.pixelSize));
            if pozx >= self.gestureSize: pozx = self.gestureSize-1
            pozy = int(((x[1]-0)/self.pixelSize));
            if pozy >= self.gestureSize: pozy = self.gestureSize-1
            self.gestureBox[pozy][pozx] = 1
        self.ReverseGestureBox()
        
    def BoxInitialization(self):
        """
        Initialize empty gesture box with size defined in gesture size.
        """
        for i in range(self.gestureSize):
            row = []
            for j in range(self.gestureSize):
                row.append(0)
            self.gestureBox.append(row)
        self.pixelSize = 100/(self.gestureSize)
    
    def ParseCoordinations(self):
        """
        Create coordinates from vector loaded from XML.
        """
        for i in range(len(self.helpLines)):
            a = self.helpLines[i][0].partition(',')
            b = self.helpLines[i][1].partition(',')
            x1 = int(100*float(a[0]))
            y1 = int(100*float(a[2]))
            x2 = int(100*float(b[0]))
            y2 = int(100*float(b[2]))
        
            #8 possible directions of vector
            #NorthWest direction
            if (x1 > x2) and (y1 > y2):
                pomx = x2
                pomy = y2
                self.coordinates.append([pomx,pomy])
                while pomx != x1 and pomy != y1:
                    pomx = pomx+1
                    pomy = pomy+1
                    self.coordinates.append([pomx,pomy])
            #SouthEast direction
            if (x1 < x2) and (y1 < y2):
                pomx = x1
                pomy = y1
                self.coordinates.append([pomx,pomy])
                while pomx != x2 and pomy != y2:
                    pomx = pomx+1
                    pomy = pomy+1
                    self.coordinates.append([pomx,pomy])
            #South direction
            if (x1 == x2) and (y1 < y2):
                pomx = x1
                pomy = y1
                self.coordinates.append([pomx,pomy])
                while pomy != y2:
                    pomy = pomy+1
                    self.coordinates.append([pomx,pomy])
            #North direction
            if (x1 == x2) and (y1 > y2):
                pomx = x1
                pomy = y2
                self.coordinates.append([pomx,pomy])
                while pomy != y1:
                    pomy = pomy+1
                    self.coordinates.append([pomx,pomy])
            #East direction
            if (x1 < x2) and (y1 == y2):
                pomx = x1
                pomy = y1
                self.coordinates.append([pomx,pomy])
                while pomx != x2:
                    pomx = pomx+1
                    self.coordinates.append([pomx,pomy])
            #West direction
            if (x1 > x2) and (y1 == y2):
                pomx = x2
                pomy = y1
                self.coordinates.append([pomx,pomy])
                while pomx != x1:
                    pomx = pomx+1
                    self.coordinates.append([pomx,pomy])
            #SouthEast direction
            if (x1 < x2) and (y1 > y2):
                pomx = x1
                pomy = y1
                self.coordinates.append([pomx,pomy])
                while pomx != x2 and pomy != y2:
                    pomx = pomx+1
                    pomy = pomy-1
                    self.coordinates.append([pomx,pomy])
            #NorthWest direction
            if (x1 > x2) and (y1 < y2):
                pomx = x1
                pomy = y1
                self.suradnice.append([pomx,pomy])
                while pomx != x2 and pomy != y2:
                    pomx = pomx-1
                    pomy = pomy+1
                    self.coordinates.append([pomx,pomy])
            #Only one point
            if (x1 == x2) and (y1 == y2):
                self.coordinates.append([x1,y1])