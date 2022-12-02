import os
import pathlib
import random
import string
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfile

'''
  screens/base.py
'''

class SearchOptions(tk.Frame):
  ''' selection options for searching '''

  def __init__(self,*args,**kwargs):
    tk.Frame.__init__(self,*args,**kwargs)

    # main objects
    self.header  = tk.Frame(self)
    self.main    = tk.Frame(self)

    # self.header objects
    self.title   = tk.Label(self.header,text='Data Browser')
    self.btn_bar = tk.Frame(self.header)

    # self.btn_bar objects
    self.btn_search = tk.Button(self.btn_bar,text='Search')
    self.btn_reset  = tk.Button(self.btn_bar,text='Reset')

    # self.main objects
    self.lbl_parent = tk.Label(self.main,text='Parent')
    self.lbl_story  = tk.Label(self.main,text='Story')
    self.lbl_charm  = tk.Label(self.main,text='Charm')
    self.lbl_desc   = tk.Label(self.main,text='Description')
    self.lbl_tran   = tk.Label(self.main,text='Transport')
    self.lbl_obj    = tk.Label(self.main,text='Object')
    self.lbl_objty  = tk.Label(self.main,text='Object Type')
    self.ent_parent = tk.Entry(self.main)
    self.ent_story  = tk.Entry(self.main)
    self.ent_charm  = tk.Entry(self.main)
    self.ent_desc   = tk.Entry(self.main)
    self.ent_tran   = tk.Entry(self.main)
    self.ent_obj    = tk.Entry(self.main)
    self.ent_objty  = tk.Entry(self.main)

    # config
    self.header.configure(borderwidth=2,relief='ridge',bg='dark gray')
    self.title.configure(bg='dark gray',fg='black',font=('Arial',12,'bold'))
    self.btn_bar.configure(bg='dark gray')
    self.main.configure(borderwidth=2,relief='groove')

    # events
    self.btn_search.bind('<Button-1>', self.search)
    self.btn_reset.bind('<Button-1>', self.reset_fields)

    # main grid
    self.header.grid(row=0)
    self.main.grid(row=1,sticky='nsew')

    # self.header grid
    self.title.grid(row=0,column=0,padx=5)
    self.btn_bar.grid(row=0,column=1,padx=2,pady=5)

    # self.btn_bar grid
    self.btn_search.grid(row=0,column=0,padx=(5,2))
    self.btn_reset.grid(row=0,column=1,padx=2)

    # self.main grid
    self.lbl_parent.grid(row=0,column=0,pady=(5,0))
    self.ent_parent.grid(row=0,column=1,pady=(5,0))
    self.lbl_story.grid(row=1,column=0)
    self.ent_story.grid(row=1,column=1)
    self.lbl_charm.grid(row=2,column=0)
    self.ent_charm.grid(row=2,column=1)
    self.lbl_desc.grid(row=3,column=0)
    self.ent_desc.grid(row=3,column=1)
    self.lbl_tran.grid(row=4,column=0)
    self.ent_tran.grid(row=4,column=1)
    self.lbl_obj.grid(row=5,column=0)
    self.ent_obj.grid(row=5,column=1)
    self.lbl_objty.grid(row=6,column=0,pady=(0,5))
    self.ent_objty.grid(row=6,column=1,pady=(0,5))

  def search(self,event):
    ''' select from the database and display to user '''
    pass
    
  def reset_fields(self,event=None):
    ''' reset the screen '''
    pass


