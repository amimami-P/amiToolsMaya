#----------------------------------------------------------
import maya.cmds as cmds
import os
import amiToolsLauncher
#----------------------------------------------------------

def add_ui_with_buttons(ui_func, label, py_create_cmd, py_query_cmd, description, mel_create_cmd, mel_query_cmd,parent):
    """UI要素の作成、コマンド表示ボタン、説明を追加"""

    cmds.frameLayout(label=label, collapsable=True, collapse=False, marginWidth=20)
    cmds.columnLayout(w=400)

    cmds.text(label=description, align="left", height=40)
    ui_func()

    def print_correct_command(create_cmd, query_cmd, label, action_type):
        """ラジオボタンでPythonかMelを選択し、コマンドを表示"""
        # PythonかMelを判定
        if cmds.radioButtonGrp("UI_Sample_languageSel", query=True, select=True) == 1:
            is_mel = False
        else:
            is_mel = True

        cmd_to_print = mel_create_cmd if is_mel else create_cmd
        query_to_print = mel_query_cmd if is_mel else query_cmd

        if action_type == "create":
            print_command(cmd_to_print, f"{label} の作成コマンド")
        elif action_type == "query":
            print_command(query_to_print, f"{label} の情報取得コマンド")

    # 作成コマンドボタン
    cmds.button(label="作成コマンドをプリント",
                command=lambda x: print_correct_command(py_create_cmd, py_query_cmd, label, "create"))

    # 情報取得コマンドボタン
    cmds.button(label="情報取得コマンドをプリント",
                command=lambda x: print_correct_command(py_create_cmd, py_query_cmd, label, "query"))

    cmds.setParent(parent)

def printTemplateUI():
    if cmds.radioButtonGrp("UI_Sample_languageSel", query=True, select=True) == 1:
        cmd ='''
*--------------------------------------------------------------------------------------*
import maya.cmds as cmds
if cmds.window("Sample_Window", exists=True):
    cmds.deleteUI("Sample_Window")
window = cmds.window("Sample_Window", title="Sample_Window", widthHeight=(400, 700))

"ここにUIコードを入れる"

cmds.setParent("..")#レイアウトから外に出る
cmds.showWindow(window)''' 
    else:
        cmd ='''
*--------------------------------------------------------------------------------------*
// mel
if (`window -exists Sample_Window`) {
    deleteUI Sample_Window;
}
window -title "Sample_Window" -widthHeight 400 700 Sample_Window;
// ここにUIコードを入れる
setParent ..; // レイアウトから外に出る
showWindow Sample_Window;
''' 
    print(cmd)

def printScriptJob():
    if cmds.radioButtonGrp("UI_Sample_languageSel", query=True, select=True) == 1:
        cmd ='''
*--------------------------------------------------------------------------------------*
scriptJobId = cmds.scriptJob(
    event=["イベント宣言", 使いたい関数], parent="MayaWindow"
)
# ウィンドウを閉じた際に両方の scriptJob を破棄
cmds.window(window, e=True,cc=f"cmds.scriptJob(kill={scriptJobId})")''' 
    else:
        cmd ='''
*--------------------------------------------------------------------------------------*
// mel
int $scriptJobId = `scriptJob -event "イベント宣言" "使いたい関数" -parent "MayaWindow"`;

// ウィンドウを閉じた際に両方の scriptJob を破棄
window -e -cc ("scriptJob -kill " + $scriptJobId + ") $window;
''' 
    print(cmd)

