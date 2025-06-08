

# ------------------------------------------------------
# -*- coding: utf-8 -*-
# ------------------------------------------------------
"""ConstrainOperator.py

git:https://github.com/amimami-P/amiToolsMaya.git

coding by amimami
MayaVer Maya2024

Ver　1.0

"""
# ------------------------------------------------------
import maya.cmds as cmds
import os
import amiToolsLauncher
# ------------------------------------------------------
def constrain_blend_offset(target):
    talansFlag = True
    rotateFlag = True
    pb ="CoOp_pb_" + target
    if cmds.objExists("CoOp_pb_" + target) ==False:
        cmds.createNode("pairBlend", n=pb)
    elif cmds.objExists("CoOp_pb_" + target):
        if cmds.listConnections(pb + ".inTranslateX2", plugs=True):
            talansFlag = False
        if  cmds.listConnections(pb + ".inRotateX2", plugs=True):
            rotateFlag = False

    if talansFlag:
        for axis in ['X', 'Y', 'Z']:
            attr = "translate" + axis
            conn = cmds.listConnections(target + "." + attr, source=True, destination=False, plugs=True)
            if conn:
                if"CoOp_" in conn[0]:
                    cmds.disconnectAttr(conn[0], target + "." + attr)
                    # Target側のOffset代わり
                    cmds.setAttr(pb + ".inTranslate" + axis + "1",cmds.getAttr(target + "." + attr))
                    cmds.connectAttr(conn[0], pb + ".inTranslate" + axis + "2")
                    cmds.connectAttr(pb + ".outTranslate" + axis, target + "." + attr)
    if rotateFlag :
        for axis in ['X', 'Y', 'Z']:
            attr = "rotate" + axis
            conn = cmds.listConnections(target + "." + attr, source=True, destination=False, plugs=True)
            if conn:
                if"CoOp_" in conn[0]:
                    cmds.disconnectAttr(conn[0], target + "." + attr)
                    cmds.connectAttr(conn[0], pb + ".inRotate" + axis + "2")
                    cmds.connectAttr(pb + ".outRotate" + axis, target + "." + attr)
        cmds.setAttr(pb + ".weight", 1.0)
    return pb

def create_locator_Center(attrLock,spaceNode=True):
    """選択したオブジェクトの中心にスケール指定のロケーターを作成"""
    select_list = cmds.ls(selection=True,)
    if cmds.objExists("PosLocatorGrp") == False:
        cmds.createNode("transform",name="PosLocatorGrp")
        cmds.setAttr("PosLocatorGrp.useOutlinerColor", 1)
        cmds.setAttr("PosLocatorGrp.outlinerColor",0.0, 1.0, 1.0)
    scale = cmds.floatSliderGrp("LocatorScale", query=True, value=True)

    
    if not select_list:
        cmds.warning("オブジェクトを選択してください！")
        return
    total_position = [0.0, 0.0, 0.0]
    for obj in select_list:
        position = cmds.xform(obj, query=True, worldSpace=True, translation=True)
        total_position[0] += position[0]
        total_position[1] += position[1]
        total_position[2] += position[2]
    # 平均位置を計算
    num_objects = len(select_list)
    center_position = [coord / num_objects for coord in total_position]
    print (center_position)
    # 中心位置にロケーターを作成
    locator = cmds.spaceLocator()[0]
    cmds.setAttr(locator + ".rotateOrder",cb=True,lock=True)
    cmds.setAttr(locator + ".scale",lock=True)
    cmds.setAttr(locator + ".v",lock=True)
    cmds.xform(locator, worldSpace=True, translation=center_position)
    # localScale を設定
    locator_shape = cmds.listRelatives(locator, shapes=True)[0]
    cmds.setAttr(locator_shape + ".localScaleX", scale)
    cmds.setAttr(locator_shape + ".localScaleY", scale)
    cmds.setAttr(locator_shape + ".localScaleZ", scale)
    cmds.parent(locator,"PosLocatorGrp")

    if spaceNode ==True:
        sp=cmds.createNode("transform",n=locator + "Space")
        cmds.parent(sp,locator)
        cmds.setAttr(sp + ".translate",0,0,0)
        cmds.setAttr(sp + ".rotate",0,0,0)
        cmds.setAttr(sp + ".scale",1,1,1)
        cmds.parent(sp,"PosLocatorGrp")
        cmds.parent(locator,sp)
    try:
        cmds.setAttr(locator + "." + attrLock,lock=True)
    except:
        pass

def copy_animation(source_node,target_node):


    attrs = ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"]

    for attr in attrs:
        source_attr = f"{source_node}.{attr}"
        target_attr = f"{target_node}.{attr}"
        anim_curve = cmds.listConnections(source_attr, type="animCurve", destination=False)

        if anim_curve:
            cmds.copyKey(source_attr)
            cmds.pasteKey(target_attr, option="replaceCompletely")

