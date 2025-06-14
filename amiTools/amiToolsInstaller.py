# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
import sys
sys.dont_write_bytecode = True
# ------------------------------------------------------------------------------
try:
    from importlib import reload
except:
    pass

import os
from maya import cmds,mel

def onMayaDroppedPythonFile(*args, **kwargs):
    """Functions executed by drag and drop..

    Functions executed by drag and drop.

    Args:
        None

    Returns:
        None

    """
    _create_shelf()

def _create_shelf(*args, **kwargs):
    """Functions to create shelves.

    Function to create a shelf.
    Adds a button to the currently selected shelf.

    Args:
        None

    Returns:
        None

    """
    script_path = os.path.dirname(__file__)

    command = """
import importlib
import sys
if not r'{0}' in sys.path:
    sys.path.append(r'{0}')

import amiToolsLauncher
importlib.reload(amiToolsLauncher)
amiToolsLauncher.amiToolsLauncher()

""".format(script_path)

    print(command)
    shelf = mel.eval("$gShelfTopLevel=$gShelfTopLevel")
    parent = cmds.tabLayout(shelf, query=True, selectTab=True)
    try:
        cmds.shelfButton(
            command=command,
            image=script_path + "//Image//amiIcon.png",
            annotation="amiToolsLauncher",
            label="amiTools",
            imageOverlayLabel="amiTools",
            sourceType="Python",
            parent=parent
        )
    except:
        import traceback
        print(traceback.format_exc())
