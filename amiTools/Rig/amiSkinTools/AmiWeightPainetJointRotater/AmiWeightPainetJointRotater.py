import maya.cmds as cmds

def AmiWPJR_Targetset():
    if cmds.radioButtonGrp("miWPJR_Radio", query=True, select=True) == 2:
        return
    ctx = cmds.currentCtx()
    if cmds.contextInfo(ctx, query=True, title=True) == "Paint Skin Weights Tool":

        # 現在ペイント中のジョイント（インフルエンス）を取得
        edit_influence = cmds.artAttrSkinPaintCtx(ctx, query=True, influence=True)
        cmds.textField("AmiWPJR_Target", text=edit_influence,edit=True )
            

def AmiWPJR_RotX(val,):
    AmiWPJR_Targetset()
    jnt = cmds.textField("AmiWPJR_Target", text=True,query=True, )
    cmds.setAttr(f"{jnt}.rx",val)

def AmiWPJR_RotY(val,):
    AmiWPJR_Targetset()
    jnt = cmds.textField("AmiWPJR_Target", text=True,query=True, )
    cmds.setAttr(f"{jnt}.ry",val)

def AmiWPJR_RotZ(val,):
    AmiWPJR_Targetset()
    jnt = cmds.textField("AmiWPJR_Target", text=True,query=True, )
    cmds.setAttr(f"{jnt}.rz",val)

def AmiWPJR_RotReset():
    try:
        cmds.floatSliderGrp('AmiWPJR_RotXSlider',edit=True,value=0)
        cmds.floatSliderGrp('AmiWPJR_RotYSlider',edit=True,value=0)
        cmds.floatSliderGrp('AmiWPJR_RotZSlider',edit=True,value=0)
    except:
        pass
    AmiWPJR_Targetset()
    jnt = cmds.textField("AmiWPJR_Target", text=True,query=True, )
    cmds.setAttr(f"{jnt}.rotate",0,0,0)

def AmiWeightPainetJointRotater():
    if cmds.window("AmiWeightPainetJointRotater", exists=True):
        cmds.deleteUI("AmiWeightPainetJointRotater")
    ctx = cmds.currentCtx()
    if cmds.contextInfo(ctx, query=True, title=True) == "Paint Skin Weights Tool":
        if cmds.workspaceControl("AmiWeightPainetJointRotater", exists=True):
            cmds.deleteUI("AmiWeightPainetJointRotater", control=True)

        cmds.workspaceControl(
            "AmiWeightPainetJointRotater",
            label="WeightPainetJointRotater",
            floating=True,
            initialWidth=250,
            initialHeight=180
        )


        cmds.columnLayout(adjustableColumn=True)

        cmds.text(label="WeightPainetJointRotater" )
        
        cmds.separator(height=5)
        cmds.radioButtonGrp("miWPJR_Radio",
                            numberOfRadioButtons=2, labelArray2=["Auto", "Lock", ], select=1)

        cmds.rowLayout(numberOfColumns=3)

        cmds.text(label="Target :" )
        cmds.textField("AmiWPJR_Target", text="",edit=False ,w=200)
        cmds.setParent("..")

        cmds.separator(height=5)
        cmds.text(label="RotateX")
        cmds.floatSliderGrp(
            'AmiWPJR_RotXSlider',
            field=True,
            min=-180,
            max=180,
            value=0,
            step=0.1,
            dragCommand=AmiWPJR_RotX
        )
        cmds.separator(height=5)
        cmds.text(label="RotateY")
        cmds.floatSliderGrp(
            'AmiWPJR_RotYSlider',
            field=True,
            min=-180,
            max=180,
            value=0,
            step=0.1,
            dragCommand=AmiWPJR_RotY
        )
        cmds.separator(height=5)
        cmds.text(label="RotateZ")
        cmds.floatSliderGrp(
            'AmiWPJR_RotZSlider',
            field=True,
            min=-180,
            max=180,
            value=0,
            step=0.1,
            dragCommand=AmiWPJR_RotZ
        )
        cmds.separator(height=20)
        cmds.button("myButton", label="Reset",h=30,command=lambda *args:AmiWPJR_RotReset())

        cmds.setFocus("")
    else:
        cmds.inViewMessage(
            smg=(u"Paint Skin Weights Toolを開いて実行してください"),
            pos="topCenter",
            bkc=0x00000000,
            fadeStayTime=3000,
            fade=True,
            )        
