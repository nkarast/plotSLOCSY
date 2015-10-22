import os, sys

def exportLocalModules():
    print('[INFO] (exportLocalModules) Exporting local modules (./local/lib) .')
    command = "export PATH=$PWD/.local/bin:$PATH"
    os.system(command)
    command = "LD_LIBRARY_PATH=$PWD/.local/lib:$LD_LIBRARY_PATH"
    os.system(command)


# - * - * - * - * - * - * - * - * - * - * - * - * - * - *

def linkPyROOT():
    roopath = os.environ["ROOTSYS"]
    if roopath == "":
        print('[FATAL] (linkPyROOT) $ROOTSYS has not been set. Cannot link to PyROOT.')
        sys.exit(2)

    print('[INFO] (linkPyROOT) Setting ROOT to PYTHONPATH.')
    command = "export LD_LIBRARY_PATH=$ROOTSYS/lib:$PYTHONDIR/lib:$LD_LIBRARY_PATH"
    os.system(command)
    command = "export PYTHONPATH=$ROOTSYS/lib:$PYTHONPATH"
    os.system(command)


