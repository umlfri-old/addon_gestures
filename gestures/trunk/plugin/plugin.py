from lib.Addons.Plugin.Client.Interface import CInterface
from lib.Exceptions import *
from gui import CGestureGUI

from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import gobject
import os

import random

class Plugin(object):
    def __init__(self,interface):
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
            
            ic = os.getcwd()+"\\share\\addons\\gestures\\plugin\\icon\\icon.png"
            print type(ic)
            
            self.interface.GetAdapter().GetButtonBar().AddButton(lambda:self.OpenSettings(),-1,'Activate',True)
            
            
            #ic,                                                                                                                                                                               
            #self.interface.GetAdapter().GetMainMenu().GetItems()[(len(self.interface.GetAdapter().GetMainMenu().GetItems())-1)].GetSubMenu().AddCheckMenuItem(
            #None,0,'Activated','True',None)

   #AddCheckMenuItem                                                               
 #           self.interface.GetAdapter().GetButtonBar().AddMenuItem(None,
  #          -1,'Gestures','True',os.getcwd()+"icon.png")
                  
            #self.interface.AddMenu('MenuItem', 'mnuMenubar', 'gestures', None, text = 'Gestures')
            #self.interface.AddMenu('submenu', 'mnuMenubar/gestures', None, None)
            #self.interface.AddMenu('MenuItem', 'mnuMenubar/gestures', 'ChangeMode', self.ChangeMode, text = 'Activate')
            #self.interface.AddMenu('MenuItem', 'mnuMenubar/gestures', 'OpenSettings', self.OpenSettings, text = 'Settings')
                                                        
            #self.interface.AddMenu(
            #'ToolButton', 
            #'hndCommandBar', 
            #''.join(chr(random.randint(97,125))for i in xrange(6)),
            #self.ChangeMode,
            #stock_id = 'gtk-refresh',
            #text = 'Activate gestures')
             
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
         
pluginMain = Plugin