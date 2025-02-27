#!/usr/bin/env python3

# Attempts to download and assemble maven artifacts for use in traditional
# development environments.

import os, shutil, subprocess, stat, zipfile
from artifactory import ArtifactoryPath
from os.path import join

from deps import unzip, WPILIB_VERSION, BASEDIR, SRCDIR, WORKDIR, LIBDIR, INCDIR

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

def baseurl (name):
    return '%s/%s/%s-cpp/%s' % (BASEURL_WPI, name, name, WPILIB_VERSION)

def headers_filename (name):
    return '%s-cpp-%s-headers.zip' % (name, WPILIB_VERSION)

def headers_url (name):
    return baseurl(name) + '/%s' % headers_filename (name)

def libs_filename (name, system='linuxathena'):
    return '%s-cpp-%s-%s.zip' % (name, WPILIB_VERSION, system)

def libs_url (name):
    return baseurl(name) + '/%s' % libs_filename (name)

def downloaded (name):
    f1 = join (SRCDIR, libs_filename (name))
    f2 = join (SRCDIR, headers_filename (name))
    return os.path.exists (f1) and os.path.exists (f2)

def download_package (name):
    if downloaded (name):
        return
    
    packages = [{
        'filename': libs_filename (name),
        'url': libs_url(name),
    },
    {
        'filename': headers_filename (name),
        'url': headers_url (name)
    }]
    
    for pkg in packages:
        print (pkg['url'])
        continue
        path = ArtifactoryPath(pkg['url'])
        outfile = join (SRCDIR, pkg['filename'])
        try:
            with path.open() as fd, open (outfile, "wb") as out:
                out.write (fd.read())
            print(f"File downloaded successfully to {outfile}")
        except Exception as e:
            print(f"Error downloading file: {e}")

def download():
    if not os.path.exists (BASEDIR):
        os.makedirs (BASEDIR, 511, True)
    
    for dir in [ WORKDIR, INCDIR, LIBDIR ]:
        if os.path.exists(dir):
            shutil.rmtree (dir)
    os.makedirs (dir, 511, True)
    
    if not os.path.exists (SRCDIR):
        os.mkdir (SRCDIR)
    
    for name in PACKAGES:
        download_package (name)

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

def extract():
    for name in PACKAGES:
        extract_package (name)

def assemble():
    os.chdir (BASEDIR)
    download()
    extract()
    subprocess.call ([ 'sh', join (BASEDIR, 'luajit.sh') ])

if __name__ == "__main__":
    assemble()
    exit (0)
