'''
Closer to camera 3.3

More info on the github project: https://github.com/0x45mi/closerToCamera
Tutorial: https://vimeo.com/765705742

### Changelog
03/01/2024 - Changed default bake to simulation=True, as this is safer.
'''

import maya.cmds as cmds
import maya.mel as mm

loadObjects = set()
layersCB = True

            
start = cmds.playbackOptions( q=True, min=True )
end  = cmds.playbackOptions( q=True, max=True )

gChannelBoxName = mm.eval('$temp=$gChannelBoxName')

#colours
green = [0.5, 0.8, 0.2]
red = [0.4, 0.0, 0.0]
darkGrey = [0.25, 0.25, 0.25]
lightGrey = [0.365, 0.365, 0.365]

def field_add(txt_field, x):
    sel= cmds.ls(sl=True)
    if not sel:
        raise RuntimeError("Please select objects to load")
    if x == 1:
        if cmds.nodeType(sel[0]) != "transform":
            sel= cmds.listRelatives(parent=True)
        cmds.textField(txt_field, edit=True, tx=sel[0], backgroundColor=green)
    else:
        global loadObjects
        loadObjects.update(sel)     
        cmds.textField(txt_field, edit=True, tx=', '.join(loadObjects), backgroundColor=green)        

def field_clear(txt_field):
    cmds.textField(txt_field, edit=True, tx="", backgroundColor=darkGrey)
    if txt_field == "TF02":
        global loadObjects
        loadObjects.clear()

def check_list():
    if (cmds.textField("TF01", q=True, text=1) != "") and (cmds.textField("TF02", q=True, text=1) != ""):
        for i in loadObjects:
            if (cmds.objExists("scaleLoc_" + i)) or (cmds.objExists(i+ "_offset")):
                raise RuntimeError("Object already in a closer to camera setup")
            else: return True
    else: 
        raise RuntimeError("Please load objects to continue")  
              
def create_list():    
    if len(loadObjects) == 1: lista = list(loadObjects)
    else: lista = average_points()        
    lista.insert(0, cmds.textField("TF01", q=True, text=1))
    return lista

def add_implicit_str_attr(ctrl, i):
    cmds.addAttr(ctrl, longName="implicit", dataType="string", ct="emi_closerToCamera") 
    cmds.setAttr(ctrl+ ".implicit", i, type="string", lock=True)


def average_points():
    selection = list(loadObjects)
    master = cmds.spaceLocator(name= "scaleOffset_"+ selection[0])
    babies=[]
    for i in selection:
        child= cmds.spaceLocator(name="scaleLoc_offset_"+ i)
        add_implicit_str_attr(child[0], i)
        babies.append(child[0])        
        cmds.parentConstraint(i, child, mo=False)
        cmds.parentConstraint(i, master, mo=False)
    
    cmds.bakeResults(master, simulation=layersCB, at=["tx","ty","tz","rx","ry","rz"], time=(start,end), animation="objects", sampleBy=1.0, disableImplicitControl=True);
    
    for i in babies:
        cmds.parent(i, master)
    for i in babies:
        cmds.select(i, add=True)
  
    cmds.bakeResults(simulation=layersCB, at=["tx","ty","tz"], time=(start,end), animation="objects", sampleBy=1.0, disableImplicitControl=True); 
    cmds.delete(cmds.listRelatives(master, ad=1, type='parentConstraint'))
    
    for i in babies:
        cmds.pointConstraint(i, implicit(i), name="scaleToCamera_" +i + "_pointConstraint", mo=True)

    return master          

