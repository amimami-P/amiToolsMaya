#----------------------------------------------------------
# -*- coding: utf-8 -*-
"""
amimamiがスキニングで使うツールをまとめて管理するランチャーです
"""
#----------------------------------------------------------
import os
import maya.cmds as cmds
import amiToolsLauncher
def amiTL_show_help():
    if cmds.window("helpWindow", exists=True):
        cmds.deleteUI("helpWindow")

    cmds.window("helpWindow", title="amiSkinTools Help", widthHeight=(400, 200),
                sizeable=False, maximizeButton=False, minimizeButton=False)

    cmds.columnLayout(adjustableColumn=True)

    cmds.scrollField(editable=False, wordWrap=True,width=400, height=200,  text=
        """
ツールヘルプ\n

amimamiがスキニングで使うツールをまとめて管理するランチャーです
        """
    )

    cmds.showWindow("helpWindow")

def amiSkinTools():
    """amiSkinToolsUI
    """
    # スクリプト格納ディレクトリ
    my_path = os.path.dirname(os.path.abspath(__file__))

    folder_list = [file for file in os.listdir(my_path) if not "." in file]
    if "Image" in folder_list:
        folder_list.remove("Image")

    if cmds.workspaceControl("amiSkinTools", exists=True):
        cmds.deleteUI("amiSkinTools", control=True)

    cmds.workspaceControl(
        "amiSkinTools",
        label="ami Skin Tools",
        floating=True,
        initialWidth=300,
        initialHeight=300 
    )

    form = cmds.formLayout("amiSkinToolsMainForm", parent="amiSkinTools")

    header = cmds.columnLayout("amiSkinToolsTopColumn", adjustableColumn=True, parent=form)
    cmds.rowLayout(numberOfColumns=3,
                columnAttach=[(1, "left", 0), (2, "left", 0), (3, "right", 0)],
                columnWidth=[(1, 100), (2, 170)])

    image_path = my_path.split("amiTools\\")[0]
    cmds.symbolButton(image=image_path + r"\amiTools\Image\amiIcon.png", w=30,h=30,
                        command=lambda *args:amiToolsLauncher.amiToolsLauncher())
    cmds.text(label="ami Skin Tools", height=30, font="boldLabelFont")
    cmds.button(label="?", width=30, height=30, command=lambda *_: amiTL_show_help())

    cmds.setParent("..")
    cmds.separator(height=10)

    scroll = cmds.scrollLayout("amiSkinToolsScroll", childResizable=True, parent=form)
    scroll_content = cmds.columnLayout("amiSkinToolsColumn", adjustableColumn=True, parent=scroll)

    for folder in enumerate(folder_list):
        command_test = f"""import Rig.amiSkinTools.{folder[1]}.{folder[1]} as {folder[1]}\n
from importlib import reload\nreload({folder[1]})\n{folder[1]}.{folder[1]}()"""
        cmds.button(label=folder[1], command=command_test, parent=scroll)
        cmds.separator(height=5, parent=scroll)
    cmds.setParent("..")

    cmds.formLayout(form, edit=True,
        attachForm=[
            (header, 'top', 0),
            (header, 'left', 0),
            (header, 'right', 0),
            (scroll, 'left', 0),
            (scroll, 'right', 0),
            (scroll, 'bottom', 0),
        ],
        attachControl=[
            (scroll, 'top', 0, header)
        ]
    )
