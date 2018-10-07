__author__ = 'aserver'
__tags__ = 'package',

def main(q, i, params, tags):
    qpackage = params["qpackage"]
    # do some cleaning before
    metadataDir = qpackage.getPathMetadata()
    filesDir = qpackage.getPathFiles()
    q.system.fs.removeDirTree(filesDir)
    q.system.fs.createDir(filesDir)

    q.system.fs.copyDirTree(q.system.fs.joinPaths(q.dirs.baseDir, 'var', 'src', 'nfs_extension', 'tasklets'), q.system.fs.joinPaths(metadataDir, 'tasklets'))
    q.system.fs.copyDirTree(q.system.fs.joinPaths(q.dirs.baseDir, 'var', 'src', 'nfs_extension', 'files'), q.system.fs.joinPaths(filesDir, 'linux', 'lib', 'pymonkey', 'extensions'))

