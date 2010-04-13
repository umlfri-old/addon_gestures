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
        #vysledne suradnice        
        self.coordinates = []
    
    #prevrat mriezku hore nohami
    def ReverseGestureBox(self):
        p = int(self.gestureSize/2)
        for i in range(p):
            pom = self.gestureBox[i]
            self.gestureBox[i] = self.gestureBox[len(self.gestureBox)-i-1]
            self.gestureBox[len(self.gestureBox)-i-1] = pom            
        
    def CreateGestureBox(self):
        self.BoxInitialization()
        self.ParseCoordinations()        
        #vykreslenie potrebnych bodov v mriezke pomocou suradnic        
        for x in self.coordinates:
            pozx =int(((x[0]-0)/self.pixelSize));
            if pozx >= self.gestureSize: pozx = self.gestureSize-1                
            pozy =int(((x[1]-0)/self.pixelSize) );
            if pozy >= self.gestureSize: pozy = self.gestureSize-1
            #print pozx,pozy            
            self.gestureBox[pozy][pozx] = 1                              
        self.ReverseGestureBox()
        print self.gestureBox
        #for i in range(len(self.gestureBox)):
        #    print self.gestureBox[len(self.gestureBox)-i-1]
                
    #Vytvorenie prazdnej mriezky
    def BoxInitialization(self):
        for i in range(self.gestureSize):
            row = []
            for j in range(self.gestureSize):
                row.append(0)
            self.gestureBox.append(row)
        self.pixelSize = 100/(self.gestureSize)
    
    #vyvtori z vektorov mnozinu bodov ktore pokryvaju
    def ParseCoordinations(self):
        #parsujem pomocne suradnice
        for i in range(len(self.helpLines)):
            a = self.helpLines[i][0].partition(',')
            b = self.helpLines[i][1].partition(',') 
            x1 = int(100*float(a[0]))
            y1 = int(100*float(a[2]))
            x2 = int(100*float(b[0]))
            y2 = int(100*float(b[2]))
                        
            #osem roznych smerov nakreslenia vektora
            #SV
            if (x1>x2) and (y1>y2):
                pomx = x2
                pomy = y2
                self.coordinates.append([pomx,pomy])
                while pomx!=x1 and pomy!=y1:
                    pomx = pomx+1
                    pomy = pomy+1
                    self.coordinates.append([pomx,pomy])
            #JV
            if (x1<x2) and (y1<y2):
                pomx = x1
                pomy = y1
                self.coordinates.append([pomx,pomy])
                while pomx!=x2 and pomy!=y2:
                    pomx = pomx+1
                    pomy = pomy+1
                    self.coordinates.append([pomx,pomy])
            #J
            if (x1==x2) and (y1<y2):
                pomx = x1
                pomy = y1
                self.coordinates.append([pomx,pomy])
                while pomy!=y2:
                    pomy = pomy+1
                    self.coordinates.append([pomx,pomy])
            #S 
            if (x1==x2) and (y1>y2):
                pomx = x1
                pomy = y2
                self.coordinates.append([pomx,pomy])
                while pomy!=y1:
                    pomy = pomy+1
                    self.coordinates.append([pomx,pomy])
            #V
            if (x1<x2) and (y1==y2):
                pomx = x1
                pomy = y1
                self.coordinates.append([pomx,pomy])
                while pomx!=x2:
                    pomx = pomx+1
                    self.coordinates.append([pomx,pomy])
            #Z
            if (x1>x2) and (y1==y2):                
                pomx = x2
                pomy = y1
                self.coordinates.append([pomx,pomy])
                while pomx!=x1:
                    pomx = pomx+1
                    self.coordinates.append([pomx,pomy])
            #JV
            if (x1<x2) and (y1>y2):
                pomx = x1
                pomy = y1
                self.coordinates.append([pomx,pomy])
                while pomx!=x2 and pomy!=y2:
                    pomx = pomx+1
                    pomy = pomy-1
                    self.coordinates.append([pomx,pomy])
            #SZ
            if (x1>x2) and (y1<y2):
                pomx = x1
                pomy = y1
                self.suradnice.append([pomx,pomy])
                while pomx!=x2 and pomy!=y2:
                    pomx = pomx-1
                    pomy = pomy+1
                    self.coordinates.append([pomx,pomy])
            #BOD
            if (x1==x2) and (y1==y2):
                self.coordinates.append([x1,y1])
            #print self.coordinates
