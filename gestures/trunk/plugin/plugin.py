from lib.Addons.Plugin.Client.Interface import CInterface
from lib.Exceptions import *

from lxml import etree
import xml.etree.ElementTree as etree

from GestureGUISettings import CGestureGUISettings
from GestureGUIHelp import CGestureGUIHelp
from gestureLogic.GestureManager import CGestureManager

import os.path
import sys
import random

class Plugin(object):
    def __init__(self,interface):
        self.interface = interface                      
        self.interface.SetGtkMainloop()        
        self.guiSettings = CGestureGUISettings()
        self.guiSettings.connect('changeGestureSettings', self.ChangeGestureSettings)
        self.guiHelp = CGestureGUIHelp()
        self.manager = CGestureManager()
        self.ada = self.interface.GetAdapter()
        self.metamodel = ""
        self.current = ""
        self.opened = False
        
        #pridanie GUI komponentov do pluginu         
        try:
            mainmenu = self.interface.GetAdapter().GetGuiManager().GetMainMenu()
            myMenu = mainmenu.AddMenuItem('mitGesture', None, len(mainmenu.GetItems())-1, 'Gesture')
                                   
            myMenu.AddSubmenu()
            mySubmenu = myMenu.GetSubmenu()
                        
            self.settingsButton = mySubmenu.AddStockMenuItem('mitGesturesSettings',self.OpenGestureSettings,0,'gtk-preferences','Settings')            
            #neskor pridat help 
            mySubmenu.AddStockMenuItem('mitGesturesHelp', self.OpenHelp, 1,'gtk-info','Help')
            
            bar = self.interface.GetAdapter().GetGuiManager().GetButtonBar()
            
            ic = os.path.join(os.path.dirname(__file__), "icon","button.png")
                            
            self.gestureButton = bar.AddButton('bbnGesturesActivate', self.ChangeGestureMode,-1,'Activate',ic,True)
                                    
        except PluginInvalidParameter:
            pass                
        self.ada.AddNotification('gesture-invocated',self.GestureInvocate)
        self.ada.AddNotification('project-opened',self.LoadHelp)
                        
    def ChangeGestureMode(self,parameter):                                            
        if (self.gestureButton.GetActive() == True):
            self.ada.Notify('gestureModeStarted',True)
            self.gestureButton.SetLabel('Deactivate')
        else:
            self.ada.Notify('gestureModeStarted',False)
            self.gestureButton.SetLabel('Activate')
            
    def OpenHelp(self,widget):
        if self.opened == False:
            self.ada.GetGuiManager().DisplayWarning('Project was not loaded!')
        else:
            if self.guiHelp.getOpen() == False:
                self.guiHelp.Main()
                            
    def LoadHelp(self):
        self.opened = True
        #d = self.ada.GetProject().GetMetamodel().GetUri()
        #pos = d.find('metamodel')
        #d = d[(pos+10):len(d)]
        #diagrams = []
        #ic = os.path.join(sys.path[1]+"//share//addons//"+d+"//metamodel//gestures//diagrams//")
        #for path in self.ada.GetProject().GetMetamodel().ListDir(ic):
        #        if path[0]!='.':
        #            p = etree.fromstring(self.ada.GetProject().GetMetamodel().ReadFile(ic+path))
                    #self.guiHelp.AddToCombo(p.get("id"))
                    #print p.get("id")
        
    def SetXmlDefinitions(self):
        d = self.ada.GetProject().GetMetamodel().GetUri()
        pos = d.find('metamodel')
        d = d[(pos+10):len(d)]
        if d != self.metamodel:
            xmls = []
            self.metamodel = d     
            ic = os.path.join(sys.path[1]+"//share//addons//"+d+"//metamodel//gestures//definitions//")
            try:
                for path in self.ada.GetProject().GetMetamodel().ListDir(ic):
                    if path[0]!='.':
                        xmls.append(self.ada.GetProject().GetMetamodel().ReadFile(ic+path))
            except:
                a = "This metamodel does not have any defined gestures!" 
                print a
            finally:
                self.manager.alg.patternGestures.loadGesturesFromMetamodel(xmls)
           
    def SetXmlGestures(self):
        bool = False
        d = self.ada.GetProject().GetMetamodel().GetUri()
        pos = d.find('metamodel')
        d = d[(pos+10):len(d)]
        ic = os.path.join(sys.path[1]+"//share//addons//"+d+"//metamodel//gestures//diagrams//")
        if self.current != self.ada.GetCurrentDiagram().GetType():
            try:                                    
                for path in self.ada.GetProject().GetMetamodel().ListDir(ic):
                    if path[0]!='.':
                        p = etree.fromstring(self.ada.GetProject().GetMetamodel().ReadFile(ic+path))
                        if self.ada.GetCurrentDiagram().GetType() == p.get("id"):
                            self.current = p.get("id")
                            self.manager.CreateDic(p)
                            bool = True
                if bool == False:
                    self.manager.CreateDic("")           
            except:
                a = "This metamodel does not have any defined gestures!" 
                print a
                self.manager.CreateDic("")
                                                                              
    def GetCurrentDiagram(self):
        dia = self.ada.GetCurrentDiagram().GetType()
        for i in self.ada.GetProject().GetMetamodel().GetDiagrams():
            if i.GetName() == dia:
                return i
                
    def GestureInvocate(self,coord):
        self.SetXmlDefinitions()
        self.SetXmlGestures()
        self.manager.SetCoord(coord)                
        self.ada.Notify('gesture-recognition',self.manager.Recognize())
        self.manager.alg.DeleteCoordinates()                
        self.manager.alg.ClearBox()
        self.manager.DeleteCoordinates()
    
    def OpenGestureSettings(self,widget):
        if self.opened == False:
            self.ada.GetGuiManager().DisplayWarning('Project was not loaded!')
        else:
            if self.guiSettings.getOpen() == False:
                self.guiSettings.Main()
            
    def ChangeGestureSettings(self,widget,size,color):
        self.interface.GetAdapter().Notify('changeGestureSettings',size,color)
           
pluginMain = Plugin