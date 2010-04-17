from lib.Addons.Plugin.Client.Interface import CInterface
from lib.Exceptions import *

from GestureGUI import CGestureGUI
from gestureLogic.GestureManager import CGestureManager

import os.path
import sys
import random

class Plugin(object):
    def __init__(self,interface):
        self.interface = interface                      
        self.interface.SetGtkMainloop()        
        self.gui = CGestureGUI()
        self.gui.connect('changeGestureSettings', self.ChangeGestureSettings)
        self.manager = CGestureManager()
        self.ada = self.interface.GetAdapter()
        self.metamodel = ""
        
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
            
            ic = os.path.join(os.path.dirname(__file__), "icon","button.png")
                            
            self.gestureButton = bar.AddButton('bbnGesturesActivate', self.ChangeGestureMode,-1,'Activate',ic,True)
                                    
        except PluginInvalidParameter:
            pass                
        self.ada.AddNotification('gesture-invocated',self.GestureInvocate)
                        
    def ChangeGestureMode(self,parameter):                                            
        if (self.gestureButton.GetActive() == True):
            self.ada.Notify('gestureModeStarted',True)
            self.gestureButton.SetLabel('Deactivate')
            ic = os.path.join(os.path.dirname(__file__), "icon","agregation.xml")
            print ic
            print self.interface.GetAdapter().GetProject().GetMetamodel().ReadFile(ic)
            self.GetXmlDefinitions()
        else:
            self.ada.Notify('gestureModeStarted',False)
            self.gestureButton.SetLabel('Activate')
            
    def GetXmlDefinitions(self):
        d = self.ada.GetProject().GetMetamodel().GetUri()
        pos = d.find('metamodel')
        d = d[(pos+10):len(d)]   
        if d != self.metamodel:
            xmls = []
            self.metamodel = d     
            ic = os.path.join(sys.path[1]+"//share//addons//"+d+"//metamodel//gestures//definitions//")
            for path in self.ada.GetProject().GetMetamodel().ListDir(ic):
                if path[0]!='.':
                    xmls.append(self.ada.GetProject().GetMetamodel().ReadFile(ic+path)) 
            self.manager.alg.patternGestures.loadGesturesFromMetamodel(xmls)
           
    def GetCurrentDiagram(self):
        dia = self.ada.GetCurrentDiagram().GetType()
        for i in self.ada.GetProject().GetMetamodel().GetDiagrams():
            if i.GetName() == dia:
                return i
                
    def GestureInvocate(self,coord):
        ele = []
        con = []
        dia = self.GetCurrentDiagram()
        for i in dia.GetElements():
            ele.append(i.GetName())
        for i in dia.GetConnections():                    
            con.append(i.GetName())                
        self.manager.SetCoord(coord)        
        self.manager.CreateDictionary(ele,con)
        self.ada.Notify('gesture-recognition',self.manager.Recognize())
        self.manager.alg.DeleteCoordinates()                
        self.manager.alg.ClearBox()
        self.manager.DeleteCoordinates()
        pass
    
    def OpenGestureSettings(self,widget):
        if self.gui.getOpen() == False:
           self.gui.Main()
            
    def ChangeGestureSettings(self,widget,size,color):
        self.interface.GetAdapter().Notify('changeGestureSettings',size,color)
           
pluginMain = Plugin