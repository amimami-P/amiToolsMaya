#------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------
import maya.cmds as cmds

#------------------------------------------------------------------------------------
#node_nameは関連ノードの命名に使用
#targetは揺らしたいノード名
#Attrは数値を入れたいAttrを指定(rotate / translate)
#Noise用のパラメータシェイプはtarget指定したノードにペアレントしています
#------------------------------------------------------------------------------------
def NoiseCreate(nodeName,target,Attr):
    """ノイズ用のノード群生成
    
    node_nameは関連ノードの命名に使用
    Attrは数値を入れたいAttrを指定(rotate / translate)
    """
    cmds.undoInfo(openChunk=True)

    #一応引数エラー処理(rotate / translate)以外がAttrに入ったらエラー
    if "Rotate" in Attr or "Translate" in Attr:
        attrFlag = True
    else :
        print ("--------error----------")
        print ("関数NoiseCreate(node_name,target,Attr)")
        print (u"引数Attrに対応外のアドリビュートが指定されています")
        attrFlag = False

    if attrFlag == True:
        if Attr == "inTranslate":
            type = "Trans"
        elif  Attr == "inRotate":
            type = "Rotate"
        baseName = nodeName + "_" + type

        time = "time1"
        timeOffset = cmds.createNode("plusMinusAverage", n= baseName + "_time_offset")
        cmds.connectAttr(time + ".outTime" , timeOffset + ".input1D[0]")

        uvCycle = cmds.createNode("multiplyDivide", n= baseName + "_uv_cycle")
        cmds.setAttr(uvCycle + ".operation",2)
        cmds.setAttr(uvCycle + ".input2X", 20)
        cmds.connectAttr(timeOffset + ".output1D", uvCycle + ".input1X")

        frequency = cmds.createNode("multiplyDivide", n= baseName + "_frequency")
        cmds.connectAttr(uvCycle + ".outputX",frequency + ".input1X")

        #------------------------------------------------------------------------------------
        uvOffset = cmds.createNode("place2dTexture", n= baseName + "_uv_offset")
        cmds.connectAttr(frequency + ".outputX", uvOffset + ".offsetU")
        #------------------------------------------------------------------------------------
        # Noiseノード作成
        #------------------------------------------------------------------------------------
        xNoise = cmds.createNode("noise", n= baseName + "_noise_x")
        yNoise = cmds.createNode("noise", n= baseName + "_noise_y")
        cmds.setAttr(xNoise + ".noiseType", 0)
        cmds.setAttr(yNoise + ".noiseType", 0)
        cmds.setAttr(xNoise + ".frequency", 2)
        cmds.setAttr(yNoise + ".frequency", 2)
        cmds.connectAttr(uvOffset + ".outUvFilterSize", xNoise + ".uvFilterSize")
        cmds.connectAttr(uvOffset + ".outU", xNoise + ".uCoord")
        cmds.connectAttr(uvOffset + ".outV", xNoise + ".vCoord")

        zNoise = cmds.createNode("noise", n= baseName + "_noise_z")
        cmds.setAttr(zNoise + ".noiseType", 0)
        cmds.setAttr(zNoise + ".frequency", 2)

        #------------------------------------------------------------------------------------
        #UVスクロールする用ノイズ接続
        cmds.connectAttr(uvOffset + ".outUvFilterSize", yNoise + ".uvFilterSize")
        yNoiseTure = cmds.createNode("plusMinusAverage", n= baseName + "_y_noise_offset")
        cmds.connectAttr(uvOffset + ".outV", yNoiseTure + ".input1D[0]")
        cmds.setAttr(yNoiseTure + ".input1D[1]", 45)
        cmds.connectAttr(yNoiseTure + ".output1D", yNoise + ".vCoord")
        cmds.connectAttr(uvOffset + ".outU", yNoise + ".uCoord")
        cmds.connectAttr(uvOffset + ".outUvFilterSize", zNoise + ".uvFilterSize")
        zNoiseTure = cmds.createNode("plusMinusAverage", n= baseName + "_z_noise_offset")
        cmds.connectAttr(uvOffset + ".outV", zNoiseTure + ".input1D[0]")
        cmds.setAttr(zNoiseTure + ".input1D[1]", 20)
        cmds.connectAttr(zNoiseTure + ".output1D", zNoise + ".vCoord")
        cmds.connectAttr(uvOffset + ".outU", zNoise + ".uCoord")
        #------------------------------------------------------------------------------------
        # ノイズから取得した値を-1～1に補完
        amplitudeOffset = cmds.createNode("multiplyDivide", n= baseName + "_amplitude_offset")
        noiseValueDouble =  cmds.createNode("multiplyDivide", n= baseName + "_double_offset")
        cmds.setAttr(noiseValueDouble + ".input2X",2)
        cmds.connectAttr(xNoise + ".outColorR", noiseValueDouble + ".input1X")
        noiseValueXMinus = cmds.createNode("plusMinusAverage", n= baseName + "_x_minus_offset")
        cmds.connectAttr(noiseValueDouble + ".outputX", noiseValueXMinus + ".input1D[0]")
        cmds.setAttr(noiseValueXMinus + ".input1D[1]",-1)
        cmds.connectAttr(noiseValueXMinus + ".output1D",amplitudeOffset + ".input1X")
        cmds.setAttr(noiseValueDouble + ".input2Y",2)
        cmds.connectAttr(yNoise + ".outColorR", noiseValueDouble + ".input1Y")
        noiseValueYMinus = cmds.createNode("plusMinusAverage", n= baseName + "_y_minus_offset")
        cmds.connectAttr(noiseValueDouble + ".outputY", noiseValueYMinus + ".input1D[0]")
        cmds.setAttr(noiseValueYMinus + ".input1D[1]",-1)
        cmds.connectAttr(noiseValueYMinus + ".output1D",amplitudeOffset + ".input1Y")
        cmds.setAttr(noiseValueDouble + ".input2Z",2)
        cmds.connectAttr(zNoise + ".outColorR", noiseValueDouble + ".input1Z")
        noiseValueZMinus = cmds.createNode("plusMinusAverage", n= baseName + "_z_minus_offset")
        cmds.connectAttr(noiseValueDouble + ".outputZ", noiseValueZMinus + ".input1D[0]")
        cmds.setAttr(noiseValueZMinus + ".input1D[1]",-1)
        cmds.connectAttr(noiseValueZMinus + ".output1D",amplitudeOffset + ".input1Z")

        #intensityノード作成//最終的にこのノードが揺らしたいオブジェクトに繋がる
        intensityOffset = cmds.createNode("multiplyDivide", n= baseName + "_Intensity_offset")
        cmds.connectAttr(amplitudeOffset + ".outputX", intensityOffset + ".input1X")
        cmds.connectAttr(amplitudeOffset + ".outputY", intensityOffset + ".input1Y")

        cmds.connectAttr(intensityOffset + ".outputX", target + "." + Attr + "X2")
        cmds.connectAttr(intensityOffset + ".outputY", target + "." + Attr + "Y2")
        cmds.connectAttr(amplitudeOffset + ".outputZ", intensityOffset + ".input1Z")
        cmds.connectAttr(intensityOffset + ".outputZ", target + "." + Attr + "Z2")
        #------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------
        noiseParam = nodeName

        if Attr == "inTranslate":
            type = "Trans"
        elif  Attr == "inRotate":
            type = "Rotate"
        cmds.addAttr(noiseParam, ln= "Noise_" + type + "_Amplitude", at="float", dv=0, k=True)
        cmds.addAttr(noiseParam,  ln= "Noise_" + type + "_Frequency", at="float", dv=0,  k=True)
        cmds.addAttr(noiseParam,  ln= "Noise_" + type + "_Offset", at="float", dv=0,  k=True)

        cmds.addAttr(noiseParam, ln=  "Noise_" + type + "_X_Intensity", at="float", dv=1, k=True)
        cmds.addAttr(noiseParam,  ln=  "Noise_" + type + "_Y_Intensity", at="float", dv=1,  k=True)
        cmds.addAttr(noiseParam,  ln=  "Noise_" + type + "_Z_Intensity", at="float", dv=1,  k=True)
        cmds.setAttr(noiseParam + ".Noise_" + type + "_Frequency", keyable=False, channelBox=True)

        cmds.connectAttr(noiseParam + ".Noise_" + type + "_Amplitude", amplitudeOffset + ".input2X")
        cmds.connectAttr(noiseParam + ".Noise_" + type + "_Amplitude", amplitudeOffset + ".input2Y")
        cmds.connectAttr(noiseParam + ".Noise_" + type + "_Amplitude", amplitudeOffset + ".input2Z")
        cmds.connectAttr(noiseParam + ".Noise_" + type + "_Frequency", frequency + ".input2X")
        cmds.connectAttr(noiseParam + ".Noise_" + type + "_Offset", timeOffset + ".input1D[1]")

        cmds.connectAttr(noiseParam + ".Noise_" + type + "_X_Intensity", intensityOffset + ".input2X")
        cmds.connectAttr(noiseParam + ".Noise_" + type + "_Y_Intensity", intensityOffset + ".input2Y")
        cmds.connectAttr(noiseParam + ".Noise_" + type + "_Z_Intensity", intensityOffset + ".input2Z")

