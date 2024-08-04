#!/usr/bin/python3

import os
import configparser
from mod_entry import ModEntry
from setup import setup
import util as u 
import tkinter as tk
from tkinter import ttk
from mod_entry import ModEntry

class ModManagerGUI(tk.Frame):
   
    modlist = {}
 
    def resize_modname_field(self, event):
        self.modlist_container.column(0, width = 80, minwidth=80, stretch='no')
        self.modlist_container.column(1, width = (self.modlist_container.winfo_width()-180), stretch='no')
        self.modlist_container.column(2, width = 99, minwidth=99, stretch='no')
 
    def __init__(self, root):
        openmw_config_file = u.determine_os()
        u.validate_gamedir(u.morrowind_installation)
        u.create_modfolder() 
 
        s = ttk.Style()
        s.configure('Treeview', background='#ffffff', bordercolor='#000000', border=2, height=420)

        root.grid()
        self.modlist_container = ttk.Treeview(root, columns=['item_num', 'modname', 'enabled'], style='Treeview')

        self.modlist = u.get_mods(openmw_config_file)

        for mod in self.modlist:
            self.modlist_container.insert('', tk.END, values=(mod, self.modlist[mod].get_name(), self.modlist[mod].get_enabled()))

        self.modlist_container.grid(column=0, row=0, padx=10, pady=30, sticky=tk.E+tk.N+tk.W+tk.S)
        self.modlist_container.heading(column=0, text='Item#')
        self.modlist_container.heading(column=1, text='Mod Name')
        self.modlist_container.heading(column=2, text='Enabled')
        
        self.modlist_container.column(0, width = 80, minwidth=80, stretch='no')
        self.modlist_container.column(1, width = 300, minwidth=300, stretch='no')
        self.modlist_container.column(2, width = 99, minwidth=99, stretch='no')
      
        self.modlist_container['show'] = 'headings'
        
        action_container = tk.Frame(root, width=200, height=420, bd=3, bg='#ffffff')
        action_container.grid(column=1, row=0, padx=10, pady=30, sticky=tk.E+tk.N+tk.W+tk.S)
        
        root.columnconfigure(0, weight=1) 
        root.rowconfigure(0, weight=1)

        root.bind("<Configure>", self.resize_modname_field)
        self.modlist_container.bind('<Motion>', 'break')
        root.update()


def __main__():
    root = tk.Tk()
    tk.Canvas(root, bg='#e1e1e1')
    root.title('openmw-modmanager-gui')
    root.geometry('720x480')
    root.minsize(320,200)

    mmgui = ModManagerGUI(root)

    root.mainloop()    

if __name__ == '__main__':
    __main__()
