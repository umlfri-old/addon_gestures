from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import gobject
import os

class CGestureGUI:

    def __init__(self):
        self.glade = os.getcwd()+"\\share\\addons\\gestures\\plugin\\gui\\gestureSettings.glade"        
        self.wTree = gtk.glade.XML(self.glade)         
        self.window = self.wTree.get_widget("frmGestureOptions")
        
    def getWindow(self):
        return self.window
    
    def Main(self):
        print "AHOJ"
        #self.window.show()
        gtk.main()