class ParentEntry(tk.Toplevel):
  ''' change entry '''

  def __init__(self,*args,**kwargs):
    tk.Toplevel.__init__(self,*args,**kwargs)

    # self objects
    self.header = tk.Frame(self)
    self.main   = tk.Frame(self)

    # self.header objects
    self.title   = tk.Label(self.header,text='Create Story')
    self.btn_bar = tk.Frame(self.header)

    # self.btn_bar objects
    self.btn_submit = tk.Button(self.btn_bar,text='Submit')
    self.btn_cancel = tk.Button(self.btn_bar,text='Cancel')

    # self.main objects
    self.lbl_story  = tk.Label(self.main,text='Story')
    self.lbl_charm = tk.Label(self.main,text='Charm')
    self.lbl_descr  = tk.Label(self.main,text='Description')
    self.ent_story  = tk.Entry(self.main)
    self.ent_charm  = tk.Entry(self.main)
    self.ent_descr  = tk.Entry(self.main)

    # config
    self.wm_withdraw()
    self.protocol('WM_DELETE_WINDOW',self.cancel)
    self.header.configure(bg='dark gray',borderwidth=2,relief='ridge')
    self.title.configure(bg='dark gray',fg='black',font=('Arial',12,'bold'))
    self.btn_bar.configure(bg='dark gray')
    self.main.configure(borderwidth=2,relief='groove')

    # events
    self.btn_submit.bind('<Button-1>',self.submit)
    self.btn_cancel.bind('<Button-1>',self.cancel)

    # self grid
    self.header.grid(row=0,column=0,sticky='nsew')
    self.main.grid(row=1,column=0,sticky='nsew')

    # self.header grid
    self.title.grid(row=0,column=0,padx=5)
    self.btn_bar.grid(row=0,column=1,padx=2,pady=5)

    # self.btn_bar grid
    self.btn_submit.grid(row=0,column=0,padx=(5,2))
    self.btn_cancel.grid(row=0,column=2,padx=2)

    # self.main
    self.lbl_story.grid(row=0,column=0,padx=5,pady=(5,0),sticky='e')
    self.ent_story.grid(row=0,column=1,padx=5,pady=(5,0),sticky='w')
    self.lbl_charm.grid(row=1,column=0,padx=5,sticky='e')
    self.ent_charm.grid(row=1,column=1,padx=5,pady=1,sticky='w')
    self.lbl_descr.grid(row=2,column=0,padx=5,sticky='e')
    self.ent_descr.grid(row=2,column=1,padx=5,pady=1,sticky='w')

  def submit(self,event=None):
    ''' submit button event handler '''
    pass

  def cancel(self):
    ''' cancel '''
    pass

  def new_story(self):
    ''' new story '''
    pass


