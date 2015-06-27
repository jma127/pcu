#!/usr/bin/env python

import os
import shutil

# Variables

dir = os.path.dirname(os.path.abspath(__file__))
defaulttemplatefolder = os.path.join(dir, 'defaulttemplates')
templatefolder = os.path.join(dir, 'templates')
defaultsettings = os.path.join(dir, 'defaultsettings.py')
settings = os.path.join(dir, 'settings.py')
path =  os.environ['PATH'].split(os.pathsep)
installed = False

# Installer

print 'PCU Installer'

# Launcher Installation

print
print 'Installing launcher...'
for folder in path:
    try:
        link = os.path.join(folder, 'pcu')
        os.symlink(os.path.join(dir, 'main.py'), link)
        os.chmod(link, 0755)
        print 'Launcher installed in ' + folder
        installed = True
        break
    except Exception:
        pass

if not installed:
    print 'Could not install launcher to system path'

# Template Installation

print
print 'Installing default templates...'
try:
    shutil.rmtree(templatefolder, ignore_errors=True)
    shutil.copytree(defaulttemplatefolder,
                    templatefolder)
    os.chmod(templatefolder, 0777)
    for file in os.listdir(templatefolder):
        os.chmod(os.path.join(templatefolder, file), 0666)
    print 'Templates installed'
except shutil.Error as err:
    print 'Could not install templates: ' + repr(err)
    installed = False

# Settings Installation

print
print 'Installing settings file...'
try:
    if os.path.isfile(settings):
        os.remove(settings)
    shutil.copy(defaultsettings,
                    os.path.join(settings))
    os.chmod(settings, 0666)
    print 'settings.py installed'
except shutil.Error as err:
    print 'Could not install settings file: ' + repr(err)
    installed = False

# User Instructions

print
if installed:
    print 'Install successful, you may now use pcu'
    print 'See the README for more info'
else:
    print 'Install failed'
    print '(try running sudo python install.py)'
