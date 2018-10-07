__author__ = 'aserver'
__tags__ = 'install',

def main(q, i, params, tags):
    qpackage = params["qpackage"]
    qpackage.copyFiles()
    