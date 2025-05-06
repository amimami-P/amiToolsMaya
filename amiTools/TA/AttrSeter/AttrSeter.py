import maya.cmds as cmds
import amiToolsLauncher
import os
def AttrSet():
    Attr = cmds.textField("AttributeField", query=True, text=True)
    AttrValue = cmds.textField("AttributeValueField", query=True, text=True)
    # 両方とも空なら処理を中断
    if not Attr or not AttrValue:
        cmds.inViewMessage(
            smg="属性名または値が空です",
            pos="topCenter",
            bkc=0x00000000,
            fadeStayTime=3000,
            fade=True,
        )
        cmds.warning("属性名または値が空です。")
        return
    ErrorNode = []
    for sel in cmds.ls(sl=True):
        try:
            print(f"{sel}.{Attr}")

            if AttrValue.lower() == "true":
                val = True
            elif AttrValue.lower() == "false":
                val = False
            else:
                try:
                    val = eval(AttrValue)
                except:
                    val = AttrValue
            cmds.setAttr(f"{sel}.{Attr}", val)
        except Exception as e:
            ErrorNode.append(sel)
            print(f"エラー: {e}")
    if ErrorNode:
        print(u"以下のノードにアトリビュート設定出来ませんでした：")
        for node in ErrorNode:
            print(node)

def AttrSeter():
    if cmds.window("AttrSeter", exists=True):
        cmds.deleteUI("AttrSeter")

    window = cmds.window("AttrSeter", title="AttrSeter", widthHeight=(400, 120),
        sizeable=False, maximizeButton=False, minimizeButton=False)

    cmds.columnLayout("AttrSeterColumn", adjustableColumn=True)
    cmds.rowLayout(numberOfColumns=3,columnAttach=[(2, "both", 142),])
    my_path =os.path.dirname(os.path.abspath(__file__))
    image_path = my_path.split("amiTools\\")[0]
    cmds.symbolButton(image=image_path + r"\amiTools\Image\amiIcon.png", w=30,h=30,
                        command=lambda *args:amiToolsLauncher.amiToolsLauncher())
    cmds.text(label="AttrSeter",h=30, font="boldLabelFont")
    cmds.button(label="?", width=30, height=30, command=lambda *_:print("help"))
    cmds.setParent("..")
    cmds.rowLayout(numberOfColumns=3, adjustableColumn=True)
    cmds.text(label="set Attribute",w=190)
    cmds.text(label=".",w=20)
    cmds.text(label="Attribute Value",w=190)
    cmds.setParent("..")
    cmds.rowLayout(numberOfColumns=3, adjustableColumn=True)
    cmds.textField("AttributeField", h=20,w=190)
    cmds.text(label=".",w=20)
    cmds.textField("AttributeValueField", h=20,w=190)
    cmds.setParent("..")
    cmds.separator(height=10)
    cmds.button(label="ボタン", h=40, command=lambda *args: AttrSet())
    cmds.setParent("..")
    cmds.showWindow(window)
