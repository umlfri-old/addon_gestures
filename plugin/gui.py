from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import gobject
import os

class CGestureGUI:

    def __init__(self):
        print os.getcwd()+"\\share\\addons\\gestures\\plugin\\gui\\gestureSettings.glade" 
        self.wTree = gtk.glade.XML(os.getcwd()+"\\share\\addons\\gestures\\plugin\\gui\\gestureSettings.glade") 
        #self.window = self.wTree.get_widget("frmGestureOptions")        
    
    def Main(self):
        print "AHOJ"
        #self.window.show()
        gtk.main()