class ParentRecords(tk.Frame):
    ''' change entry data '''

    def __init__(self,*args,**kwargs):
      tk.Frame.__init__(self,*args,**kwargs)

      # variables
      self.row_index = 0

      # self objects
      self.header = tk.Frame(self)
      self.main   = tk.Frame(self)

      # self.header objects
      self.title   = tk.Label(self.header,text='Service Now')
      self.btn_bar = tk.Frame(self.header)

      # self.btn_bar objects
      self.btn_new_story = tk.Button(self.btn_bar,text='New Story')

      # self.main objects
      self.main_parent  = tk.Frame(self.main)
      self.header_story = tk.Frame(self.main)
      self.main_story   = tk.Frame(self.main)

      #self.main_parent objects
      self.lbl_parent  = tk.Label(self.main_parent,text='Parent')
      self.lbl_p_descr = tk.Label(self.main_parent,text='Parent Desc.')
      self.ent_parent  = tk.Entry(self.main_parent)
      self.ent_p_descr = tk.Entry(self.main_parent)

      # self.header_story objects
      self.h_lbl_story = tk.Label(self.header_story,text='Story')
      self.h_lbl_charm = tk.Label(self.header_story,text='Charm')
      self.h_lbl_descr = tk.Label(self.header_story,text='Description')

      # self.main_story objects
      self.vscroll = tk.Scrollbar(self.main_story)
      self.canvas  = tk.Canvas(self.main_story)

      # self.canvas objects
      self.window = tk.Frame(self.canvas)

      # config
      self.header.configure(bg='dark gray',borderwidth=2,relief='ridge')
      self.title.configure(bg='dark gray',fg='black',font=('Arial',12,'bold'))
      self.btn_bar.configure(bg='dark gray')
      self.btn_new_story.configure(font=('Arial',8),pady=0)
      self.main.configure(borderwidth=2,relief='groove')
      self.header_story.configure(bg='light gray')
      self.h_lbl_story.configure(bg='light gray',width=10,anchor='w')
      self.h_lbl_charm.configure(bg='light gray',width=10,anchor='w')
      self.h_lbl_descr.configure(bg='light gray',width=40,anchor='w')
      self.ent_p_descr.configure(width=50)
      self.canvas.configure(height=70,yscrollcommand=self.vscroll.set)
      self.vscroll.configure(command=self.canvas.yview)

      # events
      self.btn_new_story.bind('<Button-1>',self.new_story)

      # self grid
      self.header.grid(row=0,column=0,sticky='nsew')
      self.main.grid(row=1,column=0,sticky='nsew')

      # self.header grid
      self.title.grid(row=0,column=0,padx=4)
      self.btn_bar.grid(row=0,column=1,padx=2,pady=4)

      # self.btn_bar grid
      self.btn_new_story.grid(row=0,column=0,padx=(5,2),pady=0)

      # self.main grid
      self.main_parent.grid(row=0,column=0,sticky='w')
      self.header_story.grid(row=1,column=0,sticky='nsew',pady=(3,0))
      self.main_story.grid(row=2,column=0,sticky='ew')

      # self.main_parent grid
      self.lbl_parent.grid(row=1,column=0,padx=5,pady=(5,0),sticky='w')
      self.ent_parent.grid(row=1,column=1,padx=5,pady=(5,0),sticky='w')
      self.lbl_p_descr.grid(row=2,column=0,padx=5,pady=(0,2),sticky='w')
      self.ent_p_descr.grid(row=2,column=1,padx=5,pady=(0,2),sticky='w')

      # self.header_story grid
      self.h_lbl_story.grid(row=0,column=0,padx=(5,0))
      self.h_lbl_charm.grid(row=0,column=1)
      self.h_lbl_descr.grid(row=0,column=2)

      # self.main_story grid
      self.canvas.grid(row=0,column=0)
      self.canvas.create_window((0,0),window=self.window,anchor='nw')

    def new_story(self,event=None):
      ''' new story '''
      pass

    def add_story(self,event=None):
      ''' add story '''
      pass

    def reset_fields(self):
      ''' reset fields '''
      pass

    def set_scroll(self,event=None):
      ''' set the scroll region based of the amount of entries '''
      pass


class ChangeEntry(tk.Toplevel):
  ''' change entry '''

  def __init__(self,*args,**kwargs):
    tk.Toplevel.__init__(self,*args,**kwargs)

    self.wm_withdraw()
    self.protocol('WM_DELETE_WINDOW',self.cancel)

    self.v_charm = tk.StringVar()

    self.header = tk.Frame(self)
    self.main = tk.Frame(self)

    self.title   = tk.Label(self.header,text='Create Transport')
    self.btn_bar = tk.Frame(self.header)

    # window objects
    #self.lbl_story  = tk.Label(self.main,text='Story')
    self.lbl_charm  = tk.Label(self.main,text='Charm')
    self.lbl_trans  = tk.Label(self.main,text='Transport')
    self.lbl_descr  = tk.Label(self.main,text='Description')
    #self.opt_story = tk.OptionMenu(self.main,self.v_story,'Select a Story',*[])
    self.opt_charm  = tk.OptionMenu(self.main,self.v_charm,'Select a Charm',*[])
    self.ent_trans  = tk.Entry(self.main)
    self.ent_descr  = tk.Entry(self.main)
    self.btn_submit = tk.Button(self.btn_bar,text='Submit')
    self.btn_cancel = tk.Button(self.btn_bar,text='Cancel')

    # config
    self.main.configure(borderwidth=2,relief='groove')
    self.btn_bar.configure(bg='dark gray')
    self.header.configure(bg='dark gray',borderwidth=2,relief='ridge')
    self.title.configure(bg='dark gray',fg='black',font=('Arial',12,'bold'))
    self.btn_submit.bind('<Button-1>',self.submit)
    self.btn_cancel.bind('<Button-1>',self.cancel)
    #self.v_story.set('Select a Story')
    self.v_charm.set('Select a Charm')

    self.header.grid(row=0,column=0,sticky='nsew')
    self.main.grid(row=1,column=0,sticky='nsew')

    self.title.grid(row=0,column=0,padx=5)
    self.btn_bar.grid(row=0,column=1,padx=2,pady=5)

    # grid
   # self.lbl_story.grid(row=0,column=0,padx=5,pady=(5,0),sticky='e')
    #self.opt_story.grid(row=0,column=1,padx=5,pady=(5,0),sticky='w')
    self.lbl_charm.grid(row=0,column=0,padx=5,pady=(5,0),sticky='e')
    self.opt_charm.grid(row=0,column=1,padx=5,pady=(5,0),sticky='w')
    self.lbl_trans.grid(row=1,column=0,padx=5,sticky='ne')
    self.ent_trans.grid(row=1,column=1,padx=5,pady=2,sticky='w')
    self.lbl_descr.grid(row=2,column=0,padx=5,pady=(0,5),sticky='ne')
    self.ent_descr.grid(row=2,column=1,padx=5,pady=(0,5),sticky='w')
    self.btn_submit.grid(row=0,column=0,padx=(5,2))
    self.btn_cancel.grid(row=0,column=2,padx=2)

  def submit(self,event):
    ''' top level submit event '''
    pass

  def cancel(self,event=None):
    ''' top cancel '''
    pass

  def new_change(self):
    ''' new change '''
    pass


