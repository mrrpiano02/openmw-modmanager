import os
import sys 
import configparser 
from setup import setup
from mod_entry import ModEntry

config = configparser.ConfigParser()
user_dir = ''

# return if system is a Windows system
def is_windows():
    return not os.name == 'posix'

if is_windows():
    user_dir = os.environ['USERPROFILE']
else:
    user_dir = os.environ['HOME']

if is_windows():
    ini = '.\\mminfo.ini'
else:
    ini = './mminfo.ini'

if not os.path.exists(ini):
    setup(ini)

config.read(ini)

openmw_config_file = ''
morrowind_installation = config['General']['MorrowindDirectory']

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
def get_mods(openmw_config_file):
    
    modlist = {}

    mod_dir = get_modfolder('')
    mods = os.listdir(mod_dir)

    for mod in mods:
        name = mod

        fullpath = get_modfolder(mod)

        enabled = False
        with open(openmw_config_file) as cfg:
            idx=0 
            lines = cfg.readlines()
            while idx<len(lines): 
                if name in lines[idx] and lines[idx].startswith('## ['): # check if name appears in header line
                    idx+=1
                    if not lines[idx].startswith('##'):
                        enabled=True
                        break
                    else:
                        break
                idx+=1
                    
        m = ModEntry(name, fullpath, enabled)
        modlist[len(modlist)+1] = m

    return modlist

# this method is a misnomer; rename later
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
        
        elif '.esp' in element.lower() or '.esm' in element.lower():
            esps.append('\ncontent='+element) 
     
    return esps
    
def remove_modfolder(to_remove):
    
    if is_windows():
        folder_char = '\\'
    else:
        folder_char = '/'
       
    # removes elements in a DFS fashion
    for item in os.listdir(to_remove):
        if os.path.isdir(to_remove+item):
            remove_modfolder(to_remove+item+folder_char)
        elif os.path.isfile(to_remove + item):
            os.chmod(to_remove+item, 0o222) # grants write permissions to remove file
            os.remove(to_remove+item)
        
    os.chmod(to_remove, 0o222)
    os.rmdir(to_remove)

def table(number, mod):
    maxchar_number = 5
    maxchar_name = 50
    
    modname = mod.get_name()

    if len(modname) > 50:
        modname = modname[:47] 
        modname += '...'
 
    print(str(number), '.', end=''),
    for i in range(maxchar_number-len(str(number))-1):
        print(' ', end=''),

    print('|', modname, end=''),
    for i in range(maxchar_name-len(modname)):
        print(' ', end=''),

    print('|', 'Yes' if mod.get_enabled() else 'No')
