from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import gobject

import os
import os.path

class CGestureGUISettings(gobject.GObject):
    __gsignals__ = {
        'changeGestureSettings':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_INT,gobject.TYPE_STRING,
                                                                                gobject.TYPE_INT,gobject.TYPE_INT,
                                                                                gobject.TYPE_INT,gobject.TYPE_INT))}                        
    def __init__(self):
        gobject.GObject.__init__(self)
        self.glade = os.path.join(os.path.dirname(__file__), "gui", "gestureSettings.glade")        
        self.wTree = gtk.glade.XML(self.glade)
        self.open = False         
        self.window = self.wTree.get_widget("frmGestureOptions")
        self.btnGui = self.wTree.get_widget("btnOk")
        
        self.combo1 = self.wTree.get_widget("combobox1")
        self.combo2 = self.wTree.get_widget("combobox2") 
        self.combo3 = self.wTree.get_widget("combobox3") 
        self.combo4 = self.wTree.get_widget("combobox4")          
        dic = {"on_btnOk_clicked" : self.on_btnOk_clicked,
               "on_btnDefault_clicked" : self.on_btnDefault_clicked,
               "on_frmGestureOptions_destroy" : self.on_frmGestureOptions_destroy}                        
        self.wTree.signal_autoconnect(dic)
        self.color = '#00FF00'         
        self.size = 3 
        self.combos = [7,6,13,12]
        self.combo1.set_active(7)
        self.combo2.set_active(6)
        self.combo3.set_active(13)
        self.combo4.set_active(12)                        

    def Main(self):
        self.setOpen(True)        
        self.window.show()
        
    def getColor(self):
        return self.color
    
    def getSize(self):
        return self.size  
        
    def on_btnOk_clicked(self,widget):
        self.color = self.wTree.get_widget("cbnLineColor").get_color()
        self.size = self.wTree.get_widget("sbpLineSize").get_value()
        self.combos[0] = self.combo1.get_active()
        self.combos[1] = self.combo2.get_active()
        self.combos[2] = self.combo3.get_active()
        self.combos[3] = self.combo4.get_active()       
        self.emit('changeGestureSettings',self.size,self.color,self.combos[0],self.combos[1],self.combos[2],self.combos[3])
        self.on_frmGestureOptions_destroy(widget)
        
    def on_btnDefault_clicked(self,widget):        
        self.combo1.set_active(7)
        self.combo2.set_active(6)
        self.combo3.set_active(13)
        self.combo4.set_active(12)                
        self.wTree.get_widget("sbpLineSize").set_value(3)
        self.wTree.get_widget("cbnLineColor").set_color(gtk.gdk.Color('#00FF00'))               
        
    def on_frmGestureOptions_destroy(self,widget):
        self.window.hide()
        self.setOpen(False)
        
    def setOpen(self,bool):
        self.open = bool
        
    def getOpen(self):
        return self.open
        
        