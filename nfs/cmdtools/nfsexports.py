from pymonkey import q
from sys import *
import re
import pprint

class nfsexports(object):
    """
    /etc/exports manager
    """
    def __init__(self, fstabFile=None):
        """
        Init
        """
        self._exportsFile = '/etc/exports'

    def _access(self):
        """
        Read from /etc/exports
        """
        q.logger.log("Buffering /etc/exports")
        f = open(self._exportsFile, 'r')
        dlist = []
        for line in f:
            dlist.append(line)
        f.close()
        dlist = [ i.strip() for i in dlist if not i.startswith('#') ]
        dlist = [ re.split('\s+|\(|\)',i) for i in dlist ]
        keys=['dir','network','params']
        ldict = [ dict(zip(keys,line)) for line in dlist ]

        return ldict
        
    def showConfig(self):
        """
        Print the content of /etc/exports
        """
        l = self._access()
        for i in l:
            print " %s %s(%s)" %(i['dir'], i['network'], i['params'])
            
    def showExportedShares(self):
        """
        Print the expoterd shares
        """
        exitcode, output = q.system.process.execute('exportfs')
        q.console.echo(output)

    def addNfsShare(self, nfs_dir, nfs_network, nfs_params):
        """
        Add an entry to /etc/exports

        @param nfs_dir: directory to export
        @type nfs_dir: string
        @param nfs_network: network range allowed
        @type nfs_network: string
        @param nfs_params: params for export (eg, 'ro,async,no_root_squash,no_subtree_check')
        @type nfs_params: string
        """
        l = self._access()
        for i in l:
            if i['dir'] == nfs_dir:
                q.console.echo('Directory already exported, please remove first')
                return
        q.logger.log("/etc/exports: appending entry %s %s(%s) to /etc/exports" % (nfs_dir, nfs_network, nfs_params))
        f = open(self._exportsFile, 'a')
        f.write('%s %s(%s)\n' % (nfs_dir, nfs_network, nfs_params))
        f.close
    
    def removeConfigByDirectory(self, nfs_dir):
        """
        Remove an entry from /etc/exports
        """
        l = self._access()
        for i in l:
            if i['dir'] == nfs_dir:
                l.remove(i)
                f = open(self._exportsFile, 'w')
                for i in l:
                    f.write("%s %s(%s) \n" % ( i['dir'], i['network'], i['params']))
                f.close()
                q.logger.log("/etc/exports: removing entry %s" % i)
                return
        q.logger.log("/etc/exports: no such entry %s found" % nfs_dir)

    def reloadNfsServer(self):
        """
        Reload the nfs server
        """
        exitcode, output = q.system.process.execute('/usr/sbin/exportfs -rav')
        if exitcode == 0:
            q.console.echo('Successfully reloaded nfs server')
        else:
            q.console.echo('Error while reloading nfs server')