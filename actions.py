import util as u
import py7zr
import zipfile
import os
from mod_entry import ModEntry

def install_mod(file, mod_name, filetype, modlist, openmw_config_file):
   
    mod_name = mod_name.replace('\\', '/')
    separated_mod_name = mod_name.split('/')
    mod_stripped_name = separated_mod_name[-1]

    mod_dir = ''
    for i in range(len(separated_mod_name)-1):
        mod_dir = mod_dir.join(separated_mod_name[i])
 
    if filetype == '7z':
        with py7zr.SevenZipFile(file, mode='r') as archive:
            archive.extractall(path=mod_name)
   
    if filetype == 'zip':
        with zipfile.ZipFile(file, mode='r') as archive:
            archive.extractall(mod_name)

    contents = u.search_esps(mod_name) 
    add_config_line = 'data=\"' + mod_name + '\"'

    with open(openmw_config_file, 'a') as cfg:
        cfg.write('\n\n## [' + mod_stripped_name + ']')
        cfg.write('\n' + add_config_line)
        print('Added ' + mod_stripped_name + ' to openmw.cfg')

        for element in contents:
            cfg.write(element)
            print('Added ' + element + ' to openmw.cfg')

    new_entry = ModEntry(mod_name, mod_dir, True)
    
    modlist[len(modlist)+1] = new_entry 
    
def enable_mod(modlist, selection, openmw_config_file):
    with open(openmw_config_file, mode='r') as cfg:
        lines = cfg.readlines()

    idx=0
    while idx<len(lines):
        if modlist[selection].get_name() in lines[idx]:
            idx += 1 # move to first 'data=' line 
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

def disable_mod(modlist, selection, openmw_config_file):
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
