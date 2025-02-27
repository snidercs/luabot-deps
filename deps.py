from os.path import abspath, dirname, expanduser, join, realpath
import zipfile

# Version of wpilib to assemble for
WPILIB_VERSION = '2025.2.1'
# The FRC year
WPILIB_YEAR = WPILIB_VERSION.split()[0]
# Path to installed wpilib. Usually it's $HOME/wpilib/$FRC_YEAR
WPILIBDIR = expanduser ('~/wpilib/%s/' % (WPILIB_YEAR))
# Path to installed luabot files within wpilib dir
LUABOTDIR = join (WPILIBDIR, 'luabot')
# Path to this code base.
BASEDIR   = abspath (dirname (realpath (__file__)))
# Where git repos downloaded code go
SRCDIR  = join (BASEDIR, 'src')
# Scratch directory when building make and other projects
WORKDIR = join (BASEDIR, 'work')
# Library output directory
LIBDIR  = join (BASEDIR, 'dist', 'lib')
# Header output directory
INCDIR  = join (BASEDIR, 'dist', 'include')

class Artifact:
    pass

class Repository:
    pass

# Unzips file into destdir.
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