def FirstAll_CreateLocater(attrLock,FirstAll=True,spaceNode=True,):
    """

    Args:
        attrLock (string) : ロックをかけるアドリビュート
        FirstAll (ターゲットの判定): Trueで最初に選択したもの　/　Falseで全て
        spaceNode(スペースノードの有無): True作る
    Returns:
        list: 作ったLocatorをリストで返す
    """
    scale = cmds.floatSliderGrp("LocatorScale", query=True, value=True)
    if FirstAll == True:
        sel_list = [cmds.ls(sl=True)[0]]
    elif FirstAll == False:
        sel_list = cmds.ls(sl=True)


    if cmds.objExists("PosLocatorGrp") == False:
        cmds.createNode("transform",name="PosLocatorGrp")
        cmds.setAttr("PosLocatorGrp.useOutlinerColor", 1)
        cmds.setAttr("PosLocatorGrp.outlinerColor",0.0, 1.0, 1.0)
    Lo_List = []

    if sel_list:
        for sel in sel_list:
            count = 1
            while True:
                if  cmds.objExists(sel + "_locator_"+ str(count)) == False:
                    Lo =cmds.spaceLocator(name=sel + "_locator_"+ str(count))
                    cmds.setAttr(Lo[0] + ".rotateOrder",cb=True,lock=True)
                    cmds.setAttr(Lo[0] + ".scale",lock=True)
                    cmds.setAttr(Lo[0] + ".v",lock=True)

                    break
                else:
                    count = count + 1
            cmds.parent(Lo[0],sel)
            cmds.setAttr(Lo[0] + ".translate",0,0,0)
            cmds.setAttr(Lo[0] + ".rotate",0,0,0)
            cmds.setAttr(Lo[0] + ".overrideEnabled",1)
            cmds.setAttr(Lo[0] + ".rotate",0,0,0)
            cmds.setAttr(Lo[0] + ".overrideColor", 20)
            cmds.setAttr(Lo[0]+"Shape.localScaleX",scale)
            cmds.setAttr(Lo[0]+"Shape.localScaleY",scale)
            cmds.setAttr(Lo[0]+"Shape.localScaleZ",scale)
            cmds.parent(Lo,"PosLocatorGrp")
            Lo_List.append(Lo[0])
    if spaceNode == True:
        for i in Lo_List:
            sp=cmds.createNode("transform",n=i + "Space")
            cmds.parent(sp,i)
            cmds.setAttr(sp + ".translate",0,0,0)
            cmds.setAttr(sp + ".rotate",0,0,0)
            cmds.setAttr(sp + ".scale",1,1,1)
            cmds.parent(sp,"PosLocatorGrp")
            cmds.parent(i,sp)
    for i in Lo_List:
        if attrLock:
            cmds.setAttr(Lo[0] + "." + attrLock,lock=True)
    return Lo_List

def CreateLocater(attrLock):

    Locator_Pos_Flug = cmds.radioButtonGrp("LocatorPosition_Ui", query=True, select=True)
    space_node = cmds.checkBox("space_create_flug", query=True, value=True)
    if Locator_Pos_Flug == 1:
        FirstAll_CreateLocater(attrLock,FirstAll=True,spaceNode=space_node)
    elif Locator_Pos_Flug == 2:
        create_locator_Center(attrLock,spaceNode=space_node)
    elif Locator_Pos_Flug == 3:
        FirstAll_CreateLocater(attrLock,FirstAll=False,spaceNode=space_node)

def Constrain_Run(parent =False,point=False,orient=False):

    source_node = cmds.textField("SlectNodeField", query=True,text=True)
    target_node = cmds.ls(sl=True)
    try:
        target_node.remove(source_node)
    except:
        pass
    offset = cmds.checkBox("const_offset_flug", query=True, value=True)
    constCheck = True
    for target in target_node:
        if parent == True:
            # 回転のロック状態を取得
            locked_rot_axes = []
            for axis in ["x", "y", "z"]:
                attr = f"{target}.rotate{axis.upper()}"
                if cmds.getAttr(attr, lock=True):
                    locked_rot_axes.append(axis)
            if not cmds.listConnections(target, type='parentConstraint', source=True, destination=False):
            # ロックされている回転軸をスキップ
                PaCo = cmds.parentConstraint(source_node, target, maintainOffset=offset, skipRotate=locked_rot_axes)[0]

                cmds.rename(PaCo,"CoOp_" + PaCo)
                constrain_blend_offset(target)
            else:
                constCheck = False
        elif point == True:
            if not cmds.listConnections(target, type='pointConstraint', source=True, destination=False):
                PoCo =  cmds.pointConstraint(source_node,target,mo=offset)[0]
                cmds.rename(PoCo,"CoOp_" + PoCo)
                constrain_blend_offset(target)
            else:

                constCheck = False
        elif orient == True:
            if not cmds.listConnections(target, type='orientConstraint', source=True, destination=False):
                oriCo = cmds.orientConstraint(source_node,target,mo=offset)[0]
                cmds.rename(oriCo,"CoOp_" + oriCo)
                constrain_blend_offset(target)
            else:
                constCheck = False
    if constCheck ==False:
        cmds.inViewMessage(
            smg=(u"このツールはコンストレインの重ね掛けには対応していません"),
            pos="topCenter",
            bkc=0x00000000,
            fadeStayTime=3000,
            fade=True,
            )
    Const_Info_Ui()
    cmds.select(target_node)
    cmds.setFocus("")

