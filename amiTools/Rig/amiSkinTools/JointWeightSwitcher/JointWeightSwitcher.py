#----------------------------------------------------------
# -*- coding: utf-8 -*-


import maya.cmds as cmds
color_labels = []
def exchange_skin_weights_with_threshold(mesh, joint1, joint2, min_threshold, max_threshold):
    # スキンクラスタの取得
    skin_cluster = cmds.ls(cmds.listHistory(mesh), type='skinCluster')
    if not skin_cluster:
        cmds.error('指定されたメッシュにはスキンが適用されていません。')
        return
    skin_cluster = skin_cluster[0]
    # ジョイントのインデックスを取得
    joints = cmds.skinCluster(skin_cluster, query=True, influence=True)
    joint1_index = joints.index(joint1)
    joint2_index = joints.index(joint2)
    # すべての頂点のスキンウェイトを取得
    vertices = cmds.ls(mesh + '.vtx[*]', flatten=True)
    for vertex in vertices:
        weights = cmds.skinPercent(skin_cluster, vertex, query=True, value=True)
        # 条件を満たす場合、新しいウェイトリストを作成
        if min_threshold <= weights[joint1_index] <= max_threshold:
            new_weights = list(weights)
            new_weights[joint2_index] = weights[joint1_index]
            new_weights[joint1_index] = 0.0
            # スキンウェイトを設定
            influence_weights = [(joint, new_weights[i]) for i, joint in enumerate(joints)]
            cmds.skinPercent(skin_cluster, vertex, transformValue=influence_weights)
def JointWeightSwitcherMain():
    mesh_name = cmds.textField("JWSwTargetMeshField", query=True, text=True)
    joint1_name = cmds.textField("JWSwSourceJointField", query=True, text=True)
    joint2_name = cmds.textField("JWSwTargetJointField", query=True, text=True)
    min_threshold = cmds.floatSliderGrp("JWSwMinWeight", query=True, value=True)
    max_threshold = cmds.floatSliderGrp("JWSwMaxWeight", query=True, value=True)
    exchange_skin_weights_with_threshold(mesh_name, joint1_name, joint2_name, min_threshold, max_threshold)
def setTargetMesh():
    target = cmds.ls(sl=True)[0]
    cmds.textField("JWSwTargetMeshField", e=True,text=target)
def setPairJoint():
    sourceLock = cmds.checkBox("JWSwSourceLock", query=True, value=True)
    targetLock = cmds.checkBox("JWSwTargetLock", query=True, value=True)
    # 両方ロックされている場合は何もしない
    if sourceLock and targetLock:
        return
    sel_list = cmds.ls(sl=True, type="joint")
    if not sel_list:
        return
    # 1個か2個までに制限
    pair_list = sel_list[:2]
    if sourceLock:
        if len(pair_list) >= 1:
            cmds.textField("JWSwTargetJointField", edit=True, text=pair_list[0])
    elif targetLock:
        if len(pair_list) >= 1:
            cmds.textField("JWSwSourceJointField", edit=True, text=pair_list[0])
    else:
        if len(pair_list) >= 1:
            cmds.textField("JWSwSourceJointField", edit=True, text=pair_list[0])
        if len(pair_list) >= 2:
            cmds.textField("JWSwTargetJointField", edit=True, text=pair_list[1])
def update_color_ramp(*args):
    min_w = cmds.floatSliderGrp("JWSwMinWeight", query=True, value=True)
    max_w = cmds.floatSliderGrp("JWSwMaxWeight", query=True, value=True)
    ramp_colors = [
        (0.0, 0.0, 1.0),   # blue
        (0.2, 0.5, 1.0),
        (0.4, 1.0, 1.0),
        (0.6, 1.0, 0.6),
        (0.8, 1.0, 0.2),
        (1.0, 1.0, 0.0),   # yellow
        (1.0, 0.7, 0.0),
        (1.0, 0.4, 0.0),
        (1.0, 0.2, 0.0),
        (1.0, 0.0, 0.0)    # red
    ]
    for i, lbl in enumerate(color_labels):
        t = i / 9.0  # 0.0〜1.0 に正規化
        if t < min_w or t > max_w:
            cmds.text(lbl, edit=True, backgroundColor=(0.2, 0.2, 0.2))  # グレーアウト
        else:
            cmds.text(lbl, edit=True, backgroundColor=ramp_colors[i])

