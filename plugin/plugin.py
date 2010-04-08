from lib.Addons.Plugin.Client.Interface import CInterface
from lib.Exceptions import *

from GestureGUI import CGestureGUI
from gestureLogic.GestureManager import CGestureManager

import os
import random

class Plugin(object):
    def __init__(self,interface):
        self.interface = interface                      
        self.interface.SetGtkMainloop()        
        self.gui = CGestureGUI()
        self.gui.connect('changeGestureSettings', self.ChangeGestureSettings)
        self.manager = CGestureManager()
        self.ada = self.interface.GetAdapter()
        
        #pridanie GUI komponentov do pluginu         
        try:
            mainmenu = self.interface.GetAdapter().GetGuiManager().GetMainMenu()
            myMenu = mainmenu.AddMenuItem('mitGesture', None, len(mainmenu.GetItems())-1, 'Gesture')
                                   
            myMenu.AddSubmenu()
            mySubmenu = myMenu.GetSubmenu()
                        
            self.settingsButton = mySubmenu.AddStockMenuItem('mitGesturesSettings',self.OpenGestureSettings,0,'gtk-preferences','Settings')            
            #neskor pridat help 
            mySubmenu.AddStockMenuItem('mitGesturesHelp', None, 1,'gtk-info','Help')
            
            bar = self.interface.GetAdapter().GetGuiManager().GetButtonBar()                        
            ic = os.getcwd()+"\\share\\addons\\gestures\\plugin\\icon\\button.png"        
            self.gestureButton = bar.AddButton('bbnGesturesActivate', self.ChangeGestureMode,-1,'Activate',ic,True)
                                    
        except PluginInvalidParameter:
            pass
                
        self.ada.AddNotification('gesture-invocated',self.GestureInvocate)
                                                
    def ChangeGestureMode(self,parameter):  
        if (self.gestureButton.GetActive() == True):
            self.ada.Notify('gestureModeStarted',True)
            self.gestureButton.SetLabel('Deactivate')   
        else:
            self.ada.Notify('gestureModeStarted',False)
            self.gestureButton.SetLabel('Activate')
             
    def GestureInvocate(self,coord):
        print "AAA"
        print coord        
        pass
    
    def OpenGestureSettings(self,widget):
        if self.gui.getOpen() == False:
           self.gui.Main()
            
    def ChangeGestureSettings(self,widget,size,color):
        self.interface.GetAdapter().Notify('changeGestureSettings',size,color)
    
    def GetDrawingCoordinates(self,widget,coor):        
        print coor
        #self.interface.AddNotification('coordinatesSend',self.FillCoordinates)
       
pluginMain = Plugin