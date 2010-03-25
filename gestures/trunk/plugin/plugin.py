from lib.Addons.Plugin.Client.Interface import CInterface
from lib.Exceptions import *
from gui import CGestureGUI

import random

class Plugin(object):
    def __init__(self,interface):
        self.interface = interface
        #pridanie GUI komponentov do pluginu 
        try:
            self.interface.AddMenu('MenuItem', 'mnuMenubar', 'gestures', None, text = 'Gestures')
            self.interface.AddMenu('submenu', 'mnuMenubar/gestures', None, None)
            self.interface.AddMenu('MenuItem', 'mnuMenubar/gestures', 'ChangeMode', self.ChangeMode, text = 'Activate')
            self.interface.AddMenu('MenuItem', 'mnuMenubar/gestures', 'OpenSettings', self.OpenSettings, text = 'Settings')
                                                        
            self.interface.AddMenu(
            'ToolButton', 
            'hndCommandBar', 
            ''.join(chr(random.randint(97,125))for i in xrange(6)),
            self.ChangeMode,
            stock_id = 'gtk-refresh',
            text = 'Activate gestures')
             
        except PluginInvalidParameter:
            pass
              
    def ChangeMode(self, *args):
         print "B"          
         
    def OpenSettings(self, *args):
        print "A"        
        CGestureGUI().Main() 
         
pluginMain = Plugin