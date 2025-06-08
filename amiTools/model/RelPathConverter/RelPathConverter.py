import maya.cmds as cmds
import os
import amiToolsLauncher
def find_deepest_common_folder_name(path1, path2):
    path1_parts = path1.replace("\\", "/").split("/")
    path2_parts = path2.replace("\\", "/").split("/")
    
    # 共通するフォルダ名を取得
    common_folders = set(path1_parts) & set(path2_parts)
    # path1の中で一番深い共通フォルダを探す
    deepest_folder = None

    for folder in reversed(path1_parts): 
        if folder in common_folders:
            deepest_folder = folder
            break  
    return deepest_folder  

def get_project_root():
    """Mayaの現在のプロジェクトディレクトリを取得"""
    project_root = cmds.workspace(query=True, rootDirectory=True)
    return os.path.normpath(project_root)

def make_relative_path(texture_path, root_dir):
    """絶対パスを相対パスに変換"""
    if not texture_path or not os.path.isabs(texture_path):
        return texture_path  # すでに相対パスならそのまま

    try:
        relative_path = os.path.relpath(texture_path, root_dir)
        return relative_path.replace("\\", "/")  # Mayaはスラッシュを使用
    except ValueError:
        return texture_path  # 変換できなかった場合はそのまま

def convert_textures_to_relative():
    """シーン内の全テクスチャのパスを相対パスに変換"""
    project_root = get_project_root().replace("\\", "/")
    if not project_root:
        cmds.inViewMessage(
            smg=u"プロジェクトパスが見つかりません。",
            pos="topCenter",
            bkc=0x00000000,
            fadeStayTime=3000,
            fade=True,
            )
        return
    if not get_project_root().replace("\\","/") in cmds.file(q=True, sceneName=True):
        cmds.inViewMessage(
            smg=u"プロジェクトパスとシーンパスが一致しません",
            pos="topCenter",
            bkc=0x00000000,
            fadeStayTime=3000,
            fade=True,
            )
        return
    file_nodes = cmds.ls(type="file")
    if not file_nodes:
        cmds.warning("テクスチャが見つかりません。")
        return

    scene_path = cmds.file(q=True, sceneName=True)
    for node in file_nodes:
        file_path = cmds.getAttr(f"{node}.fileTextureName").replace("\\", "/")
        common_folder = find_deepest_common_folder_name(scene_path, file_path)
        relative_path =scene_path.split("/" + common_folder + "/")[0]
        relative_path = relative_path.replace(project_root,"") + "/" + common_folder + "/"
        relative_path += file_path.split("/" + common_folder + "/")[-1]
        if relative_path.startswith("/"):
            relative_path = relative_path[1:]
        cmds.setAttr(f"{node}.fileTextureName", relative_path, type="string")
    cmds.inViewMessage(
        smg=u"相対パスへの変換終了",
        pos="topCenter",
        bkc=0x00000000,
        fadeStayTime=3000,
        fade=True,
        )
        
        

def RelPathConverter():
    """UIを作成"""
    if cmds.window("RelPathConverter", exists=True):
        cmds.deleteUI("RelPathConverter")

    window = cmds.window("RelPathConverter", title="RelPathConverter", widthHeight=(250, 125),
                         sizeable=False,maximizeButton=False, minimizeButton=False,)
    cmds.columnLayout(adjustableColumn=True)
    cmds.columnLayout("RelPathConverterMainColumn", adjustableColumn=True)
    cmds.rowLayout(numberOfColumns=3,columnAttach=[(2, "both", 45),])
    my_path =os.path.dirname(os.path.abspath(__file__))
    image_path = my_path.split("amiTools\\")[0]
    cmds.symbolButton(image=image_path + r"\amiTools\Image\amiIcon.png", w=30,h=30,
                        command=lambda *args:amiToolsLauncher.amiToolsLauncher())
    cmds.text(label="RelPathConverter",h=30, font="boldLabelFont")
    cmds.button(label="?", width=30, height=30, command=lambda *_:print("help"))
    cmds.setParent("..")
    cmds.text(label="シーン内の全テクスチャパスを相対パスに変換します。",h=40)
    cmds.button(label="実行",h=50,command=lambda *args:convert_textures_to_relative())
    cmds.showWindow(window)











