import maya.cmds as cmds
import os
import amiToolsLauncher
def JointExporterMain(override=False):
    cmds.select(cmds.ls(sl=True), hi=True)
    selected_joints = cmds.ls(selection=True, type="joint")
    scene_path = cmds.file(q=True, sceneName=True)
    directory = os.path.dirname(scene_path)
    export_name = scene_path.split("/")[-1].split(".")[0] + "_CreatNewJoint.mel"
    if override:
        export_name = scene_path.split("/")[-1].split(".")[0] + "_OverrideJoint.mel"
    # 出力するファイルのパス
    output_path = os.path.join(directory, export_name)

    # MEL コマンドとして出力するスクリプト内容を作成
    script_content = "select -cl;\n"
    script_content += "string $parent[];\n"
    parent_command = ""
    setattr_command = ""
    for joint in selected_joints:
        # ジョイントの translate, rotate, jointOrient の値を取得
        translate = cmds.getAttr(joint + ".translate")[0]
        rotate = cmds.getAttr(joint + ".rotate")[0]
        joint_orient = cmds.getAttr(joint + ".jointOrient")[0]
        parent_joint = cmds.listRelatives(joint, parent=True)
        parent_joint = parent_joint[0] if parent_joint else None

        if not override:
            new_joint_name = joint + "_new"
        else:
            new_joint_name = joint

        # joint作成
        script_content += "if (!`objExists \"" + new_joint_name + "\"`) {\n"
        script_content += "    joint -n \"" + new_joint_name + "\";\n"
        script_content += "}\n"
        script_content += "select -cl;\n"


        if parent_joint:# 親が無いものは回避
            if not override:
                parent_joint = parent_joint + "_new"
            # 親子付けコマンドと既に親子付けされている場合の回避コマンド
            parent_command += (
                "$parent = `listRelatives -p \"" + new_joint_name + "\"`;\n"
                + "if (size($parent) == 0 || $parent[0] != \"" + parent_joint + "\") {\n"
                + "    parent \"" + new_joint_name + "\" \"" + parent_joint + "\";\n"
                + "}\n"
            )

        # アトリビュート設定
        setattr_command += "setAttr \"" + new_joint_name + ".translate\" " + str(translate[0]) + " " + str(translate[1]) + " " + str(translate[2]) + ";\n"
        setattr_command += "setAttr \"" + new_joint_name + ".rotate\" " + str(rotate[0]) + " " + str(rotate[1]) + " " + str(rotate[2]) + ";\n"
        setattr_command += "setAttr \"" + new_joint_name + ".jointOrient\" " + str(joint_orient[0]) + " " + str(joint_orient[1]) + " " + str(joint_orient[2]) + ";\n"

    script_content += parent_command
    script_content += setattr_command

    # ファイルに書き出す
    with open(output_path, 'w') as file:
        file.write(script_content)

    print("----------------------------------------------------------")
    print("スクリプトが保存されました: " + output_path)
    print("----------------------------------------------------------")
    cmds.inViewMessage(
        smg="スクリプトが保存されました: " + export_name,
        pos="topCenter",
        bkc=0x00000000,
        fadeStayTime=3000,
        fade=True,
    )

def JointExporter():
    # UI Setup
    if cmds.window("JointExporter", exists=True):
        cmds.deleteUI("JointExporter", window=True)

    window = cmds.window("Joint Exporter", title="Joint Exporter",  widthHeight=(210, 185),
                                sizeable=False,maximizeButton=False, minimizeButton=False,)
    cmds.columnLayout(adjustableColumn=True)
    cmds.rowLayout(numberOfColumns=3,columnAttach=[(2, "both", 35),])
    my_path =os.path.dirname(os.path.abspath(__file__))
    image_path = my_path.split("amiTools\\")[0]
    cmds.symbolButton(image=image_path + r"\amiTools\Image\amiIcon.png", w=30,h=30,
                        command=lambda *args:amiToolsLauncher.amiToolsLauncher())
    cmds.text(label="Joint Exporter",h=30, font="boldLabelFont")
    cmds.button(label="?", width=30, height=30, command=lambda *_:print("help"))
    cmds.setParent("..")
    cmds.separator(height=10)
    cmds.text(label="今のジョイント名にNewを付けて\n再生成コマンドを作ります")
    cmds.button(label="New joint", h=40,
                command=lambda *args: JointExporterMain(override=False))
    cmds.text(label="今のジョイント名のまま再生成コマンドを作ります\n同名ジョイントがある場合上書き")
    cmds.button(label="override", h=40, command=lambda *args: JointExporterMain(override=True))

    cmds.showWindow(window)