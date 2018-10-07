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
 
from pymonkey.baseclasses.BaseEnumeration import BaseEnumeration, EnumerationWithValue

class NFSAccessRight(EnumerationWithValue):

    """
    Enumaration of NFS access rights
    READ:     can only read from the share
    WRITE:    can also write to te share
    ROOT:     has root access to the share
    """
    pass
NFSAccessRight.registerItem('read', 'ro')
NFSAccessRight.registerItem('write', 'rw')
NFSAccessRight.registerItem('root', 'root')
NFSAccessRight.finishItemRegistration()

class NFSSecurityMode(EnumerationWithValue):
    """
    Enumaration of NFS security modes
    """
    pass
NFSSecurityMode.registerItem('none', 'none')
NFSSecurityMode.registerItem('sys', 'sys')
NFSSecurityMode.registerItem('dh', 'dh')
NFSSecurityMode.registerItem('krb5', 'krb5')
NFSSecurityMode.registerItem('krb5i', 'krb5i')
NFSSecurityMode.registerItem('krb5p', 'krb5p')
NFSSecurityMode.finishItemRegistration()