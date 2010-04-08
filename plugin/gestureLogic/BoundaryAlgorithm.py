from GestureAlgorithm import CGestureAlgorithm
from BoundaryGestureSet import CBoundaryGestureSet

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

    #Vytvorenie prazdnejmriezky
    def BoxInitialization(self):
        for i in range(self.boxSize):
            row = []
            for j in range(self.boxSize):
                row.append(0)
            self.box.append(row)
    
    #Vycistenie mriezky
    def ClearBox(self):
        for i in range(3):
            for j in range(self.boxSize):
                self.box[i][j] = 0
                
    #naplnenie mriezky hodnotami z programu            
    def FillBox(self):
        minz = 9999
        maxv = 0
        mins = 9999    
        maxj = 0
        #vypocet rozmerov pomyselnej mriezky
        for x in self.coordinates[1:len(self.coordinates)]:
            if x[0] >maxv: maxv=x[0]                        
            if x[0] <minz: minz=x[0]
            if x[1] >maxj: maxj=x[1]
            if x[1] <mins: mins=x[1]        
            
        #vypocet vysky a sirky dielov mriezky
        sir = (maxv-minz)/self.boxSize
        vys = (maxj-mins)/self.boxSize
        print sir,vys
        print minz,maxv
        print mins,maxj
        
        #samotne naplnenie mriezky    
        for x in self.coordinates[1:len(self.coordinates)]:
            pozx =int(((x[0]-minz)/sir) );
            if x[0] == maxv: pozx = 4
            pozy =int(((x[1]-mins)/vys) );
            if x[1] == maxj: pozy = 4
            print pozx,pozy
            self.box[pozy][pozx] +=1     
    
    #algoritmus, ktory vrati rozoznane gesto, diagram je typ diagramu, v ktorom rozoznavame, type je typ gesta, ci sa jedna o spojenie, element... 
    def Recognition(self,diagram,type):
        return None