class ChangeRecords(tk.Frame):
  ''' view for charm records '''

  def __init__(self,*args,**kwargs):
    tk.Frame.__init__(self,*args,**kwargs)

    # variables
    self.row_index = 0

    # main objects
    self.change  = tk.Frame(self)
    self.header  = tk.Frame(self)
    self.main    = tk.Frame(self)
    self.vscroll = tk.Scrollbar(self,orient='vertical')

    # self.main objects
    self.main_header = tk.Frame(self.main)
    self.canvas  = tk.Canvas(self.main,height=90,width=200,yscrollcommand=self.vscroll.set)

    # self.canvas
    self.charms = tk.Frame(self.canvas)
    self.canvas.create_window((0,0),window=self.charms,anchor='nw')

    # self.header objects
    self.title   = tk.Label(self.header,text='Charms | Transports')
    self.btn_bar = tk.Frame(self.header)

    # self.btn_bar objects
    self.btn_add = tk.Button(self.btn_bar,text='Add')
    self.btn_rem = tk.Button(self.btn_bar,text='Remove')

    # self.main_header objects
    #self.lbl_h_story = tk.Label(self.main_header,anchor='w',width=10,bg='light gray',text='Story')
    self.lbl_h_charm = tk.Label(self.main_header,anchor='w',width=10,bg='light gray',text='Charm')
    self.lbl_h_trans = tk.Label(self.main_header,anchor='w',width=10,bg='light gray',text='Transport')
    self.lbl_h_descr = tk.Label(self.main_header,anchor='w',width=40,bg='light gray',text='Description')

    # config
    self.main_header.configure(bg='light gray')
    self.canvas.bind('<Configure>',self.set_scroll)
    self.btn_add.bind('<Button-1>', self.add)
    self.btn_rem.bind('<Button-1>', self.remove)
    self.header.configure(borderwidth=2,relief='ridge',bg='dark gray')
    self.btn_bar.configure(bg='dark gray')
    self.title.configure(bg='dark gray',fg='black',font=('Arial',12,'bold'))
    self.main.configure(borderwidth=2,relief='groove')
    self.vscroll.configure(command=self.canvas.yview)

    # main grid
    self.header.grid(row=0,column=0,sticky='nsew')
    self.main.grid(row=1,sticky='nsew')

    # self.main grid
    self.main_header.grid(row=0,column=0)
    self.canvas.grid(row=1,column=0,sticky='nsew')

    # self.header grid
    self.title.grid(row=0,column=0,padx=5)
    self.btn_bar.grid(row=0,column=1,padx=2,pady=5)

    # self.btn_bar grid
    self.btn_add.grid(row=0,column=0,padx=(5,2))
    #self.btn_rem.grid(row=0,column=1)

    # self.main_header grid
    #self.lbl_h_story.grid(row=0,column=0,padx=(6,5))
    self.lbl_h_charm.grid(row=0,column=0,padx=(6,5))
    self.lbl_h_trans.grid(row=0,column=1,padx=5)
    self.lbl_h_descr.grid(row=0,column=2,padx=5)

  def add(self,event):
    ''' add charm & transport '''
    pass

  def remove(self,event):
    ''' remove charm & transport '''
    pass

  def set_scroll(self,event=None):
    ''' set the scroll region based of the amount of entries '''
    pass

  def call_object_records(self,event):
    ''' add object records to view that are related to clicked transports '''
    pass

  def set_display(self):
    ''' add items to the parent and charm/transport view '''
    pass

  def reset_fields(self):
    ''' reset the data '''
    pass


