#----------------------------------------------------------
# -*- coding: utf-8 -*-

#----------------------------------------------------------
import maya.cmds as cmds
import maya.mel as mel
import os
import subprocess
try:#amiToolsを導入しない場合のError回避
    import amiToolsLauncher
except:
    pass
#----------------------------------------------------------

def delete_nameSpace(file_path):

    with open(file_path, "r") as f:
        file_content = f.read()

    lines = file_content.split("\n")
    found_namespace = False
    for line in lines:
        end = line.rfind(":")
        if end != -1:
            start = line.rfind('"Model::', 0, end)
            if start != -1:
                NameSpace = line[start+len('"Model::'):end]
                NameSpace = (NameSpace + ":")
                print(NameSpace)
                print("-")

                file_content = file_content.replace(NameSpace, "")
                with open(os.path.join(file_path), "w") as f:
                    f.write(file_content)
                found_namespace = True
                break

def Anim_FBX_Export():


    scenePath = cmds.file(q=True, sceneName=True)
    if not scenePath:
        cmds.inViewMessage(
            smg=u"開いているシーンパスが取得できません。\nシーン保存してから実行してください",
            pos="topCenter",
            bkc=0x00000000,
            fadeStayTime=3000,
            fade=True,
            )
        return
    sceneName = scenePath.split("/")[-1]
    rootPath = scenePath.split("/")[:-1]
    rootPath += ["motion_FBX"]
    rootPath  = "/".join(rootPath)
    export_Path = rootPath + "/" + sceneName.replace(".ma",".fbx")
    exportRoot = cmds.textField("AAEEexportRoot", query=True, text=True)
    if not exportRoot:
        cmds.inViewMessage(
            smg=u"エクスポートルートが設定されていません",
            pos="topCenter",
            bkc=0x00000000,
            fadeStayTime=3000,
            fade=True,
            )
        return

    children = cmds.listRelatives(exportRoot, allDescendents=True, fullPath=True)
    cmds.select(exportRoot,children)

    if not os.path.exists(rootPath):
        os.makedirs(rootPath)
    takeName = sceneName.split(".")[0]
    start_time = int(cmds.textField("AAEMin", query=True, text=True))
    end_time = int(cmds.textField("AAEMax", query=True, text=True))
    mel.eval("FBXResetExport;")
    mel.eval("FBXExportSplitAnimationIntoTakes -clear;")
    mel.eval(f"FBXExportSplitAnimationIntoTakes -v {takeName} {start_time} {end_time};")
    mel.eval("FBXExportDeleteOriginalTakeOnSplitAnimation -v true;")
    mel.eval("FBXExportInputConnections -v false;")
    mel.eval("FBXExportUpAxis \"y\";")
    mel.eval("FBXExportInAscii -v true;")
    mel.eval("FBXExportBakeComplexAnimation -v true;")
    mel.eval(f"FBXExportBakeComplexStart -v {start_time};")
    mel.eval(f"FBXExportBakeComplexEnd -v {end_time};")
    mel.eval("FBXExportBakeComplexStep -v 1;")
    mel.eval("FBXExportIncludeChildren -v false;")
    mel.eval("FBXExportBakeResampleAnimation -v true;")
    mel.eval(f"FBXExport -f \"{export_Path}\" -s;")

    split_animation = mel.eval("FBXExportSplitAnimationIntoTakes -q;")
    delete_original_take = mel.eval(
        "FBXExportDeleteOriginalTakeOnSplitAnimation -q;")
    in_ascii = mel.eval("FBXExportInAscii -q;")
    if cmds.checkBox("AAEdeleteNameSpace", query=True, value=True) ==True:
        delete_nameSpace(export_Path)
    if cmds.checkBox("AAEopenExportFolder", query=True, value=True) ==True:
        openPath = rootPath.replace("/", "\\")
        subprocess.Popen(f'explorer {openPath}')
    print(u"Export Success")
    print(u"Export Path : " + export_Path)
    cmds.inViewMessage(
        smg=(u"Export Success!!"),
        pos="topCenter",
        bkc=0x00000000,
        fadeStayTime=3000,
        fade=True,
    )
    return export_Path

def AAE_RootSet():
    ExportRoot = cmds.ls(sl=True)[0]
    if not ExportRoot:
        return
    cmds.textField("AAEEexportRoot",edit=True, text=ExportRoot,)
    cmds.setFocus("")

def AAE_setPlaynack():
    start_time = int(cmds.playbackOptions(query=True, minTime=True))
    end_time = int(cmds.playbackOptions(query=True, maxTime=True))
    cmds.textField("AAEMin",edit=True, text=start_time)
    cmds.textField("AAEMax",edit=True, text=end_time)
    cmds.setFocus("")

def Ami_AnimExporter():
    if cmds.window("Ami_AnimExporter", exists=True):
        cmds.deleteUI("Ami_AnimExporter")
    window = cmds.window("Ami_AnimExporter", title="Ami_AnimExporter", widthHeight=(200,300),
                        sizeable=False,maximizeButton=False, minimizeButton=False,)
    cmds.columnLayout("AAEColumn", adjustableColumn=True)

    cmds.rowLayout(numberOfColumns=3,columnAttach=[(2, "both", 20),])
    try:#amiToolsを導入しない場合のError回避
        my_path =os.path.dirname(os.path.abspath(__file__))
        image_path = my_path.split("amiTools\\")[0]
        cmds.symbolButton(image=image_path + r"\amiTools\Image\amiIcon.png", w=30,h=30,
                            command=lambda *args:amiToolsLauncher.amiToolsLauncher())
        cmds.text(label="Ami AnimExporter",h=30, font="boldLabelFont")
        cmds.button(label="?", width=30, height=30, command=lambda *_:print("helpはあとで書きます"))
    except:
        pass
    cmds.setParent("..")
    cmds.separator(height=20)
    cmds.button(label="get playnack",command=lambda *args:AAE_setPlaynack(),w=130)

    cmds.separator(height=20)
    cmds.text(label="書き出し範囲")
    cmds.rowLayout("AAEInfoRow", numberOfColumns=3,columnAttach=[(1, "both",7)])
    start_time = int(cmds.playbackOptions(query=True, minTime=True))
    end_time = int(cmds.playbackOptions(query=True, maxTime=True))
    cmds.textField("AAEMin", text=start_time, w=80)
    cmds.text(label=" - ")
    cmds.textField("AAEMax", text=end_time, w=80)
    cmds.setParent("..")
    cmds.separator(height=20)
    cmds.text(label="エクスポートルートを設定")
    cmds.rowLayout("AAEexportRootRow", numberOfColumns=3,columnAttach=[(1, "both", 5),(3, "both", 5)])
    cmds.textField("AAEEexportRoot", text="", w=120)
    cmds.button(label="get Root",command=lambda *args:AAE_RootSet())
    cmds.setParent("..")
    cmds.checkBox("AAEdeleteNameSpace", label="delete NameSpace",value=True,h=30)
    cmds.checkBox("AAEopenExportFolder", label="open ExportFolder",value=True,h=30)
    cmds.separator(height=20)
    cmds.button(label="エクスポート",command=lambda *args:Anim_FBX_Export(),h=30)
    cmds.setParent("..")
    cmds.showWindow(window)
    cmds.setFocus("")