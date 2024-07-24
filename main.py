#!/usr/bin/python3

import os
import sys 
import configparser 
import py7zr
import zipfile
from mod_entry import ModEntry
from setup import setup

# return if system is a Windows system
def is_windows():
    return not os.name == 'posix'

# determines the operating system and location of config directory 
def determine_os():
    if 'linux' in sys.platform:
        print('Platform detected as Linux.\n')
        return user_dir + '/.config/openmw/openmw.cfg'
    elif 'win32' in sys.platform:
        print('Platform detected as Windows.\n')
        return user_dir + '\\Documents\\My Games\\OpenMW\\openmw.cfg'
    elif 'darwin' in sys.platform:
        print('Platform detected as MacOS.\n')
        return user_dir + '/Library/Preferences/openmw/openmw.cfg'
    else:
        print('Error: Operating system unsupported. Terminating...')
        quit(1)

# ensures game directory is assigned directory

def validate_gamedir(configval):
    if os.path.isdir(configval):
        print('Game directory located.') 
        return configval 
    else:
        print('Game directory location unsuccessful.')
        return ''

# returns location of mod folder because it's cluttering things up to keep rewriting code
def get_modfolder(mod_name):
    if is_windows():
        return morrowind_installation + '\\Mods' + mod_name
    else:
        return morrowind_installation + '/Mods' + mod_name

# checks for existence of mod folder and creates it as needed
def create_modfolder():
    mod_dir = get_modfolder('')

    if not os.path.isdir(mod_dir):
        print('Mod folder not detected. Creating...')
        os.mkdir(mod_dir)
        print('Mod directory \'%s\' created.' % mod_dir) 

# fetches all mods in modfolder
def get_mods():
    mod_dir = get_modfolder('')

    mods = os.listdir(mod_dir)

    for mod in mods:
        name = mod

        if is_windows():
            fullpath = mod_dir + '\\' + mod
        else:
            fullpath = mod_dir + '/' + mod 

        enabled = False
        with open(openmw_config_file) as cfg:
            lines = cfg.readlines()
            for line in lines:
                if name in line and not line.startswith('##'):
                    enabled = True
                    break

        m = ModEntry(name, fullpath, enabled)
        modlist[len(modlist)+1] = m
        print('Loaded ', name) 

def search_esps(dir_name):
    esps = []

    ls = os.listdir(dir_name)

    for element in ls: 
        if is_windows():
            new_element = dir_name + '\\' + element
        else:
            new_element = dir_name + '/' + element
        
        if os.path.isdir(new_element) and 'compatibility' not in new_element.lower():
            esps.append('\ndata=\"'+new_element+'\"') 
            esps.extend(search_esps(new_element))
        
        elif '.esp' in element.lower():
            esps.append('\ncontent='+element) 
     
    return esps
    
def remove_modfolder(to_remove):
    
    if is_windows():
        folder_char = '\\'
    else:
        folder_char = '/'
        
    for item in os.listdir(to_remove):
        if os.path.isdir(to_remove+item):
            remove_modfolder(to_remove+item+folder_char)
        elif os.path.isfile(to_remove + item):
            os.chmod(to_remove+item, 0o222)
            os.remove(to_remove+item)
        
    os.chmod(to_remove, 0o222)
    os.rmdir(to_remove)

user_dir = ''
if is_windows():
    user_dir = os.environ['USERPROFILE'] 
else:
    user_dir = os.environ['HOME']

config = configparser.ConfigParser()
if is_windows():
    ini = '.\\mminfo.ini'
else:
    ini = './mminfo.ini'

if not os.path.exists(ini):
    setup(ini)

config.read(ini)

openmw_config_file = ''
morrowind_installation = config['General']['MorrowindDirectory']

modlist = {}