class ObjectEntry(tk.Toplevel):
    ''' object data entry '''

    def __init__(self,*args,**kwargs):
      tk.Toplevel.__init__(self,*args,**kwargs)

      # current selection and all selections for optionmenu
      self.v_objty    = tk.StringVar(self) 
      self.v_trans = tk.StringVar(self)
      self.list_objty = ['Function Module','Program','Table',
                         'Data Element','Domain','Structure']

      # set the object id, one over current id in the DB
      try:
        self.object_id = self.master.master.db_conn.select_table(\
                          'object','object_id',max=True).fetchone()[0] + 1
      except(TypeError):
        self.object_id = 0

      # main objects
      self.header = tk.Frame(self)
      self.main   = tk.Frame(self)

      # self.header objects
      self.title   = tk.Label(self.header,text='Create Object')
      self.btn_bar = tk.Frame(self.header)

      # self.btn_bar objects
      self.btn_add_obj  = tk.Button(self.btn_bar,text='Submit')
      #self.btn_attf_obj = tk.Button(self.btn_bar,text='Attach File')
      self.btn_canc_obj = tk.Button(self.btn_bar,text='Cancel')

      # self.main objects
      self.lbl_trans  = tk.Label(self.main,text='Transport',anchor='s')
      self.lbl_objty = tk.Label(self.main,text='Object Type')
      self.lbl_obj   = tk.Label(self.main,text='Object')
      self.lbl_desc  = tk.Label(self.main,text='Description')
      self.opt_trans  = tk.OptionMenu(self.main,self.v_trans,'Select a Transport',*[])
      self.opt_objty = tk.OptionMenu(self.main,self.v_objty,self.list_objty[0],*self.list_objty[1:])
      self.ent_obj   = tk.Entry(self.main,width=40)
      self.txt_desc  = tk.Text(self.main,height=5,width=50,wrap='word')

      # config
      self.wm_withdraw()
      self.protocol('WM_DELETE_WINDOW',self.close_window)
      self.v_trans.set('Select a Transport')
      self.v_objty.set('Select an Object Type')
      self.header.configure(bg='dark gray',borderwidth=2,relief='ridge')
      self.main.configure(borderwidth=2,relief='groove')
      self.btn_bar.configure(bg='dark gray')
      self.title.configure(bg='dark gray',fg='black',font=('Arial',12,'bold'))
      self.btn_canc_obj.bind('<Button-1>',self.reset_fields)
      self.btn_add_obj.bind('<Button-1>',self.add_obj)
      #self.btn_attf_obj.bind('<Button-1>',self.attach_file)

      # main grid
      self.header.grid(row=0,column=0,sticky='nsew')
      self.main.grid(row=1,column=0)

      # self.header grid
      self.title.grid(row=0,column=0,padx=5)
      self.btn_bar.grid(row=0,column=1,padx=2,pady=5)

      # self.btn_bar grid
      self.btn_add_obj.grid(row=0,column=0,padx=(5,2))
      #self.btn_attf_obj.grid(row=0,column=1,padx=2)
      self.btn_canc_obj.grid(row=0,column=2,padx=2)

      # self.main grid
      self.lbl_trans.grid(row=0,column=0,padx=5,pady=(5,0),sticky='e')
      self.opt_trans.grid(row=0,column=1,padx=5,pady=(5,0),sticky='w')
      self.lbl_objty.grid(row=1,column=0,padx=5,sticky='e')
      self.opt_objty.grid(row=1,column=1,padx=5,pady=1,sticky='w')
      self.lbl_obj.grid(row=2,column=0,padx=5,sticky='ne')
      self.ent_obj.grid(row=2,column=1,padx=5,pady=2,sticky='w')
      self.lbl_desc.grid(row=3,column=0,padx=5,pady=(0,5),sticky='ne')
      self.txt_desc.grid(row=3,column=1,padx=5,pady=(0,5),sticky='w')

    def add_obj(self,event=None):
      ''' add obj '''
      pass
      
    def reset_fields(self,event=None):
      ''' reset fields '''
      pass

    def new_object(self,event=None):
      ''' new object '''
      pass

    def close_window(self,event=None):
      ''' close window '''
      pass


