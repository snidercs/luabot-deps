from os.path import abspath, dirname, exists, expanduser, join, realpath

import os, shutil, stat, zipfile

# Version of wpilib to assemble for.
WPILIB_VERSION = '2025.2.1'
# The FRC year
FRC_YEAR = WPILIB_VERSION.split()[0]
# Path to installed wpilib. Usually it's $HOME/wpilib/$FRC_YEAR
WPILIBDIR = expanduser ('~/wpilib/%s/' % (FRC_YEAR))
# Path to installed luabot files within wpilib dir.
LUABOTDIR = join (WPILIBDIR, 'luabot')
# Path to this code base.
BASEDIR   = abspath (dirname (realpath (__file__)))
# Dist dir
DISTDIR = join (BASEDIR, 'dist')
# Where git repos and downloaded sources go.
SRCDIR  = join (BASEDIR, 'src')
# Scratch directory when building make and other projects.
WORKDIR = join (BASEDIR, 'work')
# Library output directory.
LIBDIR  = join (DISTDIR, 'lib')
# Exe output directory.
BINDIR = join (DISTDIR, 'bin')
# Header output directory.
INCDIR  = join (DISTDIR, 'include')
# Data dir
SHAREDIR = join (DISTDIR, 'share')

# Possible platforms
PLATFORMS = '''
    windowsx86-64
    linuxx86-64
    linuxarm64
    linuxathena
    osxuniversal
'''.split()

class Artifact:
    pass

class Repository:
    pass

def clean():
    # Don't ever erase srcdir!
    if not os.path.exists (SRCDIR):
        os.mkdir (SRCDIR)

    for dir in [ WORKDIR, DISTDIR ]:
        if os.path.exists (dir):
            shutil.rmtree (dir)
        os.makedirs (dir, 511, True)

    os.makedirs (INCDIR, 511, True)

    for p in PLATFORMS:
        os.makedirs (join (LIBDIR, p), 511, True)

# Returns true if the filename has been downloaded.
def downloaded (filename):
    return exists (join (SRCDIR, filename))

# Unzips file into destdir.
def unzip (file, destdir):
    try:
        with zipfile.ZipFile (file, 'r') as zip_ref:
            zip_ref.extractall(destdir)
        print (f"Extracted '{file}' to '{destdir}'")
    except FileNotFoundError:
        print (f"Error: file '{file}' not found.")
    except zipfile.BadZipFile:
        print (f"Error: '{file}' is not a valid archive.")
    except Exception as e:
        print (f"Error: Exception: {e}")

def noext (input: str):
    return input.rsplit ('.', 1)[0].strip()

def system (filename: str):
    input = noext (filename)
    if 'linux' in input: return 'linux'
    if 'windows' in input: return 'windows'
    if 'osx' or 'darwin' in input: return ''
    raise Exception(f'unknown platfrom for: {input}')

def arch (filename: str):
    input = noext (filename)
    if 'x86-64' in input: return 'x86-64'
    if 'athena' in input: return 'athena'
    if 'universal' in input: return 'universal'
    raise Exception(f'unknown arch for: {input}')

def platform (filename: str):
    for p in PLATFORMS:
        if p in filename:
            return p

def libsubpath (filename: str):
    return join (system (filename), arch (filename), 'shared')

def extractlib (filename: str):
    zipfile = join (SRCDIR, filename)
    outpath = join (WORKDIR, filename.rsplit ('.', 1)[0])
    os.makedirs (outpath, 511, True)
    unzip (zipfile, outpath)

    libpath = join (outpath, libsubpath (filename))
    if not exists (libpath):
        raise FileNotFoundError (libpath)

    libdir = join (LIBDIR, platform (filename))
    if not exists (libdir): os.makedirs (libdir)
    for f in os.listdir (libpath):
        of = shutil.copy2 (join (libpath, f), libdir)
        st = os.stat (of)
        os.chmod (of, st.st_mode | stat.S_IEXEC)

def extractheaders (filename: str):
    zipfile = join (SRCDIR, filename)
    outpath = join (INCDIR)
    os.makedirs (outpath, 511, True)
    unzip (zipfile, outpath)

def extract (filename: str):
    fnoext = filename.rsplit ('.', 1)[0].strip()
    if fnoext.endswith ('headers'):
        extractheaders (filename)
    else:
        for p in PLATFORMS:
            if fnoext.endswith (p):
                extractlib (filename)

def extractall():
    for fn in os.listdir (SRCDIR):
        extract (fn)

def main():
    clean()
    extractall()
    import subprocess
    subprocess.call ([ 'sh', join (BASEDIR, 'luajit.sh') ])

if __name__ == '__main__':
   main()
