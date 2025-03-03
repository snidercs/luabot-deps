#!/usr/bin/env python3

# Right now all this file does is echo a shell script that wget's
# the required maven artifacts from CTRE.

BASEURL = 'https://maven.ctr-electronics.com/release'

import deps, json

class MavenArtifact (deps.Artifact):
    def __init__(self, dep):
        self.dep = dep
    
    def version (self): return self.dep['version']
    def hasHeaders(self): return self.dep['headerClassifier'] == 'headers'
    def hasLibrary (self): return self.dep['sharedLibrary'] == True

    def supportedOn (self, platform):
        if not isinstance (platform, str):
            return False
        return platform.strip() in self.dep['binaryPlatforms']
    
    def groupId (self) -> str: return self.dep['groupId']
    def artifactId (self) -> str: return self.dep['artifactId']

    def headersZipFile (self):
        return '%s-%s-headers.zip' % (self.artifactId(), self.version())
    def libsZipFile (self, platform = 'linuxx86-64'):
        if not isinstance(platform, str) or len(platform.strip()) <= 0:
            raise RuntimeError
        return '%s-%s-%s.zip' % (self.artifactId(), self.version(), platform.strip())
    
    def baseURL (self):
        return '%s/%s/%s/%s' % (BASEURL, 
                                self.groupId().replace('.', '/'), 
                                self.artifactId(), 
                                self.version())
    def headersURL (self):
        return '%s/%s' % (self.baseURL(), self.headersZipFile())
    def libraryURL (self, platform = 'linuxx86-64'):
        return '%s/%s' % (self.baseURL(), self.libsZipFile (platform))
    def libraryURLs (self):
        return [self.libraryURL(plat) for plat in self.dep['binaryPlatforms']]

def load_json():
    with open ('vendordeps/phoenix6.json') as json_data:
        d = json.load (json_data)
        json_data.close()
        return d
    raise IOError()

def main():
    data = {}

    try:
        data = load_json()
    except IOError:
        print("Error reading json")
        return -1
    
    print ('''
#!/usr/bin/sh
# This file is auto generated: do not modify directly
    
set -e
    '''.strip())
    print()
    for d in [ MavenArtifact (dep) for dep in data['cppDependencies'] ]:
        if d.hasHeaders():
            print ('wget ' + d.headersURL())
        # for u in d.libraryURLs():
        #     print (u)
        print ('wget ' + d.libraryURL())
        if (d.supportedOn ('linuxathena')):
            print ('wget ' + d.libraryURL ('linuxathena'))
    print()
    print('exit 0')
    return 0

if __name__ == "__main__":
    exit (main())