def main():
    decision = ''
    print('Welcome to the cli OpenMW mod manager.')

    while decision != 'q':
        print('\nChoose an operation:\n'
                '\t(s)et game directory\n'
                '\t(i)nstall mod\n'
                '\t(u)ninstall mod\n'
                '\t(e)nable mod\n'
                '\t(d)isable mod\n'
                '\t(c)heck modlist\n'
                '\t(q)uit\n')
        decision = input('selection: ')

        decision = decision[0].lower()

        if decision == 's':
            valid_dir_entered = False

            while not valid_dir_entered:
                newdir = input('\nType the new filesystem location of your Morrowind directory (type \'q\' to quit):\t')

                if newdir == 'q':
                    break

                if newdir[0] == '~' and not is_windows():
                    newdir = newdir[1:]
                    newdir = user_dir + newdir 

                dir_to_add = validate_gamedir(newdir)

                if dir_to_add != '':
                    config['General']['MorrowindDirectory'] = dir_to_add 
                    with open('mminfo.ini', 'w') as configfile:
                        config.write(configfile)

                    print('Directory set successfully.\n')
                    valid_dir_entered = True 
                else:
                    print('Error: directory invalid.\n')
                    
        elif decision == 'i':
            file = ''
            mod_name = ''

            while (file == ''):
                file = input('Type the full path of your zip file\'s location: ')
                if is_windows(): 
                    mod_name = file.split('\\')[-1] 
                else:
                    mod_name = file.split('/')[-1]
                mod_name_breakdown = mod_name.split('.')
                mod_name = mod_name_breakdown[0]
                filetype = mod_name_breakdown[1]
                
                if file == 'q': 
                    print('Quitting installation process...')
                    break
                elif not os.path.exists(file):
                    print('Error: path not found.')
                    file = ''

            if (file == 'q'): break

            mod_dir = get_modfolder(mod_name) 
                
            if filetype == '7z':
                with py7zr.SevenZipFile(file, mode='r') as archive:
                    archive.extractall(path=mod_dir)
           
            if filetype == 'zip':
                with zipfile.ZipFile(file, mode='r') as archive:
                    archive.extractall(mod_dir)
 
            contents = search_esps(mod_dir) 
            add_config_line = 'data=\"' + mod_dir + '\"' 
  
            with open(openmw_config_file, 'a') as cfg:
                cfg.write('\n\n## [' + mod_name + ']')
                cfg.write('\n' + add_config_line)
                print('Added ' + mod_dir + ' to openmw.cfg')

                for element in contents:
                    cfg.write(element)
                    print('Added ' + element + ' to openmw.cfg')

            new_entry = ModEntry(mod_name, mod_dir, True)
            
            modlist[len(modlist)+1] = new_entry 
                  
        elif decision == 'e':
            selection=0
            while selection<1 or selection>len(modlist):
                selection_temp = input('Type number 1-' + str(len(modlist)) + ' to select mod to enable: ')
                try:
                    selection = int(selection_temp) 
                except ValueError:
                    print('Error: input must be a number.')
                    selection = 0
                else:
                    if selection<1 or selection>len(modlist):
                        print('Error: selection out of range 1-' + str(len(modlist)))
      
            with open(openmw_config_file, mode='r') as cfg:
                lines = cfg.readlines()

            idx=0
            while idx<len(lines):
                if modlist[selection].get_name() in lines[idx]:
                    idx += 1 
                    if lines[idx].startswith('## '):
                        while idx<len(lines) and lines[idx] != '\n':
                            lines[idx] = lines[idx][3:]
                            idx += 1

                        modlist[selection].flip_enabled_status()
                    else:
                        print('Mod already enabled.')
                    
                    break

                idx += 1 

            with open(openmw_config_file, mode='w') as cfg:
                cfg.writelines(lines) 

        elif decision == 'd':
            selection=0
            while selection<1 or selection>len(modlist):
                selection_temp = input('Type number 1-' + str(len(modlist)) + ' to select mod to disable: ')
                try:
                    selection = int(selection_temp) 
                except ValueError:
                    print('Error: input must be a number.')
                    selection = 0
                else:
                    if selection<1 or selection>len(modlist):
                        print('Error: selection out of range 1-' + str(len(modlist)))

            
            with open(openmw_config_file, mode='r') as cfg:
                lines = cfg.readlines()

            idx=0
            while idx<len(lines):
                if modlist[selection].get_name() in lines[idx]:
                    idx += 1
                    if not lines[idx].startswith('## '):
                        while idx<len(lines) and lines[idx] != '\n':
                            lines[idx] = ''.join(["## ", lines[idx]]) 
                            idx += 1

                        modlist[selection].flip_enabled_status()
                    else:
                        print('Mod already disabled.')
                    break
                    
                idx += 1 

            with open(openmw_config_file, mode='w') as cfg:
                cfg.writelines(lines)
                
        elif decision == 'u':
            selection=0
            while selection<1 or selection>len(modlist):
                selection_temp = input('Type number 1-' + str(len(modlist)) + ' to select mod to uninstall: ')
                try:
                    selection = int(selection_temp) 
                except ValueError:
                    print('Error: input must be a number.')
                    selection = 0
                else:
                    if selection<1 or selection>len(modlist):
                        print('Error: selection out of range 1-' + str(len(modlist)))
                
            check = input("This action will uninstall " + modlist[selection].get_name() + ". Are you sure? (y/N)")
            
            if check.lower() == 'y' or check.lower() == 'yes':
                if is_windows():
                    to_remove = morrowind_installation + '\\Mods\\' + modlist[selection].get_name() + '\\'
                else:
                    to_remove = morrowind_installation + '/Mods/' + modlist[selection].get_name() + '/'
                    
                remove_modfolder(to_remove)
                
                with open(openmw_config_file, 'r') as cfg:
                    lines = cfg.readlines()
                  
                idx=0
                lines_removed=0
                while idx<len(lines):
                    if modlist[selection].get_name() in lines[idx]:
                        while idx<len(lines) and lines[idx] != '\n':
                            idx += 1
                            lines_removed += 1
                            
                    else:
                        lines[idx-lines_removed] = lines[idx]
                        
                    idx += 1
                        
                lines = lines[:idx-lines_removed-2]
                
                with open(openmw_config_file, 'w') as cfg:
                    cfg.writelines(lines)
                
            else:
                print("Removal of " + modlist[selection].get_name() + " cancelled.")
 
        elif decision == 'c':
            print('Mod#\t|Name\t\t\t\t\t\t\t|Enabled\t\n------------------------------------------------------------------------------------------------------------')
            idx=1 
            while idx <= len(modlist):
                print(idx, '\t', end='')
                modlist[idx].print_entry()
                idx+=1 

        elif decision == 'q': 
            print('Terminating program...')
            quit(0) 
        else:
            print('Error: Input does not select one of the provided options.\n') 


if __name__ == '__main__':
    openmw_config_file = determine_os()
    validate_gamedir(morrowind_installation)
    create_modfolder() 
    get_mods() 
    main()

