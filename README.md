## OpenMW Mod Manager

This project aims to serve as a mod manager for OpenMW - the open-source engine for *The Elder Scrolls III: Morrowind*. This project is not affiliated with the OpenMW team in any way, shape, or form - this is simply a project I worked on for fun and to get familiar with Python. 

This mod manager can essentially be thought of as an automation tool for unpacking archive files and adding their paths to your openmw.cfg file. The goal I have in mind is to provide flexibility in enabling/disabling mods, as well as allowing for easy installation/uninstallation.

**Note: this project is in the early stages of development.** As such, the feature set is fairly limited, and the presence of bugs is certain. Since this program reads/writes to your openmw.cfg file, use at your own risk. It would be greatly appreciated if you could report any bugs that you may happen to come across - there are lots of fringe cases that have not been tested.

#### Requirements
 - Python >= 3.7
 - [OpenMW](https://openmw.org/)
 - A copy of *The Elder Scrolls III: Morrowind*.

#### Dependencies
 - [py7zr](https://github.com/miurahr/py7zr/)

#### Installation
One can install the project using `git clone` and run it using `python`:
1. `git clone https://github.com/mrrpiano02/openmw-modmanager.git`
2. `cd openmw-modmanager`
3. `python main.py`
4. Alternatively, if you are on Linux, you can run the program by using `chmod +x main.py` and `./main.py`
