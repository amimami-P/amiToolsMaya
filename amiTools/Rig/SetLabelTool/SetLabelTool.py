#----------------------------------------------------------
# -*- coding: utf-8 -*-
"""
"""
#----------------------------------------------------------
import os
import maya.cmds as cmds
import amiToolsLauncher

def setLabel(AllJoint=True):
    jointList = cmds.ls(sl=True,type="joint")
    if AllJoint:
        jointList = cmds.ls(type="joint")
    leftName = cmds.textField("leftNameTF", query=True, text=True)
    rightName = cmds.textField("rightNameTF", query=True, text=True)
    for i in jointList:
        cmds.setAttr(i + ".type",18)
        if leftName in i:
            cmds.setAttr(i + ".side",1)
        elif rightName in i:
            cmds.setAttr(i + ".side",2)
        else:
            cmds.setAttr(i + ".side",0)

        label_Name= i.replace(rightName,"")
        label_Name= label_Name.replace(leftName,"")
        if label_Name.startswith("_"):
            label_Name = label_Name[1:]
        print (label_Name)
        cmds.setAttr(i + ".otherType",label_Name,type="string")

def ToggleLabel(AllJoint=True):

    jointList = cmds.ls(sl=True,type="joint")
    if AllJoint:
        jointList = cmds.ls(type="joint")
    for index,jnt in enumerate(jointList):
        if index == 0:
            ShowHide = cmds.getAttr(jnt + ".drawLabel")
        cmds.setAttr(jnt + ".drawLabel",not ShowHide)

def SetLabelTool():
    if cmds.window("SetLabelTool", exists=True):
        cmds.deleteUI("SetLabelTool")
    window = cmds.window("SetLabelTool", title="SetLabelTool", widthHeight=(320, 200),
                                sizeable=False,maximizeButton=False, minimizeButton=False,)
    cmds.columnLayout("SetLabelToolMainColumn", adjustableColumn=True)
    cmds.rowLayout(numberOfColumns=3,columnAttach=[(2, "both", 102),])
    my_path =os.path.dirname(os.path.abspath(__file__))
    image_path = my_path.split("amiTools\\")[0]
    cmds.symbolButton(image=image_path + r"\amiTools\Image\amiIcon.png", w=30,h=30,
                        command=lambda *args:amiToolsLauncher.amiToolsLauncher())
    cmds.text(label="Set Label",h=30, font="boldLabelFont")
    cmds.button(label="?", width=30, height=30, command=lambda *_:print("help"))
    cmds.setParent("..")
    cmds.separator( height=10)
    cmds.text(label="左右の識別子を入力")
    cmds.rowLayout(numberOfColumns=3)
    
    cmds.textField("leftNameTF", text="L_",w=150,h=30)
    cmds.text(label=" - ")
    cmds.textField("rightNameTF", text="R_",w=150,h=30)
    cmds.setParent("..")
    
    cmds.separator( height=15)
    cmds.rowLayout(numberOfColumns=3)
    cmds.button(label="Set All Label",h=35,w=160,command=lambda *_:setLabel(AllJoint=True))
    cmds.button(label="Set Select Label",h=35,w=160,command=lambda *_:setLabel(AllJoint=False))
    cmds.setParent("..")
    cmds.separator( height=10)
    cmds.rowLayout(numberOfColumns=3)
    
    cmds.button(label="Toggle All Label",h=40,w=160,command=lambda *_:ToggleLabel(AllJoint=True))
    cmds.button(label="Toggle Select Label",h=40,w=160,command=lambda *_:ToggleLabel(AllJoint=False))
    cmds.setParent("..")
    cmds.showWindow(window)
    cmds.setFocus("")
