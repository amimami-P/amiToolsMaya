#----------------------------------------------------------
# -*- coding: utf-8 -*-
#----------------------------------------------------------
import maya.cmds as cmds

def get_blendshape_nodes(target=None):
    """選択または指定オブジェクトに接続されたブレンドシェイプノードを取得"""
    if not target:
        sel = cmds.ls(sl=True)
        if not sel:
            cmds.warning("オブジェクトを選択してください")
            return []
        target = sel[0]
    # ヒストリーから blendShape ノードを探す
    history = cmds.listHistory(target, pruneDagObjects=True) or []
    blend_nodes = cmds.ls(history, type="blendShape")
    return blend_nodes or []

def get_blendshape_targets(blendshape_node):
    """指定したブレンドシェイプノードの全モーフターゲット名を取得"""
    if not cmds.objExists(blendshape_node):
        cmds.warning(f"{blendshape_node} は存在しません。")
        return []

    aliases = cmds.aliasAttr(blendshape_node, q=True) or []
    targets = [aliases[i] for i in range(0, len(aliases), 2)]
    return targets

#----------------------------------------------------------
# main
#----------------------------------------------------------

def createMorphCtrl():
    sel = cmds.ls(sl=True)[0]
    ctrlName = sel.split(":")[0] + "_MorphCtrl"
    cmds.curve(name=ctrlName,d=1,
        p=[(0.0, 0.0, -2.993802), (-0.886951, 0.0, -0.993802),
            (-3.0, 0.0, -0.993802), (-1.271527, 0.0, 0.388976),
            (-2.0, 0.0, 3.006198), (-0.0221259, 0.0, 1.423899),
            (2.0, 0.0, 3.006198), (1.250591, 0.0, 0.383265),
            (3.0, 0.0, -0.993802), (0.894704, 0.0, -0.993802),
            (0.0, 0.0, -2.993802)],
        k=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])

    cmds.setAttr(ctrlName + ".lineWidth",3)
    cmds.addAttr(ctrlName, ln="Attr_Spacer", at="enum",nn="- -", en="MorphWeight:", k=True)

    nodes = get_blendshape_nodes(sel)

    for bs in nodes:
        targets = get_blendshape_targets(bs)
        for MorphName in targets:
            cmds.addAttr(ctrlName, ln=MorphName, at="float",min=0,max=1,k=True)
            cmds.connectAttr(f"{ctrlName}.{MorphName}",f"{bs}.{MorphName}")

if __name__ == '__main__':
    createMorphCtrl()