def scale_to_camera():
    
    if check_list():
        
        if layersCB:
            cmds.ogs(pause=True)
        
        lista = create_list()
        cam=[]
        locators =[]
        
        for i in lista:
            if i == lista[0]:
                locator = cmds.spaceLocator(name= "scaleLoc_cam_" + "##")
                objPosition = cmds.xform(i, q=True,t=True,ws=True)
                cmds.xform(locator, ws=True, translation=objPosition)
                cmds.pointConstraint(i, locator, mo=True)
                cmds.orientConstraint(i, locator, mo=False)
                locators.append(locator[0]); cam.append(locator[0])
            elif i != lista[0]:
                locator = cmds.spaceLocator(name= "scaleLoc_" + i)
                add_implicit_str_attr(locator[0], i)
                cmds.addAttr(locator, longName="ScaleToCamera", niceName="Scale to Camera", at= "float", dv=1, min=0, hnv=True, hxv=False, readable=True, keyable=True, hidden=False)
                cmds.connectAttr(locator[0]+'.ScaleToCamera', locators[0]+'.sx')
                cmds.connectAttr(locator[0]+'.ScaleToCamera', locators[0]+'.sy')
                cmds.connectAttr(locator[0]+'.ScaleToCamera', locators[0]+'.sz')

                cmds.pointConstraint(i, locator, mo=False)
                cmds.parent(locator, locators[0])

                locators.append(locator[0])
        
        for i in locators:
            cmds.select(i, add=True);        
        cmds.bakeResults(simulation=layersCB, at=["tx","ty","tz","rx","ry","rz"], time=(start,end), animation="objects", sampleBy=1.0, disableImplicitControl=False);
        cmds.delete(cmds.listRelatives(locators[0], allDescendents=True, type='constraint')) 
        locators.pop(0)

        for i in locators:
            cmds.pointConstraint(i, implicit(i), name="scaleToCamera_" +i + "_pointConstraint", mo=True)

        if lista[1].find("scaleOffset_") >= 0: 
            cmds.group (lista[1], cam[0], name= "closer_to_camera_setup###")

        cmds.textScrollList("TSL01", edit=True, append=[str(locators[0])])
        
        if layersCB:
            cmds.ogs(pause=True)

def refresh_STL():
    cmds.textScrollList("TSL01", edit=True, removeAll=True)
    cmds.button("B04", edit=True, label="Toggle", enableBackground=True, backgroundColor=lightGrey)
    if cmds.objExists('scaleLoc_cam_*'):
        to_load= cmds.ls((cmds.listRelatives('scaleLoc_cam_*')), exactType='transform')
        for i in to_load:
            cmds.textScrollList("TSL01", edit=True, append=[i])
    
def cleanup():
    for i in (cmds.textScrollList("TSL01", query=True, allItems=True)):
        for n in get_ctrl(i):
            if cmds.listRelatives(n, children=True, type='pointConstraint'): pass
            else: delete_setup(i); break

def check_select():
    return(cmds.textScrollList("TSL01", query=True, selectItem=True))[0]

def implicit(n):
    return(cmds.getAttr(n+ ".implicit"))

def get_ctrl(n):
    getCtrl=[]
    getCtrl.append(implicit(n))
    if getCtrl[0].find("scaleOffset_") >= 0:
        getCtrl= cmds.ls(cmds.listRelatives(getCtrl[0]), exactType='transform')
        for i in getCtrl: getCtrl[getCtrl.index(i)]= implicit(i)
    return getCtrl

def getTop(node):
    topNode = ''
    par = cmds.listRelatives(node, p=True)
    if par != None:
        topNode = getTop(par)
        node = par[0]
        return topNode
    else:
        return node  

def update_slider():
    attr_val = cmds.getAttr(check_select()+ '.ScaleToCamera')
    max_val = attr_val*2
    cmds.floatSlider( "slideScale", edit=True, maxValue=max_val)   
    
def pick_item():
    cmds.select(check_select())
    cmds.connectControl('slideScale', check_select()+'.ScaleToCamera')
    update_slider()
    if cmds.getAttr(pointAttr()) == 0: cmds.button("B04", edit=True, label="Control OFF", enableBackground=True, backgroundColor=red)
    elif cmds.getAttr(pointAttr()) == 1: cmds.button("B04", edit=True, label="Control ON", enableBackground=True, backgroundColor=green)

    #it's not a bug, it's a *feature*
    cmds.channelBox(gChannelBoxName , edit=True, select=(True, check_select()+".ScaleToCamera"))
    
def set_key():
    cmds.setKeyframe(check_select()+ '.ScaleToCamera')
    
def set_zero_key():
    cmds.setAttr(check_select()+ '.ScaleToCamera', 1)
    set_key()

def delete_setup(item):
    cmds.delete(getTop(item))
    refresh_STL()
                
def bake():
    save = check_select()
    cmds.select(clear=True)
    for i in get_ctrl(check_select()): cmds.select(i, add=True)
    if layersCB:
            cmds.ogs(pause=True)
    cmds.bakeResults(simulation=layersCB, attribute=["tx","ty","tz"], time=(start,end), animation="objects", sampleBy=1.0, disableImplicitControl=True, preserveOutsideKeys=True, bakeOnOverrideLayer=True)
    if layersCB:
            cmds.ogs(pause=True)
    delete_setup(save)   
    refresh_STL()
          
def pointAttr():
    point= cmds.listConnections(implicit(check_select()), type='pointConstraint')[0]
    try: check_select().index(":"); attrStr= check_select().rsplit(":", 1)[1]
    except: attrStr= check_select()         
    attr = cmds.listAttr(point, string=attrStr+ "*")[0]
    return (point+ "."+ attr)

