import os
import sys

def setup(ini_file):
    print('\nWelcome to the setup process for openmw-modmanager. To begin, please type the root directory of your Morrowind installation. This is the directory that contains Morrowind.exe.')
    directory = ''

    while not os.path.isdir(directory):
        directory = input("Directory of Morrowind installation: ")

        if not os.path.isdir(directory):
            print('Error: directory provided does not exist.')
    
    with open(ini_file, 'w') as f:
        initial_text = ['[General]\n', 'MorrowindDirectory='+directory]
        f.writelines(initial_text)

    print("Setup complete!\n") 