def JointWeightSwitcher():
    if cmds.window("JointWeightSwitcher", exists=True):
        cmds.deleteUI("JointWeightSwitcher")
    window = cmds.window("JointWeightSwitcher", title="Joint Weight Switcher", widthHeight=(400, 350), sizeable=False)
    main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=10)
    # ---------- Target Mesh ----------
    cmds.frameLayout(label="Target Mesh", collapsable=False, marginWidth=10, marginHeight=5)
    cmds.rowLayout(numberOfColumns=3, adjustableColumn=2, columnAttach=[(1, 'left', 5), (2, 'both', 5), (3, 'right', 5)], columnWidth=[(3, 50)])
    cmds.text(label="Mesh: ", align='right', width=40)
    cmds.textField("JWSwTargetMeshField", pht="edit mesh")
    cmds.button(label="Set", width=40, command=lambda *args:setTargetMesh())
    cmds.setParent("..")
    cmds.setParent("..")
    # ---------- Joint Pair ----------
    cmds.frameLayout(label="Joint Pair", collapsable=False, marginWidth=10, marginHeight=5)
    cmds.rowLayout(numberOfColumns=5, adjustableColumn=1, columnAttach=[(1, 'both', 5)])
    cmds.textField("JWSwSourceJointField", pht="SourceJoint")
    cmds.checkBox("JWSwSourceLock", label="Lock")
    cmds.text(label="→", align='center', width=15)
    cmds.textField("JWSwTargetJointField", pht="TargetJoint")
    cmds.checkBox("JWSwTargetLock", label="Lock")
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.frameLayout(label="Weight Color Indicator", collapsable=False, marginWidth=10, marginHeight=5)
    ramp_row = cmds.rowLayout(numberOfColumns=10)
    for i in range(10):
        lbl = cmds.text(label="", backgroundColor=(0.2, 0.2, 0.2), height=20, width=30)
        color_labels.append(lbl)
    cmds.setParent("..")
    cmds.setParent("..")
    # ---------- Weight Range ----------
    cmds.frameLayout(label="Weight Range", collapsable=False, marginWidth=10, marginHeight=5)
    cmds.floatSliderGrp("JWSwMinWeight", label="Min Weight", field=True,
                        minValue=0, maxValue=1, value=0.0, step=0.001,
                        columnWidth=[(1, 100), (2, 60)],
                        dragCommand=update_color_ramp)
    cmds.floatSliderGrp("JWSwMaxWeight", label="Max Weight", field=True,
                        minValue=0, maxValue=1, value=1.0, step=0.001,
                        columnWidth=[(1, 100), (2, 60)],
                        dragCommand=update_color_ramp)
    cmds.setParent("..")
    cmds.frameLayout(label="", borderVisible=False, marginHeight=5, marginWidth=10)
    cmds.rowLayout(numberOfColumns=1, adjustableColumn=1, columnAlign=[(1, 'center')])
    cmds.button(label="Run", width=120, height=30, backgroundColor=(0.3, 0.3, 0.3),
                                    command=lambda *args:JointWeightSwitcherMain())
    cmds.setParent("..")
    cmds.setParent("..")
    scriptJobId = cmds.scriptJob(
        event=["SelectionChanged", setPairJoint], parent="MayaWindow"
    )
    cmds.window(window, e=True,cc=f"cmds.scriptJob(kill={scriptJobId})")
    cmds.showWindow(window)