def ResetUiValue():
    """選択ノード表示更新
    """
    if cmds.checkBox("selectLock", query=True, value=True)==True:
        Const_Info_Ui()
        return
    selectedNodes = cmds.ls(selection=True)
    if not selectedNodes:
        cmds.textField("SlectNodeField", edit=True, text="None...")
    else:
        cmds.textField("SlectNodeField", edit=True, text=selectedNodes[0])
    Const_Info_Ui()
    cmds.setFocus("")

def constrain_Act(ConstrainNamne):


    if cmds.checkBox("bake_flug",q=True ,value=True,)==True:
        start_frame = cmds.playbackOptions(query=True, minTime=True)
        end_frame = cmds.playbackOptions(query=True, maxTime=True)
        bake_target =ConstrainNamne.rsplit("_", 1)[0].split("CoOp_")[-1]
        attr_list = ["tx","ty","tz","rx","ry","rz"]
        for attr in attr_list:
            if cmds.getAttr(bake_target + "." + attr, lock=True):
                attr_list.remove(attr)
        cmds.select(clear=True)
        cmds.select(bake_target)
        cmds.bakeResults(
            simulation=True,
            time=(start_frame, end_frame),
            sampleBy=1,
            oversamplingRate=1,
            disableImplicitControl=True,
            preserveOutsideKeys=True,
            sparseAnimCurveBake=False,
            removeBakedAttributeFromLayer=False,
            removeBakedAnimFromLayer=False,
            bakeOnOverrideLayer=False,
            minimizeRotation=True,
            attribute=attr_list
            )
    cmds.delete(ConstrainNamne)
    Const_Info_Ui()
    cmds.setFocus("")

def transfer_animation():

    Option = cmds.radioButtonGrp("Animation_Copy_Option_Ui", query=True, select=True)
    if Option == 1:
        mode="copy"
    elif Option == 2:
        mode="smartBake"
    elif Option == 3:
        mode="fullBake"
    print (Option)
    source_node = cmds.textField("SlectNodeField", query=True,text=True)
    target_node_list = cmds.ls(sl=True)
    try:
        target_node_list.remove(source_node)
    except:
        pass
    print (target_node_list)
    for target_node in target_node_list:
        if mode == "copy":
            copy_flig = True
            parentNodes = cmds.listRelatives(target_node, parent=True)[0]
            if not parentNodes.endswith("Space"):
                result = cmds.confirmDialog(
                title='Confirmation',
                message=u'ターゲットにスペースノードがないようです\n\nコピーしても同じ動きにならないかもです\nコピーしますか？\n',
                button=['OK', 'Cancel'],
                defaultButton='OK',
                cancelButton='Cancel',
                dismissString='Cancel'
                )
                if result == 'Cancel':
                    copy_flig = False
            if copy_flig == True:
                attrs = [
                        "translateX", "translateY", "translateZ", 
                        "rotateX", "rotateY", "rotateZ"
                        ]

                for attr in attrs:
                    source_attr = source_node + "." + attr
                    target_attr = target_node + "." + attr
                    anim_curve = cmds.listConnections(source_attr, type="animCurve", destination=False)

                    if anim_curve:
                        cmds.copyKey(source_attr)
                        cmds.pasteKey(target_attr, option="replaceCompletely")

        if "Bake" in mode :
            locked_rot_axes = []
            for axis in ["x", "y", "z"]:
                attr = f"{target_node}.rotate{axis.upper()}"
                if cmds.getAttr(attr, lock=True):
                    locked_rot_axes.append(axis)
            # ロックされている回転軸をスキップ
            PaCo = cmds.parentConstraint(source_node, target_node, maintainOffset=False, skipRotate=locked_rot_axes)[0]

            attr_list = ["tx","ty","tz","rx","ry","rz"]
            for attr in attr_list:
                if cmds.getAttr(target_node + "." + attr, lock=True):
                    attr_list.remove(attr)
            start_frame = cmds.playbackOptions(query=True, minTime=True)
            end_frame = cmds.playbackOptions(query=True, maxTime=True)
            if mode == "smartBake":
                cmds.bakeResults(
                    [target_node],
                    simulation=True,
                    time=(start_frame, end_frame),
                    smart=True,
                    disableImplicitControl=True,
                    preserveOutsideKeys=True,
                    sparseAnimCurveBake=False,
                    removeBakedAttributeFromLayer=False,
                    removeBakedAnimFromLayer=False,
                    bakeOnOverrideLayer=False,
                    minimizeRotation=True,
                    controlPoints=False,
                    attribute=attr_list)
            if mode == "fullBake":\
                cmds.bakeResults(
                    [target_node],
                    time=(start_frame, end_frame),
                    sampleBy=1,
                    oversamplingRate=1,
                    disableImplicitControl=True,
                    preserveOutsideKeys=True,
                    sparseAnimCurveBake=False,
                    removeBakedAttributeFromLayer=False,
                    removeBakedAnimFromLayer=False,
                    bakeOnOverrideLayer=False,
                    minimizeRotation=True,
                    attribute=attr_list
                    )
            cmds.delete(PaCo)

