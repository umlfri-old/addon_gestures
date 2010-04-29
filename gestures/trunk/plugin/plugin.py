from lib.Addons.Plugin.Client.Interface import CInterface
from lib.Exceptions import *
from lib.Distconfig import SCHEMA_PATH

from GestureGUISettings import CGestureGUISettings
from GestureGUIHelp import CGestureGUIHelp
from gestureLogic.GestureManager import CGestureManager
from gestureLogic.Gesture import CGesture

import StringIO

from lxml import etree
import os.path
import sys
import random

class Plugin(object):
    """
    Plugin for mouse gesture recognition.
    """
    
    def __init__(self,interface):
        """
        Constructor of class Plugin.
        
        @type  interface: CInterface
        @param interface: UML .FRI interface of plugin
        """
        #plugin interface
        self.interface = interface
        self.interface.SetGtkMainloop()
        #settings gui
        self.guiSettings = CGestureGUISettings()
        self.guiSettings.connect('changeGestureSettings', self.ChangeGestureSettings)
        #help gui
        self.guiHelp = CGestureGUIHelp()
        #gesture manager
        self.manager = CGestureManager()
        #plugin adapter
        self.ada = self.interface.GetAdapter()
        #current metamodel
        self.metamodel = ''
        #current diagram 
        self.current = ''
        #if settings gui is opened
        self.opened = False
        
        #add GUI components to plugin
        try:
            mainmenu = self.interface.GetAdapter().GetGuiManager().GetMainMenu()
            myMenu = mainmenu.AddMenuItem('mitGesture', None, len(mainmenu.GetItems())-1, 'Gesture')
            
            myMenu.AddSubmenu()
            mySubmenu = myMenu.GetSubmenu()
            
            self.settingsButton = mySubmenu.AddStockMenuItem('mitGesturesSettings',self.OpenGestureSettings,0,'gtk-preferences','Settings')
            mySubmenu.AddStockMenuItem('mitGesturesHelp', self.OpenHelp, 1,'gtk-info','Help')
            
            bar = self.interface.GetAdapter().GetGuiManager().GetButtonBar()
            
            ic = os.path.join(os.path.dirname(__file__), 'icon','button.png')
            
            self.gestureButton = bar.AddButton('bbnGesturesActivate', self.ChangeGestureMode,-1,'Activate',ic,True)
        except PluginInvalidParameter:
            pass
        self.ada.AddNotification('gesture-invocated',self.GestureInvocate)
        xmlschema_doc = etree.parse(os.path.join(SCHEMA_PATH, "gestures.xsd"))
        #XML schema for validation
        self.xmlschema = etree.XMLSchema(xmlschema_doc)
        #metamodel indicator for help GUI
        self.helpmetamodel = ''
    
    def ChangeGestureMode(self,parameter):
        """
        Activate or deactivate gesture mode.
        
        @type  parameter: bool
        @param parameter: state of gestures mode
        """
        if (self.gestureButton.GetActive() == True):
            self.ada.Notify('gestureModeStarted',True)
            self.gestureButton.SetLabel('Deactivate')
        else:
            self.ada.Notify('gestureModeStarted',False)
            self.gestureButton.SetLabel('Activate')
    
    def OpenHelp(self,widget):
        """
        Open window with gesture help
        
        @type  widget: IImageMenuItem
        @param widget: on which menu item was clicked
        """
        if self.ada.GetProject() != None:
            d = self.ada.GetProject().GetMetamodel().GetUri()
            self.helpmetamodel = d
        
        if self.guiHelp.GetMetamodel() != self.helpmetamodel:
            self.guiHelp.ShowHelpDialog()
            self.LoadHelp()
        else:
            self.guiHelp.ShowHelpDialog()
    
    def SetXmlDefinitions(self):
        """
        Load gesture definitions from metamodel.
        """
        d = self.ada.GetProject().GetMetamodel().GetUri()
        bool = True
        if d != self.metamodel:
            xmls = []
            self.metamodel = d
            ic = "gestures/definitions/"
            try:
                for path in self.ada.GetProject().GetMetamodel().ListDir(ic):
                    if path[0] != '.':
                        pom = self.ada.GetProject().GetMetamodel().ReadFile(ic+path)
                        valid = StringIO.StringIO(pom)
                        doc = etree.parse(valid)
                        if self.xmlschema.validate(doc) == False:
                            print "File" +ic+path+ "was not validate!" 
                        else:
                            xmls.append(pom)
            except:
                bool = False
                self.eror = True
                a = 'This metamodel does not have any defined gestures!'
                print a
            finally:
                self.manager.alg.patternGestures.LoadGesturesFromMetamodel(xmls,bool)
    
    def SetXmlGestures(self):
        """
        Load gesture actions from metamodel.
        """
        bool = False
        d = self.ada.GetProject().GetMetamodel().GetUri()
        ic = "gestures/diagrams/"
        if self.current != self.ada.GetCurrentDiagram().GetType():
            try:
                for path in self.ada.GetProject().GetMetamodel().ListDir(ic):
                    if path[0] != '.':
                        pom = self.ada.GetProject().GetMetamodel().ReadFile(ic+path)
                        p = etree.fromstring(pom)
                        valid = StringIO.StringIO(pom)
                        doc = etree.parse(valid)
                        if self.xmlschema.validate(doc) == False:
                            print "File" +ic+path+ "was not validate!"   
                        if self.ada.GetCurrentDiagram().GetType() == p.get('id'):
                            self.current = p.get('id')
                            self.manager.CreateDictionary(p)
                            bool = True
                            return
                if bool == False:
                    self.manager.CreateDictionary('')
            except:
                a = 'This metamodel does not have any defined gestures!'
                self.manager.CreateDictionary('')
    
    def LoadHelp(self):
        """
        Generate and load help for gestures.
        """
        if self.ada.GetProject()== None:
            return
        bool = True
        d = self.ada.GetProject().GetMetamodel().GetUri()
        all = []
        ic = "gestures/diagrams/"
        try:
            for path in self.ada.GetProject().GetMetamodel().ListDir(ic):
                if path[0] != '.':
                    p = etree.fromstring(self.ada.GetProject().GetMetamodel().ReadFile(ic+path))
                    pom = []
                    pom.append(p.get('id'))
                    if len(p[0])>0:
                        for i in range(len(p[0])):
                            ces = "elements/"
                            for elePath in self.ada.GetProject().GetMetamodel().ListDir(ces):
                                print elePath
                                if elePath[0] != '.':
                                    e = etree.fromstring(self.ada.GetProject().GetMetamodel().ReadFile(ces+elePath))
                                    if e.get("id") == p[0][i].get('objectId'):
                                        iko = e[0].get('path')
                                        break
                            ikona = self.ada.GetProject().GetMetamodel().ReadFile(iko)
                            ces = "gestures/definitions/"         
                            for gestPath in self.ada.GetProject().GetMetamodel().ListDir(ces):
                                if gestPath[0] != '.':
                                    e = etree.fromstring(self.ada.GetProject().GetMetamodel().ReadFile(ces+gestPath))
                                    if e.get('name') == p[0][i].get('gestureName'):
                                        a = CGesture(self.manager.alg.patternGestures.GetId(),e)
                                        a.ParseXMLFromString(self.ada.GetProject().GetMetamodel().ReadFile(ces+gestPath))
                                        for j in range(len(a.description)):
                                            a.description[j].gestureSize = self.manager.alg.patternGestures.GetBoxsize()
                                        a.FillDescription()
                                        break
                            pom.append([ikona,a.GetDescriptions(),p[0][i].get('help')])
                    if len(p[1]) > 0:
                        for i in range(len(p[1])):
                            ces = "connections/"        
                            for conPath in self.ada.GetProject().GetMetamodel().ListDir(ces):
                                if conPath[0] != '.':
                                    e = etree.fromstring(self.ada.GetProject().GetMetamodel().ReadFile(ces+conPath))
                                    if e.get("id") == p[1][i].get('objectId'):
                                        iko = e[0].get('path')
                                        break
                            ikona = self.ada.GetProject().GetMetamodel().ReadFile(iko)
                            ces = "gestures/definitions/"
                            for gestPath in self.ada.GetProject().GetMetamodel().ListDir(ces):
                                if gestPath[0] != '.':
                                    e = etree.fromstring(self.ada.GetProject().GetMetamodel().ReadFile(ces+gestPath))
                                    if e.get("name") == p[1][i].get('gestureName'):
                                        a = CGesture(self.manager.alg.patternGestures.GetId(),e)
                                        a.ParseXMLFromString(self.ada.GetProject().GetMetamodel().ReadFile(ces+gestPath))
                                        for j in range(len(a.description)):
                                            a.description[j].gestureSize = self.manager.alg.patternGestures.GetBoxsize()
                                        a.FillDescription()
                                        break
                            pom.append([ikona,a.GetDescriptions(),p[1][i].get('help')])
                    all.append(pom)
            self.helpmetamodel = d
            self.guiHelp.SetData(all)
        except:
            a = 'This metamodel does not have any defined gestures!'
            print a
            bool = False
        if bool == False:
            self.guiHelp.SetData([])
        self.guiHelp.SetMetamodel(d)
    
    def GetCurrentDiagram(self):
        """
        Get name of current diagram.
        
        @rtype : string
        @return : current diagram name
        """
        dia = self.ada.GetCurrentDiagram().GetType()
        for i in self.ada.GetProject().GetMetamodel().GetDiagrams():
            if i.GetName() == dia:
                return i
    
    def GestureInvocate(self,coord):
        """
        Send gesture manager coordinates for recognition.
        
        @type  coord: list
        @param coord: coordinates to by analyzed
        """
        self.SetXmlDefinitions()
        self.SetXmlGestures()
        self.manager.SetCoord(coord)
        self.ada.Notify('gesture-recognition',self.manager.Recognize())
        self.manager.alg.DeleteCoordinates()
        self.manager.alg.ClearBox()
        self.manager.DeleteCoordinates()
    
    def OpenGestureSettings(self,widget):
        """
        Open gesture settings GUI.
        
        @type  widget: IImageMenuItem
        @param widget: Item on which was clicked
        """
        if self.guiSettings.GetOpen() == False:
            self.guiSettings.Main()
    
    def ChangeGestureSettings(self,widget,size,color,combo1,combo2,combo3,combo4):
        """
        Change gesture settings.
        
        @type  widget: CGestureGUISettings
        @param widget: Who invoke changing of settings
        @type  size: int
        @param size: gesture pixel size
        @type  color: string
        @param color: gesture color
        @type  combo1: int
        @param combo1: index of action for system gesture one
        @type  combo2: int
        @param combo2: index of action for system gesture two
        @type  combo3: int
        @param combo3: index of action for system gesture three
        @type  combo4: int
        @param combo4: index of action for system gesture four                                
        """
        combos = []
        combos.append(combo1)
        combos.append(combo2)
        combos.append(combo3)
        combos.append(combo4)
        self.guiHelp.SetColor(color)
        self.guiHelp.SetCombos(combos)
        self.interface.GetAdapter().Notify('changeGestureSettings',size,color,combos)
        
pluginMain = Plugin