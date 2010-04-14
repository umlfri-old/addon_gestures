from GestureAlgorithm import CGestureAlgorithm
from BoundaryGestureSet import CBoundaryGestureSet
import math

#Boundary Box algoritmus na rozoznavanie gest
class CBoundaryAlgorithm(CGestureAlgorithm):
    #konstruktor
    def __init__(self, size = 5):
        #nazov algoritmu
        self.name = "Boundary Box Algorithm"
        #id algoritmu
        self.algorithmID = 1
        #velkost mriezky
        self.boxSize = size
        #mriezka
        self.box = []
        #Nainicializuj mriezku
        self.BoxInitialization()
        #Nahraj vzorove gesta
        self.patternGestures = CBoundaryGestureSet(self.algorithmID,self.boxSize)
        #odchylka ciary
        self.lineDeviation = 20
        self.connectionDistance = 40

    #Vytvorenie prazdnej mriezky
    def BoxInitialization(self):
        for i in range(self.boxSize):
            row = []
            for j in range(self.boxSize):
                row.append(0)
            self.box.append(row)        
         
    #Vycistenie mriezky
    def ClearBox(self):
        for i in range(self.boxSize):
            for j in range(self.boxSize):
                self.box[i][j] = 0
                
    #Uprav na tvar jedniciek a nul
    def MakeBinaryBox(self):
        for i in range(self.boxSize):
            for j in range(self.boxSize):
                if self.box[i][j] >= 1:
                    self.box[i][j] = 1                
                                        
    #Zisti hranice gesta                    
    def Boundaries(self):
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
        bool = True
        if (self.maxj - self.mins) <= self.lineDeviation:
            #gesto z prava do lava
            if self.coordinates[0][0]-self.coordinates[len(self.coordinates)-1][0]>=0:
                for i in range(len(self.coordinates)-1):
                    if self.coordinates[i][0]>=self.coordinates[i+1][0] and math.fabs(self.coordinates[i][1]-self.coordinates[0][1])<=self.lineDeviation:
                        pass                        
                    else:
                        bool = False                                                 
                if bool == False:
                    return "direction error"
                else:
                    return "from right to left"
            #gesto z lava do prava
            if self.coordinates[0][0]-self.coordinates[len(self.coordinates)-1][0]<=0:
                for i in range(len(self.coordinates)-1):
                    if self.coordinates[i][0]<=self.coordinates[i+1][0] and math.fabs(self.coordinates[i][1]-self.coordinates[0][1])<=self.lineDeviation:
                        pass                        
                    else:
                        bool = False                                                 
                if bool == False:
                    return "direction error"
                else:
                    return "from left to right"
        if (self.maxv - self.minz) <= self.lineDeviation:
            #gesto z dola na hor
            if self.coordinates[0][1]-self.coordinates[len(self.coordinates)-1][1]>=0:
                for i in range(len(self.coordinates)-1):
                    if self.coordinates[i][1]>=self.coordinates[i+1][1] and math.fabs(self.coordinates[i][0]-self.coordinates[0][0])<=self.lineDeviation:
                        pass                        
                    else:
                        bool = False                                                 
                if bool == False:
                    return "direction error"
                else:
                    return "from down to up"
            #gesto zhora nadol
            if self.coordinates[0][1]-self.coordinates[len(self.coordinates)-1][1]<=0:
                for i in range(len(self.coordinates)-1):
                    if self.coordinates[i][1]<=self.coordinates[i+1][1] and math.fabs(self.coordinates[i][0]-self.coordinates[0][0])<=20:
                        pass                        
                    else:
                        bool = False                                                 
                if bool == False:
                    return "direction error"
                else:
                    return "from up to down"                                
        return "direction error"
    
    #naplnenie mriezky hodnotami z programu            
    def FillBox(self):
        #vypocet vysky a sirky dielov mriezky
        sir = (self.maxv-self.minz)/self.boxSize
        vys = (self.maxj-self.mins)/self.boxSize
        
        #samotne naplnenie mriezky    
        for x in self.coordinates:
            pozx =int(((x[0]-self.minz)/sir) );
            if x[0] == self.maxv: pozx = self.boxSize-1
            pozy =int(((x[1]-self.mins)/vys) );
            if x[1] == self.maxj: pozy = self.boxSize-1
            #print pozx,pozy
            self.box[pozy][pozx] +=1                  
    
    #porovnava vzorky s nakreslenym gestom                        
    def ElementComparation(self):
        zh = self.boxSize*self.boxSize;      
        ind = 0;
        for x in range(len(self.patternGestures.GetGestures())):
            if self.patternGestures.GetGesture(x).gestureType == 'element':
                for k in range(len(self.patternGestures.GetGesture(x).description)):                            
                    a = 0
                    for i in range(self.boxSize):
                        for j in range(self.boxSize):
                            if self.box[i][j] == self.patternGestures.GetGesture(x).description[k].gestureBox[i][j]:
                                a = a+1
                if a==zh:
                    ind = x
                    zh = a
                    return self.patternGestures.GetGesture(x).GetName()
        return "unknown"
    
    def ConnectionComparation(self):
        zh = self.boxSize*self.boxSize;      
        ind = 0;
        for x in range(len(self.patternGestures.GetGestures())):
            if self.patternGestures.GetGesture(x).gestureType == 'connection':
                print "AAA"
                for k in range(len(self.patternGestures.GetGesture(x).description)):
                    print "JB"                            
                    a = 0
                    for i in range(self.boxSize):
                        for j in range(self.boxSize):
                            if self.box[i][j] == self.patternGestures.GetGesture(x).description[k].gestureBox[i][j]:
                                a = a+1
                    if a==zh:
                        ind = x
                        zh = a
                        return self.patternGestures.GetGesture(x).GetName()
        return "unknown"
    
    #algoritmus, ktory vrati rozoznane gesto, type je typ gesta, ci sa jedna o spojenie, element... 
    def Recognition(self,type):
        result = []
        if type == 'delete element':
            result.append('delete element')
            result.append(self.coordinates[0])
            return result                   
        if type == 'delete connection':
            result.append('delete connection')
            #result.append(self.coordinates[0])
            #print self.coordinates[0]            
            return result                        
        if type == 'element or system':
            self.Boundaries()
            res = self.SystemGesture()
            #ak sa jedna o systemove gesto - t.j. len  pohyb jednym smerom
            if res!= "direction error":                
                result.append(res)
                print "KOKO"
                return result
            else:
                self.FillBox()                
                self.MakeBinaryBox()
                print self.box
                ele = self.ElementComparation()
                if ele !='unknown':
                    result.append('element')
                    result.append(ele) 
                    return result
        if type == 'connection':
            bendPoints = []
            print self.coordinates
            for i in self.coordinates:
                if i == ('x','x'):
                    poz = self.coordinates.index(i)                    
            for i in range(poz):
                if self.coordinates[i] == ('p','p'):
                    bendPoints.append(self.coordinates[i-1])
            print bendPoints
            #ak sa jedna o ciste spojenie                                
            if self.coordinates[len(self.coordinates)-1][0]=='x':
                self.MakeBinaryBox()                
                ele = self.ConnectionComparation()
                if ele!='unknown':
                    result.append('connection')
                    result.append(ele)
                    result.append(bendPoints)
                    result.append(self.coordinates[0])
                    result.append(self.coordinates[len(self.coordinates)-2])                                                                                                                                                                                                                    
                return result
            if self.coordinates[len(self.coordinates)-1][0]!='x':
                result.append('connection')
                result.append(bendPoints)                        
                poc = 0
                roz = 0
                prv = 0.0
                posl = 0.0                
                #vzdialenost od zaciatku                
                for i in self.coordinates[poz+1:len(self.coordinates)+1]:
                    if i!=('p','p'):
                        poc = poc+1
                        roz = roz+ math.sqrt(math.fabs(i[0]-self.coordinates[0][0])*math.fabs(i[0]-self.coordinates[0][0])+
                                    math.fabs(i[1]-self.coordinates[0][1])*math.fabs(i[1]-self.coordinates[0][1]))
                poc = 0
                roz = 0                
                #vzdialenost od konca
                for i in self.coordinates[poz+1:len(self.coordinates)+1]:
                    if i!=('p','p'):
                        poc = poc+1
                        roz = roz+ math.sqrt(math.fabs(i[0]-self.coordinates[poz-1][0])*math.fabs(i[0]-self.coordinates[poz-1][0])+
                                    math.fabs(i[1]-self.coordinates[poz-1][1])*math.fabs(i[1]-self.coordinates[poz-1][1]))
                if prv >= posl:
                    if posl <= self.connectionDistance:
                        result.append(self.coordinates[0])
                        result.append(self.coordinates[poz-1])                                                                                                                                                                                                                    
                    else:
                        del result[:]
                        result.append("error")
                        return result                                
                if prv < posl:
                    if prv <= self.connectionDistance:
                        result.append(self.coordinates[poz-1])
                        result.append(self.coordinates[0])                                                                                                                                                                                                                                            
                    else:
                        del result[:]
                        result.append("error")
                        return result
                new = []
                for i in self.coordinates[poz+1:len(self.coordinates)+1]:
                    if i!=('p','p'):
                        new.append(i)                    
                self.coordinates = new
                print self.coordinates
                self.Boundaries()                
                self.FillBox()                
                self.MakeBinaryBox()
                ele = self.ConnectionComparation()
                if ele!='unknown':
                    result.insert(1, ele)
                print self.box
                print "SEX"
                print result
                return result   
        del result[:]                                 
        result.append("error")
        return result
        