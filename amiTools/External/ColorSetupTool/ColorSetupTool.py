#----------------------------------------------------------
# -*- coding: utf-8 -*-
import os
import maya.cmds as cmds
import amiToolsLauncher

def apply_color_to_selected(rgb, apply_viewport, apply_outliner):
    """選択中オブジェクトに指定色を適用（オプション付き）"""
    selected = cmds.ls(selection=True)
    if not selected:
        cmds.warning("オブジェクトを選択してください。")
        return

    for obj in selected:
        if apply_viewport:
            cmds.setAttr(obj + ".overrideEnabled", 1)
            cmds.setAttr(obj + ".overrideRGBColors", 1)
            cmds.setAttr(obj + ".overrideColorRGB", rgb[0], rgb[1], rgb[2])

        if apply_outliner:
            cmds.setAttr(obj + ".useOutlinerColor", 1)
            cmds.setAttr(obj + ".outlinerColor", rgb[0], rgb[1], rgb[2])

def ColorSetupTool():
    if cmds.window("ColorSetupTool", exists=True):
        cmds.deleteUI("ColorSetupTool")

    window = cmds.window("ColorSetupTool", title="ColorSetupTool",widthHeight=(210, 170),
                                sizeable=False,maximizeButton=False, minimizeButton=False,)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=8)
    cmds.rowLayout(numberOfColumns=3,columnAttach=[(2, "both", 40),])
    my_path =os.path.dirname(os.path.abspath(__file__))
    image_path = my_path.split("amiTools\\")[0]
    cmds.symbolButton(image=image_path + r"\amiTools\Image\amiIcon.png", w=30,h=30,
                        command=lambda *args:amiToolsLauncher.amiToolsLauncher())
    cmds.text(label="Color Setup",h=30, font="boldLabelFont")
    cmds.button(label="?", width=30, height=30, command=lambda *_:print("help"))
    cmds.setParent("..")
    cmds.separator(height=5)
    current_color = [0.5, 0.5, 0.5]  # 初期色
    cmds.rowLayout( numberOfColumns=2)
    apply_viewport_cb = cmds.checkBox(label="Viewport", value=True)
    apply_outliner_cb = cmds.checkBox(label="Outliner", value=True)
    cmds.setParent("..")
    def pick_color(*args):
        nonlocal current_color
        if cmds.colorEditor():
            rgb_str = cmds.colorEditor(query=True, rgb=True)
            current_color = list(map(float, rgb_str))
            cmds.button("ColorSetupToolcolorDisplay", edit=True, backgroundColor=current_color)

    def apply_color(*args):
        apply_viewport = cmds.checkBox(apply_viewport_cb, query=True, value=True)
        apply_outliner = cmds.checkBox(apply_outliner_cb, query=True, value=True)
        apply_color_to_selected(current_color, apply_viewport, apply_outliner)

    # 色選択表示ボタン
    cmds.button("ColorSetupToolcolorDisplay", label="select Color", backgroundColor=current_color, command=pick_color, height=40)

    # 実行ボタン
    cmds.button(label="Apply selecte objects", command=apply_color, height=40)

    cmds.showWindow(window)

