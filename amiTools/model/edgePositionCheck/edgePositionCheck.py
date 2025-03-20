import maya.cmds as cmds
import math

def select_open_edges():
    """
    オープンエッジ探して選択
    """
    selected_objects = cmds.ls(selection=True, long=True)

    if not selected_objects:
        cmds.warning("オブジェクトが選択されていません。")
        return
    open_edges = []
    for obj in selected_objects:
        edges = cmds.ls(f"{obj}.e[*]", flatten=True)

        for edge in edges:
            connected_faces = cmds.polyListComponentConversion(edge, fromEdge=True, toFace=True)
            connected_faces = cmds.ls(connected_faces, flatten=True)
            if not connected_faces or len(connected_faces) == 1:
                open_edges.append(edge)

    if open_edges:
        cmds.select(open_edges, replace=True)
    else:
        cmds.warning("開いたエッジは見つかりませんでした。")

def is_close_positions(pos1, pos2, tolerance):
    """指定した誤差率（tolerance）以内ならTrueを返す"""
    return all(math.isclose(a, b, abs_tol=tolerance) for a, b in zip(pos1, pos2))

def deselect_duplicate_edges():
    """選択したエッジのうち、誤差範囲内で重複するエッジを全て選択解除"""
    select_open_edges()
    tolerance = cmds.floatSliderGrp("toleranceSlider", query=True, value=True)  # UIから誤差率を取得
    selected_edges = cmds.ls(selection=True, flatten=True)

    if not selected_edges:
        cmds.warning("エッジが選択されていません。")
        return

    edge_positions = {}
    edges_to_deselect = set()
    for edge in selected_edges:
        vertices = cmds.polyListComponentConversion(edge, fromEdge=True, toVertex=True)
        vertices = cmds.ls(vertices, flatten=True)
        positions = [tuple(cmds.pointPosition(v, world=True)) for v in vertices]
        positions = tuple(sorted(positions))
        for stored_pos, stored_edges in edge_positions.items():
            if all(is_close_positions(p1, p2, tolerance) for p1, p2 in zip(positions, stored_pos)):
                edges_to_deselect.add(edge)
                edges_to_deselect.update(stored_edges)
                stored_edges.append(edge)
                break
        else:
            edge_positions[positions] = [edge]

    if edges_to_deselect:
        cmds.select(list(edges_to_deselect), deselect=True)
        cmds.text("statusText", edit=True, label=f"{len(edges_to_deselect)} 個の重複エッジを選択解除（誤差率: {tolerance:.5f}）")
    else:
        cmds.text("statusText", edit=True, label="重複するエッジは見つかりませんでした。")

def edgePositionCheck():
    """UIを作成"""
    if cmds.window("edgePositionCheck", exists=True):
        cmds.deleteUI("edgePositionCheck")

    window = cmds.window("edgePositionCheck", title="エッジ位置チェック", widthHeight=(300, 150))
    cmds.columnLayout(adjustableColumn=True)

    cmds.text(label="誤差率を調整（小さいほど厳密）")
    cmds.floatSliderGrp("toleranceSlider", label="誤差率", field=True, minValue=0.00001, maxValue=0.01, value=0.001, step=0.00001)

    cmds.button(label="重複エッジ選択解除", command=lambda x: deselect_duplicate_edges())

    cmds.separator(height=10)
    cmds.text("statusText", label="")

    cmds.showWindow(window)

# UIを起動
edgePositionCheck()
