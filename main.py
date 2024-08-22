#!/usr/bin/python3

import os
import sys 
import configparser 
from mod_entry import ModEntry
from setup import setup
import util as u


openmw_config_file = ''

modlist = {}
config = configparser.ConfigParser()

if u.is_windows():
    ini = '.\\mminfo.ini'
else:
    ini = './mminfo.ini'

if not os.path.exists(ini):
    setup(ini)

config.read(ini)

u.morrowind_installation = config.['General']['morrowinddirectory']

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

        # set Morrowind's install directory
        if decision == 's':
            valid_dir_entered = False

            while not valid_dir_entered:
                newdir = input('\nType the new filesystem location of your Morrowind directory (type \'q\' to quit):\t')

                if newdir == 'q':
                    break

                if newdir[0] == '~' and not is_windows():
                    newdir = newdir[1:]
                    newdir = user_dir + newdir 

                dir_to_add = u.validate_gamedir(newdir)

                if dir_to_add != '':
                    config['General']['MorrowindDirectory'] = dir_to_add 
                    with open('mminfo.ini', 'w') as configfile:
                        config.write(configfile)

                    print('Directory set successfully.\n')
                    valid_dir_entered = True 
                else:
                    print('Error: directory invalid.\n')
                   
        # install new mod
        elif decision == 'i':
            file = ''
            mod_name = ''

            while (file == ''):
                file = input('Type the full path of your zip file\'s location: ')
                if u.is_windows(): 
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

            slash = '\\' if u.is_windows() else '/'
            mod_dir = u.get_modfolder(slash) 
            
            mod_fullpath = mod_dir + mod_name
            install_mod(file, mod_fullpath, filetype, modlist, openmw_config_file)
                
        # enable mod
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
     
            enable_mod(modlist, selection, openmw_config_file) 
            
        # disable mod
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
            
            disable_mod(modlist, selection, openmw_config_file)
               
        #uninstall mod
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
                if u.is_windows():
                    to_remove = u.morrowind_installation + '\\Mods\\' + modlist[selection].get_name() + '\\'
                else:
                    to_remove = u.morrowind_installation + '/Mods/' + modlist[selection].get_name() + '/'
                    
                u.remove_modfolder(to_remove)
                modlist.pop(selection) 
 
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

        # print list of mods in a tabular fashion
        elif decision == 'c':
            print(' Mod# | Name                                              | Enabled\n------------------------------------------------------------------------------------------------------------')
            idx=1 
            while idx <= len(modlist): 
                u.table(idx, modlist[idx])
                idx+=1 

        # quit
        elif decision == 'q': 
            print('Terminating program...')
            quit(0) 
        else:
            print('Error: Input does not select one of the provided options.\n') 

if __name__ == '__main__':
    openmw_config_file = u.determine_os()
    u.validate_gamedir(u.morrowind_installation)
    u.create_modfolder() 
    modlist = u.get_mods(openmw_config_file)
    main()

