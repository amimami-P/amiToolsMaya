#------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------
import maya.cmds as cmds
import os
import amiToolsLauncher

def CheckJointRotate(checkJointList):
    result_list = []
    for jnt in checkJointList:
        try:
            rx = cmds.getAttr(jnt + ".rx")
            ry = cmds.getAttr(jnt + ".ry")
            rz = cmds.getAttr(jnt + ".rz")
        except:
            continue  # アトリビュート取得失敗時はスキップ
    
        # 極小値をゼロ扱い
        rx = 0 if abs(rx) < 1e-10 else rx
        ry = 0 if abs(ry) < 1e-10 else ry
        rz = 0 if abs(rz) < 1e-10 else rz
    
        if rx != 0 or ry != 0 or rz != 0:
            result_list.append(jnt)
    
    return result_list

def RotateReset(jointList):
    for i in jointList:
        try:
            cmds.setAttr(f"{i}.rx",0)
            cmds.setAttr(f"{i}.ry",0)
            cmds.setAttr(f"{i}.rz",0)
        except:
            cmds.warning(f"{i}のRotateを正しく初期化出来ませんでした")

def JointRotatecheckResultInfo(Allcheck=True):
    if Allcheck:
        checkJointList = cmds.ls(type="joint")
    else:
        checkJointList = cmds.ls(sl=True, type="joint")
        if not checkJointList:
            cmds.inViewMessage(
                smg="選択ジョイントが取得できませんでした",
                pos="topCenter",
                bkc=0x00000000,
                fadeStayTime=3000,
                fade=True,
            )
            return

    Result = CheckJointRotate(checkJointList)

    cmds.setParent("JointRotatecheckerColumn")
    
    # 既存のUIがあれば削除
    if cmds.control("JointRotatecheckerScroll", exists=True):
        cmds.deleteUI("JointRotatecheckerScroll", layout=True)

    # 結果表示用のスクロールレイアウト
    
    if not Result:
        cmds.text("JointRotatecheckerResult", e=True, label="回転値が入ったジョイントは見つかりませんでした")
        return
    else:
        cmds.text("JointRotatecheckerResult", e=True, label="Result")
        cmds.scrollLayout("JointRotatecheckerScroll", width=325, height=500)
        cmds.rowLayout(numberOfColumns=2)
        cmds.text(label="Joint\nSelect",h=30,w=200,)
        cmds.text(label="Rotate\nReset",h=30,w=100,)
        cmds.setParent("..")
        for jnt in Result:
                cmds.rowLayout(numberOfColumns=2)
                cmds.rowLayout(numberOfColumns=2)
                cmds.button(label=jnt, h=30, w=200, command=lambda _, j=jnt: cmds.select(j))
                cmds.button(label="Reset", h=30, w=100, command=lambda _, j=jnt:RotateReset([j]))

                cmds.setParent("JointRotatecheckerScroll")
        cmds.separator(height=5)
    if Result:
        cmds.setParent("JointRotatecheckerColumn")
        cmds.rowLayout(numberOfColumns=2)
        cmds.button(label="All　Select", h=30, w=200, command=lambda _,: cmds.select(Result))
        cmds.button(label="All　Reset", h=30, w=100, command=lambda _,: RotateReset(Result))
    cmds.setParent("JointRotatecheckerColumn")

    cmds.setParent("..")  

def JointRotatechecker():
    if cmds.window("JointRotatechecker", exists=True):
        cmds.deleteUI("JointRotatechecker")

    window = cmds.window("JointRotatechecker", title="JointRotatechecker", sizeable=False, maximizeButton=False, minimizeButton=False)
    cmds.columnLayout("JointRotatecheckerColumn", adjustableColumn=True)
    cmds.rowLayout(numberOfColumns=3,columnAttach=[(2, "both", 72),])
    my_path =os.path.dirname(os.path.abspath(__file__))
    image_path = my_path.split("amiTools\\")[0]
    cmds.symbolButton(image=image_path + r"\amiTools\Image\amiIcon.png", w=30,h=30,
                        command=lambda *args:amiToolsLauncher.amiToolsLauncher())
    cmds.text(label="JointRotatechecker",h=30, font="boldLabelFont")
    cmds.button(label="?", width=30, height=30, command=lambda *_:print("help"))
    cmds.setParent("..")
    cmds.rowLayout("JointRotatecheckerRow", numberOfColumns=3)
    cmds.button(label="選択ジョイントのみ", h=30, w=150, command=lambda *args: JointRotatecheckResultInfo(Allcheck=False))
    cmds.text("spacer", label=" ")
    cmds.button(label="シーン内ジョイント全て", h=30, w=150, command=lambda *args: JointRotatecheckResultInfo(Allcheck=True))
    cmds.setParent("..")

    cmds.separator(height=5)
    cmds.text("JointRotatecheckerResult", label="Rotateに値が入っているジョイントを検出できます", h=30)
    cmds.separator(height=5)

    cmds.showWindow(window)