class ObjectRecords(tk.Frame):
    ''' view for session added objects '''

    def __init__(self,*args,**kwargs):
      tk.Frame.__init__(self,*args,**kwargs)

      # variables
      self.row_index = 0
      self.sel_row = None

      # main objects
      self.window  = tk.Frame(self)
      self.header  = tk.Frame(self)
      self.vscroll = tk.Scrollbar(self,orient='vertical')

      # self.window objects
      self.main_header = tk.Frame(self.window)
      self.canvas      = tk.Canvas(self.window,height=100,yscrollcommand=self.vscroll.set)

      # self.header objects
      self.btn_bar = tk.Frame(self.header)
      self.title   = tk.Label(self.header,font=10,text='Objects')

      # self.btn_bar objects
      self.btn_add  = tk.Button(self.btn_bar,text='Add') #+++
      self.btn_edit = tk.Button(self.btn_bar,text='Edit')
      self.btn_rmv  = tk.Button(self.btn_bar,text='Remove')

      # self.main_header objects
      self.lbl_h_sel   = tk.Label(self.main_header,bg='light gray',width=4,anchor='w',text=' ')
      self.lbl_h_tran  = tk.Label(self.main_header,bg='light gray',width=15,anchor='w',text='Transport')
      self.lbl_h_objty = tk.Label(self.main_header,bg='light gray',width=15,anchor='w',text='Obj. Type')
      self.lbl_h_obj   = tk.Label(self.main_header,bg='light gray',width=40,anchor='w',text='Object')
      self.lbl_h_desc  = tk.Label(self.main_header,bg='light gray',width=25,anchor='w',text='Description') 

      # self.canvas
      self.main = tk.Frame(self.canvas)
      self.canvas.create_window((0,0),window=self.main,anchor='nw')

      # config
      self.header.configure(bg='dark gray',borderwidth=2,relief='ridge')
      self.title.configure(bg='dark gray',fg='black',font=('Arial',12,'bold'))
      self.window.configure(borderwidth=2,relief='groove')
      self.btn_bar.configure(bg='dark gray')
      self.vscroll.configure(command=self.canvas.yview)

      # events
      self.canvas.bind('<Configure>',self.set_scroll)
      self.btn_add.bind('<Button-1>',self.call_object_entry)
      self.btn_edit.bind('<Button-1>',self.edit_entry)
      self.btn_rmv.bind('<Button-1>', self.remove_obj_from_view)

      # main grid
      self.header.grid(row=0,sticky='nsew')
      self.vscroll.grid(row=1,column=1,sticky='ns')
      self.window.grid(row=1)

      # self.window grid
      self.main_header.grid(row=0,column=0,sticky='nsew')
      self.canvas.grid(row=1,column=0,sticky='nsew')

      # self.header grid
      self.title.grid(row=0,column=0,padx=5)
      self.btn_bar.grid(row=0,column=1,padx=2,pady=5)

      # self.btn_bar grid
      self.btn_add.grid(row=0,column=0,padx=(5,2))
      self.btn_edit.grid(row=0,column=1,padx=2)
      self.btn_rmv.grid(row=0,column=2,padx=2)

      # self.main_header grid
      self.lbl_h_sel.grid(row=0,column=0,ipadx=1)
      self.lbl_h_tran.grid(row=0,column=1)
      self.lbl_h_objty.grid(row=0,column=2)
      self.lbl_h_obj.grid(row=0,column=3)
      self.lbl_h_desc.grid(row=0,column=4)

    def add_obj_to_view(self,objectId=None):
      ''' add object to view '''
      pass

    def call_object_entry(self,event): #+++
      ''' get the object entry frame '''
      pass

    def reset_fields(self):
      ''' reset fields '''
      pass

    def sel_obj(self,event):
      ''' select object '''
      pass

    def remove_obj_from_view(self,objectId):
      ''' remove object from view '''
      pass

    def set_scroll(self,event=None):
      ''' set the scroll region based of the amount of entries '''
      pass

    def edit_entry(self, event=None):
      ''' edit entry '''
      pass

