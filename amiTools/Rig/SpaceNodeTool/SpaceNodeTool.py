#----------------------------------------------------------
# -*- coding: utf-8 -*-
"""
"""
#----------------------------------------------------------
import os
import maya.cmds as cmds
import amiToolsLauncher


def insert_spaceNode(transform=False, joint=False):

    if transform and joint:
        raise ValueError("transform と joint の両方を True にすることはできません。")

    if transform:
        for i in cmds.ls(sl=True):
            parentNodes = cmds.listRelatives(i, parent=True)
            sp = cmds.createNode("transform", n=i + "Space")
            cmds.parent(sp, i)
            cmds.setAttr(sp + ".translate", 0, 0, 0)
            cmds.setAttr(sp + ".rotate", 0, 0, 0)
            cmds.setAttr(sp + ".scale", 1, 1, 1)
            if parentNodes:
                cmds.parent(sp, parentNodes)
            else:
                cmds.parent(sp, world=True)
            cmds.parent(i, sp)

    if joint:
        for i in cmds.ls(sl=True):
            cmds.select(clear=True)
            cmds.select(i)
            sp = cmds.joint(n=i + "Space")
            parentNodes = cmds.listRelatives(i, parent=True)
            if parentNodes:
                cmds.parent(sp, parentNodes)
            else:
                cmds.parent(sp, world=True)
            cmds.parent(i, sp)

def SpaceNodeTool():
    if cmds.window("SpaceNodeTool", exists=True):
        cmds.deleteUI("SpaceNodeTool")
    window = cmds.window("SpaceNodeTool", title="SpaceNodeTool", widthHeight=(204, 145),
                                sizeable=False,maximizeButton=False, minimizeButton=False,)
    cmds.columnLayout(adjustableColumn=True)
    cmds.rowLayout(numberOfColumns=3,columnAttach=[(2, "both", 30),])
    my_path =os.path.dirname(os.path.abspath(__file__))
    image_path = my_path.split("amiTools")[0]
    cmds.symbolButton(image=image_path + r"\amiTools\Image\amiIcon.png", w=30,h=30,
                        command=lambda *args:amiToolsLauncher.amiToolsLauncher())
    cmds.text(label="SpaceNodeTool",h=30, font="boldLabelFont")
    cmds.button(label="?", width=30, height=30, command=lambda *_:print("help"))
    cmds.setParent("..")
    cmds.separator(height=10)
    cmds.button(label="joint",h=50,command=lambda *_:insert_spaceNode(joint=True))
    cmds.separator(height=2)
    cmds.button(label="transform",h=50,command=lambda *_:insert_spaceNode(transform=True))
    cmds.showWindow(window)


