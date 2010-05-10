from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import gobject

import os
import os.path
import sys

class CGestureGUIHelp(object):
    """
    Gesture Help user interface.
    """
    
    def __init__(self):
        """
        Constructor of class CGEestureGUIHelp
        """
        self.InitComponents()
        #check if combos were loaded
        self.loaded = False
        #current metamodel name
        self.metamodel = 'unknown'
        #data for generating help
        self.data = []
        #pixbuf width
        self.width = 61
        #pixbuf height
        self.height = 61
        #color help
        self.color = '#00FF00'
        #actions indexes
        self.combos = [7,6,13,12]
        self.CreateGeneralHelp()
        #items loaded
        self.count = 0
        #current diagram
        self.diagram = ""
    
    def InitComponents(self):
        """
        Gesture Help user interface component initialization.
        """
        self.dialog = gtk.Dialog('Gestures help')
        self.dialog.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.dialog.connect('delete-event',self.__CloseDialogHandler2)
        button = gtk.Button('Close')
        button.connect('clicked',self.__CloseDialogHandler,self.dialog)
        self.dialog.action_area.pack_end(button,False,False)
        label = gtk.Label('Diagrams:')
        alg = gtk.Alignment(0,0)
        alg.add(label)
        self.combo = gtk.combo_box_new_text()
        self.combo.connect('changed',self.__ComboHandler)
        self.dialog.vbox.pack_start(alg,False,False)
        self.dialog.vbox.pack_start(self.combo,False,False)
        label = gtk.Label('Instructions:')
        alg = gtk.Alignment(0,0)
        alg.set_padding(5,0,0,0)
        
        alg.add(label)
        text = gtk.TextView()
        self.dialog.vbox.pack_start(alg,False,False)
        self.dialog.vbox.pack_start(text,False,False)
        
        ic = os.path.join(os.path.dirname(__file__), 'gui','gesturesHelp.txt')
        infile = open(ic, 'r')
        if infile:
            string = infile.read()
        infile.close()
        text.get_buffer().set_text(string)
        
        text.set_editable(False)
        label = gtk.Label('Gestures table:')
        alg = gtk.Alignment(0,0)
        alg.set_padding(5,0,0,0)
        alg.add(label)
        self.dialog.vbox.pack_start(alg,False,False)
        
        self.store = gtk.ListStore(gtk.gdk.Pixbuf,gtk.gdk.Pixbuf,gtk.gdk.Pixbuf,gtk.gdk.Pixbuf,gtk.gdk.Pixbuf,str)
        self.treeview = gtk.TreeView(self.store)
        
        scroll = gtk.ScrolledWindow()
        scroll.add(self.treeview)
        scroll.set_size_request(0,220)
        scroll.set_policy(gtk.POLICY_NEVER,gtk.POLICY_AUTOMATIC)
        
        tvcolumn = gtk.TreeViewColumn('Gesture')
        self.treeview.append_column(tvcolumn)
        cell = gtk.CellRendererPixbuf()
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'pixbuf', 0)
        
        tvcolumn = gtk.TreeViewColumn()
        self.treeview.append_column(tvcolumn)
        cell = gtk.CellRendererPixbuf()
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'pixbuf', 1)
        
        tvcolumn = gtk.TreeViewColumn()
        self.treeview.append_column(tvcolumn)
        cell = gtk.CellRendererPixbuf()
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'pixbuf', 2)
        
        tvcolumn = gtk.TreeViewColumn()
        self.treeview.append_column(tvcolumn)
        cell = gtk.CellRendererPixbuf()
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'pixbuf', 3)
        
        tvcolumn = gtk.TreeViewColumn('Effect')
        self.treeview.append_column(tvcolumn)
        cell = gtk.CellRendererPixbuf()
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'pixbuf', 4)
        
        tvcolumn = gtk.TreeViewColumn('Description')
        self.treeview.append_column(tvcolumn)
        cell = gtk.CellRendererText()
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'text', 5)
        self.dialog.vbox.pack_start(scroll,True,True)
    
    def __CloseDialogHandler(self,button,dg):
        """
        Handler for hiding Help dialog.
        
        @type button: gtk.Button
        @param button: Button on which was clicked.
        @type dg: gtk.Dialog
        @param dg: dialog which was hide
        """
        dg.hide()
    
    def __CloseDialogHandler2(self,dg,event):
        """
        Handler for hiding Help dialog.
        
        @type dg: gtk.Dialog
        @param dg: dialog which was hide
        @type event: gtk.gdk.Event
        @param event: event which hide the dialog
        """
        dg.hide()
        return True
    
    def __ComboHandler(self,widget):
        """
        Handler for changing combos.
        
        @type widget: gtk.ComboBox
        @param widget: Combobox on which was changed item
        """
        if self.combo.get_active() == 0:
            self.DrawGeneralHelp()
        else:
            self.LoadCombo(self.combo.get_active()-1)
    
    def ShowHelpDialog(self): 
        """
        Show dialog, if its shown for firs time create pixmap, color map and grpahic context.
        """
        self.dialog.show_all()
        if self.loaded == False:
            self.loaded = True
            self.pixmap = gtk.gdk.Pixmap(self.dialog.window, self.width, self.height)
            self.cmap = self.dialog.window.get_colormap()
            self.gc = self.dialog.window.new_gc(foreground = self.cmap.alloc_color(self.color))
        self.combo.set_active(0)
    
    def FillHelp(self):
        """
        Fill combo boxes with diagram names.
        """
        for i in range(len(self.data)):
            self.combo.append_text(self.data[i][0])
    
    def AddComboItems(self):
        """
        Add new combo to Combo Box.
        """ 
        if len(self.data) == 0:
            return
        for i in range(len(self.data)):
            self.combo.append_text(self.data[i][0])
        self.count = len(self.data)
    
    def DrawGeneralHelp(self):
        """
        Create pictures for general help.
        """
        self.store.clear()
        pxb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8, self.width,self.height)
        self.gc.foreground = self.cmap.alloc_color('#FFFFFF')
        self.pixmap.draw_rectangle(self.gc, True, 0, 0, 60, 60)
        self.gc.foreground = self.cmap.alloc_color('#000000')
        self.pixmap.draw_rectangle(self.gc, False, 0, 0, 60, 60)
        self.gc.foreground = self.cmap.alloc_color(self.color)
        self.pixmap.draw_arc(self.gc, True, 10, 20, 15, 15, 0, 360*64)
        self.pixmap.draw_rectangle(self.gc, True, 18, 25, 32, 5)
        pxb.get_from_drawable(self.pixmap,self.cmap,0,0,0,0,self.width,self.height)
        self.store.append([pxb,None,None,None,None,'Line to LEFT: '+self.ReturnEffect(self.combos[0])])
        
        pxb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8, self.width,self.height)
        self.gc.foreground = self.cmap.alloc_color('#FFFFFF')
        self.pixmap.draw_rectangle(self.gc, True, 0, 0, 60, 60)
        self.gc.foreground = self.cmap.alloc_color('#000000')
        self.pixmap.draw_rectangle(self.gc, False, 0, 0, 60, 60)
        self.gc.foreground = self.cmap.alloc_color(self.color)
        self.pixmap.draw_arc(self.gc, True, 40, 20, 15, 15, 0, 360*64)
        self.pixmap.draw_rectangle(self.gc, True, 10, 25, 32, 5)
        pxb.get_from_drawable(self.pixmap,self.cmap,0,0,0,0,self.width,self.height)
        self.store.append([pxb,None,None,None,None,'Line to RIGHT: '+self.ReturnEffect(self.combos[1])])
        
        pxb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8, self.width,self.height)
        self.gc.foreground = self.cmap.alloc_color('#FFFFFF')
        self.pixmap.draw_rectangle(self.gc, True, 0, 0, 60, 60)
        self.gc.foreground = self.cmap.alloc_color('#000000')
        self.pixmap.draw_rectangle(self.gc, False, 0, 0, 60, 60)
        self.gc.foreground = self.cmap.alloc_color(self.color)
        self.pixmap.draw_arc(self.gc, True, 20, 10, 15, 15, 0, 360*64)
        self.pixmap.draw_rectangle(self.gc, True, 25, 10, 5, 40)
        pxb.get_from_drawable(self.pixmap,self.cmap,0,0,0,0,self.width,self.height)
        self.store.append([pxb,None,None,None,None,'Line to UP: '+self.ReturnEffect(self.combos[2])])
        
        pxb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8, self.width,self.height)
        self.gc.foreground = self.cmap.alloc_color('#FFFFFF')
        self.pixmap.draw_rectangle(self.gc, True, 0, 0, 60, 60)
        self.gc.foreground = self.cmap.alloc_color('#000000')
        self.pixmap.draw_rectangle(self.gc, False, 0, 0, 60, 60)
        self.gc.foreground = self.cmap.alloc_color(self.color)
        self.pixmap.draw_arc(self.gc, True, 20, 40, 15, 15, 0, 360*64)
        self.pixmap.draw_rectangle(self.gc, True, 25, 10, 5, 40)
        pxb.get_from_drawable(self.pixmap,self.cmap,0,0,0,0,self.width,self.height)
        self.store.append([pxb,None,None,None,None,'Line to DOWN: '+self.ReturnEffect(self.combos[3])])
        
        pxb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8, self.width,self.height)
        self.gc.foreground = self.cmap.alloc_color('#FFFFFF')
        self.pixmap.draw_rectangle(self.gc, True, 0, 0, 60, 60)
        self.gc.foreground = self.cmap.alloc_color('#000000')
        self.pixmap.draw_rectangle(self.gc, False, 0, 0, 60, 60)
        self.pixmap.draw_rectangle(self.gc, False, 10, 10, 40, 40)
        self.pixmap.draw_rectangle(self.gc, False, 11, 11, 38, 38)
        self.pixmap.draw_rectangle(self.gc, False, 12, 12, 36, 36)
        self.pixmap.draw_rectangle(self.gc, True, 10, 20, 40,3)
        self.gc.foreground = self.cmap.alloc_color(self.color)
        self.pixmap.draw_arc(self.gc, True, 25, 25, 15, 15, 0, 360*64)
        pxb.get_from_drawable(self.pixmap,self.cmap,0,0,0,0,self.width,self.height)
        self.store.append([pxb,None,None,None,None,'Delete ELEMENT'])
        
        pxb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8, self.width,self.height)
        self.gc.foreground = self.cmap.alloc_color("#FFFFFF")
        self.pixmap.draw_rectangle(self.gc, True, 0, 0, 60, 60)
        self.gc.foreground = self.cmap.alloc_color("#000000")
        self.pixmap.draw_rectangle(self.gc, False, 0, 0, 60, 60)
        self.pixmap.draw_rectangle(self.gc, True, 10, 25, 40,3)
        self.gc.foreground = self.cmap.alloc_color(self.color)
        self.pixmap.draw_arc(self.gc, True, 25, 20, 15, 15, 0, 360*64)
        pxb.get_from_drawable(self.pixmap,self.cmap,0,0,0,0,self.width,self.height)
        self.store.append([pxb,None,None,None,None,'Delete CONNECTION'])
    
    def LoadCombo(self,index):
        """
        Load help for diagram selected from combo box.
        
        @type index: int
        @param index: index of item selected from combo box
        """
        self.store.clear()
        for i in range(len(self.data[index])-1):
            loader = gtk.gdk.PixbufLoader()
            pathx = self.data[index][i+1][0]
            loader.write(pathx)
            loader.close()
            tmp = loader.get_pixbuf()
            obr1 = self.CreatePixbufFromBox(self.data[index][i+1][1][0].GetGestureBox(),self.data[index][i+1][1][0].GetHelpLines())
            if len(self.data[index][i+1][1])>1:
                obr2 = self.CreatePixbufFromBox(self.data[index][i+1][1][1].GetGestureBox(),self.data[index][i+1][1][1].GetHelpLines())
            else:
                obr2 = None
            if len(self.data[index][i+1][1])>2:
                obr3 = self.CreatePixbufFromBox(self.data[index][i+1][1][2].GetGestureBox(),self.data[index][i+1][1][2].GetHelpLines())
            else:
                obr3 = None
            if len(self.data[index][i+1][1])>3:
                obr4 = self.CreatePixbufFromBox(self.data[index][i+1][1][3].GetGestureBox(),self.data[index][i+1][1][3].GetHelpLines())
            else:
                obr4 = None
            self.store.append([obr1,obr2,obr3,obr4,tmp,self.data[index][i+1][2]])
    
    def CreatePixbufFromBox(self,paBox,paLines):
        """
        Create gesture pictures from description.
        
        @type paBox: list
        @param paBox: gesture description's boundary box
        @type paLines: list
        @param paLines: gesture description's help vectors
        """
        empty = True
        size = len(paBox[0])
        for i in range(size):
            for j in range(size):
                if paBox[i][j] == 1:
                    empty = False
                    break
        pxb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8, self.width,self.height)
        self.gc.foreground = self.cmap.alloc_color('#FFFFFF')
        self.pixmap.draw_rectangle(self.gc, True, 0, 0, 60, 60)
        self.gc.foreground = self.cmap.alloc_color('#000000')
        self.pixmap.draw_rectangle(self.gc, False, 0, 0, 60, 60)
        self.gc.foreground = self.cmap.alloc_color(self.color)
        self.gc.line_width = 4
        
        for i in range(len(paLines)):
            a = paLines[i][0].partition(',')
            b = paLines[i][1].partition(',')
            x1 = 5 + int(50*(float(a[0])))
            y1 = 5 + int(50*(1-float(a[2])))
            x2 = 5 + int(50*(float(b[0])))
            y2 = 5 + int(50*(1-float(b[2])))
            self.pixmap.draw_line(self.gc, x1, y1, x2, y2)
        self.gc.line_width = 0
        if empty == False:
            pxb.get_from_drawable(self.pixmap,self.cmap,0,0,0,0,self.width,self.height)
            return pxb
        else:
            self.gc.foreground = self.cmap.alloc_color('#000000')
            self.pixmap.draw_rectangle(self.gc, False, 5, 5, 20, 20)
            self.pixmap.draw_rectangle(self.gc, False, 6, 6, 18, 18)
            self.pixmap.draw_rectangle(self.gc, False, 7, 7, 16, 16)
            self.pixmap.draw_rectangle(self.gc, False, 35, 35, 20, 20)
            self.pixmap.draw_rectangle(self.gc, False, 36, 36, 18, 18)
            self.pixmap.draw_rectangle(self.gc, False, 37, 37, 16, 16)
            self.gc.foreground = self.cmap.alloc_color(self.color)
            self.gc.line_width = 4
            self.pixmap.draw_line(self.gc,15, 15, 45, 45)
            self.gc.line_width = 0
            pxb.get_from_drawable(self.pixmap,self.cmap,0,0,0,0,self.width,self.height)
            return pxb
    
    def CreateGeneralHelp(self):
        """
        Add general help item to combo box.
        """
        self.combo.append_text('General')
    
    def SetMetamodel(self,parameter):
        """
        Metamodel name setter.
        
        @type parameter: string
        @param parameter: name of loaded metamodel
        """
        self.metamodel = parameter
    
    def GetMetamodel(self):
        """
        Metamodel name getter.
        
        @rtype : string
        @return: name of loaded metamodel
        """
        return self.metamodel
    
    def SetData(self,paData):
        """
        Data loaded from metamodel setter.
        
        @type paData: list
        @param paData: data which contains information about gestures help to be generated
        """
        self.data = paData
        if self.count > 0:
            for i in range(self.count):
                self.combo.remove_text(1)
            self.count = 0
        self.AddComboItems()
    
    def GetData(self):
        """
        Data in metamodel getter.
        
        @rtype : list
        @return: data in which are information about current metamodel elements and connections
        """
        return self.data
    
    def SetColor(self,paColor):
        """
        Help color setter.
        
        @type paColor: string
        @param paColor: Color used to paint gestures help
        """
        self.color = paColor
    
    def SetCombos(self,paCombos):
        """
        Combo strings name setter.
        
        @type paCombos: list
        @param paCombos: list of system gesture settings
        """
        self.combos = paCombos
    
    def SetCurrentDiagram(self,paDiagram):
        """
        Current diagram name setter.
        
        @type paDiagram: string
        @param paDiagram: name of current diagram
        """
        self.diagram = paDiagram
    
    def ReturnEffect(self,index):
        """
        Returns name of action under index in combo box.
        
        @type index: int
        @param index: combo box index
        @rtype : string
        @return: name of action
        """
        if index == 0:
            return 'Open project'
        if index == 1:
            return 'Save project'
        if index == 2:
            return 'Open options'
        if index == 3:
            return 'Export diagram'
        if index == 4:
            return 'About'
        if index == 5:
            return 'Website'
        if index == 6:
            return 'Next tab'
        if index == 7:
            return 'Previous tab'
        if index == 8:
            return 'Close tab'
        if index == 9:
            return 'Close all tabs'
        if index == 10:
            return 'Best fit'
        if index == 11:
            return 'Normal size'
        if index == 12:
            return 'Zoom in'
        if index == 13:
            return 'Zoom out'