class FileEntry(tk.Toplevel):
  ''' file entry '''

  def __init__(self,*args,**kwargs):
    tk.Toplevel.__init__(self,*args,**kwargs)

    # variables
    self.v_transport = tk.StringVar()
    self.v_object = tk.StringVar()

    # main objects
    self.header = tk.Frame(self)
    self.main = tk.Frame(self)

    # self.header objects
    self.title = tk.Label(self.header,text='Attach a File')
    self.btn_bar = tk.Frame(self.header)

    # self.btn_bar objects
    self.btn_submit = tk.Button(self.btn_bar,text='Submit')
    self.btn_cancel = tk.Button(self.btn_bar,text='Cancel')

    # self.main objects
    self.lbl_trans  = tk.Label(self.main,text='Transport')
    self.lbl_obj  = tk.Label(self.main,text='Object')
    self.opt_trans = tk.OptionMenu(self.main,self.v_transport,'Select a Transport',[])
    self.opt_obj = tk.OptionMenu(self.main,self.v_object,'Select an Object',[])
    self.lbl_file = tk.Label(self.main)
    self.btn_select   = tk.Button(self.main,text='Select File')

    # config
    self.wm_withdraw()
    self.protocol('WM_DELETE_WINDOW',self.cancel)
    self.opt_obj.option_add(0,'Text')
    self.v_transport.set('Select a Transport')
    self.v_object.set('Select an Object')
    self.v_transport.trace_add('write',self.list_obj)
    self.header.configure(bg='dark gray',borderwidth=2,relief='ridge')
    self.title.configure(bg='dark gray',fg='black',font=('Arial',12,'bold'))
    self.btn_bar.configure(bg='dark gray')

    # events
    self.btn_select.bind('<Button-1>',self.select)
    self.btn_submit.bind('<Button-1>',self.submit)
    self.btn_cancel.bind('<Button-1>',self.cancel)

    # main grid
    self.header.grid(row=0,column=0)
    self.main.grid(row=1,column=0)

    # self.header grid
    self.title.grid(row=0,column=0,padx=5)
    self.btn_bar.grid(row=0,column=1,padx=2,pady=5)

    # self.btn_bar grid
    self.btn_submit.grid(row=0,column=0,padx=(5,2))
    self.btn_cancel.grid(row=0,column=1,padx=2)

    # self.main grid
    self.lbl_trans.grid(row=0,column=0)
    self.opt_trans.grid(row=0,column=1)
    self.lbl_obj.grid(row=1,column=0)
    self.opt_obj.grid(row=1,column=1)
    self.btn_select.grid(row=2,column=0)
    self.lbl_file.grid(row=2,column=1)

  def submit(self,event):
    ''' submit '''
    pass

  def select(self,event):
    ''' select '''
    pass

  def cancel(self,event=None):
    ''' cancel '''
    pass

  def list_obj(self,event,callback,mode):
    ''' list object '''
    pass

  def new_file(self,event=None):
    ''' attach file '''
    pass

  def parse_file_name(self,file_name):
    ''' parse file name '''
    pass


