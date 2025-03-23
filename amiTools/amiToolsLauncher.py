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

def amiToolsLauncher():
    """amiToolsLauncherUI
    """
    # スクリプト格納ディレクトリ
    my_path = os.path.dirname(os.path.abspath(__file__))

    folder_list = [file for file in os.listdir(my_path) if not "." in file]
    if "Image" in folder_list:
        folder_list.remove("Image")

    # 既存のウィンドウを削除
    if cmds.window("amiToolsLauncher", exists=True):
        cmds.deleteUI("amiToolsLauncher")

    # ウィンドウ作成
    window = cmds.window("amiToolsLauncher", title="amiToolsLauncher", widthHeight=(310, 500),
                        sizeable=False, maximizeButton=False, minimizeButton=False)

    cmds.columnLayout("topColumn", adjustableColumn=True)

    # ヘッダー部分
    cmds.rowLayout(numberOfColumns=3,
                columnAttach=[(1, "left", 0), (2, "left", 0), (3, "right", 0)],
                columnWidth=[(1, 100), (2, 170)])

    image_path = my_path.split("amiTools")[0]
    cmds.symbolButton(image=image_path + r"\amiTools\Image\amiIcon.png", w=30, h=30)
    cmds.text(label="ami Tools Launcher", height=30, font="boldLabelFont")
    cmds.button(label="?", width=30, height=30, command=lambda *_: amiTL_show_help())

    cmds.setParent("..")
    cmds.separator(height=20)

    # スクロールレイアウト
    cmds.scrollLayout("toolScroll", h=480)
    cmds.columnLayout(adjustableColumn=True)

    bgc_list = [[0.4, 0.1, 0.1], [0.1, 0.4, 0.1], [0.1, 0.1, 0.4],
                [0.4, 0.4, 0.1], [0.1, 0.4, 0.4], [0.4, 0.1, 0.4]]

    # フレーム作成
    for index, folder in enumerate(folder_list):
        bgc_nam = index % len(bgc_list)

        frame = cmds.frameLayout(folder + "Frame", label=folder, bgc=bgc_list[bgc_nam],
                                collapsable=True, collapse=True, width=300)

        folder_path = os.path.join(my_path, folder)
        for file in os.listdir(folder_path):
            if not file.endswith(".py"):
                command_test = f"import {folder}.{file}.{file} as {file}\nfrom importlib import reload\nreload({file})\n{file}.{file}()"
                cmds.button(label=file, command=command_test, parent=frame,w=50,h=30)

        cmds.setParent("..")
        cmds.separator(height=5)
    cmds.setParent("..")
    cmds.separator(height=20)
    cmds.showWindow(window)
