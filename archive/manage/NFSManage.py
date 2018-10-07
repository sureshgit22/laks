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
 
from pymonkey import q
from pymonkey.baseclasses.ManagementApplication import ManagementApplication, CMDBLockMixin
from pymonkey.enumerators import AppStatusType
from NFSCMDB import NFSCMDB
from NFSEnums import NFSAccessRight, NFSSecurityMode

class NFSManage(ManagementApplication, CMDBLockMixin):
    
    cmdb = NFSCMDB()
    
    def applyConfig(self):
        """
        Apply the configuration defined in cmdb to the server 
        """
        deletedShares = set()
        self.startChanges()
        for name, share in self.cmdb.shares.iteritems():
            anonymousUserId = securityMode = None
            if share.anonymousUserId:
                anonymousUserId = share.anonymousUserId
            if share.securityMode != NFSSecurityMode.NONE:
                securityMode = share.securityMode
                
            #if not share.new and (share.deleted or share.isDirty): # @TODO get isDirty working on dict,list... 
            if share.path.strip() in q.cmdtools.sharemgr.listNFSShares():
                q.cmdtools.sharemgr.removeNFSShare(share.path)
                if share.deleted:
                    deletedShares.add(name)
            
            #if share.new or share.isDirty: # @TODO get isDirty working on dict,list...
            if not share.deleted:
                readList = share.pm_getAccessList(NFSAccessRight.READ)
                rootList = share.pm_getAccessList(NFSAccessRight.ROOT)
                writeList = share.pm_getAccessList(NFSAccessRight.WRITE)
                writeList = writeList.union(rootList)
                q.cmdtools.sharemgr.addNFSShare(sharePath = share.path,
                                                securityMode = securityMode,
                                                readList = readList, 
                                                writeList = writeList, 
                                                rootList = rootList, 
                                                anonymousUser = anonymousUserId)
                q.cmdtools.sharemgr.setProperties(sharePath = share.path,
                                                  protocol = 'nfs',
                                                  options = 'nosuid=%s'%share.nosuid)
                share.new = False
            share.dirtyProperties.clear()
        for share in deletedShares:
            del self.cmdb.shares[share]
        self.save()
    
    def save(self):
        """
        Save the configuration in the cmdb
        """
        self.cmdb.save()
        self.cmdb.dirtyProperties.clear()
    
    def init(self):
        """
        Initialize the NFS environment
        """
        pass #TODO still necessary?
    
    def start(self):
        """
        Start the NFS service
        """
        pass #TODO need svcs wrapper?
    
    def stop(self):
        """
        Stop the NFS service
        """
        pass #TODO need svcs wrapper?
    
    def restart(self):
        """
        Restart the NFS service
        """
        pass #TODO need svcs wrapper?
    
    def printStatus(self):
        """
        Print status
        """
        q.console.echo("Application [%s] is %s" % (self.cmdb.cmdbtypename, self.getStatus()))
    
    def getStatus(self):
        """
        check system what current status of application is
        """
        return AppStatusType.UNKNOWN #TODO need svcs wrapper?
    
    def printConfig(self):
        """
        Print configuration
        """
        q.console.echo('Name           : %s'%self.cmdb.cmdbtypename)
        q.console.echo('ConfigFilePath : %s'%self.cmdb.configFilePath)
        q.console.echo('Shares:')
        if len(self.cmdb.shares)==0:
            q.console.echo('  None')
        for share in self.cmdb.shares.itervalues():
            share._printConfig()
            q.console.echo('')
            
        q.console.echo('')
        q.console.echo('* marked for deletion !')