def select_const_list(parent =False,point=False,orient=False):
    source_node = cmds.textField("SlectNodeField", query=True,text=True)
    source_node = cmds.textField("SlectNodeField", query=True,text=True)

    connected_nodes = cmds.listConnections(source_node + ".parentMatrix" )
    parentConstraint_list = []
    orientConstraint_list = []
    pointConstraint_list = []
    all_constrain_flug = cmds.checkBox("all_constrain_flug", q=True,value=False,)
    cmds.setFocus("")

    if connected_nodes:
        for node in connected_nodes:
            if cmds.nodeType(node) == "parentConstraint":
                parentConstraint_list.append(node)
            elif cmds.nodeType(node) == "pointConstraint":
                pointConstraint_list.append(node)
            elif cmds.nodeType(node) == "orientConstraint":
                orientConstraint_list.append(node)
    if all_constrain_flug == True:
        parentConstraint_list = [paCo for paCo in parentConstraint_list if paCo.startswith("CoOp_")]
        pointConstraint_list = [opCo for opCo in pointConstraint_list if opCo.startswith("CoOp_")]
        orientConstraint_list = [orCo for orCo in orientConstraint_list if orCo.startswith("CoOp_")]


    if parent ==True:
        cmds.select([Constraint.rsplit("_", 1)[0].split("CoOp_")[-1] for Constraint in parentConstraint_list])
    elif orient ==True:
        cmds.select([Constraint.rsplit("_", 1)[0].split("CoOp_")[-1] for Constraint in orientConstraint_list])
    elif point ==True:
        cmds.select([Constraint.rsplit("_", 1)[0].split("CoOp_")[-1] for Constraint in pointConstraint_list])


def list_all_run(parent =False,point=False,orient=False):
    source_node = cmds.textField("SlectNodeField", query=True,text=True)

    connected_nodes = cmds.listConnections(source_node + ".parentMatrix" )
    parentConstraint_list = []
    orientConstraint_list = []
    pointConstraint_list = []
    all_constrain_flug = cmds.checkBox("all_constrain_flug", q=True,value=False,)
    cmds.setFocus("")

    if connected_nodes:
        for node in connected_nodes:
            if cmds.nodeType(node) == "parentConstraint":
                parentConstraint_list.append(node)
            elif cmds.nodeType(node) == "pointConstraint":
                pointConstraint_list.append(node)
            elif cmds.nodeType(node) == "orientConstraint":
                orientConstraint_list.append(node)
    if all_constrain_flug == True:
        parentConstraint_list = [paCo for paCo in parentConstraint_list if paCo.startswith("CoOp_")]
        pointConstraint_list = [opCo for opCo in pointConstraint_list if opCo.startswith("CoOp_")]
        orientConstraint_list = [orCo for orCo in orientConstraint_list if orCo.startswith("CoOp_")]



    if parent ==True:
        for i in parentConstraint_list:
            constrain_Act(i)
    elif orient ==True:
        for i in orientConstraint_list:
            constrain_Act(i)
    elif point ==True:
        for i in pointConstraint_list:
            constrain_Act(i)

def set_constrain_weight(name,value):

    cmds.setAttr("CoOp_pb_" + name.rsplit("_", 1)[0].split("CoOp_")[-1] + ".weight" ,value)
    print("CoOp_pb_" + name.rsplit("_", 1)[0].split("CoOp_")[-1] + ".weight" )
    cmds.setKeyframe("CoOp_pb_" + name.rsplit("_", 1)[0].split("CoOp_")[-1] + ".weight" )
    cmds.setFocus("")