def printScriptJobEvent():
    cmd ="""
*--------------------------------------------------------------------------------------*
"SelectionChanged"
選択が変更されたときに実行されます。

"SceneUpdate"
シーンが更新されたときに実行されます（例えば、ノードの状態が変更されたときなど）。

"Undo"
ユーザーがUndo操作を実行したときに実行されます。

"Redo"
ユーザーがRedo操作を実行したときに実行されます。

"NodeAdded"
新しいノードがシーンに追加されたときに実行されます。

"NodeRemoved"
シーンからノードが削除されたときに実行されます。

"NameChanged"
ノード名が変更されたときに実行されます。

"Changed"
ノードが変更されたときに実行されます。特定の属性やノードに対する変更を監視できます。

"Idle"
Mayaがアイドル状態（何も操作がない状態）になったときに実行されます。

"AttributeChanged"
ノードの属性が変更されたときに実行されます。

"TimeChanged"
タイムラインのフレームが変更されたときに実行されます。

"RenderComplete"
レンダリングが完了したときに実行されます。

"AfterLoad"
Mayaがロードされた後に実行されます。

"AfterSave"
Mayaがセーブされた後に実行されます。

"BeforeQuit"
Mayaが終了する前に実行されます。

"FileNew"
新しいファイルが作成されたときに実行されます。

"FileOpen"
ファイルが開かれたときに実行されます。

"FileSave"
ファイルが保存されたときに実行されます。

"AddNode"
新しいノードが追加されたときに実行されます。

"SelectionChanged"
シーンの選択が変更されたときに実行されます。
"""
    print(cmd)

def printLayoutDelete():
    if cmds.radioButtonGrp("UI_Sample_languageSel", query=True, select=True) == 1:
        cmd ='''
*--------------------------------------------------------------------------------------*
if cmds.control("レイアウト名", exists=True):
        cmds.deleteUI("レイアウト名", layout=True)
    ''' 
    else:
        cmd ='''
*--------------------------------------------------------------------------------------*
if (`control -exists レイアウト名`) {
    deleteUI -layout レイアウト名;
}'''
    print(cmd)

def print_command(command, description=""):
    """ボタンが押されたときに cmds コマンドと説明を出力"""
    print ("**---------------------------------------------------------**")
    print(f"{description}\n\n{command}\n")