#------------------------------------------------------------------------------------------
def ctrlShape(name):
    cmds.curve(name=name,d=1,
        p=[(0.0, 0.0, 0.0), (11.25, 0.0, 0.0), (15.0, 3.75, 0.0),
            (18.75, 0.0, 0.0), (15.0, -3.75, 0.0), (11.25, 0.0, 0.0),
            (15.0, 0.0, 3.75), (18.75, 0.0, 0.0), (15.0, 0.0, -3.75),
            (15.0, 3.75, 0.0), (15.0, 0.0, 3.75), (15.0, -3.75, 0.0),
            (15.0, 0.0, -3.75), (11.25, 0.0, 0.0), (0.0, 0.0, 0.0),
            (-11.25, 0.0, 0.0), (-15.0, 3.75, 0.0), (-18.75, 0.0, 0.0),
            (-15.0, -3.75, 0.0), (-11.25, 0.0, 0.0), (-15.0, 0.0, 3.75),
            (-18.75, 0.0, 0.0), (-15.0, 0.0, -3.75), (-15.0, 3.75, 0.0),
            (-15.0, 0.0, 3.75), (-15.0, -3.75, 0.0), (-15.0, 0.0, -3.75),
            (-11.25, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 11.25, 0.0),
            (0.0, 15.0, -3.75), (0.0, 18.75, 0.0), (0.0, 15.0, 3.75),
            (0.0, 11.25, 0.0), (-3.75, 15.0, 0.0), (0.0, 18.75, 0.0),
            (3.75, 15.0, 0.0), (0.0, 15.0, 3.75), (-3.75, 15.0, 0.0),
            (0.0, 15.0, -3.75), (3.75, 15.0, 0.0), (0.0, 11.25, 0.0),
            (0.0, 0.0, 0.0), (0.0, -11.25, 0.0), (0.0, -15.0, -3.75),
            (0.0, -18.75, 0.0), (0.0, -15.0, 3.75), (0.0, -11.25, 0.0),
            (-3.75, -15.0, 0.0), (0.0, -18.75, 0.0), (3.75, -15.0, 0.0),
            (0.0, -15.0, -3.75), (-3.75, -15.0, 0.0), (0.0, -15.0, 3.75),
            (3.75, -15.0, 0.0), (0.0, -11.25, 0.0), (0.0, 0.0, 0.0),
            (0.0, 0.0, -11.25), (0.0, 3.75, -15.0), (0.0, 0.0, -18.75),
            (0.0, -3.75, -15.0), (0.0, 0.0, -11.25), (-3.75, 0.0, -15.0),
            (0.0, 0.0, -18.75), (3.75, 0.0, -15.0), (0.0, 3.75, -15.0),
            (-3.75, 0.0, -15.0), (0.0, -3.75, -15.0), (3.75, 0.0, -15.0),
            (0.0, 0.0, -11.25), (0.0, 0.0, 0.0), (0.0, 0.0, 11.25),
            (0.0, 3.75, 15.0), (0.0, 0.0, 18.75), (0.0, -3.75, 15.0),
            (0.0, 0.0, 11.25), (-3.75, 0.0, 15.0), (0.0, 0.0, 18.75),
            (3.75, 0.0, 15.0), (0.0, 3.75, 15.0), (-3.75, 0.0, 15.0),
            (0.0, -3.75, 15.0), (3.75, 0.0, 15.0), (0.0, 0.0, 11.25)]
            )

    cmds.rename(cmds.listRelatives(name,c=True, s=True, type="nurbsCurve"),name + "Shape" )
    cmds.setAttr(name + ".overrideEnabled", 1)
    cmds.setAttr(name + ".overrideRGBColors", 0)
    cmds.setAttr(name + ".overrideColor", 17)
    cmds.setAttr(name + ".lineWidth",2)
    return name

