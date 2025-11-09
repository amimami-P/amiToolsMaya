#----------------------------------------------------------
# -*- coding: utf-8 -*-
"""
amimamiがJoint系のセットアップをするときに使うスクリプトを
雑にまとめたツール群です
"""
#----------------------------------------------------------
import os
import maya.cmds as cmds
import maya.mel as mel
import amiToolsLauncher
#---------------------------------------------------
def set_display_and_outliner_color(node, rgb):
    """表示色とアウトライナ色を設定"""
    # 表示色（Viewport Color）
    cmds.setAttr(node + ".overrideEnabled", 1)
    cmds.setAttr(node + ".overrideRGBColors", 1)
    cmds.setAttr(node + ".overrideColorRGB", rgb[0], rgb[1], rgb[2])

    # アウトライナ色
    cmds.setAttr(node + ".useOutlinerColor", 1)
    cmds.setAttr(node + ".outlinerColor", rgb[0], rgb[1], rgb[2])

def get_joint_depth_map(root_joint):
    """ジョイント階層を深さで分類"""
    depth_map = {}
    def traverse(joint, depth):
        if depth not in depth_map:
            depth_map[depth] = []
        depth_map[depth].append(joint)

        children = cmds.listRelatives(joint, type="joint", children=True) or []
        for child in children:
            traverse(child, depth + 1)

    traverse(root_joint, 0)
    return depth_map

def colorize_joint_hierarchy():
    selection = cmds.ls(selection=True, type="joint")
    if not selection:
        cmds.warning("ジョイントのルートを選択してください。")
        return

    root_joint = selection[0]

    # 階層ごとのジョイントを取得
    depth_map = get_joint_depth_map(root_joint)

    # 色を階層ごとにランダム or サンプルから設定
    sample_colors = [
        (1.0, 0.2, 0.2),   # 赤
        (0.2, 1.0, 0.2),   # 緑
        (0.2, 0.5, 1.0),   # 青
        (1.0, 1.0, 0.2),   # 黄色
        (1.0, 0.5, 1.0),   # ピンク
        (0.2, 1.0, 1.0),   # シアン
        (0.9, 0.4, 0.2),   # オレンジ
        (0.6, 0.2, 1.0),   # パープル
        (0.4, 1.0, 0.6),   # ミント
        (1.0, 0.8, 0.3),   # ゴールド
        (0.6, 0.6, 0.6),   # グレー
        (0.3, 0.8, 1.0),   # スカイブルー
    ]

    for i, depth in enumerate(sorted(depth_map.keys())):
        color = sample_colors[i % len(sample_colors)]
        for joint in depth_map[depth]:
            set_display_and_outliner_color(joint, color)

    print("階層ごとに色分け完了しました。")

#---------------------------------------------------

def toggle_joint_display(show=True):
    if cmds.ls(selection=True,type="joint"):
        cmds.select(cmds.ls(selection=True, type="joint")[0],hi=True)
        selected_joints = cmds.ls(selection=True, type="joint")
    else:
        selected_joints = cmds.ls(type="joint")
    for joint in selected_joints:
        cmds.setAttr(joint + ".displayLocalAxis", show)


def create_joint_at_vertex():
    selected_vertices = cmds.ls(selection=True, flatten=True)
    cmds.select(clear=True)
    if not selected_vertices:
        cmds.warning("Please select vertices.")
        return
    for vertex in selected_vertices:
        pos = cmds.pointPosition(vertex, world=True)
        joint = cmds.joint(position=pos)
        cmds.setAttr(joint + ".overrideEnabled", 1)
        cmds.setAttr(joint + ".overrideRGBColors", 0)  # インデックスカラーを使用
        cmds.setAttr(joint + ".overrideColor", 20)  # ピンク
        cmds.select(clear=True)
    print("Joint(s) created at selected vertex position(s).")


def reset_joint_orient():
    selected_joints = cmds.ls(selection=True, type="joint")
    if not selected_joints:
        cmds.warning("Please select a joint.")
        return
    for joint in selected_joints:
        cmds.setAttr(joint + ".jointOrientX", 0)
        cmds.setAttr(joint + ".jointOrientY", 0)
        cmds.setAttr(joint + ".jointOrientZ", 0)
    print("jointOrient attributes reset to 0.")

def toggle_joint_display(show):
    if cmds.ls(selection=True,type="joint"):
        cmds.select(cmds.ls(selection=True, type="joint")[0],hi=True)
        selected_joints = cmds.ls(selection=True, type="joint")
    else:
        selected_joints = cmds.ls(type="joint")
    for joint in selected_joints:
        cmds.setAttr(joint + ".displayLocalAxis", show)


def set_name_chain_joint():
    sel = cmds.ls(sl=True)
    setname = sel[0]
    for index,i in enumerate(sel):
        if not index == 0:
            num = index + 1
            cmds.rename(i,setname.replace("01","0" + str(num)))


def CreateLocater():
    sel = cmds.ls(sl=True)
    if sel:
        for i in sel:
            Lo =cmds.spaceLocator (name=i + "_locator")
            cmds.parent(Lo[0],i)
            cmds.setAttr(Lo[0] + ".translate",0,0,0)
            cmds.setAttr(Lo[0] + ".rotate",0,0,0)
            cmds.setAttr(Lo[0] + ".overrideEnabled",1)
            cmds.setAttr(Lo[0] + ".rotate",0,0,0)
            cmds.setAttr(Lo[0] + ".overrideColor", 20)

