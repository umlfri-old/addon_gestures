from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import gobject

import os
import os.path

class CGestureGUIHelp(object):            
    def __init__(self):
        self.glade = os.path.join(os.path.dirname(__file__), "gui", "gestureHelp.glade")        
        self.wTree = gtk.glade.XML(self.glade)
        self.open = False         
        self.window = self.wTree.get_widget("frmGestureHelp")
        self.combo = self.wTree.get_widget("cbxDiagram")
                
        #self.btnGui = self.wTree.get_widget("btnOk") 
        dic = {"on_cbxDiagram_changed" : self.on_cbxDiagram_changed}
        #       "on_btnDefault_clicked" : self.on_btnDefault_clicked,
        #       "on_frmGestureOptions_destroy" : self.on_frmGestureOptions_destroy}                        
        self.wTree.signal_autoconnect(dic)

    def Main(self):
        self.setOpen(True)
 #       response = wid.run()
#        if response =         
        self.window.show()
                        
    def setOpen(self,bool):
        self.open = bool
        
    def getOpen(self):
        return self.open
    
    def on_cbxDiagram_changed(self,widget):
        print "Jahoda"
    
    def AddToCombo(self,row):
        self.combo.append_text(row)
    
    #def     
    
    #def FillCombos(self,col):
    #    for i in col:
    #        self.combo.append_text(i)        
        