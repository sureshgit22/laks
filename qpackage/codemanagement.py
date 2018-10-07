__author__ = 'aserver'
__tags__ = 'codemanagement',
def main(q, i, params, tags):
    from pymonkey.clients.hg.HgRecipe import HgRecipe
    recipe = HgRecipe()
    
    connection = i.hg.connections.findByUrl("http://bitbucket.org/despiegk/nfs_extension")
    taskletsexportDir = q.system.fs.joinPaths(q.dirs.varDir, 'src', 'nfs_extension', 'tasklets') 
    filesexportDir = q.system.fs.joinPaths(q.dirs.varDir, 'src', 'nfs_extension', 'files')
    
    if q.system.fs.exists(taskletsexportDir):
        q.system.fs.removeDirTree(taskletsexportDir)
    if q.system.fs.exists(filesexportDir):
        q.system.fs.removeDirTree(filesexportDir)

    recipe.addRepository(connection)
    recipe.addSource(connection, 'qpackage', q.system.fs.joinPaths('var', 'src', 'nfs_extension', 'tasklets'),branch='default')
    recipe.addSource(connection, 'nfs', q.system.fs.joinPaths('var', 'src', 'nfs_extension', 'files', 'nfs'), branch='default')

    if params['action'] == 'getSource':
        params['action'] = 'export'
        
    recipe.executeTaskletAction(params["action"])