def ResetBindPose():
    try:
        cmds.delete(cmds.ls(type="dagPose"))
    except:
        pass
    selection = cmds.ls(sl=True,type="joint")[0]
    if not selection:
        cmds.warning("ジョイントのルートを選択してください。")
        return
    cmds.select(selection, hi=True)
    cmds.dagPose(cmds.ls(sl=True, type="joint"), s=True, bp=True)
    cmds.select(None)
    print("Reset Successfully!!!"),


def ShowCBJointOrient(Show):

    for jnt in cmds.ls(type="joint"):
        for axis in ["X", "Y", "Z"]:
            if Show ==True:
                cmds.setAttr(f"{jnt}.jointOrient{axis}", keyable=False, channelBox=True)
            else:
                cmds.setAttr(f"{jnt}.jointOrient{axis}", keyable=False, channelBox=False)


def RotateFreezeRun():
    cmds.undoInfo(openChunk=True)

    for jnt in cmds.ls(sl=True):
        if cmds.nodeType(jnt) == "joint":
            rot = cmds.xform( jnt, q = 1, worldSpace = 1, rotation = 1 )
            cmds.setAttr( jnt + '.jointOrient', 0, 0, 0, type = 'double3' )
            cmds.xform( jnt, worldSpace = 1, rotation = rot )
            newRot = cmds.xform( jnt, q = 1, objectSpace = 1, rotation = 1 )
            cmds.setAttr( jnt + '.jointOrient', newRot[0], newRot[1], newRot[2], type = 'double3' )
            cmds.setAttr( jnt + '.rotate', 0, 0, 0, type = 'double3' )

    cmds.undoInfo(closeChunk=True)

def orientJoint():
    setJoint = cmds.ls(sl=True)[0]
    parentNodes = cmds.listRelatives(setJoint, parent=True)
    cmds.parent(setJoint,world=True)
    mel.eval('joint -e  -oj xyz -secondaryAxisOrient yup -ch -zso;')
    cmds.parent(setJoint,parentNodes[0])

def JointTool():
    if cmds.window("jointTool", exists=True):
        cmds.deleteUI("jointTool")

    window = cmds.window("jointTool", title="Joint Tool", widthHeight=(280, 550), sizeable=False)

    cmds.columnLayout(adjustableColumn=True, rowSpacing=10)
    cmds.rowLayout(numberOfColumns=3,columnAttach=[(2, "both", 82),])
    my_path =os.path.dirname(os.path.abspath(__file__))
    image_path = my_path.split("amiTools\\")[0]
    cmds.symbolButton(image=image_path + r"\amiTools\Image\amiIcon.png", w=30,h=30,
                        command=lambda *args:amiToolsLauncher.amiToolsLauncher())
    cmds.text(label="Joint Tool",h=30, font="boldLabelFont")
    cmds.button(label="?", width=30, height=30, command=lambda *_:print("help"))
    cmds.setParent("..")
    # --- セクション: 基本ジョイント処理
    cmds.frameLayout(label="Joint Operations", collapsable=True, bgc=(0.15, 0.15, 0.15), labelAlign="center", marginWidth=5)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
    cmds.button(label="Create Joint at Vertex", height=30, command=lambda *args: create_joint_at_vertex())
    cmds.button(label="Create joint()", height=30, command=lambda *args: cmds.joint())
    cmds.button(label="Rotate Freeze", height=30, command=lambda *args: RotateFreezeRun())
    cmds.button(label="Reset Joint Orient", command=lambda *args: reset_joint_orient())
    cmds.button(label="orient Joint", command=lambda *args: orientJoint())
    
    cmds.setParent("..")  # frameLayout 終了
    cmds.setParent("..")
    # --- セクション: 表示切替
    cmds.frameLayout(label="Display Control", collapsable=True, bgc=(0.2, 0.2, 0.2), labelAlign="center", marginWidth=5)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
    cmds.button(label="Show Joint Axis", height=30, command=lambda *args: toggle_joint_display(True))
    cmds.button(label="Hide Joint Axis", height=30, command=lambda *args: toggle_joint_display(False))
    cmds.button(label="Show CB Orient", height=30, command=lambda *args: ShowCBJointOrient(True))
    cmds.button(label="Show CB Orient", height=30, command=lambda *args: ShowCBJointOrient(False))
    cmds.button(label="colorize joint hierarchy", height=30, command=lambda *args: colorize_joint_hierarchy())
    
    cmds.setParent("..")
    cmds.setParent("..")
    # --- セクション: 名前や補助機能
    cmds.frameLayout(label="Tools", collapsable=True, bgc=(0.18, 0.18, 0.18), labelAlign="center", marginWidth=5)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
    cmds.button(label="Set Name Chain", height=30, command=lambda *args: set_name_chain_joint())
    cmds.button(label="Create Locator", height=30, command=lambda *args: CreateLocater())
    cmds.button(label="Reset Bind Pose", height=30, command=lambda *args: ResetBindPose())
    cmds.setParent("..")

    cmds.setParent("..") 
    cmds.showWindow(window)