def blendAttrFunc(blendAttr, ctrl):
    try: blendAttr.append(cmds.listConnections(cmds.listConnections(ctrl, type="pairBlend")[0]+ ".weight", plugs=True)[0])    
    except: 
        try: blendAttr.append(cmds.listConnections(ctrl, type="pairBlend")[0]+ ".weight")
        except: pass
       
def blendAttr():
    blendAttr=[]
    blendAttrFunc(blendAttr, implicit(check_select()))                
    if len(get_ctrl(check_select())) > 1:
        for i in get_ctrl(check_select()):
            blendAttrFunc(blendAttr, i)
    return blendAttr
   
def enable_disable():
    if cmds.getAttr(pointAttr()) != 0:
        cmds.setAttr(pointAttr(), 0)
        for i in blendAttr():
            cmds.setAttr(i, 0)
        cmds.button("B04", edit=True, label="Control OFF", enableBackground=True, backgroundColor=red)
    else: 
        cmds.setAttr(pointAttr(), 1)
        for i in blendAttr():
            cmds.setAttr(i, 1)
        cmds.button("B04", edit=True, label="Control ON", enableBackground=True, backgroundColor=green)

def updatelayersCB():
    layersCB = cmds.menuItem("Layers", q=True, checkBox=True) 
    
#_________________UI__________________#

def ui():
    if cmds.window('emi_closerToCamera', exists=True):
        cmds.deleteUI('emi_closerToCamera')

 
    cmds.window('emi_closerToCamera', title="Closer to camera")

    cmds.columnLayout( columnAttach=('both', 0), adjustableColumn=True, rowSpacing=1)
    cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 80), (2, 320), (3, 24)], rowOffset=[1, 'top', 2], rowSpacing=[(1,2)], adjustableColumn=2, columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)] )

    cmds.button("Load Camera", command=lambda *x:field_add("TF01", 1), annotation='Select camera or pivot object to load. This field takes only one selection')    
    cmds.textField('TF01', ed=False)
    cmds.iconTextButton(style="iconOnly", image='delete.png', command=lambda *x:field_clear("TF01"), annotation='Clear field')
    cmds.button("Load Objects", command=lambda *x:field_add("TF02", 0), annotation='Select controls to load') 
    cmds.textField('TF02', ed=False)
    cmds.iconTextButton(style="iconOnly", image='delete.png', command= lambda *x:field_clear("TF02"), annotation='Clear field')

    cmds.setParent( '..' )
    cmds.rowColumnLayout( numberOfColumns=1, columnWidth=[(1, 80)], adjustableColumn=1, columnAttach=[(1, 'both', 0)])
    cmds.button(label="Create!", command=lambda *x:scale_to_camera(), annotation='Create closer to camera setup')

    cmds.separator() 
    cmds.textScrollList('TSL01', height=80, allowMultiSelection=False, selectCommand=lambda *x:pick_item())
    cmds.popupMenu()
    cmds.menuItem('Refresh', command=lambda *x:refresh_STL())
    cmds.menuItem('Cleanup', command=lambda *x:cleanup())
    cmds.menuItem('Layers', checkBox=(1), command=lambda *x:updatelayersCB())

    cmds.setParent( '..' )
    cmds.rowLayout(numberOfColumns=4, columnWidth4=(24, 350, 20, 24), adjustableColumn=2, columnAlign=(1, 'center'), columnAttach=[(1, 'left', 4), (2, 'both', 2), (3, 'both', 0), (4, 'right', 2)] )
    cmds.picture(image='Camera.png') 
    cmds.floatSlider('slideScale', enable=False, minValue=0.0, maxValue=2.0, step=.1, changeCommand=lambda *x:update_slider())

    cmds.iconTextButton(style='iconOnly', image='setKeyframe.png', height=19, annotation='Set Key', command=lambda *x:set_key())
    cmds.iconTextButton(style='iconOnly', image='zeroKey.png', annotation='Set Zero Key', command=lambda *x:set_zero_key())

    cmds.setParent( '..' )
    cmds.paneLayout(configuration="vertical3")
    cmds.button('B04', label = "Toggle", command=lambda *x:enable_disable(), annotation='Toggle implicit control')
    cmds.button(label= "Bake", command=lambda *x:bake(), annotation='Bake changes to layer and delete setup')
    cmds.button(label="Delete", command=lambda *x:delete_setup(check_select()), annotation='Delete setup')

    cmds.showWindow()
    refresh_STL()
