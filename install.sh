#!/bin/bash

#install script for Linux version of OpenMW mod manager

if [ -z `command -v python` ]; then
	echo "Your system does not have Python installed. Install Python through your system's package manager."
	exit -1
fi

if [ -z `command -v pip` ]; then
	echo "You must install pip before running this script. Install the python-pip package through your system's package manager."
	exit -1
fi

touch .tmp_pip_list
chmod +rw .tmp_pip_list
pip list > .tmp_pip_list

python_version=$(python -V 2>&1 | sed -e 's/Python//g')
major=$(echo $python_version | sed 's/\..*//')
minor=$(echo $python_version | sed -e 's/[^.]*.//' -e 's/\..*//')

if [ $major -lt 3 ] || [[ $major -eq 3 && $minor -lt 7 ]]; then
	echo "Python must be at least version 3.7 to use this program."
	exit -1
fi

if [ $major -eq 3 ] && [ $minor -gt 11 ]; then
	echo "Python >3.11. Creating virtualenv..."
	if [[ -z $(grep "virtualenv" ./.tmp_pip_list) ]]; then
		echo "virtualenv module not found. Installing..."
		pip install virtualenv
	fi

	read -p "Python 3.11 will now be installed from source. sudo permissions are required for this. Type \"y\" to proceed. " permission
	
	if [ $permission == "y" ]; then
		curl https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz > Python-3.11.0.tgz	
		chmod +rwx Python-3.11.0.tgz
		tar -xf Python-3.11.0.tgz

		sudo sh -c Python-3.11.0/configure --enable-optimizations
		sudo make -j $(nproc --all) Python-3.11.0
		sudo make Python-3.11.0 altinstall

		python -m virtualenv -p python3.11 venv
		rm -r Python-3.11.0
		rm Python-3.11.0.tgz
	fi
	
	echo "Installation complete. Please rerun the script under the new venv."
	exit 0
fi

pip install py7zr

rm -f .tmp_pip_list
