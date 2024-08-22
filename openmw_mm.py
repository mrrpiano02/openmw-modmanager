#!/usr/bin/python3

import os
import configparser
from mod_entry import ModEntry
from setup import setup
import util as u 
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from mod_entry import ModEntry
from actions import *


class SetupGUI(tk.Toplevel):
    
    def launch_filedialog(self):
        directory = filedialog.askdirectory(title='Select Game Directory')

        to_add = ['[General]', 'morrowinddirectory = '+directory]
        with open('./mminfo.ini', 'w') as file:
            for entry in to_add:
                file.write(entry+'\n')

        os.chmod('./mminfo.ini', 0o777)

    def __init__(self, root):

        root.grid()
        self.msg = ttk.Label(root, text='Game directory not detected.\nIn order to continue, please\n specify a game directory.', padding=[65,25])
        self.btn = ttk.Button(root, text='Select directory', command=self.launch_filedialog) 
        self.msg.grid(column=0, row=0)
        self.btn.grid(column=0, row=1)


class ModManagerGUI(tk.Frame):
    
    openmw_config_file = ''   
    modlist = {}
    current_selection = ''
    num_selection = 0    

    def refresh(self):
        self.modlist_container.delete(*self.modlist_container.get_children()) 
 
        for mod in self.modlist:
            self.modlist_container.insert('', tk.END, values=(mod, self.modlist[mod].get_name(), self.modlist[mod].get_enabled()))

    def refresh(self, entry):
        mod_num = self.modlist_container.item(self.modlist_container.selection())['values'][0]
        mod_name = entry.get_name() 
        mod_status = entry.get_enabled() 

        self.modlist_container.delete(self.modlist_container.selection()[0])

        replace = self.modlist_container.insert('', tk.END, values=[mod_num, mod_name, mod_status])
        self.modlist_container.move(replace, '', mod_num-1)
 
    def set_gamedir(self):
        directory = filedialog.askdirectory(title='Select Game Directory')

        inifile = os.getcwd() + '/mminfo.ini'
        with open(inifile, 'r') as file:
            lines = file.readlines()
                     
        idx=0               
        while idx<len(lines):
            if lines[idx].startswith('morrowinddirectory'):
                lines[idx] = lines[idx][:21]
                lines[idx] = lines[idx] + '{}'.format(directory) 
                print('point reached')
            idx += 1 
        
        with open(inifile, 'w') as file:
            file.writelines(lines)
     
        self.gamedir_entry.delete(0, tk.END)
        self.gamedir_entry.insert(0, directory)

        config = configparser.ConfigParser() 
        config.read('./mminfo.ini')

        u.morrowind_installation = config['General']['morrowinddirectory'] 
        validate = u.validate_gamedir(u.morrowind_installation)
        u.create_modfolder()
        self.modlist = u.get_mods(self.openmw_config_file)

    def resize_modname_field(self, event):
        self.modlist_container.column(0, width = 80, minwidth=80, stretch='no')
        self.modlist_container.column(1, width = (self.modlist_container.winfo_width()-180), stretch='no')
        self.modlist_container.column(2, width = 99, minwidth=99, stretch='no')

    def select_mod(self, event):
        self.current_selection = self.modlist_container.item(self.modlist_container.focus())['values'][1]
        self.num_selection = self.modlist_container.item(self.modlist_container.focus())['values'][0]

    def enable_selected(self):
        if not self.modlist[self.num_selection].get_enabled():
            enable_mod(self.modlist, self.num_selection, self.openmw_config_file)
            self.refresh(self.modlist[self.num_selection])

    def disable_selected(self):
        if self.modlist[self.num_selection].get_enabled():
            disable_mod(self.modlist, self.num_selection, self.openmw_config_file)
            self.refresh(self.modlist[self.num_selection])

    def install_selected(self):
        install_file = filedialog.askopenfilename(filetypes=[('.7z', '*.7z'), ('.zip', '*.zip')])
        
        if install_file == '':
            print('no install file selected.')
            return

        install_file.replace('\\', '/')
        mod_name = install_file.split('/')[-1]
 
        mod_name_breakdown = mod_name.split('.')
        mod_name = mod_name_breakdown[0]
        filetype = mod_name_breakdown[1]

        mod_dir = u.get_modfolder('/')
        mod_name = mod_dir + mod_name 

        install_mod(install_file, mod_name, filetype, self.modlist, self.openmw_config_file)

        self.refresh()

    def uninstall_selected(self):

        if self.current_selection == '':
            print('No mod selected.')
            return

        proceed = tk.messagebox.askquestion(title='Proceed with uninstallation?', message='This action will remove ' + self.current_selection + ' from modlist. Proceed?')
        
        if proceed == tk.messagebox.YES:
            to_remove = u.morrowind_installation + '/Mods/' + self.current_selection + '/'
            u.remove_modfolder(to_remove)

            with open(self.openmw_config_file, 'r') as cfg:
                lines = cfg.readlines()
                  
            idx=0
            lines_removed=0
            while idx<len(lines):
                if self.current_selection in lines[idx]:
                    while idx<len(lines) and lines[idx] != '\n':
                        idx += 1
                        lines_removed += 1
                        
                else:
                    lines[idx-lines_removed] = lines[idx]
                    
                idx += 1
                    
            lines = lines[:idx-lines_removed-2]
            
            with open(self.openmw_config_file, 'w') as cfg:
                cfg.writelines(lines)
 
            self.modlist.pop(self.num_selection)
            self.refresh() 
            self.current_selection = '' 
        
        else:
            print('Operation cancelled.')

    def __init__(self, root):
        self.openmw_config_file = u.determine_os()
       
        config = configparser.ConfigParser()
        config.read('./mminfo.ini')

        u.morrowind_installation = config['General']['morrowinddirectory'] 
        validate = u.validate_gamedir(u.morrowind_installation)
        u.create_modfolder() 
 
        s = ttk.Style()
        s.configure('Treeview', background='#ffffff', bordercolor='#000000', border=2, height=420)

        root.grid()

        self.select_gamedir = ttk.LabelFrame(root, text='Game directory: ', width=350, height=50)
        self.select_gamedir.grid_propagate(0)
        self.select_gamedir.grid(column=0, row=0, pady=5)

        self.gamedir_entry = ttk.Entry(self.select_gamedir)
        self.gamedir_entry.delete(0, tk.END)
        self.gamedir_entry.insert(0, u.morrowind_installation)
        self.gamedir_entry.grid(column=0, row=0, padx=5, pady=2)

        self.gamedir_entry.columnconfigure(0, weight=1)

        self.browse_files = ttk.Button(self.select_gamedir, text='Open Directory', command=self.set_gamedir)
        self.browse_files.grid(column=1, row=0) 

        self.modlist_container = ttk.Treeview(root, columns=['item_num', 'modname', 'enabled'], style='Treeview')

        self.modlist = u.get_mods(self.openmw_config_file)

        for mod in self.modlist:
            self.modlist_container.insert('', tk.END, values=(mod, self.modlist[mod].get_name(), self.modlist[mod].get_enabled()))

        self.modlist_container.grid(column=0, row=1, padx=10, sticky=tk.E+tk.N+tk.W+tk.S)
        self.modlist_container.heading(column=0, text='Item#')
        self.modlist_container.heading(column=1, text='Mod Name')
        self.modlist_container.heading(column=2, text='Enabled')
        
        self.modlist_container.column(0, width = 80, minwidth=80, stretch='no')
        self.modlist_container.column(1, width = 300, minwidth=300, stretch='no')
        self.modlist_container.column(2, width = 99, minwidth=99, stretch='no')
      
        self.modlist_container['show'] = 'headings'
        
        action_container = tk.Frame(root, width=200, height=420, bd=3, bg='#ffffff')
        action_container.grid(column=1, row=1, padx=10, pady=30, sticky=tk.E+tk.N+tk.W+tk.S)

        enable_button = ttk.Button(action_container, text='Enable', command=self.enable_selected)
        disable_button = ttk.Button(action_container, text='Disable', command=self.disable_selected)
        install_button = ttk.Button(action_container, text='Install from File', command=self.install_selected)
        uninstall_button = ttk.Button(action_container, text='Uninstall Mod', command=self.uninstall_selected)

        enable_button.grid(column=0, row=0, padx=20, pady=10, sticky=tk.W+tk.E+tk.S)
        disable_button.grid(column=0, row=1, padx=20, pady=10, sticky=tk.W+tk.E)
        install_button.grid(column=0, row=2, padx=20, pady=10, sticky=tk.W+tk.E)
        uninstall_button.grid(column=0, row=3, padx=20, pady=10, sticky=tk.W+tk.E+tk.N)
        
        root.columnconfigure(0, weight=1) 
        root.rowconfigure(1, weight=1)

        root.bind("<Configure>", self.resize_modname_field)
        self.modlist_container.bind('<Motion>', 'break')
        self.modlist_container.bind('<<TreeviewSelect>>', self.select_mod)        

        root.update()


def __main__():
    
    if not os.path.isfile('./mminfo.ini'):
        setup_root = tk.Tk()
        tk.Canvas(setup_root, bg='#e1e1e1')
        setup_root.title('setup-gui')
        setup_root.geometry('320x200')
        setup_root.minsize(320,200)
        setup_root.resizable(width=False, height=False)
        setupgui = SetupGUI(setup_root)

        setup_root.mainloop()

    root = tk.Tk()
    tk.Canvas(root, bg='#e1e1e1')
    root.title('openmw-modmanager-gui')
    root.geometry('720x480')
    root.minsize(320,200)

    mmgui = ModManagerGUI(root)

    root.mainloop() 

if __name__ == '__main__':
    __main__()