def CO_show_help():
    if cmds.window("helpWindow", exists=True):
        cmds.deleteUI("helpWindow")

    cmds.window("helpWindow", title="ConstrainOperator Help", widthHeight=(400, 800), sizeable=True)

    cmds.columnLayout(adjustableColumn=True)

    cmds.scrollField(editable=False, wordWrap=True,width=400, height=800,  text=
        """
        ツールヘルプ\n

        できること\n

        1. ロケータの作成\n
        1. 選択ノードのコンストレイン管理 (リスト表示されます)\n
        1. 新規コンストレイン作成 / 削除 / ベイク\n
        1. コンストレイン先のコントローラーベイク (ベイク範囲はプレイバック範囲)\n
        1. アニメーションのコピペ\n
        \n
    --------------------------------------------------------------------------
        ● SelesetNnode\n
            ● 選択したノードが自動入力されます。ここに入っているノードがコンストレインのソースになります。\n
                ● Lockにチェックすることで入力を固定できます。\n

        ● locatorScale\n
            ● このツールで作るlocatorの大きさを変えられます\n
        ● locator Option\n
            ● SelesetFirst\n
                ● 最初に選択したノードの位置にロケータを作ります。\n
            ● Center\n
                ● 複数選択したノードの中心にロケータを作ります。\n
            ● SelesetAll\n
                ● 選択したノードすべてを対象に同座標にロケータを作ります\n
            \n
        ● OnSpace\n
            ● チェックを入れるとロケータにスペースノードをつけてアトリビュートを初期値を0にした状態にできます。\n
        ● Createlocator\n
            ● 普通のlロケータを作ります\n
        ● Trans Lock\n
            ● Teanslateのアトリビュートをロックしたロケータを作ります\n
        ● Rot Lock\n
            ● Rotateのアトリビュートをロックしたロケータを作ります\n
        \n
        ● Offset\n
            ● チェックを入れておくとオフセットありでコンストレインできます。(デフォルトOn)\n
        ● Bale\n
            ● 後述するボタンの機能を削除からベイクに変更することができます。\n
        \n\n
        ● parent\n
            ● SelesetNnode内のノードをソースにペアレントコントストレインを実行します\n
        ● Point\n
            ● SelesetNnode内のノードをソースにポイントコントストレインを実行します\n
        ● Orient\n
            ● SelesetNnode内のノードをソースにオリエントコントストレインを実行します\n
        \n
        ● non-tool constrain\n
            ● ConstrainOperatorで作られたコンストレイン以外もツールに表示するかどうか\n
                ● offにするとConstrainOperatorで作られたコンストレイン以外もツールに表示します\n
        ● 真ん中のボタン\n
            ● 選択したノードがコンストレインしているノードがボタンになります。\n
                ● 押すとコンストレインを削除\n
            ● Bakeのチェックボックスにチェックでベイクした後にコンストレインを削除\n
        ● ボタン下スライダー\n
            ● コンストレインのウェイトを設定できます\n
            ● 値が変更されたフレームに自動でセットキーもします\n
        ● List Select\n
            ● リスト内のノードをまとめて選択\n
        ● List All Run\n
            ● リスト内のノードのコンストレインをまとめて削除\n
                ● Bakeチェックも機能します\n
        \n
        ● Animation Copy\n
            ● Copy\n
                ● アニメーションのコピペをします。スペースノード付きのロケータでないと同じ動きはしないかもです\n
            ● smartBake\n
                ● スマートベイクします\n
            ● Bake\n
                ● フルベイクします\n
            """
    )

    cmds.showWindow("helpWindow")