def noiseShape(name):
    cmds.curve(name=name,d=1,
                p=[(-5, 5, -5), (-5, 5, 5), (5, 5, 5), (5, 5, -5), (-5, 5, -5), (-5, -5, -5), (-5, -5, 5),
                    (5, -5, 5), (5, 5, 5), (-5, 5, 5), (-5, -5, 5), (-5, -5, -5), (5, -5, -5), (5, 5, -5),
                    (5, 5, 5), (5, -5, 5), (5, -5, -5)])
    cmds.rename(cmds.listRelatives(name,c=True, s=True, type="nurbsCurve"),name + "Shape" )
    cmds.setAttr(name + ".overrideEnabled", 1)
    cmds.setAttr(name + ".overrideRGBColors", 0)
    cmds.setAttr(name + ".overrideColor", 18)
    cmds.setAttr(name + ".lineWidth",2)
    return name

def NoiseLocator(name):

    select_flag=False
    select = cmds.ls(sl=True)
    if select:
        select_node = select[0]
        select_flag=True

    Locator = noiseShape(name)


    # Noiseスイッチ用ペアブレンド作成
    noiseSwPb = cmds.createNode("pairBlend",n= Locator + "_Noise_Sw_pb")
    cmds.setAttr(noiseSwPb + ".rotInterpolation", 1)

    cmds.connectAttr(noiseSwPb + ".outRotateX", Locator + ".rx")
    cmds.connectAttr(noiseSwPb + ".outRotateY", Locator + ".ry")
    cmds.connectAttr(noiseSwPb + ".outRotateZ", Locator + ".rz")
    cmds.connectAttr(noiseSwPb + ".outTranslateX", Locator + ".tx")
    cmds.connectAttr(noiseSwPb + ".outTranslateY", Locator + ".ty")
    cmds.connectAttr(noiseSwPb + ".outTranslateZ", Locator + ".tz")

    ctrl = ctrlShape(Locator + "_Ctrl")
    cmds.parent(Locator,ctrl)
    cmds.addAttr(ctrl, ln="Attr_Spacer", at="enum",nn="- -", en="Rotate:  :", k=True)
    NoiseCreate(ctrl,noiseSwPb,"inRotate")
    cmds.addAttr(ctrl, ln="Attr_Spacer_1", at="enum",nn="- -", en="Trans:  :", k=True)
    NoiseCreate(ctrl,noiseSwPb,"inTranslate")

    cmds.setAttr( Locator + ".rotate", keyable=False,lock=True, channelBox=True)
    cmds.setAttr( Locator + ".translate", keyable=False,lock=True, channelBox=True)
    if select_flag ==True:
        position = cmds.xform(select_node, query=True, worldSpace=True, translation=True)
        cmds.setAttr(ctrl + ".tx",position[0])
        cmds.setAttr(ctrl + ".ty",position[1])
        cmds.setAttr(ctrl + ".tz",position[2])

def NoiseController():
    count = 1
    while True:
        if  cmds.objExists("NoiseController_" + str(count)) == False:
            NoiseLocator(name="NoiseController_" + str(count))
            cmds.inViewMessage(
                smg=f"NoiseController_{str(count)}を作成しました" ,
                pos="topCenter",
                bkc=0x00000000,
                fadeStayTime=3000,
                fade=True,
                )
            cmds.select(clear=True)
            break
        else:
            count = count + 1

