from lib.Addons.Plugin.Client.Interface import CInterface
from lib.Exceptions import *

from lxml import etree
import xml.etree.ElementTree as etree

from GestureGUISettings import CGestureGUISettings
from GestureGUIHelp import CGestureGUIHelp
from gestureLogic.GestureManager import CGestureManager
from gestureLogic.Gesture import CGesture

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
        #self.ada.AddNotification('project-opened',self.LoadHelp)
                        
    def ChangeGestureMode(self,parameter):                                            
        if (self.gestureButton.GetActive() == True):
            self.ada.Notify('gestureModeStarted',True)
            self.gestureButton.SetLabel('Deactivate')
        else:
            self.ada.Notify('gestureModeStarted',False)
            self.gestureButton.SetLabel('Activate')
            
    def OpenHelp(self,widget):
        if self.guiHelp.GetMetamodel()!=self.metamodel:            
            self.LoadHelp()
        self.guiHelp.ShowHelpDialog()
        
        #d = self.ada.GetProject().GetMetamodel().GetUri()
        #pos = d.find('metamodel')
        #d = d[(pos+10):len(d)]
        #if d != self.metamodel:

        
        #if self.opened == False:
#            self.ada.GetGuiManager().DisplayWarning('Project was not loaded!')
#        else:
#            if self.guiHelp.getOpen() == False:
#                self.guiHelp.Main()
                            
    #def LoadHelp(self):
        #self.opened = True
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
                
    def LoadHelp(self):
        if self.ada.GetProject()== None:            
            return
        #self.opened = True
        d = self.ada.GetProject().GetMetamodel().GetUri()
        pos = d.find('metamodel')
        d = d[(pos+10):len(d)]
        all = []
        ic = os.path.join(sys.path[1],"share","addons",d,"metamodel","gestures","diagrams")        
        try:     
            for path in self.ada.GetProject().GetMetamodel().ListDir(ic):
                if path[0]!='.':
                    p = etree.fromstring(self.ada.GetProject().GetMetamodel().ReadFile(ic+"\\"+path))
                    pom = []
                    pom.append(p.get("id"))
                    if len(p[0])>0:
                        for i in range(len(p[0])):
                            ces = os.path.join(sys.path[1],"share","addons",d,"metamodel","elements")
                            for elePath in self.ada.GetProject().GetMetamodel().ListDir(ces):
                                if elePath[0] != '.':                                                                    
                                    e = etree.fromstring(self.ada.GetProject().GetMetamodel().ReadFile(ces+"\\"+elePath))
                                    if e.get("id") == p[0][i].get('objectId'):
                                        iko = e[0].get('path')
                                        ikoCes = os.path.join(sys.path[1],"share","addons",d,"metamodel",iko)                                        
                                        break
                            ikona = self.ada.GetProject().GetMetamodel().ReadFile(ikoCes)                            
                            ces = os.path.join(sys.path[1],"share","addons",d,"metamodel","gestures","definitions")
                            for gestPath in self.ada.GetProject().GetMetamodel().ListDir(ces):
                                if gestPath[0] != '.':                                                                    
                                    e = etree.fromstring(self.ada.GetProject().GetMetamodel().ReadFile(ces+"\\"+gestPath))
                                    if e.get("name") == p[0][i].get('gestureName'):
                                        a = CGesture(self.manager.alg.patternGestures.GetId(),e)                                        
                                        a.ParseXMLFromString(self.ada.GetProject().GetMetamodel().ReadFile(ces+"\\"+gestPath))
                                        for j in range(len(a.description)):
                                            a.description[j].gestureSize = self.manager.alg.patternGestures.GetBoxsize()
                                        a.FillDescription()
                                        break                            
                            pom.append([ikona,a.GetDescriptions(),p[0][i].get('help')])                                                                                    
                    if len(p[1])>0:
                        for i in range(len(p[1])):
                            ces = os.path.join(sys.path[1],"share","addons",d,"metamodel","connections")
                            for conPath in self.ada.GetProject().GetMetamodel().ListDir(ces):
                                if conPath[0] != '.':                                                                    
                                    e = etree.fromstring(self.ada.GetProject().GetMetamodel().ReadFile(ces+"\\"+conPath))
                                    if e.get("id") == p[1][i].get('objectId'):
                                        iko = e[0].get('path')
                                        ikoCes = os.path.join(sys.path[1],"share","addons",d,"metamodel",iko)                                        
                                        break
                            ikona = self.ada.GetProject().GetMetamodel().ReadFile(ikoCes)
                            ces = os.path.join(sys.path[1],"share","addons",d,"metamodel","gestures","definitions")
                            for gestPath in self.ada.GetProject().GetMetamodel().ListDir(ces):
                                if gestPath[0] != '.':                                                                    
                                    e = etree.fromstring(self.ada.GetProject().GetMetamodel().ReadFile(ces+"\\"+gestPath))
                                    if e.get("name") == p[1][i].get('gestureName'):
                                        a = CGesture(self.manager.alg.patternGestures.GetId(),e)                                        
                                        a.ParseXMLFromString(self.ada.GetProject().GetMetamodel().ReadFile(ces+"\\"+gestPath))
                                        for j in range(len(a.description)):
                                            a.description[j].gestureSize = self.manager.alg.patternGestures.GetBoxsize()
                                        a.FillDescription()
                                        break
                            pom.append([ikona,a.GetDescriptions(),p[1][i].get('help')])
                    all.append(pom)  
        except:
            a = "This metamodel does not have any defined gestures!" 
            print a
        self.guiHelp.SetData(all)

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
        if self.guiSettings.getOpen() == False:
            self.guiSettings.Main()
            
    def ChangeGestureSettings(self,widget,size,color,combo1,combo2,combo3,combo4):
        combos = []
        combos.append(combo1)
        combos.append(combo2)
        combos.append(combo3)
        combos.append(combo4)
        print self.guiHelp.color        
        self.guiHelp.SetColor(color)
        self.guiHelp.SetCombos(combos)
        print self.guiHelp.color
        self.interface.GetAdapter().Notify('changeGestureSettings',size,color,combos)
           
pluginMain = Plugin