def Const_Info_Ui():
    """UIのリロード処理"""

    source_node = cmds.textField("SlectNodeField", query=True,text=True)
    if source_node == "None...":
        connected_nodes = []
    else:
        try:
            connected_nodes = cmds.listConnections(source_node + ".parentMatrix" )
        except:
            return
    parentConstraint_list = []
    orientConstraint_list = []
    pointConstraint_list = []
    all_constrain_flug = cmds.checkBox("all_constrain_flug", q=True,value=True,)


    if connected_nodes:
        for node in connected_nodes:
            if cmds.nodeType(node) == "parentConstraint":
                parentConstraint_list.append(node)
            elif cmds.nodeType(node) == "pointConstraint":
                pointConstraint_list.append(node)
            elif cmds.nodeType(node) == "orientConstraint":
                orientConstraint_list.append(node)
    if all_constrain_flug == True:
            parentConstraint_list = [paCo for paCo in parentConstraint_list if paCo.startswith("CoOp_")]
            pointConstraint_list = [opCo for opCo in pointConstraint_list if opCo.startswith("CoOp_")]
            orientConstraint_list = [orCo for orCo in orientConstraint_list if orCo.startswith("CoOp_")]

    if cmds.control("parentScroll", exists=True):
        cmds.deleteUI("parentScroll", layout=True)

    if cmds.control("pointScroll", exists=True):
        cmds.deleteUI("pointScroll", layout=True)

    if cmds.control("orientScroll", exists=True):
        cmds.deleteUI("orientScroll", layout=True)

    # レイアウトを親に設定し直してから再作成
    cmds.setParent("constInfoUI")

    # parentScroll
    scroll_layout1 = cmds.scrollLayout("parentScroll",
                                    horizontalScrollBarThickness=20,
                                    verticalScrollBarThickness=20, width=130, height=200
                                    )
    
    cmds.columnLayout("parentScroll_mid")
    if parentConstraint_list:
        for i in parentConstraint_list:
            label_name = i.split("_parentConstraint")[0].split("CoOp_")[-1]
            cmds.columnLayout()

            # ボタン
            cmds.button(label=label_name, width=135, command=lambda _, name=i: constrain_Act(name))
            Slider_value = cmds.getAttr("CoOp_pb_" + i.rsplit("_", 1)[0].split("CoOp_")[-1] + ".weight")
            connections = cmds.listConnections("CoOp_pb_" + i.rsplit("_", 1)[0].split("CoOp_")[-1] + ".weight", source=True, destination=False)
            if bool(connections) ==True: # 接続があれば True、なければ False
                cmds.floatSliderGrp(field=True, minValue=0, maxValue=1,step=0.01, value=Slider_value,bgc=(0.5,0.35,0.35),
                                    width=120, columnWidth=[(1, 40), (2, 80)], columnAlign=[(1, "left")],
                                    changeCommand=lambda value, name=i: set_constrain_weight(name,value))
            else:
                cmds.floatSliderGrp(field=True, minValue=0, maxValue=1,step=0.01, value=Slider_value,
                                    width=120, columnWidth=[(1, 40), (2, 80)], columnAlign=[(1, "left")],
                                    changeCommand=lambda value, name=i: set_constrain_weight(name,value))
        cmds.setParent("parentScroll_mid")

    cmds.setParent("..")
    cmds.setParent("..")

    # pointScroll
    scroll_layout2 = cmds.scrollLayout("pointScroll",
                                        horizontalScrollBarThickness=20,
                                        verticalScrollBarThickness=20, width=150, height=200
                                        )
    cmds.columnLayout("pointScroll_mid" )
    if pointConstraint_list:
        for i in pointConstraint_list:
            label_name = i.split("_pointConstraint")[0].split("CoOp_")[-1]
            cmds.columnLayout()

            # ボタン
            cmds.button(label=label_name, width=135, command=lambda _, name=i: constrain_Act(name))
            Slider_value = cmds.getAttr("CoOp_pb_" + i.rsplit("_", 1)[0].split("CoOp_")[-1] + ".weight")
            connections = cmds.listConnections("CoOp_pb_" + i.rsplit("_", 1)[0].split("CoOp_")[-1] + ".weight", source=True, destination=False)
            if bool(connections) ==True: # 接続があれば True、なければ False
                cmds.floatSliderGrp(field=True, minValue=0, maxValue=1,step=0.01, value=Slider_value,bgc=(0.5,0.3,0.3),
                                    width=120, columnWidth=[(1, 40), (2, 80)], columnAlign=[(1, "left")],
                                    changeCommand=lambda value, name=i: set_constrain_weight(name,value))
            else:
                cmds.floatSliderGrp(field=True, minValue=0, maxValue=1,step=0.01, value=Slider_value,
                                    width=120, columnWidth=[(1, 40), (2, 80)], columnAlign=[(1, "left")],
                                    changeCommand=lambda value, name=i: set_constrain_weight(name,value))
        cmds.setParent("pointScroll_mid")
    cmds.setParent("..")  
    cmds.setParent("..")

    # orientScroll
    scroll_layout3 = cmds.scrollLayout("orientScroll",
                                        horizontalScrollBarThickness=20,
                                        verticalScrollBarThickness=20, width=150, height=200
                                        )
    cmds.columnLayout("orientScroll_mid" )
    if orientConstraint_list:
        for i in orientConstraint_list:
            label_name = i.split("_orientConstraint")[0].split("CoOp_")[-1]
            cmds.columnLayout()

            # ボタン
            cmds.button(label=label_name, width=135, command=lambda _, name=i: constrain_Act(name))
            Slider_value = cmds.getAttr("CoOp_pb_" + i.rsplit("_", 1)[0].split("CoOp_")[-1] + ".weight")
            connections = cmds.listConnections("CoOp_pb_" + i.rsplit("_", 1)[0].split("CoOp_")[-1] + ".weight", source=True, destination=False)
            if bool(connections) ==True: # 接続があれば True、なければ False
                cmds.floatSliderGrp(field=True, minValue=0, maxValue=1,step=0.01, value=Slider_value,bgc=(0.5,0.3,0.3),
                                    width=120, columnWidth=[(1, 40), (2, 80)], columnAlign=[(1, "left")],
                                    changeCommand=lambda value, name=i: set_constrain_weight(name,value))
            else:
                cmds.floatSliderGrp(field=True, minValue=0, maxValue=1,step=0.01, value=Slider_value,
                                    width=120, columnWidth=[(1, 40), (2, 80)], columnAlign=[(1, "left")],
                                    changeCommand=lambda value, name=i: set_constrain_weight(name,value))
        cmds.setParent("orientScroll_mid") 
    cmds.setParent("..") 
    cmds.setParent("..") 
    cmds.setParent("..")
