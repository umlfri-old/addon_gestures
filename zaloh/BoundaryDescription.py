from Description import CDescription
import time
import random

#popis gesta Boundary Box algoritmu
class CBoundaryDescription(CDescription):
    #konstruktor
    def __init__(self,id,lines):
        #pomocne ciary vektorovo znazornene
        self.helpLines = lines
        #id algoritmu
        self.id = id
        #velkost vzorovejmriezky
        self.gestureSize = 5
        #mriezka vzoroveho gesta
        self.gestureBox = []
        #definuje velkost jedneho stvorceka mriezky
        self.pixelSize = 0.0;
        
        self.coordinates = []
        
    def CreateGestureBox(self):
        self.BoxInitialization()
        self.ParseCoordinations()
        
        #vykreslenie potrebnych bodov v mriezke pomocou suradnic        
        for x in self.coordinates:
            pozx =int(((x[0]-0)/self.pixelSize));
            if x[0] >= 1: pozx = self.gestureSize-1
            pozy =int(((x[1]-0)/self.pixelSize) );
            if x[1] == 1: pozy = self.gestureSize-1
            print pozx,pozy            
            self.gestureBox[pozy][pozx] = 1                              
            
        #print self.gestureBox[4]
        print self.gestureBox[3]
        print self.gestureBox[2]
        print self.gestureBox[1]
        print self.gestureBox[0]
        print ""
        
    #Vytvorenie prazdnej mriezky
    def BoxInitialization(self):
        for i in range(self.gestureSize):
            row = []
            for j in range(self.gestureSize):
                row.append(0)
            self.gestureBox.append(row)
        self.pixelSize = float(1/float(self.gestureSize))
    
    #vyvtori z vektorov mnozinu bodov ktore pokryvaju
    def ParseCoordinations(self):
        #parsujem pomocne suradnice
        for i in range(len(self.helpLines)):
            a = self.helpLines[i][0].partition(',')
            b = self.helpLines[i][1].partition(',') 
            x1 = float(a[0])
            y1 = float(a[2])
            x2 = float(b[0])
            y2 = float(b[2])
            
            xRoz = round(float(abs(x1-x2)/self.gestureSize),2)
            yRoz = round(float(abs(y1-y2)/self.gestureSize),2)
            
            #osem roznych smerov nakreslenia vektora
            #SV
            if (x1>x2) and (y1>y2):
                pomx = float(x2)
                pomy = float(y2)
                self.coordinates.append([pomx,pomy])
                while (round(pomx,2)!=round(x1,2)) and (round(pomy,2)!=round(y1,2)):
                    pomx = pomx+xRoz
                    pomy = pomy+yRoz
                    self.coordinates.append([pomx,pomy])
            #JV
            if (x1<x2) and (y1<y2):
                pomx = float(x1)
                pomy = float(y1)
                self.coordinates.append([pomx,pomy])
                while (round(pomx,2)!=round(x2,2)) and (round(pomy,2)!=round(y2,2)):
                    pomx = pomx+xRoz
                    pomy = pomy+yRoz
                    self.coordinates.append([pomx,pomy])
            #J
            if (x1==x2) and (y1<y2):
                pomx = float(x1)
                pomy = float(y1)
                self.coordinates.append([pomx,pomy])
                while (round(pomy,2)!=round(y2,2)):
                    pomy = pomy+yRoz
                    self.coordinates.append([pomx,pomy])
            #S 
            if (x1==x2) and (y1>y2):
                pomx = float(x1)
                pomy = float(y2)
                self.coordinates.append([pomx,pomy])
                while (round(pomy,2)!=round(y1,2)):
                    pomy = pomy+yRoz
                    self.coordinates.append([pomx,pomy])
            #V
            if (x1<x2) and (y1==y2):
                pomx = float(x1)
                pomy = float(y1)
                self.coordinates.append([pomx,pomy])
                while (round(pomx,2)!=round(x2,2)):
                    pomx = pomx+xRoz
                    self.coordinates.append([pomx,pomy])
            #Z
            if (x1>x2) and (y1==y2):                
                pomx = float(x2)
                pomy = float(y1)
                self.coordinates.append([pomx,pomy])
                while (round(pomx,2)!=round(x1,2)):
                    pomx = pomx+xRoz
                    self.coordinates.append([pomx,pomy])
            #JV
            if (x1<x2) and (y1>y2):
                pomx = float(x1)
                pomy = float(y1)
                self.coordinates.append([pomx,pomy])
                while (round(pomx,2)!=round(x2,2)) and (round(pomy,2)!=round(y2,2)):
                    pomx = pomx+xRoz
                    pomy = pomy-yRoz
                    self.coordinates.append([pomx,pomy])
            #SZ
            if (x1>x2) and (y1<y2):
                pomx = float(x1)
                pomy = float(y1)
                self.suradnice.append([pomx,pomy])
                while (round(pomx,2)!=round(x2,2)) and (round(pomy,2)!=round(y2,2)):
                    pomx = pomx-xRoz
                    pomy = pomy+yRoz
                    self.coordinates.append([pomx,pomy])
            #BOD
            if (x1==x2) and (y1==y2):
                self.coordinates.append([x1,y1])
            print self.coordinates
