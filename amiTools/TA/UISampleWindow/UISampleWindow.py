#----------------------------------------------------------
# -*- coding: utf-8 -*-
#----------------------------------------------------------
"""UISampleWindow.py

git:https://github.com/amimami-P/amiToolsMaya.git

coding by amimami
MayaVer Maya2024

Ver　1.0

"""
#----------------------------------------------------------
import maya.cmds as cmds
import os
import amiToolsLauncher
#----------------------------------------------------------


def print_command(command, description=""):
    """ボタンが押されたときに cmds コマンドと説明を出力"""
    print ("**---------------------------------------------------------**")
    print(f"{description}\n\n{command}\n")

def UISampleWindow():
    """UIのサンプルを作成して表示"""
    if cmds.window("UI_Sample_Window", exists=True):
        cmds.deleteUI("UI_Sample_Window")

    window = cmds.window("UI_Sample_Window", title="UI Elements Viewer", widthHeight=(450, 700),
                            sizeable=False,maximizeButton=False, minimizeButton=False,)
    cmds.scrollLayout(verticalScrollBarThickness=16,h=600)
    cmds.columnLayout(adjustableColumn=True)
    cmds.rowLayout(numberOfColumns=3,columnAttach=[(2, "both", 120),])
    my_path =os.path.dirname(os.path.abspath(__file__))
    image_path = my_path.split("amiTools")[0]
    cmds.symbolButton(image=image_path + r"\amiTools\Image\amiIcon.png", w=30,h=30,
                        command=lambda *args:amiToolsLauncher.amiToolsLauncher())
    cmds.text(label="UI Elements Viewer",h=30,font="boldLabelFont")
    cmds.setParent("..")

    cmds.columnLayout(adjustableColumn=True)
    cmds.button(label="Pirnt UI Template",h=50,command=lambda *args:print('''
*--------------------------------------------------------------------------------------*
import maya.cmds as cmds
if cmds.window("Sample_Window", exists=True):
    cmds.deleteUI("Sample_Window")
window = cmds.window("Sample_Window", title="Sample_Window", widthHeight=(400, 700))

"ここにUIコードを入れる"

cmds.setParent("..")#レイアウトから外に出る
cmds.showWindow(window)
''' ))


    cmds.columnLayout("UI_Sample_main")

    def add_ui_with_buttons(ui_func, label, create_cmd, query_cmd, description):
        """UI要素の作成、コマンド表示ボタン、説明を追加"""
        cmds.frameLayout(label=label, collapsable=True, collapse=False, marginWidth=20)
        cmds.columnLayout(w=400)

        cmds.text(label=description, align="left", height=40)
        ui_func()

        cmds.button(label="作成コマンドをプリント",
                    command=lambda x: print_command(create_cmd, f"{label} の作成コマンド"))
        cmds.button(label="情報取得コマンドをプリント",
                    command=lambda x: print_command(query_cmd, f"{label} の情報取得コマンド"))
        cmds.setParent("UI_Sample_main")



    add_ui_with_buttons(lambda: cmds.columnLayout("myColumn", adjustableColumn=True),
                        "Column Layout",
                        'cmds.columnLayout("myColumn", adjustableColumn=True)',
                        'cmds.columnLayout("myColumn", query=True, adjustableColumn=True)',
                        "UI要素を縦に並べるためのレイアウト。ボタンやスライダーを整理するのに便利。")

    add_ui_with_buttons(lambda: cmds.rowLayout("myRow", numberOfColumns=3),
                        "Row Layout",
                        'cmds.rowLayout("myRow", numberOfColumns=3)',
                        'cmds.rowLayout("myRow", query=True, numberOfColumns=True)',
                        "UI要素を横に並べるためのレイアウト。複数のボタンを1行で並べたいときに便利。")
    add_ui_with_buttons(lambda: cmds.scrollLayout("myScroll", width=200, height=100),
                        "Scroll Layout",
                        'cmds.scrollLayout("myScroll", width=200, height=100)',
                        'cmds.scrollLayout("myScroll", query=True, width=True)',
                        "スクロール可能なレイアウトです。ウィジェットが多い場合に便利です。",)

    add_ui_with_buttons(lambda: cmds.frameLayout("myFrame", label="Frame Layout", collapsable=True),
                        "Frame Layout",
                        'cmds.frameLayout("myFrame", label="Frame Layout", collapsable=True)',
                        'cmds.frameLayout("myFrame", query=True, collapsable=True)',
                        "折りたたみ可能なフレームで、UIを整理できます。",)

    add_ui_with_buttons(lambda: cmds.text(label="サンプルテキスト"),
                        "Text Label",
                        'cmds.text("myText", label="サンプルテキスト")',
                        'cmds.text("myText", query=True, label=True)',
                        "テキストを表示するできる")

    add_ui_with_buttons(lambda: cmds.button(label="ボタン",h=30,w=50,
                        ann="annフラグで簡単な説明メッセージ表示ができます"),
                        "Button",
                        'cmds.button("myButton", label="ボタン")'
                        '''annフラグで簡単な説明メッセージ表示ができます

ボタンを押したと時のアクション
    command=lambda *args:function()

右クリックでポップアップメニューを出す
cmds.popupMenu(parent="myButton")# ボタンを指定してparent
cmds.menuItem(label="ヘルプを表示", command=lambda _: cmds.confirmDialog(title="ヘルプ",
        message="このボタンの説明:\nクリックすると処理が実行されます。", button=["OK"]))''',
                        '''cmds.button("myButton", query=True, label=True)''',
                        "ボタンを押すとコマンドを実行できる")

    add_ui_with_buttons(lambda: cmds.radioButtonGrp("myRadioButtonGrp",
                        numberOfRadioButtons=3,
                        labelArray3=["test1", "test2", "test2"],
                        select=1,
                        ),
                        "radioButton",
                        '''cmds.radioButtonGrp("myRadioButtonGrp",
                        numberOfRadioButtons=3,
                        labelArray3=["test1", "test2", "test2"],
                        select=1,
                        )''',
                        'cmds.radioButtonGrp("myRadioButtonGrp", query=True, select=True)',
                        "ラジオボタン/n複数チェックを許したくない時に使う")
    add_ui_with_buttons(lambda: cmds.checkBox("myCheckBox", label="チェックボックス"),
                        "CheckBox",
                        'cmds.checkBox("myCheckBox", label="チェックボックス")',
                        '''cmds.checkBox("myCheckBox", query=True, value=True)
チェックオンでアクション
    onCommand=lambda *args: function()
チェックオフでアクション
    offCommand=lambda *args: function()''',
                        "チェックボックス")

    add_ui_with_buttons(lambda: cmds.intSliderGrp("myIntSlider", label="Float Slider", field=True, minValue=0, maxValue=100, value=50),
                        "Float Slider",
                        'cmds.floatSliderGrp("myFloatSlider", label="Float Slider", field=True, minValue=0, maxValue=100, value=50)',
                        '''cmds.floatSliderGrp("myFloatSlider", query=True, value=True)
スライダーの変化に反応してアクション
    changeCommand=lambda value: function(value)
      ->valueには変更されたスライダー数値が入る''',
                        """整数調整できるスライダー。""")
    add_ui_with_buttons(lambda: cmds.floatSliderGrp("myFloatSlider", label="Float Slider", field=True, minValue=0, maxValue=1, value=0.5),
                        "Float Slider",
                        'cmds.floatSliderGrp("myFloatSlider", label="Float Slider", field=True, minValue=0, maxValue=1, value=0.5)',
                        '''cmds.floatSliderGrp("myFloatSlider", query=True, value=True)
スライダーの変化に反応してアクション
    changeCommand=lambda value: function(value)
     ->valueには変更されたスライダー数値が入る''',
                        """小数を調整できるスライダー。""")

    add_ui_with_buttons(lambda: cmds.textField("myTextField", text="テキスト入力",w=200),
                        "Text Field",
                        'cmds.textField("myTextField", text="テキスト入力",w=200)',
                        '''cmds.textField("myTextField", query=True, text=True)
テキストをコマンドで入力したい時
    cmds.textField("myTextField", edit=True, text="入力したいテキスト")''',
                        "テキストを入力するできる")
    add_ui_with_buttons(lambda: cmds.text(label="------------------------------------------------"),
                        "separator",
                        'cmds.separator( height=20)',
                        '''取得できる情報なし''',
                        "UIに区切り線をいれる")
    add_ui_with_buttons(lambda: (
        cmds.optionMenu("optionMenu", label="optionMenu", w=150),
        cmds.menuItem(label="test", parent="optionMenu"),
        cmds.menuItem(label="test2", parent="optionMenu")
    ),
    "Option Menu",
    '''cmds.optionMenu("optionMenu", label="optionMenu", w=150)
    cmds.menuItem(label="test", parent="optionMenu")
    cmds.menuItem(label="test2", parent="optionMenu")''',
    'cmds.optionMenu("optionMenu", query=True, value=True)',
    "ドロップダウンメニューを作成")
    add_ui_with_buttons(lambda: (cmds.symbolButton(image=image_path +
    r"\amiTools\Image\amiIcon.png", w=50,h=50)
    ),
    "symbolButton",
    'cmds.symbolButton("mySymbolButton", label="ボタン")',
    '''cmds.symbolButton("mySymbolButton", query=True, label=True)
ボタンを押したと時のアクション
    command=lambda *args:function()''',
    "画像をボタンに出来る")
    add_ui_with_buttons(lambda: cmds.scrollField("myScrollField",
                width=200, height=100,text="testText1\ntestText2\ntestText3\n"),
    "scrollField",
    '''cmds.scrollField("myScrollField", text="好きなテキストを入力")
\\nで改行''',
    '''cmds.scrollField("myScrollField", query=True, text=True)''',
    "スクロール可能なテキストボックス\n複数データを表示する時とかに使う")



    cmds.showWindow(window)



