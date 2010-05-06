from lib.Depend.gtk2 import gtk

from lib.Connections import CConnectionObject
from lib.Elements import CElementObject
from lib.Drawing import CConnection,CElement,Element
from lib.Exceptions.UserException import *
from lib.Addons.Plugin.Interface.decorators import *

import time

class CPatchPlugin():
    """
    Gesture recognition patch plugin.
    """
    
    def __init__(self, app):
        """
        Constructor of class CPatchPlugin.
        
        @type  app: CApplication
        @param app: UML .FRI application in which I am currently working.
        """
        #instance of apllication
        self.__app = app
        #UML .FRI drawing area
        self.drawing_area = self.__app.GetWindow('frmMain').picDrawingArea.picDrawingArea
        #handlers defined in this plugin
        self.__handler = None
        self.__handler2 = None
        self.__handler3 = None
        self.__handler4 = None
        self.__handler5 = None
        #indicates if settings were changed
        self.settingsChanged = False
        #number of pixels in current stroke
        self.counter = 0
        #check creation of graphic context
        self.init = False
        #Drawing area graphic context
        self.gc = None
        #gesture coordinates with symptoms
        self.pixels = []
        #method for paint from picdrawingarea in UML .FRI
        self.oldPaint = self.__app.GetWindow('frmMain').picDrawingArea.Paint
        #color of gesture
        self.color = '#00FF00'
        #size of gestures pixels
        self.size = 3
        #system gesture settings
        self.combos = [7,6,13,12]
        #current mouse position
        self.poz = ()
        #check id mouse position is on element or connection
        self.inObject = True
        #check if anything is selected
        self.selectedObject = False
        #minimalna stroke length
        self.minimumLength = 10
        
    def Start(self):
        """
        Patch plugin start.
        """
        self.__app.GetPluginAdapter().AddNotification('gestureModeStarted',self.GestureMode)
        self.__app.GetPluginAdapter().AddNotification('gesture-recognition',self.GestureRecognize)
        self.__app.GetPluginAdapter().AddNotification('changeGestureSettings',self.GestureSettings)
        
        if self.__app.GetPluginAdapter().GetProject() != None:
            self.__app.GetPluginAdapter().Notify('help-loaded',True)
        else:
            self.__app.GetPluginAdapter().Notify('help-loaded',False)
        
    def CanStop(self):
        """
        Method to stop Patch plugin.
        @rtype: bool
        return: plugin stopped
        """
        return True
    
    def CreateGraphicContext(self):
        """
        Create graphic context for drawing gesture.
        """
        self.cmap = self.drawing_area.window.get_colormap()
        self.gc = self.drawing_area.window.new_gc(foreground = self.cmap.alloc_color(self.color))
    
    @mainthread
    def GestureMode(self,mode):
        """
        Activate/deactivate gesture mode.
        
        @type  mode: bool
        @param mode: gestures on or gestures of
        """
        if mode == True:
            self.GesturesOn()
        else:
            self.GesturesOff()
    
    def GeneralGesture(self,index):
        """
        Execute action in combo under position defined index.
        
        @type  index: int
        @param index: position in combo in gesture settings
        """
        if index == 0:
            self.__app.GetWindow('frmMain').ActionOpen(self.__app.GetWindow('frmMain').cmdOpen)
            return
        if index == 1:
            self.__app.GetWindow('frmMain').ActionSave(self.__app.GetWindow('frmMain').cmdSave)
            return
        if index == 2:
            self.__app.GetWindow('frmMain').on_mnuOptions_activate(self.__app.GetWindow('frmMain').mnuOptions)
            return
        if index == 3:
            self.__app.GetWindow('frmMain').on_mnuExport_activate(self.__app.GetWindow('frmMain').mnuExport)
            return
        if index == 4:
            self.__app.GetWindow('frmMain').on_mnuAbout_activate(self.__app.GetWindow('frmMain').mnuAbout)
            return
        if index == 5:
            self.__app.GetWindow('frmMain').on_mnuWebsite_activate(self.__app.GetWindow('frmMain').mnuWebsite)
            return
        if index == 6:
            self.__app.GetWindow('frmMain').nbTabs.NextTab()
            return
        if index == 7:
            self.__app.GetWindow('frmMain').nbTabs.PreviousTab()
            return
        if index == 8:
            self.__app.GetWindow('frmMain').nbTabs.CloseTab(self.__app.GetWindow('frmMain').picDrawingArea.Diagram)
            return
        if index == 9:
            self.__app.GetWindow('frmMain').nbTabs.CloseAll()
            return
        if index == 10:
            self.__app.GetWindow('frmMain').mnuBestFit_click(self.__app.GetWindow('frmMain').mnuBestFit)
            self.Repaint()
            return
        if index == 11:
            self.__app.GetWindow('frmMain').mnuNormalSize_click(self.__app.GetWindow('frmMain').mnuNormalSize)
            return
        if index == 12:
            self.__app.GetWindow('frmMain').on_mnuZoomOut_click(self.__app.GetWindow('frmMain').mnuZoomOut)
            return
        if index == 13:
            self.__app.GetWindow('frmMain').on_mnuZoomIn_click(self.__app.GetWindow('frmMain').mnuZoomIn)
            return
            
    def AddElement(self,elementName):
        """
        Create element in picDrawingArea.
        
        @type  elementName: string
        @param elementName: name of the element to be created
        """
        ElementType = self.__app.GetProject().GetMetamodel().GetElementFactory().GetElement(elementName)
        ElementObject = CElementObject(ElementType)
        newElement = CElement(self.__app.GetWindow('frmMain').picDrawingArea.Diagram, ElementObject)
        newElement.SetPosition(self.poz)
        self.__app.GetWindow('frmMain').picDrawingArea.Diagram.DeselectAll()
        self.__app.GetWindow('frmMain').picDrawingArea.emit('add-element', ElementObject, self.__app.GetWindow('frmMain').picDrawingArea.Diagram, None)        
        self.__app.GetWindow('frmMain').picDrawingArea.Diagram.AddToSelection(newElement)
        self.__app.GetWindow('frmMain').picDrawingArea.emit('selected-item', list(self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetSelected()),True)                              
        self.Repaint()
        
    def AddConnection(self,variables):
        """
        Create connection in picDrawingArea.
        
        @type  variables: list
        @param variables: list of parameters(name,source,destination,bend points...) of connection to be created
        """
        source = self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetElementAtPosition(
                        self.__app.GetWindow('frmMain').picDrawingArea.canvas, variables[3])
        
        destination = self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetElementAtPosition(
                        self.__app.GetWindow('frmMain').picDrawingArea.canvas, variables[4])
        
        poz = -1
        for i in variables[5][1]:
            try:
                ConnectionType = self.__app.GetProject().GetMetamodel().GetConnectionFactory().GetConnection(i)
                obj = CConnectionObject(ConnectionType, source.GetObject(), destination.GetObject())
                poz = i 
            except ConnectionRestrictionError:
                pass
        if poz == -1:
            self.__app.GetWindow('frmMain').picDrawingArea.emit('run-dialog', 'warning', _('Invalid connection'))
            self.Repaint()
            return
        else:
            ConnectionType = self.__app.GetProject().GetMetamodel().GetConnectionFactory().GetConnection(poz)
            points = variables[2]
            obj = CConnectionObject(ConnectionType, source.GetObject(), destination.GetObject())
            x = CConnection(self.__app.GetWindow('frmMain').picDrawingArea.Diagram, obj, source, destination, points)
            self.__app.GetWindow('frmMain').picDrawingArea.Diagram.AddToSelection(x)
            self.__app.GetWindow('frmMain').picDrawingArea.emit('selected-item', list(self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetSelected()),True)
            self.Repaint()
    
    @mainthread
    def GestureRecognize(self,result):
        """
        Recognize gesture. Parameter result was send by plugin.
        
        @type  result: list
        @param result: result which contains information about recognized gesture
        """
        self.inObject = True
        self.ClearArea()
        if len(result) == 0:
            self.Blink()
            return
        if result[0] == 'unknown':
            self.Blink()
            return
        if result[0] == 'system':
            if result[1] == 'from right to left':
                self.GeneralGesture(self.combos[0])
                return
            if result[1] == 'from left to right':
                self.GeneralGesture(self.combos[1])
                return
            if result[1] == 'from down to up':
                self.GeneralGesture(self.combos[2])
                return
            if result[1] == 'from up to down':
                self.GeneralGesture(self.combos[3])
                return
        if result[0] == 'element':
            self.AddElement(result[2][1])
            return
        if result[0] == 'connection':
            self.AddConnection(result)
            return
        if result[0] == 'delete element':
            pos = (result[1][0],result[1][1])
            itemSel = self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetElementAtPosition(
            self.__app.GetWindow('frmMain').picDrawingArea.canvas, pos)
            self.__app.GetWindow('frmMain').picDrawingArea.Diagram.AddToSelection(itemSel)
            self.__app.GetWindow('frmMain').picDrawingArea.DeleteElements()
            return
        if result[0] == 'delete connection':
            pos = (result[1][0],result[1][1])
            itemSel = self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetElementAtPosition(
            self.__app.GetWindow('frmMain').picDrawingArea.canvas, pos)
            self.__app.GetWindow('frmMain').picDrawingArea.Diagram.AddToSelection(itemSel)
            self.__app.GetWindow('frmMain').picDrawingArea.DeleteElements()
            return
    
    def GestureSettings(self,size,color,combos):
        """
        Set gesture settings.
        
        @type  size: int
        @param size: gesture pixel size
        @type  color: string
        @param color: gesture color
        @type  combos: list
        @param combos: settings for system gestures
        """
        self.size = size
        self.color = color
        self.settingsChanged = True
        self.combos = combos
    
    def GesturesOn(self):
        """
        Turn gesture mode on.
        """
        self.__app.GetWindow('frmMain').picDrawingArea.on_picEventBox_button_press_event.disable()
        self.__app.GetWindow('frmMain').picDrawingArea.on_button_release_event.disable()
        self.__app.GetWindow('frmMain').picDrawingArea.on_motion_notify_event.disable()
        self.__app.GetWindow('frmMain').nbTabs.button_clicked.disable()
        self.__handler = self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.connect('button-press-event', self.__clicked)
        self.__handler2 = self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.connect('motion-notify-event', self.__motion)
        self.__handler3 = self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.connect('button-release-event', self.__released)
        self.__app.GetWindow('frmMain').picDrawingArea.Diagram.DeselectAll()
        self.__app.GetWindow('frmMain').tbToolBox.Hide()
        self.__app.GetWindow('frmMain').picDrawingArea.Paint = self.Repaint
        #help handlers
        self.__handler4 = self.__app.GetWindow('frmMain').nbTabs.nbTabs.connect('switch-page', self.ClearTabs)
        self.__handler5 = self.__app.GetWindow('frmMain').twProjectView.twProjectView.connect('button-press-event',self.ClearTree)
    
    def GesturesOff(self):
        """
        Turn gesture mode off.
        """
        self.__app.GetWindow('frmMain').picDrawingArea.on_picEventBox_button_press_event.enable()
        self.__app.GetWindow('frmMain').picDrawingArea.on_button_release_event.enable()
        self.__app.GetWindow('frmMain').picDrawingArea.on_motion_notify_event.enable()
        self.__app.GetWindow('frmMain').nbTabs.button_clicked.enable()
        self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.disconnect(self.__handler)
        self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.disconnect(self.__handler2)
        self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.disconnect(self.__handler3)
        self.__app.GetWindow('frmMain').nbTabs.nbTabs.disconnect(self.__handler4)
        self.__app.GetWindow('frmMain').twProjectView.twProjectView.disconnect(self.__handler5)
        self.__app.GetWindow('frmMain').tbToolBox.Show()
        del self.pixels[:]
        self.Repaint()
        self.__app.GetWindow('frmMain').picDrawingArea.Paint = self.oldPaint
    
    def Stop(self):
        """
        Stop patch plugin.
        """
        if self.__handler is not None:
            self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.disconnect(self.__handler)
            self.__handler = None
        if self.__handler2 is not None:
            self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.disconnect(self.__handler2)
            self.__handler2 = None
        if self.__handler3 is not None:
            self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.disconnect(self.__handler3)
            self.__handler3 = None
        if self.__handler4 is not None:
            self.__app.GetWindow('frmMain').nbTabs.nbTabs.disconnect(self.__handler4)
            self.__handler4 = None
        if self.__handler5 is not None:
            self.__app.GetWindow('frmMain').twProjectView.twProjectView.disconnect(self.__handler5)
            self.__handler5 = None
    
    def ClearTabs(self,parA,parB,parC):
        """
        Clear DrawingArea after switching tabs.
        
        @type  parA: gtk.Notebook
        @param parA: Notebook on which was executed action
        @type  parB: gpointer
        @param parB: click of the mouse
        @type  parC: int
        @param parC: position of tab on which was clicked
        """
        self.ClearArea()
    
    def ClearTree(self,parA,parB):
        """
        Clear DrawingArea after click in project tree.
        
        @type  parA: gtk.TreeView
        @param parA: TreeView on which was clicked
        @type  parB: gtk.gdk.Event
        @param parB: Event which execute this action
        """
        self.ClearArea()
    
    def DrawBrush(self,widget, x, y):
        """
        Repaint drawing area.
        
        @type  widget: gtk.EventBox
        @param widget: widget which execute this action
        @type  x: int
        @param x: x coordinate in picDrawingArea
        @type  y: int
        @param y: y coordinate in picDrawingArea
        """
        if self.selectedObject == True:
            self.selectedObject = False
            self.__app.GetWindow('frmMain').picDrawingArea.Diagram.DeselectAll()
            self.Repaint()
        
        self.counter = self.counter+1
        self.drawing_area.window.draw_rectangle(self.gc, True, x, y,self.size,self.size)
        
        pos = self.__app.GetWindow('frmMain').picDrawingArea.GetAbsolutePos((x, y))
        if len(self.pixels) > 0 and self.inObject == True:
            if isinstance(self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetElementAtPosition(
            self.__app.GetWindow('frmMain').picDrawingArea.canvas, (self.pixels[0][0],self.pixels[0][1])),CElement):
                if (self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetElementAtPosition(
                self.__app.GetWindow('frmMain').picDrawingArea.canvas, (self.pixels[0][0],self.pixels[0][1])) 
                != self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetElementAtPosition(
                self.__app.GetWindow('frmMain').picDrawingArea.canvas, pos)):
                    self.inObject = False
                    self.pixels.append([float(pos[0]),float(pos[1]),'V'])
                    return
        
        if self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetElementAtPosition(
           self.__app.GetWindow('frmMain').picDrawingArea.canvas, pos) == None:
            self.pixels.append([float(pos[0]),float(pos[1]),'N'])
        else:
            if isinstance(self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetElementAtPosition(
                self.__app.GetWindow('frmMain').picDrawingArea.canvas, pos),CElement):
                self.pixels.append([float(pos[0]),float(pos[1]),'AE'])
            if isinstance(self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetElementAtPosition(
               self.__app.GetWindow('frmMain').picDrawingArea.canvas, pos),CConnection):
                self.pixels.append([float(pos[0]),float(pos[1]),'AC'])
    
    def Blink(self):
        """
        Blink window.
        """
        x, y, width, height = self.drawing_area.get_allocation()
        self.drawing_area.window.draw_rectangle(self.gc,True,x, y, width,height)
        time.sleep(0.05)
        self.ClearArea()
    
    def Repaint(self,changed = True):
        """
        Repaint drawing area.
        @type changed: bool
        @param changed: if there was change in area
        """
        self.oldPaint()
        if len(self.pixels)>1:
            if self.drawing_area.window != None:
                for i in self.pixels[1:len(self.pixels)]:
                    self.drawing_area.window.draw_rectangle(self.gc, True, i[0], i[1],self.size,self.size)
    
    def ClearArea(self):
        """
        Clear drawing area.
        """
        del self.pixels[:]
        self.Repaint()
    
    def __motion(self,widget,event):
        """
        Mouse motion handler.
        
        @type widget: gtk.EventBox
        @param widget: EventBox in which this event is store
        @type event: gtk.gdk.Event
        @param event: Concrete event
        """
        state = event.state
        if state & gtk.gdk.BUTTON1_MASK:
            self.DrawBrush(widget, event.x, event.y)
    
    def __clicked(self, widget, event):
        """
        Mouse click handler.
        
        @type widget: gtk.EventBox
        @param widget: EventBox in which this event is store
        @type event: gtk.gdk.Event
        @param event: Concrete event
        """
        #initialize graphic context
        if self.init == False:
            self.init = True
            self.CreateGraphicContext()
        #set new settings fot gesture
        if self.settingsChanged == True:
            self.gc.foreground = self.cmap.alloc_color(self.color)
            self.ClearArea()
            self.settingsChanged = False
        
        if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
            if len(tuple(self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetSelected())) == 1:
                for Element in self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetSelected():
                    if isinstance(Element, (CElement,CConnection)):
                        self.__app.GetWindow('frmMain').picDrawingArea.emit('open-specification',Element)
                        return True
        
        if event.button == 1:
            if self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetSelected()>0:
                self.__app.GetWindow('frmMain').picDrawingArea.Diagram.DeselectAll()
            
            pos = self.__app.GetWindow('frmMain').picDrawingArea.GetAbsolutePos((event.x, event.y))
            itemSel = self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetElementAtPosition(
                      self.__app.GetWindow('frmMain').picDrawingArea.canvas,pos)
            #if under position is element or connection select it
            if (((isinstance(itemSel,CElement)) or (isinstance(itemSel,CConnection))) and
                (len(self.pixels) == 0)):
                    self.__app.GetWindow('frmMain').picDrawingArea.Diagram.AddToSelection(itemSel)
                    self.selectedObject = True
                    self.Repaint()
                    self.__app.GetWindow('frmMain').picDrawingArea.emit('selected-item', list(self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetSelected()),True)
            else:
                self.DrawBrush(widget, event.x, event.y)
        #senf coordinates for recognition
        if event.button == 3:
            #move element to position
            if len(self.pixels) == 0 and len(tuple(self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetSelected())) == 1:
                for Element in self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetSelected():
                    if isinstance(Element, CElement):
                        Element.SetPosition(pos = self.__app.GetWindow('frmMain').picDrawingArea.GetAbsolutePos((event.x, event.y)))
                        self.Repaint()
                        return
            if len(self.pixels) >= self.minimumLength:
                self.__app.GetPluginAdapter().Notify('gesture-invocated',self.pixels)
                self.poz = self.__app.GetWindow('frmMain').picDrawingArea.GetAbsolutePos((event.x, event.y))
            else:
                self.Blink()
    
    def __released(self,widget,event):
        """
        Mouse release handler.
        
        @type widget: gtk.EventBox
        @param widget: EventBox in which this event is store
        @type event: gtk.gdk.Event
        @param event: Concrete event
        """
        #if it is connection gesture there is added symptom to it
        if event.button == 1:
            if self.counter < self.minimumLength:
            #if stroke is too short the window blinks
                self.counter = 0
                if (self.selectedObject != True):
                    self.Blink()
                return
            #add symptom to connection
            if (self.pixels[0][2] == 'AE') and (self.pixels[len(self.pixels)-1][2] == 'AE'):
                self.pixels[len(self.pixels)-1][2] = 'X'
                self.counter = 0
                return
            self.pixels[len(self.pixels)-1][2] = 'P'
            self.counter = 0