def UISampleWindow():
    """UIのサンプルを作成して表示"""
    if cmds.window("UI_Sample_Window", exists=True):
        cmds.deleteUI("UI_Sample_Window")

    window = cmds.window("UI_Sample_Window", title="UI Elements Viewer", widthHeight=(470, 700),
                            sizeable=False,maximizeButton=False, minimizeButton=False,)
    cmds.scrollLayout(verticalScrollBarThickness=16,h=600)
    cmds.columnLayout(adjustableColumn=True)
    cmds.rowLayout(numberOfColumns=3,columnAttach=[(2, "both", 120),])
    my_path =os.path.dirname(os.path.abspath(__file__))
    image_path = my_path.split("amiTools\\")[0]
    cmds.symbolButton(image=image_path + r"\amiTools\Image\amiIcon.png", w=30,h=30,
                        command=lambda *args:amiToolsLauncher.amiToolsLauncher())
    cmds.text(label="UI Elements Viewer",h=30,font="boldLabelFont")
    cmds.setParent("..")

    cmds.columnLayout(adjustableColumn=True)
    cmds.separator(height=5)
    cmds.rowLayout("UI_Sample_languageRow", numberOfColumns=3)
    cmds.text(label="Select Language :   ",h=20,font="boldLabelFont")
    cmds.radioButtonGrp("UI_Sample_languageSel",
                        numberOfRadioButtons=2, labelArray2=["Python","Mel", ], select=1)
    cmds.setParent("..")
    cmds.separator(height=5)

    cmds.button(label="Pirnt UI Template",h=50,command=lambda *args:printTemplateUI())
    cmds.separator(height=5)
    cmds.rowLayout("UI_Sample_OpRow", numberOfColumns=3,adjustableColumn=True)
    cmds.button(label="layout delete",w=150,h=30,command=lambda *args:printLayoutDelete())
    cmds.button(label="script Job",w=150,h=30,command=lambda *args:printScriptJob())
    cmds.button(label="script Job Event",w=150,h=30,command=lambda *args:printScriptJobEvent())
    cmds.setParent("..")
    cmds.separator(height=10)
    cmds.setParent("..")
    cmds.tabLayout("UI_Sample_MainTab", )
    
    #-----------------------------------------------
    # レイアウト
    #-----------------------------------------------
    cmds.columnLayout("UI_Sample_Layout")
    cmds.separator(height=10)
    add_ui_with_buttons(lambda: cmds.columnLayout("myColumn", adjustableColumn=True),
                        "Column Layout",
                        # python
                        'cmds.columnLayout("myColumn", adjustableColumn=True)',
                        'cmds.columnLayout("myColumn", query=True, childArray=True)',
                        "UI要素を縦に並べるためのレイアウト。",
                        # mel
                        "columnLayout -adjustableColumn true myColumn;",
                        "columnLayout -query -childArray myColumn;",
                        "UI_Sample_Layout")

    add_ui_with_buttons(lambda: cmds.rowLayout("myRow", numberOfColumns=3),
                        "Row Layout",
                        'cmds.rowLayout("myRow", numberOfColumns=3)',
                        'cmds.rowLayout("myRow", query=True, childArray=True)',
                        "UI要素を横に並べるためのレイアウト。",
                        "rowLayout -numberOfColumns 3 myRow;",
                        "rowLayout -query -childArray myRow;",
                        "UI_Sample_Layout")

    add_ui_with_buttons(lambda: cmds.scrollLayout("myScroll", width=200, height=100),
                        "Scroll Layout",
                        'cmds.scrollLayout("myScroll", width=200, height=100)',
                        'cmds.scrollLayout("myScroll", query=True, childArray=True)',
                        "スクロール可能なレイアウト。",
                        "scrollLayout -width 200 -height 100 myScroll;",
                        "scrollLayout -query -childArray myScroll;",
                        "UI_Sample_Layout")

    add_ui_with_buttons(lambda: cmds.frameLayout("myFrame", label="Frame Layout", collapsable=True),
                        "Frame Layout",
                        'cmds.frameLayout("myFrame", label="Frame Layout", collapsable=True)',
                        'cmds.frameLayout("myFrame", query=True, childArray=True)',
                        "折りたたみ可能なフレーム。",
                        'frameLayout -label "Frame Layout" -collapsable true myFrame;',
                        "frameLayout -query -collapsable myFrame;",
                        "UI_Sample_Layout")

    add_ui_with_buttons(lambda: cmds.text("-----------------------------"),
                        "Separator",
                        'cmds.separator(height=20)',
                        "なし",
                        "UI に区切り線を入れる",
                        'separator -height 20;',
                        "なし",
                        "UI_Sample_Layout")
    add_ui_with_buttons(
        lambda: cmds.text(label="レイアウトをタブで切り替えできる"),
        "Tab Layout",
        # Python
        '''cmds.tabLayout("myTab", innerMarginWidth=5, innerMarginHeight=5)

#レイアウトの宣言を先にしてタブへアサインしていく場合は宣言後にこんな感じに書く
cmds.tabLayout("myTab", edit=True, tabLabel=[
("レイアウト名", u"タブのラベル")])
        ''',
        '''cmds.tabLayout("myTab", query=True, childArray=True)''',
        "タブで複数のUIを切り替えられるレイアウト。",
        # MEL
        '''tabLayout -innerMarginWidth 5 -innerMarginHeight 5 myTab;
// レイアウトの宣言を先にしてタブへアサインしていく場合は宣言後にこんな感じに書く
tabLayout -edit -tabLabel ("レイアウト名" "タブのラベル") myTab;''',
        'tabLayout -query -childArray myTab;',
                        "UI_Sample_Layout")
    add_ui_with_buttons(
        lambda: cmds.gridLayout("myGrid", numberOfColumns=3, cellWidthHeight=(100, 50)),
        "Grid Layout",
        # Python
        'cmds.gridLayout("myGrid", numberOfColumns=3, cellWidthHeight=(100, 50))',
        'cmds.gridLayout("myGrid", query=True, childArray=True)',
        "グリッド状にUI要素を並べるためのレイアウト。",
        # MEL
        'gridLayout -numberOfColumns 3 -cellWidthHeight 100 50 myGrid;',
        'gridLayout -query -childArray myGrid;',
                        "UI_Sample_Layout")
    cmds.setParent("..")
    #-----------------------------------------------
    # ボタン
    #-----------------------------------------------
    cmds.columnLayout("UI_Sample_Button")
    cmds.separator(height=10)
    add_ui_with_buttons(lambda: cmds.button(label="ボタン", h=30, w=50,ann="annフラグで簡単な説明メッセージ表示ができます"),
                        "Button",
                        """cmds.button("myButton", label="ボタン")
ボタンを押したと時のアクション
    command=lambda *args:function()H

右クリックでポップアップメニューを出す
cmds.popupMenu(parent="myButton")# ボタンを指定してparent
cmds.menuItem(label="ヘルプを表示", command=lambda _: cmds.confirmDialog(title="ヘルプ",
        message="このボタンの説明:\nクリックすると処理が実行されます。", button=["OK"]))""",
                        'cmds.button("myButton", query=True, label=True)',
                        "ボタンを押すとコマンドを実行できる",
                        '''button -label "ボタン" myButton;
ボタンを押したと時のアクション
    -command "myFunction()"''',
                        'button -query -label myButton;',
                        "UI_Sample_Button")
    add_ui_with_buttons(lambda: (
        cmds.symbolButton(image=image_path + r"\\amiTools\\Image\\amiIcon.png", w=50, h=50)
    ),
    "symbolButton",
    'cmds.symbolButton("mySymbolButton", label="ボタン")',
    '''cmds.symbolButton("mySymbolButton", query=True, label=True)
    ボタンを押したと時のアクション
    command=lambda *args:function()''',
    "画像をボタンに出来る",
    'symbolButton -image ("amiTools\\Image\\amiIcon.png") -width 50 -height 50 mySymbolButton;',
    'symbolButton -query -label mySymbolButton;',
                        "UI_Sample_Button")

    add_ui_with_buttons(lambda: cmds.checkBox("myCheckBox", label="チェックボックス"),
                        "CheckBox",
                        'cmds.checkBox("myCheckBox", label="チェックボックス")',
                        """cmds.checkBox("myCheckBox", query=True, value=True)
チェックオンでアクション
    onCommand=lambda *args: function()
チェックオフでアクション
    offCommand=lambda *args: function()""",
                        "チェックボックス",
                        '''checkBox -label "チェックボックス" myCheckBox;'
チェックオンでアクション
-onCommand "functionOn()"
チェックオフでアクション
-offCommand "functionOff()" ''',
                        'checkBox -query -value myCheckBox;',
                        "UI_Sample_Button")

    add_ui_with_buttons(lambda: cmds.radioButtonGrp("myRadioButtonGrp",
                        numberOfRadioButtons=3, labelArray3=["test1", "test2", "test3"], select=1),
                        "Radio Button",
                        '''cmds.radioButtonGrp("myRadioButtonGrp",
                        numberOfRadioButtons=3, labelArray3=["test1", "test2", "test3"], select=1)''',
                        'cmds.radioButtonGrp("myRadioButtonGrp", query=True, select=True)',
                        "ラジオボタン/n複数チェックを許したくない時に使う",
                        'radioButtonGrp -numberOfRadioButtons 3 -labelArray3 "test1" "test2" "test3" -select 1 myRadioButtonGrp;',
                        'radioButtonGrp -query -select myRadioButtonGrp;',
                        "UI_Sample_Button")
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
    "ドロップダウンメニューを作成",
    'optionMenu -label "optionMenu" -width 150 myOptionMenu;',
    'optionMenu -query -value myOptionMenu;',
                        "UI_Sample_Button")
    cmds.setParent("..")
    #-----------------------------------------------
    # 入力系
    #-----------------------------------------------
    cmds.columnLayout("UI_Sample_Input")
    cmds.separator(height=10)
    add_ui_with_buttons(lambda: cmds.text(label="サンプルテキスト"),
                        "Text Label",
                        'cmds.text("myText", label="サンプルテキスト")',
                        'cmds.text("myText", query=True, label=True)',
                        "テキストを表示できる",
                        'text -label "サンプルテキスト" myText;',
                        'text -query -label myText;',
                        "UI_Sample_Input")
    
    add_ui_with_buttons(lambda: cmds.textField("myTextField", text="テキスト入力", w=200),
                        "Text Field",
                        'cmds.textField("myTextField", text="テキスト入力", w=200)',
                        'cmds.textField("myTextField", query=True, text=True)',
                        "テキストを入力できる",
                        'textField -text "テキスト入力" -width 200 myTextField;',
                        'textField -query -text myTextField;',
                        "UI_Sample_Input")
    
    add_ui_with_buttons(lambda: cmds.scrollField("myScrollField",
                width=200, height=100, text="testText1\ntestText2\ntestText3\n"),
    "scrollField",
    '''cmds.scrollField("myScrollField", text="好きなテキストを入力")
    \\nで改行''',
    '''cmds.scrollField("myScrollField", query=True, text=True)''',
    "スクロール可能なテキストボックス\n複数データを表示する時とかに使う",
    'scrollField -width 200 -height 100 -text "testText1\\ntestText2\\ntestText3" myScrollField;\n\\nで改行',
    'scrollField -query -text myScrollField;',
                        "UI_Sample_Input")
    add_ui_with_buttons(lambda: cmds.floatSliderGrp("myFloatSlider", label="Float Slider", field=True, minValue=0, maxValue=1, value=0.5),
                        "Float Slider",
                        'cmds.floatSliderGrp("myFloatSlider", label="Float Slider", field=True, minValue=0, maxValue=1, value=0.5)',
                        """cmds.floatSliderGrp("myFloatSlider", query=True, value=True)
スライダーの変化に反応してアクション
    changeCommand=lambda value: function(value)
      ->valueには変更されたスライダー数値が入る""",
                        "小数を調整できるスライダー。",
                        ''
                        ''
                        '''floatSliderGrp
-label "Float Slider" -field true
-minValue 0
-maxValue 1
-value 0.5
//スライダーの変化に反応してアクション
-changeCommand "functionName($value)"
    //->valueには変更された整数値が入る
myFloatSlider;''',
                        'floatSliderGrp -query -value myFloatSlider;',
                        "UI_Sample_Input")
    
    add_ui_with_buttons(lambda: cmds.intSliderGrp("myIntSlider", label="Int Slider", field=True, minValue=0, maxValue=10, value=5),
                        "Int Slider",
                        'cmds.intSliderGrp("myIntSlider", label="Int Slider", field=True, minValue=0, maxValue=10, value=5)',
                        '''cmds.intSliderGrp("myIntSlider", query=True, value=True)
スライダーの変化に反応してアクション
    changeCommand=lambda value: function(value)
      ->valueには変更された整数値が入る''',
    "整数を調整できるスライダー。",
                        '''intSliderGrp -label "Float Slider"
-field true
-minValue 0
-maxValue 10
-value 5
//スライダーの変化に反応してアクション
-changeCommand "functionName($value)"
    //->valueには変更された整数値が入る
myFloatSlider;
    ''',
    'intSliderGrp -query -value myIntSlider;',
                        "UI_Sample_Input")
    cmds.setParent("..")
    cmds.tabLayout("UI_Sample_MainTab",innerMarginWidth=10, innerMarginHeight=10, edit=True, tabLabel=[
        ("UI_Sample_Layout", u"レイアウト関係"),
        ("UI_Sample_Button", u"ボタン関係"),
        ("UI_Sample_Input", u"入力関係"),
    ])


    cmds.showWindow(window)


