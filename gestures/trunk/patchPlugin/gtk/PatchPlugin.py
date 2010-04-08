from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import gobject
import os
import time

from lib.Drawing.Canvas import CGtkCanvas, CSvgCanvas, CCairoCanvas, CExportCanvas
from lib.Drawing import Element

#from share.addons.gestures.gestureLogic.GestureManager import CGestureManager

class CPatchPlugin(gobject.GObject):
    __gsignals__ = {
       'sendDrawingCoordinates':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_INT,gobject.TYPE_STRING))}    
    
    def __init__(self, app):
        gobject.GObject.__init__(self)
        print os.getcwd()
        #ISTY KOD
        self.__app = app
        self.drawing_area = self.__app.GetWindow('frmMain').picDrawingArea.picDrawingArea        
        self.__handler = None
        self.__handler2 = None
        self.__handler3 = None
        self.counter = 0
        self.init = False                
        self.gc = None   
        self.pixels = [()]
        self.helpPixels = [()]        
        self.oldPaint = self.__app.GetWindow('frmMain').picDrawingArea.Paint
        self.color = '#00FF00'         
        self.size = 3 
        
        #self.manager = CGestureManager()
        #print self.manager
        #self.__app.GetWindow('frmMain').tbToolBox.Hide()                    
                                                                     
        #self.__app.GetWindow('frmMain').tbToolBox.Show()                    
        self.minz = 9999
        self.maxv = 0
        self.mins = 9999
        self.maxj = 0 
        #for x in self.zoznam_suradnic[1:len(self.zoznam_suradnic)]:
         #   if x[0] >maxv: maxv=x[0]
          #  if x[0] <minz: minz=x[0]
           # if x[1] >maxj: maxj=x[1]
#            if x[1] <mins: mins=x[1] 
                                  
    def Start(self):
        print 'Example patch plugin started'
        self.__app.GetPluginAdapter().AddNotification('gestureModeStarted',self.GestureMode)
        #self.__app.GetPluginAdapter().AddNotification('gestureModeStarted',self.GestureSettings)
        
    def CanStop(self):
        return True
    
    def CreateGraphicContext(self):
        self.gc =  self.drawing_area.window.new_gc(foreground = gtk.gdk.Color(self.color))        
        pass

    def GestureMode(self,mode):
        print mode        
        if mode == True:
            print "A"
            self.GesturesOn()
            #print
            #if self.init == False:
            #self.__app.GetWindow('frmMain').tbToolBox.Hide()
            #self.__app.GetWindow('frmMain').tbToolBox.Hide() 
        else:
            print "B"
            self.GesturesOff()
            
                     
    def GestureSettings(self,color,size):
        print color
        print size
        print "ZMENA"
                
    def GesturesOn(self):
        self.__app.GetWindow('frmMain').picDrawingArea.on_picEventBox_button_press_event.disable()
        self.__app.GetWindow('frmMain').picDrawingArea.on_button_release_event.disable()
        self.__app.GetWindow('frmMain').picDrawingArea.on_motion_notify_event.disable()
        self.__app.GetWindow('frmMain').nbTabs.button_clicked.disable()
        self.__handler = self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.connect('button-press-event', self.__clicked)        
        self.__handler2 = self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.connect('motion-notify-event', self.__motion)
        self.__handler3 = self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.connect('button-release-event', self.__released)                
        self.__app.GetWindow('frmMain').picDrawingArea.Paint = self.Repaint
        
        #self.DiagramType = self.__app.GetProject().GetMetamodel().GetDiagramFactory().GetDiagram(DiagramId) 
        #self.__app.GetWindow('frmMain').tbToolBox.SetVisible(False) 
            
                                                    
    def GesturesOff(self):
        self.__app.GetWindow('frmMain').picDrawingArea.on_picEventBox_button_press_event.enable()
        self.__app.GetWindow('frmMain').picDrawingArea.on_button_release_event.enable()
        self.__app.GetWindow('frmMain').picDrawingArea.on_motion_notify_event.enable()
        self.__app.GetWindow('frmMain').nbTabs.button_clicked.enable()
        self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.disconnect(self.__handler)
        self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.disconnect(self.__handler2)
        self.__app.GetWindow('frmMain').picDrawingArea.picEventBox.disconnect(self.__handler3)
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
                                
    def DrawBrush(self,widget, x, y):
        self.counter = self.counter+1
        self.pixels.append((x,y))            
        self.drawing_area.window.draw_rectangle(self.gc, True, x, y,self.size,self.size)
        
    def prebliknutie(self):
        x, y, width, height = self.drawing_area.get_allocation()
        self.drawing_area.window.draw_rectangle(self.gc,True,x, y, width,height)                        
        self.gc.set_foreground(gtk.gdk.Color('#ffffffffffff'))
        time.sleep(0.15)
        self.gc.set_foreground(gtk.gdk.Color(self.color))        
        self.Repaint()
                                                        
    def Repaint(self,changed = True):
        self.oldPaint()
        if len(self.pixels)>1:       
            for i in self.pixels[1:len(self.pixels)]:
                self.drawing_area.window.draw_rectangle(self.gc, True, i[0], i[1],3,3)        
                
    def ClearPixels(self):
        if len(self.pixels)>1:
            actualColor = self.gc.foreground
            print actualColor 
            self.gc.set_foreground(gtk.gdk.Color('#FFFFFF'))
            for i in self.pixels[1:len(self.pixels)]:
                self.drawing_area.window.draw_rectangle(self.gc, True, i[0], i[1],self.size,self.size)
            self.gc.foreground = self.color                
        del self.pixels[:]
                       
    def __motion(self,widget,event):
            state = event.state
            if state & gtk.gdk.BUTTON1_MASK:
                self.DrawBrush(widget, event.x, event.y)
                        
    def __clicked(self, widget, event):
        if self.init == False:
            self.init = True
            self.CreateGraphicContext()
            #self.__app.GetWindow('frmMain').tbToolBox.Hide()                    
        self.DrawBrush(widget, event.x, event.y)    
        
        if event.button == 3:
            print "PRAVE"
            #self.prebliknutie()
        print 'You clicked at (%.0f, %0f) with button no. %d' % (event.x, event.y, event.button)
                    
    def __released(self,widget,event):
        roz = 0;
        for i in self.pixels[2:len(self.pixels)]:
            roz = self.pixels[1][1]-i[1]
            print roz                 
        if self.counter<20:
            #este prebliknutie
            self.prebliknutie()
            del self.pixels[:]
            self.Repaint()
        self.counter = 0