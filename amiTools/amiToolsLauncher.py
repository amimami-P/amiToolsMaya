#----------------------------------------------------------
# -*- coding: utf-8 -*-
"""amiToolsLauncher.py

git:https://github.com/amimami-P/amiToolsMaya.git

coding by amimami
MayaVer Maya2024

Ver　1.0

自前のツールをランチャーに追加したい場合はReadmeを見てください

"""
#----------------------------------------------------------
import os
import maya.cmds as cmds

def amiTL_show_help():
    if cmds.window("helpWindow", exists=True):
        cmds.deleteUI("helpWindow")

    cmds.window("helpWindow", title="amiToolsLauncher Help", widthHeight=(400, 200),
                sizeable=False, maximizeButton=False, minimizeButton=False)

    cmds.columnLayout(adjustableColumn=True)

    cmds.scrollField(editable=False, wordWrap=True,width=400, height=200,  text=
        """
ツールヘルプ\n

amiTools内のツールの呼び出しが出来ます\n

amiTools外のツール登録も可能ですので、必要な場合はReadmeを参照ください
        """
    )

    cmds.showWindow("helpWindow")

def allTabClose():
    for ch in cmds.columnLayout("amiToolsLauncherColumn", query=True, childArray=True):
        if ch.endswith("Frame"):
            cmds.frameLayout(ch, edit=True, collapse=True)

def amiToolsLauncher():
    """amiToolsLauncherUI
    """
    # スクリプト格納ディレクトリ
    my_path = os.path.dirname(os.path.abspath(__file__))

    folder_list = [file for file in os.listdir(my_path) if not "." in file]
    if "Image" in folder_list:
        folder_list.remove("Image")
    if "__pycache__" in folder_list:
        folder_list.remove("__pycache__")
    if cmds.workspaceControl("amiToolsLauncher", exists=True):
        cmds.deleteUI("amiToolsLauncher", control=True)

    cmds.workspaceControl(
        "amiToolsLauncher",
        label="ami Tools Launcher",
        floating=True,
        initialWidth=300,
        initialHeight=300 
    )

    form = cmds.formLayout("amiToolsLauncherMainForm", parent="amiToolsLauncher")

    header = cmds.columnLayout("amiToolsLauncherTopColumn", adjustableColumn=True, parent=form)
    cmds.rowLayout(numberOfColumns=3,
                columnAttach=[(1, "left", 0), (2, "left", 0), (3, "right", 0)],
                columnWidth=[(1, 100), (2, 170)])

    image_path = my_path.split("amiTools\\")[0]
    cmds.symbolButton(image=image_path + r"\Image\amiIcon.png", w=30, h=30)
    cmds.text(label="ami Tools Launcher", height=30, font="boldLabelFont")
    cmds.button(label="?", width=30, height=30, command=lambda *_: amiTL_show_help())

    cmds.setParent("..")
    cmds.separator(height=10)
    cmds.button(label="All Tab Close", command=lambda *args:allTabClose(), bgc=(0.15, 0.15, 0.15), parent=header,h=30)

    bgc_list = [[0.4, 0.1, 0.1], [0.1, 0.4, 0.1], [0.1, 0.1, 0.4],
                [0.4, 0.4, 0.1], [0.1, 0.4, 0.4], [0.4, 0.1, 0.4]]

    
    scroll = cmds.scrollLayout("amiToolsLauncherScroll", childResizable=True, parent=form)
    scroll_content = cmds.columnLayout("amiToolsLauncherColumn", adjustableColumn=True, parent=scroll)

    for index, folder in enumerate(folder_list):
        bgc_nam = index % len(bgc_list)
        frame = cmds.frameLayout("amiToolsLauncher" + folder + "Frame", label=folder, bgc=bgc_list[bgc_nam],
                                collapsable=True, collapse=True)

        folder_path = os.path.join(my_path, folder)
        for file in os.listdir(folder_path):
            if not file.endswith(".py"):
                Run_command = f"""import {folder}.{file}.{file} as {file}\n
from importlib import reload\nreload({file})\n{file}.{file}()"""
                btn = cmds.button(label=file, command=Run_command, parent=frame)
                cmds.popupMenu(parent=btn)
                print_command = f"#-------------------\n#{file}\n#-------------------\n" + Run_command
                cmds.menuItem(label="呼びたしコマンドをプリント", command=lambda _, cc=print_command:print(cc))
        cmds.setParent("..")
        cmds.separator(height=5)


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
