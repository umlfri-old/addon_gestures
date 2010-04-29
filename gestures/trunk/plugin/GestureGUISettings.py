from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import gobject

import os
import os.path

class CGestureGUISettings(gobject.GObject):
    """
    Gesture settings user interface.
    """
    
    __gsignals__ = {
        'changeGestureSettings':  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_INT,gobject.TYPE_STRING,
                                                                                gobject.TYPE_INT,gobject.TYPE_INT,
                                                                                gobject.TYPE_INT,gobject.TYPE_INT))}
    def __init__(self):
        """
        Constructor of class CGestureGUISettings.
        """
        
        gobject.GObject.__init__(self)
        #glade file with GUI
        self.glade = os.path.join(os.path.dirname(__file__), 'gui', 'gestureSettings.glade')
        #tree of glade file
        self.wTree = gtk.glade.XML(self.glade)
        #check if gui is alreadz open
        self.open = False
        #gui window
        self.window = self.wTree.get_widget('frmGestureOptions')
        #gui ok button
        self.btnGui = self.wTree.get_widget('btnOk')
        #gui combo boxes
        self.combo1 = self.wTree.get_widget('combobox1')
        self.combo2 = self.wTree.get_widget('combobox2')
        self.combo3 = self.wTree.get_widget('combobox3')
        self.combo4 = self.wTree.get_widget('combobox4')
        #dictionary of events
        dic = {'on_btnOk_clicked' : self.on_btnOk_clicked,
               'on_btnDefault_clicked' : self.on_btnDefault_clicked,
               'on_frmGestureOptions_destroy' : self.on_frmGestureOptions_destroy}
        self.wTree.signal_autoconnect(dic)
        #gesture color
        self.color = '#00FF00'
        #gesture size
        self.size = 3
        #settings for system actions
        self.combos = [7,6,13,12]
        self.combo1.set_active(7)
        self.combo2.set_active(6)
        self.combo3.set_active(13)
        self.combo4.set_active(12)
    
    def Main(self):
        """
        Show gesture settings window.
        """
        self.SetOpen(True)
        self.window.show()
    
    def on_btnOk_clicked(self,widget):
        """
        Handler for click on ok button.
        
        @type  widget: gtk.Button
        @param widget: Button on which was clicked
        """
        self.color = self.wTree.get_widget("cbnLineColor").get_color()
        self.size = self.wTree.get_widget("sbpLineSize").get_value()
        self.combos[0] = self.combo1.get_active()
        self.combos[1] = self.combo2.get_active()
        self.combos[2] = self.combo3.get_active()
        self.combos[3] = self.combo4.get_active()
        self.emit('changeGestureSettings',self.size,self.color,self.combos[0],self.combos[1],self.combos[2],self.combos[3])
        self.on_frmGestureOptions_destroy(widget)
    
    def on_btnDefault_clicked(self,widget):
        """
        Set default settings to components.
        
        @type  widget: gtk.Button
        @param widget: Button on which was clicked
        """
        self.combo1.set_active(7)
        self.combo2.set_active(6)
        self.combo3.set_active(13)
        self.combo4.set_active(12)
        self.wTree.get_widget("sbpLineSize").set_value(3)
        self.wTree.get_widget("cbnLineColor").set_color(gtk.gdk.Color('#00FF00'))
    
    def on_frmGestureOptions_destroy(self,widget):
        """
        Hide opened window.
        
        @type  widget: gtk.Button
        @param widget: Button on which was clicked
        """
        self.window.hide()
        self.SetOpen(False)
    
    def SetOpen(self,bool):
        """
        Gesture Settings open setter.
        
        @type  bool: bool
        @param bool: indicates if window is already opened
        """
        self.open = bool
    
    def GetOpen(self):
        """
        Gesture Settings open getter.
        
        @rtype : bool
        @return: sends message which says state of window
        """
        return self.open