# ----------------------------------------------------------------------------------------
    # main
# -----------------------------------------------------------------------------------------
def ConstrainOperator():
    """MeinUI
    """
    if cmds.window("ConstrainOperator", exists=True):
        cmds.deleteUI("ConstrainOperator", window=True)

    window = cmds.window("ConstrainOperator", title="Constrain Operator", sizeable=False,
                            maximizeButton=False, minimizeButton=False,)

    cmds.columnLayout("CO_Ui_main", adjustableColumn=True)
    cmds.rowLayout(numberOfColumns=3,
            columnAttach=[(1, "left", 0),(2, "left", 0), (3, "right", 0)],
            columnWidth=[(1, 160), (2, 100), (3, 160)])
    my_path =os.path.dirname(os.path.abspath(__file__))
    image_path = my_path.split("amiTools\\")[0]
    cmds.symbolButton(image=image_path + r"\amiTools\Image\amiIcon.png", w=30,h=30,
                        command=lambda *args:amiToolsLauncher.amiToolsLauncher())
    cmds.text(label="Constrain Operator", height=30, font="boldLabelFont")
    cmds.button(label="?", width=30, height=30, command=lambda *_: CO_show_help())
    cmds.setParent("..")

    titleRow = cmds.rowLayout(numberOfColumns=4, columnWidth=[(1, 40)])
    cmds.text(label=" ", font="boldLabelFont")
    cmds.text(label="SelectNode :", font="boldLabelFont")
    sel_node = cmds.ls(sl=True)
    if sel_node :
        SlectNodeField_text = sel_node[0]
    else:
        SlectNodeField_text = "None..."
    cmds.textField("SlectNodeField", w=250, height=30,
                    editable=False, text=SlectNodeField_text, backgroundColor=(0.2, 0.2, 0.2))
    cmds.checkBox("selectLock", label="Lock", value=False,)
    cmds.setParent('..')

    separator = cmds.separator(style="in", height=20)
    cmds.setParent('..')
    cmds.frameLayout("LocatorFrame",label="Locator Create", collapsable=True, collapse=True, marginWidth=20)
    AttrRow = cmds.rowLayout(numberOfColumns=3, columnWidth=[
                            (1, 80), (2, 65), (3, 10)])
    slider = cmds.floatSliderGrp("LocatorScale",
                                label="LocatorScale",
                                field=True,
                                minValue=0,
                                maxValue=100,
                                value=20,
                                width=380,
                                columnWidth=[(1, 70)],
                                columnAlign=[(1, "left")],
                                )
    cmds.setParent('LocatorFrame')
    separator = cmds.separator(style="in", height=20)
    cmds.setParent('LocatorFrame')

    lotRow = cmds.rowLayout(numberOfColumns=2,columnWidth=[(1,80),(2, 150), ])

    cmds.text(label="Locator Option")
    cmds.radioButtonGrp("LocatorPosition_Ui",
                        numberOfRadioButtons=3,
                        labelArray3=["SelectFirst", "Center", "SelectAll"],
                        select=1,
                        )
    cmds.setParent('LocatorFrame')
    separator = cmds.separator(style="in", height=10)
    cmds.setParent('LocatorFrame')
    exRow = cmds.rowLayout(numberOfColumns=5,columnWidth=[(1, 80),(2, 80), ])

    cmds.checkBox("space_create_flug", label="OnSpace", value=False,)
    cmds.button(label="CreateLocator", width=100,
                command=lambda _: CreateLocater(""))
    cmds.button(label="Trans Lock", width=100,
                command=lambda _: CreateLocater("translate"))
    cmds.button(label="Rot Lock", width=100,
                command=lambda _: CreateLocater("rotate"))
    
    cmds.setParent('LocatorFrame')
    separator = cmds.separator(style="in", height=20)
    cmds.setParent('..')

    const_offset_row = cmds.rowLayout(numberOfColumns=4,columnWidth=[(1,125),(2, 150), ])
    cmds.text(label= "        ")
    cmds.checkBox("const_offset_flug", label="Offset", value=True,)
    cmds.checkBox("bake_flug", label="Bake", value=False,)
    cmds.setParent('..')
    const_run_Row = cmds.rowLayout(numberOfColumns=3,columnAttach=[(1, "both", 10),(2, "both", 40),(3, "both", 10)])
    cmds.button(label="parent", width=100,bgc=(0.8, 0.3, 0.3),
                command=lambda _: Constrain_Run(parent=True))
    cmds.button(label="point", width=100,bgc=(0.4, 0.8, 0.4),
                command=lambda _: Constrain_Run(point=True))
    cmds.button(label="orient", width=100,bgc=(0.4, 0.4, 0.8),
                command=lambda _: Constrain_Run(orient=True))
    cmds.setParent('..')
    separator = cmds.separator(style="in", height=20)
    cmds.setParent('..')
    exRow = cmds.rowLayout(adjustableColumn=True,numberOfColumns=3, columnAttach=[(1, "both", 50)])

    cmds.checkBox("all_constrain_flug", label="non-tool constrain",
                    value=True,onCommand=lambda _:Const_Info_Ui(), offCommand=lambda _:Const_Info_Ui())
    cmds.setParent('..')

    #-------------------------------------------------------------------------------
    # コンストレインInfo
    #--------------------------------------------------------------------------------
    InfoRow = cmds.rowLayout(numberOfColumns=4, columnWidth=[
                                (1, 40), (2, 150), (3, 150)])
    cmds.text(label=" ", h=30, font="boldLabelFont")
    cmds.text(label="parent", h=30, font="boldLabelFont")
    cmds.text(label="point", h=30, font="boldLabelFont")
    cmds.text(label="orient", h=30, font="boldLabelFont")
    cmds.setParent('..')

    #-------------------------------------------------------------------------------
    cmds.rowLayout("constInfoUI",numberOfColumns=3,columnWidth=[
                                    (1, 60), (2, 65), (3, 10)])

    Const_Info_Ui()
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    #-------------------------------------------------------------------------------


    ListSelectRow = cmds.rowLayout(numberOfColumns=3,columnAttach=[(1, "both", 10),(2, "both", 40),(3, "both", 10)])
    cmds.button(label="List Select", width=100,bgc=(0.8, 0.3, 0.3),
                command=lambda _:select_const_list(parent =True,point=False,orient=False))
    cmds.button(label="List Select", width=100,bgc=(0.4, 0.8, 0.4),
                command=lambda _: select_const_list(parent =False,point=True,orient=False))
    cmds.button(label="List Select", width=100,bgc=(0.4, 0.4, 0.8),
                command=lambda _: select_const_list(parent =False,point=False,orient=True))
    cmds.setParent('..')
    separator = cmds.separator(style="in", height=1)
    cmds.setParent('..')
    ListAllRunRow = cmds.rowLayout(numberOfColumns=3,columnAttach=[(1, "both", 10),(2, "both", 40),(3, "both", 10)])
    cmds.button(label="List All Run", width=100,bgc=(0.8, 0.3, 0.3),
                command=lambda _:list_all_run(parent =True,point=False,orient=False))
    cmds.button(label="List All Run", width=100,bgc=(0.4, 0.8, 0.4),
                command=lambda _: list_all_run(parent =False,point=True,orient=False))
    cmds.button(label="List All Run", width=100,bgc=(0.4, 0.4, 0.8),
                command=lambda _: list_all_run(parent =False,point=False,orient=True))
    cmds.setParent('..')
    separator = cmds.separator(style="in", height=10)
    cmds.setParent('..')
    cmds.frameLayout("AnimaCopy",label="Animation Copy", collapsable=True, collapse=True, marginWidth=20)
    animationCopyRow = cmds.rowLayout(adjustableColumn=True,)
    cmds.text(label="Animation Copy", height=30, font="boldLabelFont")
    cmds.setParent('..')

    cmds.rowLayout(adjustableColumn=True,columnAttach=[(1, "both", 60)])

    cmds.radioButtonGrp("Animation_Copy_Option_Ui",
                        numberOfRadioButtons=3,
                        labelArray3=["Copy", "SmartBake", "Bake"],
                        select=1,
                        )
    cmds.setParent('AnimaCopy')
    cmds.rowLayout(adjustableColumn=True,)
    cmds.button(label="Copy", width=100,h=30,
                command=lambda _:transfer_animation())
    cmds.setParent('AnimaCopy')
    cmds.setParent('..')
    separator = cmds.separator(style="in", height=10)
    cmds.setParent('..')


    cmds.showWindow(window)

    cmds.scriptJob(
        event=['SceneOpened', 'cmds.deleteUI("{}")'.format(window)], p=window)
    cmds.scriptJob(
        event=['NewSceneOpened', 'cmds.deleteUI("{}")'.format(window)], p=window)

    # scriptJob を作成
    scriptJobId = cmds.scriptJob(
        event=["SelectionChanged", ResetUiValue], parent="MayaWindow"
    )
    scriptJobId_2 = cmds.scriptJob(
        event=["timeChanged", ResetUiValue], parent="MayaWindow"
    )

    # ウィンドウを閉じた際に両方の scriptJob を破棄
    cmds.window(
        window, e=True, sizeable=False,
        cc="cmds.scriptJob(kill={}); cmds.scriptJob(kill={})".format(scriptJobId, scriptJobId_2)
    )

    cmds.setFocus("")
