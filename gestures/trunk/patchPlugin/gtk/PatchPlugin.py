from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import gobject
from lib.Connections import CConnectionObject
from lib.Drawing import CConnection,CElement
from lib.Exceptions.UserException import *

from lib.Elements import CElementObject

from lib.Addons.Plugin.Interface.decorators import *

import os
import time

from lib.Drawing.Canvas import CGtkCanvas, CSvgCanvas, CCairoCanvas, CExportCanvas
from lib.Drawing import Element

from lib.consts import BUFFER_SIZE, SCALE_MIN, SCALE_MAX, SCALE_INCREASE

class CPatchPlugin():

    def __init__(self, app):     
        self.__app = app
        self.drawing_area = self.__app.GetWindow('frmMain').picDrawingArea.picDrawingArea        
        self.__handler = None
        self.__handler2 = None
        self.__handler3 = None
        self.counter = 0
        self.init = False                
        self.gc = None   
        self.pixels = []
        self.oldPaint = self.__app.GetWindow('frmMain').picDrawingArea.Paint
        self.color = '#00FF00'         
        self.size = 3 
        self.poz = ()
        self.inObject = True
        self.selectedObject = False 
        #minimalna dlzka ciary
        self.minimumLength = 10                                                                             
                                  
    def Start(self):
        print 'Example patch plugin started'
        self.__app.GetPluginAdapter().AddNotification('gestureModeStarted',self.GestureMode)
        self.__app.GetPluginAdapter().AddNotification('gesture-recognition',self.GestureRecognize)        
        self.__app.GetPluginAdapter().AddNotification('changeGestureSettings',self.GestureSettings)
        
    def CanStop(self):
        return True
    
    def CreateGraphicContext(self):
        self.gc =  self.drawing_area.window.new_gc()        
        #self.gc.foreground = gtk.gdk.Color(self.color)        

    @mainthread   
    def GestureMode(self,mode):
        print mode        
        if mode == True:                                                        
            self.GesturesOn()
        else:
            self.GesturesOff()
            
    def AddElement(self,elementName):
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
        source = self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetElementAtPosition(                                                                                        
                        self.__app.GetWindow('frmMain').picDrawingArea.canvas, variables[3])
        
        destination = self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetElementAtPosition(                                                                                        
                        self.__app.GetWindow('frmMain').picDrawingArea.canvas, variables[4])                
        if (source.GetObject().GetType().GetId()=='Note' or 
           destination.GetObject().GetType().GetId()=='Note'):
            type = 'Note Link'
        else:
            type = variables[5][1]
        try:                            
            ConnectionType = self.__app.GetProject().GetMetamodel().GetConnectionFactory().GetConnection(type)        
            points = variables[2]
            obj = CConnectionObject(ConnectionType, source.GetObject(), destination.GetObject())
            x = CConnection(self.__app.GetWindow('frmMain').picDrawingArea.Diagram, obj, source, destination, points)
            self.__app.GetWindow('frmMain').picDrawingArea.Diagram.AddToSelection(x)
            self.__app.GetWindow('frmMain').picDrawingArea.emit('selected-item', list(self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetSelected()),True)
            self.Repaint()
        except ConnectionRestrictionError:
            self.Repaint()        
            self.__app.GetWindow('frmMain').picDrawingArea.emit('run-dialog', 'warning', _('Invalid connection'))
              
    @mainthread                               
    def GestureRecognize(self,result):
        self.inObject = True
        self.ClearArea()
        if result[0] == 'unknown':
            self.prebliknutie()
            return   
        if result[0] == 'system':
            if result[1] == 'from left to right':
                self.__app.GetWindow('frmMain').nbTabs.NextTab()        
                return
            if result[1] == 'from right to left':
                self.__app.GetWindow('frmMain').nbTabs.PreviousTab()
                return
            if result[1] == 'from up to down':
                self.__app.GetWindow('frmMain').picDrawingArea.IncScale(SCALE_INCREASE)
                self.__app.GetWindow('frmMain').UpdateMenuSensitivity()
                return            
            if result[1] == 'from down to up':
                self.__app.GetWindow('frmMain').picDrawingArea.IncScale(-SCALE_INCREASE)
                self.__app.GetWindow('frmMain').UpdateMenuSensitivity()
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
    
    def GestureSettings(self,size,color):        
        self.size = size
        self.color = color
        self.gc.foreground = gtk.gdk.Color(self.color)        
        self.ClearArea()
                
    def GesturesOn(self):
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
                                                    
    def GesturesOff(self):
        self.__app.GetWindow('frmMain').picDrawingArea.on_picEventBox_button_press_event.enable()
        self.__app.GetWindow('frmMain').picDrawingArea.on_button_release_event.enable()
        self.__app.GetWindow('frmMain').picDrawingArea.on_motion_notify_event.enable()
        self.__app.GetWindow('frmMain').nbTabs.button_clicked.enable()
        self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.disconnect(self.__handler)
        self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.disconnect(self.__handler2)
        self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.disconnect(self.__handler3)
        self.__app.GetWindow('frmMain').tbToolBox.Show()                                    
        del self.pixels[:]  
        self.Repaint()
        self.__app.GetWindow('frmMain').picDrawingArea.Paint = self.oldPaint
                                
    def Stop(self):
        print 'Example patch plugin stopped'        
        if self.__handler is not None:
            self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.disconnect(self.__handler)
            self.__handler = None
        if self.__handler2 is not None:
            self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.disconnect(self.__handler2)
            self.__handler2 = None
        if self.__handler3 is not None:
            self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.disconnect(self.__handler3)
            self.__handler3 = None
                                
    def DrawBrush(self,widget, x, y):
        if self.selectedObject == True:
            self.selectedObject = False
            self.__app.GetWindow('frmMain').picDrawingArea.Diagram.DeselectAll()
            #self.__app.GetWindow('frmMain').picDrawingArea.emit('selected-item', list(self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetSelected()),False)                    
            self.Repaint()

        self.counter = self.counter+1        
        self.drawing_area.window.draw_rectangle(self.gc, True, x, y,self.size,self.size)
        
        pos = (x,y)        
        if len(self.pixels)>0 and self.inObject == True:
            if isinstance(self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetElementAtPosition(                                                                                        
            self.__app.GetWindow('frmMain').picDrawingArea.canvas, (self.pixels[0][0],self.pixels[0][1])),CElement):            
                if (self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetElementAtPosition(                                                                                        
                self.__app.GetWindow('frmMain').picDrawingArea.canvas, (self.pixels[0][0],self.pixels[0][1])) 
                != self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetElementAtPosition(                                                                                        
                self.__app.GetWindow('frmMain').picDrawingArea.canvas, pos)):
                    self.inObject = False
                    self.pixels.append([x,y,'V'])
                    return
        
        if self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetElementAtPosition(                                                                                        
           self.__app.GetWindow('frmMain').picDrawingArea.canvas, pos) == None:
            self.pixels.append([x,y,'N'])
        else:
            if isinstance(self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetElementAtPosition(                                                                                        
                self.__app.GetWindow('frmMain').picDrawingArea.canvas, pos),CElement):
                self.pixels.append([x,y,'AE'])
            if isinstance(self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetElementAtPosition(                                                                                        
               self.__app.GetWindow('frmMain').picDrawingArea.canvas, pos),CConnection):
                self.pixels.append([x,y,'AC'])                                                
        
    def prebliknutie(self):
        x, y, width, height = self.drawing_area.get_allocation()
        self.drawing_area.window.draw_rectangle(self.gc,True,x, y, width,height)                        
        time.sleep(0.05)
        self.ClearArea()
                                                        
    def Repaint(self,changed = True):
        self.oldPaint()        
        if len(self.pixels)>1:       
            for i in self.pixels[1:len(self.pixels)]:
                self.drawing_area.window.draw_rectangle(self.gc, True, i[0], i[1],3,3)
            
    def ClearArea(self):
        del self.pixels[:]
        self.Repaint()

    def __motion(self,widget,event):
            state = event.state
            if state & gtk.gdk.BUTTON1_MASK:
                self.DrawBrush(widget, event.x, event.y)
                        
    def __clicked(self, widget, event):
        if self.init == False:
            self.init = True
            self.CreateGraphicContext()
                               
        if event.button == 1:
            if self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetSelected()>0:
                self.__app.GetWindow('frmMain').picDrawingArea.Diagram.DeselectAll()
            
            pos = (event.x,event.y)
            itemSel = self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetElementAtPosition(
                      self.__app.GetWindow('frmMain').picDrawingArea.canvas,pos)            
            if (((isinstance(itemSel,CElement)) or (isinstance(itemSel,CConnection))) and 
                (len(self.pixels)==0)):
                    self.__app.GetWindow('frmMain').picDrawingArea.Diagram.DeselectAll()
                    self.__app.GetWindow('frmMain').picDrawingArea.Diagram.AddToSelection(itemSel)
                    self.selectedObject = True
                    self.Repaint()
                    self.__app.GetWindow('frmMain').picDrawingArea.emit('selected-item', list(self.__app.GetWindow('frmMain').picDrawingArea.Diagram.GetSelected()),True)                    
            else:
                self.DrawBrush(widget, event.x, event.y)
                    
        if event.button == 3:
            if len(self.pixels)>=self.minimumLength:
                self.__app.GetPluginAdapter().Notify('gesture-invocated',self.pixels)
                self.poz = (event.x,event.y)
            else:
                self.prebliknutie()
        print 'You clicked at (%.0f, %0f) with button no. %d' % (event.x, event.y, event.button)
                    
    def __released(self,widget,event):            
        #ak sa jedna o gesto spojenia, musi byt zlozene z dvoch tahov, pri pusteni mysi sa nastavi priznak      
        if event.button == 1:
            if self.counter<self.minimumLength:
            #prebliknutie pri kratkom geste
                self.prebliknutie()
                self.counter = 0
                return
            #Pridanie priznaku spojenia            
            if (self.pixels[0][2] == 'AE') and (self.pixels[len(self.pixels)-1][2]=='AE'):
                self.pixels[len(self.pixels)-1][2] = 'X'
                self.counter = 0
                return          
            self.pixels[len(self.pixels)-1][2] = 'P'
            self.counter = 0                                
            