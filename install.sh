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

	if [ -z `command -v python3.11` ]; then
		echo "Python 3.11 is not installed. Install Python 3.11 using your system's package manager, or, alternatively, from source."
		exit -1
	fi
fi

if [ -z `command -v python3.11` ]; then
	python -m venv venv
else
	python3.11 -m venv venv
fi

source ./venv/bin/activate 
 
pip install py7zr

rm -f .tmp_pip_list
