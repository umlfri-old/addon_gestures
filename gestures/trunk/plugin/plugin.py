from lib.Addons.Plugin.Client.Interface import CInterface
from lib.Exceptions import *
from gui import CGestureGUI

from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import gobject
import os


import random

class Plugin(object):
    def __init__(self,interface):
        
    
        #self.__app = app
        #self.__handler = None
        
        self.interface = interface
        
        #pridanie GUI komponentov do pluginu 
        try:
            self.interface.GetAdapter().GetMainMenu().AddMenuItem(None,
            (len(self.interface.GetAdapter().GetMainMenu().GetItems())-1),'Gestures',None,None)
            
            a = (len(self.interface.GetAdapter().GetMainMenu().GetItems())-2)
            
            self.interface.GetAdapter().GetMainMenu().GetItems()[a].AddSubmenu()                    
            self.interface.GetAdapter().GetMainMenu().GetItems()[a].GetSubmenu().AddCheckMenuItem(
            None,0,'Activated',None,None)
            
            self.interface.GetAdapter().GetMainMenu().GetItems()[a].GetSubmenu().AddStockMenuItem(
            lambda:self.OpenSettings(),1,'gtk-preferences','Settings',None,None)
            
            self.interface.GetAdapter().GetMainMenu().GetItems()[a].GetSubmenu().AddStockMenuItem(
            lambda:self.ChangeMode(),2,'gtk-info','Help',None,None)
            
            ic = os.getcwd()+"\\share\\addons\\gestures\\plugin\\icon\\button.png"
            print type(ic)
            
            self.interface.GetAdapter().GetButtonBar().AddButton(lambda:self.OpenSettings(),-1,'Activate',ic,True)
                     
        except PluginInvalidParameter:
            pass
              
    def ChangeMode(self, *args):
         print "B"          
         
    def fun(x): 
        print x
        pass
 
    def OpenSettings(self):
        print "A"        
        self.wTree = gtk.glade.XML(os.getcwd()+"\\share\\addons\\gestures\\plugin\\gui\\gestureSettings.glade") 
        self.window = self.wTree.get_widget("frmGestureOptions")
        self.window.show()
        gtk.main()      
        #CGestureGUI().Main() 
    
    def Start(self):
        print 'Example patch plugin started'        
        #self.__handler = self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.connect('button-press-event', self.__clicked)
    
    def CanStop(self):
        return True
    
    def Stop(self):
        print 'Example patch plugin stopped'
        
        #if self.__handler is not None:
         #   self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.disconnect(self.__handler)
          #  self.__handler = None
    
    def __clicked(self, widget, event):
        pass
       # print 'You clicked at (%.0f, %0f) with button no. %d' % (event.x, event.y, event.button)
         
pluginMain = Plugin