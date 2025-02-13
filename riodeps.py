import os, shutil, subprocess, zipfile
from artifactory import ArtifactoryPath
from os.path import expanduser, join

# Version of wpilib to assemble for
WPILIB_VERSION = '2025.2.1'
# The FRC year
WPILIB_YEAR = WPILIB_VERSION.split()[0]

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

WPILIBDIR = expanduser ('~/wpilib/%s/' % (WPILIB_YEAR))
LUABOTDIR = join (WPILIBDIR, 'luabot')
BASEDIR   = os.path.dirname (os.path.realpath(__file__))

SRCDIR  = join (BASEDIR, 'src')
WORKDIR = join (BASEDIR, 'work')
LIBDIR  = join (BASEDIR, 'dist', 'lib')
INCDIR  = join (BASEDIR, 'dist', 'include')

BASEURL_WPI = 'https://frcmaven.wpi.edu/ui/native/wpilib-mvn-release/edu/wpi/first'
BASEURL_LUABOT = BASEURL_WPI
BASEURL = BASEURL_LUABOT

def baseurl (name):
    return '%s/%s/%s-cpp/%s' % (BASEURL, name, name, WPILIB_VERSION)

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

def unzip (file, destdir):
    try:
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(destdir)
        print (f"Extracted '{file}' to '{destdir}'")
    except FileNotFoundError:
         print (f"Error: file '{file}' not found.")
    except zipfile.BadZipFile:
        print (f"Error: '{file}' is not a valid archive.")
    except Exception as e:
        print (f"Error: Exception: {e}")

import stat

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

if __name__ == "__main__":
    os.chdir (BASEDIR)
    download()
    extract()    
    subprocess.call ([ 'sh', join (BASEDIR, 'luajit.sh') ])
    exit (0)
