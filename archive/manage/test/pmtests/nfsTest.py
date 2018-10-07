# <License type="Sun Cloud BSD" version="2.2">
#
# Copyright (c) 2005-2009, Sun Microsystems, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# 3. Neither the name Sun Microsystems, Inc. nor the names of other
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SUN MICROSYSTEMS, INC. "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SUN MICROSYSTEMS, INC. OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# </License>
 
from pymonkey.InitBase import *
from pymonkey import pmtypes

from servers.nfs_manage_extension.NFSEnums import NFSAccessRight, NFSSecurityMode

def createShare(name, hostAccess, netAccess):
    q.action.start('create shares')
    nfs.startChanges()
    s = n.addShare(name, q.system.fs.joinPaths('/nfsShareTest',name), NFSSecurityMode.NONE)
    addHost(s, hostAccess)
    addNetwork(s, netAccess)
    n.save()
    applyChanges()
    q.action.stop()
    
def addHost(share, hostAccess):
    q.action.start('create host')
    nfs.startChanges()
    share.addHost('127.0.0.1', hostAccess)
    n.save()
    applyChanges()
    q.action.stop()
    
def addNetwork(share, netAccess):
    q.action.start('create network')
    nfs.startChanges()
    share.addNetwork('192.168.11.0', '255.255.0.0', netAccess)
    n.save()
    applyChanges()
    q.action.stop()

def removeShare(name):
    q.action.start('remove share')
    nfs.startChanges()
    s = n.shares[name]
    removeHost(s)
    removeNetwork(s)
    n.removeShare(name)
    n.save()
    applyChanges()
    q.action.stop()

def removeHost(share):
    q.action.start('remove host')
    nfs.startChanges()
    share.removeHost('127.0.0.1')
    n.save()
    applyChanges()
    q.action.stop()
    
def removeNetwork(share):
    q.action.start('remove network')
    nfs.startChanges()
    share.removeNetwork('192.168.11.0', '255.255.0.0')
    n.save()
    applyChanges()
    q.action.stop()
    
def applyChanges():
    q.action.start('apply config')
    nfs.applyConfig()
    q.action.stop()

    
def initializeSystem():
    q.action.start('initializing system')
    try:   
        if not q.system.fs.exists('/nfsShareTest/readwrite'):
            q.system.fs.createDir('/nfsShareTest/readwrite')
        if not q.system.fs.exists('/nfsShareTest/readonly'):
            q.system.fs.createDir('/nfsShareTest/readonly')
        if not q.system.fs.exists('/nfsShareTest/mounts/readwrite'):
            q.system.fs.createDir('/nfsShareTest/mounts/readwrite')
        if not q.system.fs.exists('/nfsShareTest/mounts/readonly'):
            q.system.fs.createDir('/nfsShareTest/mounts/readonly')
            
        result, output = q.system.process.execute('chmod g+w /nfsShareTest/readwrite/', outputToStdout=False)
        result, output = q.system.process.execute('chmod o+w /nfsShareTest/readwrite/', outputToStdout=False)
        result, output = q.system.process.execute('chmod g+w /nfsShareTest/readonly/', outputToStdout=False)
        result, output = q.system.process.execute('chmod o+w /nfsShareTest/readonly/', outputToStdout=False)
        
    except:
        pass
    q.action.stop()
    
def cleanupSystem():
    q.action.start('cleanup system')
    try:   
        if q.system.fs.exists('/nfsShareTest/readwrite'):
            q.system.fs.removeDirTree('/nfsShareTest/readwrite')
        if q.system.fs.exists('/nfsShareTest/readonly'):
            q.system.fs.removeDirTree('/nfsShareTest/readonly')
        if q.system.fs.exists('/nfsShareTest/mounts/readwrite'):
            q.system.fs.removeDirTree('/nfsShareTest/mounts/readwrite')
        if q.system.fs.exists('/nfsShareTest/mounts/readonly'):
            q.system.fs.removeDirTree('/nfsShareTest/mounts/readonly')
        
    except:
        pass
            
    q.action.stop()
    
def validateNFSMounts():
    q.action.start('validate the created nfs shares')
    
    q.action.start('mounting nfs shares')
    result, output = q.system.process.execute('mount -F nfs -o rw 127.0.0.1:/nfsShareTest/readwrite /nfsShareTest/mounts/readwrite/')
    if result != 0:
        raise RuntimeError(output)   
    result, output = q.system.process.execute('mount -F nfs -o ro 127.0.0.1:/nfsShareTest/readonly /nfsShareTest/mounts/readonly/')
    if result != 0:
        raise RuntimeError(output)
    q.action.stop()
    
        
    q.action.start('create an empty file on the new shared filesystem')
    result, output = q.system.process.execute('touch /nfsShareTest/mounts/readwrite/testfile')
    if result != 0:
        raise RuntimeError(output)
    q.action.stop()
    
    
    testPassed = False
    q.action.start('create an empty file on the read-only filesystem')
    try:    
        result, output = q.system.process.execute('touch /nfsShareTest/mounts/readonly/testfile', outputToStdout=False)
    except:
        testPassed=True
    finally:
        if not testPassed:
            raise RuntimeError("creating files should not be possible on read-only filesystems")        
    q.action.stop()

        
    q.action.start('unmounting the filesystems')
    result, output = q.system.process.execute('umount /nfsShareTest/mounts/readwrite/')
    if result != 0:
        raise RuntimeError(output)
    result, output = q.system.process.execute('umount /nfsShareTest/mounts/readonly/')
    if result != 0:
        raise RuntimeError(output)    
    q.action.stop()    
    
    q.action.stop()
    
    
def validateShareRemovals():
    q.action.start('validate removed nfs shares')
    
    q.action.start('mounting removed nfs shares')
    testPassed = False
    try:
        q.system.process.execute('mount -F nfs -o rw 127.0.0.1:/nfsShareTest/readwrite /nfsShareTest/mounts/readwrite/')
    except:
        testPassed=True
    finally:
        if not testPassed:
            raise RuntimeError("Share 'readwrite' should be removed and mounting it should fail !")
        

    testPassed = False
    try:
        q.system.process.execute('mount -F nfs -o rw 127.0.0.1:/nfsShareTest/readonly /nfsShareTest/mounts/readonly/')
    except:
        testPassed=True
    finally:
        if not testPassed:
            raise RuntimeError("Share 'readonly' should be removed and mounting it should fail !")
    
    q.action.stop()    
    
    q.action.stop()












try:
    nfs = q.manage.nfs
    n = nfs.cmdb
    n.configFilePath = q.system.fs.joinPaths(q.dirs.cfgDir, 'nfs', 'nfs.cfg')
    
    initializeSystem()
    createShare('readwrite', NFSAccessRight.WRITE, NFSAccessRight.WRITE)
    createShare('readonly', NFSAccessRight.READ, NFSAccessRight.READ)
    validateNFSMounts()
    removeShare('readwrite')
    removeShare('readonly')
    validateShareRemovals()
finally:
    cleanupSystem()