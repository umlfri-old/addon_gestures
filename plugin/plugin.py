from lib.Addons.Plugin.Client.Interface import CInterface
from lib.Exceptions import *
from GestureGUI import CGestureGUI

from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import gobject
import os

import random

class Plugin(object):
    def __init__(self,interface):
        self.gui = CGestureGUI()                      
        self.interface = interface
        
        #pridanie GUI komponentov do pluginu 
        try:
            self.interface.GetAdapter().GetMainMenu().AddMenuItem(None,
            (len(self.interface.GetAdapter().GetMainMenu().GetItems())-1),'Gestures',None,None)
            
            #position in menu
            self.mp = (len(self.interface.GetAdapter().GetMainMenu().GetItems())-2)
            
            self.interface.GetAdapter().GetMainMenu().GetItems()[self.mp].AddSubmenu()                    
            self.interface.GetAdapter().GetMainMenu().GetItems()[self.mp].GetSubmenu().AddCheckMenuItem(
            self.ChangeMode,0,'Activated',None,None)
            
            self.interface.GetAdapter().GetMainMenu().GetItems()[self.mp].GetSubmenu().AddStockMenuItem(
            lambda:self.OpenSettings(),1,'gtk-preferences','Settings',None,None)
            
            self.interface.GetAdapter().GetMainMenu().GetItems()[self.mp].GetSubmenu().AddStockMenuItem(
            lambda:self.ChangeMode(),2,'gtk-info','Help',None,None)
            
            ic = os.getcwd()+"\\share\\addons\\gestures\\plugin\\icon\\button.png"
            print type(ic)
            
            self.interface.GetAdapter().GetButtonBar().AddButton(self.ChangeMode,-1,'Activate',ic,True)
                     
        except PluginInvalidParameter:
            pass
            
             
    def ChangeMode(self):
        print "ZAC"
        if (self.interface.GetAdapter().GetMainMenu().GetItems()[6].GetSubmenu().GetItems()[0].GetActive() == True or
            self.interface.GetAdapter().GetButtonBar().GetItems()[-1].GetActive() == True):   
            print "A" 
            self.interface.GetAdapter().GetButtonBar().GetItems()[-1].SetActive(True)
            self.interface.GetAdapter().GetMainMenu().GetItems()[6].GetSubmenu().GetItems()[0].SetActive(True)
            self.interface.GetAdapter().GetButtonBar().GetItems()[-1].SetLabel('Deactivate')
        else:
            self.interface.GetAdapter().GetMainMenu().GetItems()[6].GetSubmenu().GetItems()[0].SetActive(False)
            self.interface.GetAdapter().GetButtonBar().GetItems()[-1].SetActive(False)
            self.interface.GetAdapter().GetButtonBar().GetItems()[-1].SetLabel('Activate')
            
        #if (self.interface.GetAdapter().GetButtonBar().GetItems()[-1].GetActive() == True):
        #    print "A"
        #    self.interface.GetAdapter().GetButtonBar().GetItems()[-1].SetLabel('Deactivate')
        #    self.interface.GetAdapter().GetMainMenu().GetItems()[6].GetSubmenu().GetItems()[0].SetActive(True)
        #else:
        #    print "B"
        #    self.interface.GetAdapter().GetButtonBar().GetItems()[-1].SetLabel('Activate')
        #    self.interface.GetAdapter().GetMainMenu().GetItems()[6].GetSubmenu().GetItems()[0].SetActive(False)
        
                        
           
        
            
        return True 
        
        #self.DragGC = self.picDrawingArea.window.new_gc(foreground = cmap.alloc_color(str(config['/Styles/Drag/RectangleColor'].Invert())),
         #   function = gtk.gdk.XOR, line_width = config['/Styles/Drag/RectangleWidth'])
         #print "B"          
             
    def OpenSettings(self):
        self.window.show()
        gtk.main()
        return True      
        #CGestureGUI().Main() 
            
pluginMain = Plugin