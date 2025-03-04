#!/usr/bin/env python3

# Attempts to download and assemble maven artifacts for use in traditional
# development environments.

import os, shutil, subprocess, stat
from artifactory import ArtifactoryPath
from os.path import join

from deps import unzip, downloaded, WPILIB_VERSION, BASEDIR, SRCDIR, WORKDIR, LIBDIR, INCDIR

# Package list to download and extract.
PACKAGES = '''
    apriltag
    cameraserver
    cscore
    hal
    ntcore
    wpilibc
    wpilibNewCommands
    wpimath
    wpinet
    wpiutil
'''.split()

BASEURL_WPI = 'https://frcmaven.wpi.edu/ui/native/wpilib-mvn-release/edu/wpi/first'
BASEURL_CLOUDFRONT = 'https://d38c02sf6d6ar3.cloudfront.net'

def baseurl (name):
    return '%s/%s/%s-cpp/%s' % (BASEURL_WPI, name, name, WPILIB_VERSION)

def headers_filename (name):
    return '%s-cpp-%s-headers.zip' % (name, WPILIB_VERSION)

def headers_url (name):
    return baseurl(name) + '/%s' % headers_filename (name)

def libs_filename (name, system='linuxathena'):
    return '%s-cpp-%s-%s.zip' % (name, WPILIB_VERSION, system)

def libs_url (name, system):
    return baseurl(name) + '/%s' % libs_filename (name, system)

def render_download_links():
    for name in PACKAGES:
        packages = [{
            'filename': headers_filename (name),
            'url': headers_url (name)
        }]
        
        for system in 'linuxx86-64 linuxathena windowsx86-64 osxuniversal'.split():
            packages.append ({
                'filename': libs_filename (name, system),
                'url': libs_url(name, system),
            })
        
        for pkg in packages:
            print (pkg['url'])
            continue

def render_download_script():
    print ("#!/usr/bin/sh")
    print ("# This script is auto-generated. Do not modify directly.")
    print('''
set -e

wget https://d38c02sf6d6ar3.cloudfront.net/halsim_gui-2025.2.1-headers.zip
wget https://d38c02sf6d6ar3.cloudfront.net/halsim_gui-2025.2.1-linuxx86-64.zip   
''')
    for name in PACKAGES:
        print ('wget %s/%s' % (BASEURL_CLOUDFRONT, headers_filename (name)))
        for system in 'linuxx86-64 linuxathena'.split():
            print ('wget %s/%s' % (BASEURL_CLOUDFRONT, libs_filename (name, system)))
    print()

def extract_libs (name):
    zipfile = join (SRCDIR, libs_filename (name))
    outpath = join (WORKDIR, name)
    os.makedirs (outpath, 511, True)
    unzip (zipfile, outpath)
    libpath = join (outpath, 'linux/athena/shared')
    for f in os.listdir (libpath):
        of = shutil.copy2 (join (libpath, f), LIBDIR)
        st = os.stat(of)
        os.chmod (of, st.st_mode | stat.S_IEXEC)

def extract_headers (name):
    zipfile = join (SRCDIR, headers_filename (name))
    outpath = join (INCDIR)
    os.makedirs (outpath, 511, True)
    unzip (zipfile, outpath)

def extract_package (name):
    extract_headers (name)
    extract_libs (name)
    
if __name__ == "__main__":
    render_download_script()
    exit(0)
