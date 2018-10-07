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
from pymonkey import pmtypes

from pymonkey.baseclasses.CMDBSubObject import CMDBSubObject
from NFSNetwork import NFSNetwork
from NFSEnums import NFSAccessRight, NFSSecurityMode

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO 
    

class NFSShare(CMDBSubObject):
    
    # Configuration properties
    name              = q.basetype.string(doc = 'unique name for this module') 
    
    # NFS Share properties
    path              = q.basetype.filepath(doc = 'Path to share', flag_dirty = True)
    anonymousUserId   = q.basetype.string(doc = 'The effective user ID of unknown users. By default, unknown  users are given the effective user ID UID_NOBODY. If uid is set to -1, access is denied.', flag_dirty = True)
    nosuid            = q.basetype.boolean(doc = 'Specifying nosuid causes the server file system to  silently  ignore any attempt to enable the setuid or setgid mode bits', default = False, flag_dirty = True)
    hostsAllowed      = q.basetype.dictionary(doc = 'Dictionary of IPv4Addresses that can access the share with their NFSAccessRight as value', flag_dirty = True)
    networksAllowed   = q.basetype.dictionary(doc = 'Dictionary of NFSIPRange instances with network as key', flag_dirty = True)
    securityMode      = q.basetype.enumeration(NFSSecurityMode, flag_dirty = True)
    
    def addHost(self, host, accessRight = NFSAccessRight.READ):
        """
        Add a host to the list of allowed hosts with the given access right
        
        @param host:        name or ipaddress of the host to add to the list
        @param accessRight: rights granted on the share for the given host
        """
        if not q.basetype.string.check(host):
            raise TypeError('Host is not valid string type')
        
        if not NFSAccessRight.check(accessRight):
            raise TypeError('Access right is not valid NFSAccessRight type')
        
        if host in self.hostsAllowed:
            raise ValueError("Host '%s' is already in use"%host)
        
        self.hostsAllowed[host] = accessRight
        
    def removeHost(self, host):
        """
        Remove a host from the list of allowed hosts
        
        @param host:        name or ipaddress of the host to remove from the list
        """
        if not q.basetype.string.check(host):
            raise TypeError('Host is not valid string type')
        
        if not host in self.hostsAllowed:
            raise KeyError("Host '%s' isn't registerd in hosts"%host)
        
        del self.hostsAllowed[host]
    
    def addNetwork(self, network, netmask, accessRight = NFSAccessRight.READ):
        """
        Add a network to the list of allowed network with the given access right
        
        @param network:    an ipaddress e.g 192.168.1.1
        @param netmask:    an netmask e.g 255.255.255.0
        @param accessRight: rights granted on the share for the given host (ROOT will give also WRITE)
        """
        if not q.basetype.string.check(network):
            raise TypeError, 'Network is not valid string type'
        if not q.basetype.string.check(netmask):
            raise TypeError, 'Netmask is not valid string type'
        if not NFSAccessRight.check(accessRight):
            raise TypeError('Access right is not valid NFSAccessRight type')
        networkName = '%s/%s'%(network,  pmtypes.IPv4Range.convertNetmask(netmask))
        if networkName in self.networksAllowed:
            raise KeyError("Network '%s' with netmask '%s' is already in use"%(network,netmask))
        
        networkrange = NFSNetwork()
        networkrange.ipaddressrange = pmtypes.IPv4Range(netIp=network, netMask=netmask)
        networkrange.accessRight = accessRight
        self.networksAllowed[networkName] = networkrange
    
    def removeNetwork(self, network, netmask):
        """
        Remove a network from the list of allowed hosts
        
        @param network:    an ipaddress e.g 192.168.1.1
        @param netmask:    an netmask e.g 255.255.255.0
        """
        if not q.basetype.string.check(network):
            raise TypeError, 'Network is not valid string type'
        if not q.basetype.string.check(netmask):
            raise TypeError, 'Netmask is not valid string type'
        if not networkName in self.networksAllowed:
            raise KeyError("Network '%s' with netmask '%s' isn't registerd"%(network,netmask))
        networkName = '%s/%s'%(network,  pmtypes.IPv4Range.convertNetmask(netmask))
        del self.networksAllowed[networkName]
    
    def __str__(self):
        """
        String representation of this NFSShare configuration
        """
        return self._buildConfigString()
    
    def _printConfig(self):
        """
        Prints NFSShare configuration
        """
        q.console.echo(self._buildConfigString())
            
    def _buildConfigString(self):
        indentLevelOne = ' ' * 3
        indentLevelTwo = ' ' * 5        
        output = StringIO()
        
        if self.deleted:
            output.write('%sName            : %s *\n'%(indentLevelOne,self.name))
        else:
            output.write('%sName            : %s\n'%(indentLevelOne,self.name))
        
        output.write('%sPath            : %s\n'%(indentLevelOne,self.path))
        output.write('%sAnonymousUserId : %s\n'%(indentLevelOne,self.anonymousUserId))
        output.write('%sNosuid          : %s\n'%(indentLevelOne,self.nosuid))
        output.write('%sSecurityMode    : %s\n'%(indentLevelOne, self.securityMode))
        output.write('%sHosts:\n'%indentLevelOne)
        
        if not self.hostsAllowed:
            output.write('%sNone\n'%indentLevelTwo)
        
        for name, accessright in self.hostsAllowed.iteritems():
            output.write('%sHost         : %s\n'%(indentLevelTwo, name))
            output.write('%sAccess right : %s\n'%(indentLevelTwo, accessright))
            output.write('\n')
        
        output.write('%sNetworks:\n'%indentLevelOne)
        
        if len(self.networksAllowed)==0:
            output.write('%sNone\n'%indentLevelTwo)
        
        for network in self.networksAllowed.itervalues():
            output.write('%sNetwork      : %s/%s\n'%(indentLevelTwo, network.ipaddressrange.netIp, network.ipaddressrange.netMask))
            output.write('%sAccess right : %s\n'%(indentLevelTwo, network.accessRight))
            output.write('\n')

        cfgString = output.getvalue()
        output.close() 
        return cfgString


    def pm_getAccessList(self, accessRight):
        """
        Returns read configuration string of this share
        
        @param accessRight: NFSAccessRight enum
        """
        list = set()
        for host, accessright in self.hostsAllowed.iteritems():
            if accessright == accessRight:
                list.add("@%s/32"%host)
                
        for network in self.networksAllowed.itervalues():
            if network.accessRight == accessRight:
                list.add('@%s/%s'%(network.ipaddressrange.netIp, pmtypes.IPv4Range.convertNetmask(network.ipaddressrange.netMask)))
                
        return list
                        
    def __fake_data__(self):
        self.path = q.system.fs.joinPaths(q.dirs.varDir, 'shares', str(q.base.idgenerator.generateRandomInt(0, 255))                                 )
        self.anonymousUserId = 'anon'
        self.securityMode = q.enumerators.NFSSecurityMode.SYS
        for i in xrange(3):
            ip = '.'.join(str(q.base.idgenerator.generateRandomInt(0, 255)) for i in xrange(4))
            right = NFSAccessRight.READ if i % 2 == 0 else NFSAccessRight.WRITE
            self.hostsAllowed[ip] = right