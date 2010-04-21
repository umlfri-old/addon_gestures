from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import gobject

import os
import os.path
import sys

class CGestureGUIHelp(object):            
    def __init__(self):
        self.InitComponents()
        self.items = []
        
                
        self.loaded = False
        self.metamodel = "unknown"
        self.data = []
        
        #self.AddGeneralHelp()
            
    def InitComponents(self):
        self.dialog = gtk.Dialog('Gestures help')
        self.dialog.connect('delete-event',self.__CloseDialogHandler2)
        button = gtk.Button('Close')
        button.connect('clicked',self.__CloseDialogHandler,self.dialog)
        self.dialog.action_area.pack_end(button,False,False)
        label = gtk.Label('Diagrams:')
        alg = gtk.Alignment(0,0)
        alg.add(label)
        self.combo = gtk.combo_box_new_text()
        self.dialog.vbox.pack_start(alg,False,False)
        self.dialog.vbox.pack_start(self.combo,False,False)
        label = gtk.Label('Instructions:')
        alg = gtk.Alignment(0,0)
        alg.set_padding(5,0,0,0)
                
        alg.add(label)
        text = gtk.TextView()
        self.dialog.vbox.pack_start(alg,False,False)    
        self.dialog.vbox.pack_start(text,False,False)
        text.get_buffer().set_text('Gestures are activated after toggling button activate. \n'+ 
                                   'To Deactivate push the deactivate button.')
        text.set_editable(False)        
        label = gtk.Label('Gestures table:')
        alg = gtk.Alignment(0,0)
        alg.set_padding(5,0,0,0)                
        alg.add(label)
        self.dialog.vbox.pack_start(alg,False,False)
                
        self.store = gtk.ListStore(gtk.gdk.Pixbuf,gtk.gdk.Pixbuf,str)
        self.treeview = gtk.TreeView(self.store)
                         
        tvcolumn = gtk.TreeViewColumn('Gesture')
        self.treeview.append_column(tvcolumn)
        cell = gtk.CellRendererPixbuf()       
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, "pixbuf", 0)
        
        tvcolumn = gtk.TreeViewColumn('Effect')
        self.treeview.append_column(tvcolumn)
        cell = gtk.CellRendererPixbuf()
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, "pixbuf", 1)
        
        tvcolumn = gtk.TreeViewColumn('Description')
        self.treeview.append_column(tvcolumn)
        cell = gtk.CellRendererText()
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, "text", 2)                                
        
        self.dialog.vbox.pack_start(self.treeview,True,True)        
        self.width = 20
        self.height = 20
        self.color = '#00FF00'                                                                        
                                          
    def __CloseDialogHandler(self,button,dg):
        dg.hide()
    
    def __CloseDialogHandler2(self,dg,event):
        dg.hide()
        return True        
    
    def ShowHelpDialog(self):        
        self.dialog.show_all()
        if self.loaded == False:   
            self.loaded = True         
            self.pixmap = gtk.gdk.Pixmap(self.dialog.window, self.width, self.height)            
            self.cmap = self.dialog.window.get_colormap()
            self.gc = self.dialog.window.new_gc(foreground = self.cmap.alloc_color(self.color))                         
            self.pixmap.draw_rectangle(self.gc,True,10,10,3,3)
            print "OK"
            #self.AddGeneralHelp()
            self.CreateGeneralHelp()        
        
    def AddGeneralHelp(self):
                        


        #sk = gtk.gdk.pixbuf(get_from_drawable(gtk.gdk.Pixmap))
        #print sk
        
        pathx = self.data[0][1][0]
        
        #print pathx
        #print self.data[2]
        loader = gtk.gdk.PixbufLoader()
        
        #while True:
        #    tmp = pathx.read(102400)
#            if not tmp:
#                break
        loader.write(pathx)
        loader.close()
        tmp = loader.get_pixbuf()
        
        #alf = tmp.get_from_drawable(self.pixmap,self.cmap,10,10,10,10,3,3)
        
        pxb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8, 100,100)
        #print tmp
        
#        print type(tmp)
#        
        #tmp = gtk.gdk.pixbuf_new_from_file(unicode(ic))
        
        
        self.store.append([tmp,alf,'PPP'])
        
        
        #item = self.store.append(None)
        
        #self.store.set(item,0,tmp,1,None,2,'Pejko')
        
#        print "FF"


    def FillHelp(self):                
        for i in range(len(self.data)):
            self.combo.append_text(self.data[i][0])
            
    def CreateGeneralHelp(self):
        self.combo.append_text('General')
        self.combo.set_active(0)
        
                            

    def ShowDiagramHelp(self,paIndex):
        print "HELP"
    
    def SetMetamodel(self,parameter):
        self.metamodel = parameter
        
    def GetMetamodel(self):
        return self.metamodel
    
    def SetData(self,paData):
        self.data = paData
        
    def GetData(self):
        return self.data
        
    
    
        
# 