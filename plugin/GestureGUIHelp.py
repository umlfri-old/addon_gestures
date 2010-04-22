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
        self.dialog.set_position(gtk.WIN_POS_CENTER_ALWAYS)
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
        #text.get_buffer().set_text('Gestures are activated after toggling button activate. \n'+ 
        #                           'To Deactivate push the deactivate button.')
        
        ic = os.path.join(os.path.dirname(__file__), "gui","gesturesHelp.txt")
        infile = open(ic, "r")
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
        self.width = 61
        self.height = 61
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
            #self.pixmap.draw_rectangle(self.gc,True,10,10,3,3)
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
            
    def DrawGeneralHelp(self):                
        #Create pictures for general help
        pxb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8, self.width,self.height)        
        self.gc.foreground = self.cmap.alloc_color("#FFFFFF")
        self.pixmap.draw_rectangle(self.gc, True, 0, 0, 60, 60)                
        self.gc.foreground = self.cmap.alloc_color("#000000")
        self.pixmap.draw_rectangle(self.gc, False, 0, 0, 60, 60)                        
        self.gc.foreground = self.cmap.alloc_color(self.color)                                                                    
        self.pixmap.draw_arc(self.gc, True, 10, 20, 15, 15, 0, 360*64)        
        self.pixmap.draw_rectangle(self.gc, True, 18, 25, 32, 5)                        
        pxb.get_from_drawable(self.pixmap,self.cmap,0,0,0,0,self.width,self.height)
        self.store.append([pxb,None,'Line to LEFT: '])
        
        pxb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8, self.width,self.height)       
        self.gc.foreground = self.cmap.alloc_color("#FFFFFF")
        self.pixmap.draw_rectangle(self.gc, True, 0, 0, 60, 60)                
        self.gc.foreground = self.cmap.alloc_color("#000000")
        self.pixmap.draw_rectangle(self.gc, False, 0, 0, 60, 60)                        
        self.gc.foreground = self.cmap.alloc_color(self.color)        
        self.pixmap.draw_arc(self.gc, True, 40, 20, 15, 15, 0, 360*64)        
        self.pixmap.draw_rectangle(self.gc, True, 10, 25, 32, 5)                        
        pxb.get_from_drawable(self.pixmap,self.cmap,0,0,0,0,self.width,self.height)
        self.store.append([pxb,None,'Line to RIGHT: '])
        
        pxb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8, self.width,self.height)               
        self.gc.foreground = self.cmap.alloc_color("#FFFFFF")
        self.pixmap.draw_rectangle(self.gc, True, 0, 0, 60, 60)                
        self.gc.foreground = self.cmap.alloc_color("#000000")
        self.pixmap.draw_rectangle(self.gc, False, 0, 0, 60, 60)                        
        self.gc.foreground = self.cmap.alloc_color(self.color)
        self.pixmap.draw_arc(self.gc, True, 20, 40, 15, 15, 0, 360*64)
        self.pixmap.draw_rectangle(self.gc, True, 25, 10, 5, 40)
        pxb.get_from_drawable(self.pixmap,self.cmap,0,0,0,0,self.width,self.height)
        self.store.append([pxb,None,'Line to DOWN: '])
        
        pxb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8, self.width,self.height)            
        self.gc.foreground = self.cmap.alloc_color("#FFFFFF")
        self.pixmap.draw_rectangle(self.gc, True, 0, 0, 60, 60)                
        self.gc.foreground = self.cmap.alloc_color("#000000")
        self.pixmap.draw_rectangle(self.gc, False, 0, 0, 60, 60)                        
        self.gc.foreground = self.cmap.alloc_color(self.color)
        self.pixmap.draw_arc(self.gc, True, 20, 10, 15, 15, 0, 360*64)
        self.pixmap.draw_rectangle(self.gc, True, 25, 10, 5, 40)        
        pxb.get_from_drawable(self.pixmap,self.cmap,0,0,0,0,self.width,self.height)
        self.store.append([pxb,None,'Line to UP: '])
                
        pxb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8, self.width,self.height)            
        self.gc.foreground = self.cmap.alloc_color("#FFFFFF")
        self.pixmap.draw_rectangle(self.gc, True, 0, 0, 60, 60)                
        self.gc.foreground = self.cmap.alloc_color("#000000")
        self.pixmap.draw_rectangle(self.gc, False, 0, 0, 60, 60)                
        self.pixmap.draw_rectangle(self.gc, False, 10, 10, 40, 40)
        self.pixmap.draw_rectangle(self.gc, False, 11, 11, 38, 38)
        self.pixmap.draw_rectangle(self.gc, False, 12, 12, 36, 36)                                                
        self.pixmap.draw_rectangle(self.gc, True, 10, 20, 40,3)                                                                                                
        self.gc.foreground = self.cmap.alloc_color(self.color)
        self.pixmap.draw_arc(self.gc, True, 25, 25, 15, 15, 0, 360*64)
        pxb.get_from_drawable(self.pixmap,self.cmap,0,0,0,0,self.width,self.height)
        self.store.append([pxb,None,'Delete ELEMENT'])
        
        pxb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8, self.width,self.height)            
        self.gc.foreground = self.cmap.alloc_color("#FFFFFF")
        self.pixmap.draw_rectangle(self.gc, True, 0, 0, 60, 60)                
        self.gc.foreground = self.cmap.alloc_color("#000000")
        self.pixmap.draw_rectangle(self.gc, False, 0, 0, 60, 60)                
        self.pixmap.draw_rectangle(self.gc, True, 10, 25, 40,3)                                                                                                
        self.gc.foreground = self.cmap.alloc_color(self.color)
        self.pixmap.draw_arc(self.gc, True, 25, 20, 15, 15, 0, 360*64)
        pxb.get_from_drawable(self.pixmap,self.cmap,0,0,0,0,self.width,self.height)
        self.store.append([pxb,None,'Delete CONNECTION'])





        
        
        
        #self.store.append([None,alf,'PPP'])

        
        
        #print tmp
        
#        print type(tmp)
#        
        #tmp = gtk.gdk.pixbuf_new_from_file(unicode(ic))
                
        #self.pixmap.draw_rectangle(self.gc,True,10,10,3,3)
        
         

        
    def CreateGeneralHelp(self):
        self.combo.append_text('General')
        self.combo.set_active(0)
        self.DrawGeneralHelp()
        
            
        
                            

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