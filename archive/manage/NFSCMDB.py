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
from pymonkey.baseclasses.CMDBServerObject import CMDBServerObject

from NFSShare import NFSShare
from NFSEnums import NFSSecurityMode

class NFSCMDB(CMDBServerObject):
    
    # Where should this object be stored in cmdb
    cmdbtypename = "nfsserver"

    # NFS configuration properties
    shares = q.basetype.dictionary(doc = 'Dictionary containing a number of nfs share configurations', flag_dirty = True)
    configFilePath = q.basetype.filepath(doc = 'Location where the nfs configuration file is stored (Not applicable on solaris)', flag_dirty = True)
    
    def addShare(self, name, path, securityMode = NFSSecurityMode.NONE):
        """
        Adds a new share to the list
        
        @param name:                   unique name for the share
        @param path:                   path to share 
        @param securityMode:           specifies the security mode to be used on an NFS file system
        @return:                       the new share object
        """
        if name in self.shares:
            raise ValueError("Share '%s' is already in use"%name)
        
        share = NFSShare()
        share.name = name
        share.path = path
        share.securityMode = securityMode
        self.shares[name] = share
        return share
 
    def removeShare(self, name):
        """
        Removes the share with the given name from the list
        
        @param name: unique name for the share
        """
        if not q.basetype.string.check(name):
            raise TypeError('Name is not a string type')
        
        if not name in self.shares:
            raise KeyError("Share '%s' isn't registerd in shares"%name)
        
        if self.shares[name].deleted:
            raise ValueError("Share '%s' is already removed from shares"%name)
        
        self.shares[name].deleted = True
    
    def __fake_data__(self):
        """
        Generate fake data for testing
        """

        # Set directory for configuration files
        self.configFilePath = q.system.fs.joinPaths(q.dirs.varDir, 'tftproot')
        
        # Add some share's
        for i in xrange(3):
            share = NFSShare()
            share.name = 'share-%s' % q.base.idgenerator.generateRandomInt(0, 255)
            self.shares[share.name] = share