class FileRecords(tk.Frame):
    ''' view for session attached files '''

    def __init__(self,*args,**kwargs):
      tk.Frame.__init__(self,*args,**kwargs)

      # variables
      self.row_index = 0
      self.objectId = ''
      self.objectName = ''
      self.transport = ''
      self.dfile_name = ''
      self.dfile_file = ''
      self.dfile_id = ''
      self.dfile_cont = ''
      self.sel_row = None

      # main objects
      self.window  = tk.Frame(self)
      self.header  = tk.Frame(self)
      self.vscroll = tk.Scrollbar(self,orient='vertical')

      # self.window objects
      self.main_header = tk.Frame(self.window)
      self.canvas      = tk.Canvas(self.window,yscrollcommand=self.vscroll.set,height=100)

      # self.header objects
      self.btn_bar = tk.Frame(self.header)
      self.title   = tk.Label(self.header,text='Attached Files')

      # self.btn_bar objects
      self.btn_add = tk.Button(self.btn_bar,text='Add')
      self.btn_rmv = tk.Button(self.btn_bar,text='Remove')

      # self.main_header objects
      self.lbl_h_sel   = tk.Label(self.main_header,bg='light gray',width=4,anchor='w',text=' ')
      self.lbl_h_fname = tk.Label(self.main_header,bg='light gray',width=25,anchor='w',text='File Name')
      self.lbl_h_obj   = tk.Label(self.main_header,bg='light gray',width=20,anchor='w',text='Object')
      self.lbl_h_tran  = tk.Label(self.main_header,bg='light gray',width=20,anchor='w',text='Transport')

      # self.canvas
      self.main = tk.Frame(self.canvas)
      self.canvas.create_window((0,0),window=self.main,anchor='nw')

      # config
      self.title.configure(bg='dark gray',fg='black',font=('Arial',12,'bold'))
      self.btn_bar.configure(bg='dark gray')
      self.window.configure(borderwidth=2,relief='groove')
      self.vscroll.configure(command = self.canvas.yview)
      self.header.configure(bg='dark gray',borderwidth=2,relief='ridge')
      self.canvas.bind('<Configure>',self.set_scroll)
      self.btn_add.bind('<Button-1>',self.attach_file)
      self.btn_rmv.bind('<Button-1>',self.remove_file)

      # main grid
      self.header.grid(row=0,column=0,sticky='nsew')
      self.window.grid(row=1,column=0)
      self.vscroll.grid(row=1,column=1,sticky='ns')
      
      # self.window grid
      self.main_header.grid(row=0,column=0,sticky='nsew')
      self.canvas.grid(row=1,column=0,sticky='nsew')

      # self.header grid
      self.title.grid(row=0,column=0,padx=5)
      self.btn_bar.grid(row=0,column=1,padx=2,pady=5)

      # self.btn_bar grid
      self.btn_add.grid(row=0,column=0,padx=(5,2))
      self.btn_rmv.grid(row=0,column=1,padx=2)

      # self.main_header grid
      self.lbl_h_sel.grid(row=0,column=0,ipadx=1)
      self.lbl_h_fname.grid(row=0,column=1)
      self.lbl_h_obj.grid(row=0,column=2)
      self.lbl_h_tran.grid(row=0,column=3)

    def attach_file(self,event):
      ''' attach file '''
      pass

    def add_file_to_view(self):
      ''' add file to view '''
      pass

    def remove_file(self,objectId=None,event=None):
      ''' remove file '''
      pass

    def reset_fields(self):
      ''' reset fields '''
      pass

    def set_scroll(self,event=None):
      ''' set the scroll region based of the amount of entries '''
      pass


class MainButtons(tk.Frame):
  ''' buttons for primary functions like saving log and cancel '''

  def __init__(self,*args,**kwargs):
    tk.Frame.__init__(self,*args,**kwargs)

    # objects
    self.btn_save = tk.Button(self,text='Save')
    self.btn_canc = tk.Button(self,text='Cancel')
    self.btn_expo = tk.Button(self,text='Export')

    # grid placement
    self.btn_save.grid(row=0,column=0,padx=2,pady=10)
    self.btn_canc.grid(row=0,column=1,padx=2,pady=10)

    # config
    self.btn_save.bind('<Button-1>',self.save_log)
    self.btn_canc.bind('<Button-1>',self.canc_log)
    self.btn_expo.bind('<Button-1>',self.export_log)

  def canc_log(self,event=None):
    ''' cancel log '''
    pass

  def save_log(self,event=None):
    ''' save log '''
    pass

  def export_log(self,event=None):
    ''' export log '''
    pass