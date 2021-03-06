# -*- coding: utf-8 -*-
import os, re
from .. import util
import plistlib
import subprocess
import shutil

from . import base

REQUIRE = [ 'macdeployqt',
            ]

class Packager(base.Packager):

    def __init__(self, info, version, files):
        super(Packager,self).__init__(info, version, files)

        self.EXT = 'dmg'
        self.EXT_BIN = ''
        self.EXT_LIB = 'dylib'
        self.DIR_PACKAGE = os.path.join(self.DIR_STAGING,'mac')
        self.DIR_BUNDLE = os.path.join(self.DIR_PACKAGE,self.info['name']+'.app')
        self.DIR_OUT = os.path.join(self.DIR_BUNDLE,'Contents')

        self.OUT['bin'] = 'MacOS'
        self.OUT['lib'] = 'MacOS'
        self.OUT['share'] = 'Resources'

    def get_path(self):
        return self.DIR_BUNDLE

    def bundle_identifier(self):
        return 'com.'+self.info['org'].lower()+self.info['name']

    def build_plist(self, info, target):
        pl = dict(
            CFBundleDevelopmentRegion = "English",
            CFBundleDisplayName = self.info['name'],
            CFBundleExecutable = self.info['package'],
            CFBundleIconFile = "mac.icns",
            CFBundleIdentifier = self.bundle_identifier(),
            CFBundleInfoDictionaryVersion = "6.0",
            CFBundleName = self.info['package'],
            CFBundlePackageType = "APPL",
            CFBundleShortVersionString = self.VERSION,
            CFBundleVersion = "1",
            LSApplicationCategoryType = 'public.app-category.developer-tools',
            LSMinimumSystemVersion = "10.7",
            NSHumanReadableCopyright = u"Copyright © "+self.info['copyright']
                    +", "+self.info['org']+". "
                    +self.info['name']
                    +" is released under the "
                    +self.info['license']+" license.",
            NSPrincipalClass = "NSApplication",
            NSSupportsSuddenTermination = "YES",
        )
        return pl

    def mac_installer(self):
        script = util.get_template('mac/installer.AppleScript')
        rendering = script.substitute(
                        title = self.info['name'],
                        background = os.path.basename(self.background),
                        applicationName = os.path.basename(self.DIR_BUNDLE)
                    )
        return rendering


    def make(self):
        super(Packager,self).make()
        with util.pushd(self.DIR_OUT):
            plistlib.writePlist(self.build_plist(self.info, None), 
                    os.path.join(self.DIR_OUT,'Info.plist'))

    def finish(self):
        target = os.path.join(self.DIR_STAGING, self.packagename())
        self.background = 'icons/mac-dmg.png'

        size = util.command(['du','-s',self.DIR_BUNDLE])[0].split()[0]
        size = str(int(size)+10000)
        print size
        tmpdevice = os.path.join(self.DIR_PACKAGE, 'pack.temp.dmg')

        subprocess.check_call(['hdiutil','create',
            '-format','UDRW',
            '-srcfolder',self.DIR_BUNDLE,
            '-volname',self.info['name'],
            '-size',size+'k',
            tmpdevice])

        devices = subprocess.check_output(['hdiutil','attach',
            '-readwrite',
            tmpdevice]).splitlines()
        
        print devices

        r = re.compile('^/dev/')
        devices = filter(r.match, devices)
        device = devices[0].split()[0]
        
        print device

        DIR_VOLUME = os.path.join(os.sep,'Volumes',self.info['name'],'.background')
        util.mkdir(DIR_VOLUME)
        shutil.copy(self.background, DIR_VOLUME)

        p = subprocess.Popen(['osascript','-'], stdin=subprocess.PIPE)
        p.communicate(input=self.mac_installer())

        subprocess.check_call(['chmod','-Rf','go-w',DIR_VOLUME])
        subprocess.check_call(['chmod','-Rf','go-w',
            os.path.join(os.path.dirname(DIR_VOLUME),
                self.info['name']+'.app')])
        subprocess.check_call(['chmod','-Rf','go-w',
            os.path.join(os.path.dirname(DIR_VOLUME),
                'Applications')])
        subprocess.check_call(['sync'])
        subprocess.check_call(['sync'])
        subprocess.check_call(['hdiutil','detach',device])
        subprocess.check_call(['hdiutil','convert',tmpdevice,'-format','UDZO',
            '-imagekey','zlib-level=9','-o',target])
        os.remove(tmpdevice)
