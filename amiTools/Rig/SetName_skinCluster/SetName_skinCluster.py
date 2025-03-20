# ------------------------------------------------------
# -*- coding: utf-8 -*-
# ------------------------------------------------------
import os
import maya.cmds as cmds
import amiToolsLauncher


def SetName_skinCluster():
    for sc in cmds.ls(type="skinCluster"):
        meshName = (cmds.listConnections(sc + ".outputGeometry[0]", destination=True)[0])
        cmds.rename(sc,"SC_" + meshName)
    cmds.inViewMessage(
        smg=(u"skinClusterノードの名前を SC_ + meshName に変更しました"),
        pos="topCenter",
        bkc=0x00000000,
        fadeStayTime=3000,
        fade=True,
        )