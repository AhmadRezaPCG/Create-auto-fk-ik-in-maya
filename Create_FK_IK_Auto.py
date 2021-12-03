###############################################################################
# Name: 
#   Create auto FK IK in maya
#
# Description: 
#   Quickly created IK and FK just by one click . 
#   
#
# Author: 
#   Ahmadreza Rezaei
#
# Copyright (C) 2022 Ahmadreza Rezaei. All rights reserved.
###############################################################################


import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.OpenMaya as om

from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

def maya_main_window():
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window),QtWidgets.QWidget)
    
class create_fk_ik_class(QtWidgets.QDialog):
    
    FK_LIST_NAME = []
    IK_LIST_NAME = []
    BIND_JOINTS = []
    removed_list_obj = []
    
    numb = None
    
    dialog_reference = None
    
    
    def __init__(self,parent=maya_main_window()):
        super(create_fk_ik_class,self).__init__(parent)
        
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(900)
        self.setMaximumHeight(100)
        
        self.createwidget()
        self.createlayout()
        self.connectsignalslot()
    
    @classmethod
    def show_dialog(cls):
        
        if cls.dialog_reference:
                
            if cls.dialog_reference.isHidden():
                cls.dialog_reference.show()
            else:
                cls.dialog_reference.raise_()
                cls.dialog_reference.activateWindow()
        else:
            cls.dialog_reference = create_fk_ik_class()
            cls.dialog_reference.show()    


    def createwidget(self):
        
        self.LE_startjnt = QtWidgets.QLineEdit()
        self.LE_startjnt.setPlaceholderText("JNT_thigh")
        self.LE_lastjnt = QtWidgets.QLineEdit()
        self.LE_lastjnt.setPlaceholderText("JNT_ankle")
        
        self.PB_refresh = QtWidgets.QPushButton("Refresh")
        self.PB_refresh.setToolTip("Select Start And Last joint to Set names joint")
        
        self.CB_prefix_suffix = QtWidgets.QComboBox()
        self.CB_prefix_suffix.editable =False
        
        self.RB_orient = QtWidgets.QRadioButton()
        self.L_orient = QtWidgets.QLabel("Orient")
        
        self.RB_point = QtWidgets.QRadioButton()
        self.RB_point.setChecked(True)
        self.L_point = QtWidgets.QLabel("Point")
        
        self.RB_parent = QtWidgets.QRadioButton()
        self.L_parent = QtWidgets.QLabel("Parent")
        
        self.PB_create = QtWidgets.QPushButton("Create")
        self.PB_cancel = QtWidgets.QPushButton("Cancel")
        
        
        
    
    def createlayout(self):
        
        #___________________________________VL_start_last
        
        VL_start_last = QtWidgets.QVBoxLayout()
        GB_start_last = QtWidgets.QGroupBox("Start_Last_Joint")
        HL_start_last = QtWidgets.QHBoxLayout()
        
        FL_starttext = QtWidgets.QFormLayout()
        FL_starttext.addRow("Start Joint",self.LE_startjnt)
        
        FL_lasttext = QtWidgets.QFormLayout()
        FL_lasttext.addRow("Last Joint",self.LE_lastjnt)
        
        HL_start_last.addLayout(FL_starttext)
        HL_start_last.addLayout(FL_lasttext)
        
        
        VL_start_last.addLayout(HL_start_last)
        VL_start_last.addWidget(self.PB_refresh)
        
        GB_start_last.setLayout(VL_start_last)

        #___________________________________GB_suffix_prefix
        
        GB_suffix_prefix = QtWidgets.QGroupBox("Type Name")
        HL_prefix_suffix = QtWidgets.QHBoxLayout()
        
        HL_prefix_suffix.addWidget(self.CB_prefix_suffix)
        
        GB_suffix_prefix.setLayout(HL_prefix_suffix)
        
        #___________________________________GB_constraint
        
        
        GB_constraint = QtWidgets.QGroupBox("Type constraint")
        HL_constraint = QtWidgets.QHBoxLayout()
        
        HL_orient = QtWidgets.QHBoxLayout()
        HL_orient.addWidget(self.RB_orient)
        HL_orient.addWidget(self.L_orient)
        
        HL_point = QtWidgets.QHBoxLayout()
        HL_point.addWidget(self.RB_point)
        HL_point.addWidget(self.L_point)
        
        HL_parent = QtWidgets.QHBoxLayout()
        HL_parent.addWidget(self.RB_parent)
        HL_parent.addWidget(self.L_parent)
        
        HL_constraint.addLayout(HL_orient)
        HL_constraint.addStretch()
        
        HL_constraint.addLayout(HL_point)
        HL_constraint.addStretch()
        
        HL_constraint.addLayout(HL_parent)
        
        GB_constraint.setLayout(HL_constraint)
        
        #___________________________________HL_button_botom
        
        HL_button = QtWidgets.QHBoxLayout()
        
        HL_button.addStretch()
        HL_button.addWidget(self.PB_create)
        HL_button.addWidget(self.PB_cancel)
        
        #___________________________________main_layout
        
        main_layout = QtWidgets.QVBoxLayout(self)
        
        main_layout.addWidget(GB_start_last)
        main_layout.addStretch()
        
        main_layout.addWidget(GB_suffix_prefix)
        main_layout.addStretch()
        
        main_layout.addWidget(GB_constraint)
        main_layout.addLayout(HL_button)
        
        
    def connectsignalslot(self):
        
        self.PB_refresh.clicked.connect(self.set_name)
        self.PB_cancel.clicked.connect(self.close)
        self.PB_create.clicked.connect(self.create_fk_ik)
    
    def set_name(self):
        
        self.IK_LIST_NAME = []
        self.FK_LIST_NAME = []
        self.BIND_JOINTS = []
        self.removed_list_obj = []
        numb = None
        
        joints_selected = cmds.ls(sl=True,type="joint")
        if joints_selected:
            if len(joints_selected) == 2:
                
                start_joint = joints_selected[0]
                last_joint = joints_selected[1]
                
                # check last_joint is parent of start_joint
                
                hierarchy_start_joint = cmds.listRelatives(start_joint,allDescendents=True)
                if len(hierarchy_start_joint)>0: 
                    for child in hierarchy_start_joint:
                        
                        if last_joint == child :
                            self.set_text(start_joint,last_joint)
                            break
                        elif child != hierarchy_start_joint[-1]:
                            continue
                        else :
                            QtWidgets.QMessageBox.critical(self,'Order Selected',"First select parent joint and then select child joint or your joints have not unique names")
                       
                else :
                    QtWidgets.QMessageBox.critical(self,'Not Exists',"Start joint doesn't have children")
            else:
                QtWidgets.QMessageBox.warning(self,"Count Selected","select start and last joint")
        else:
            QtWidgets.QMessageBox.warning(self,"Selected","Select joints")
    
    
    def set_text(self,start_joint , last_joint):
        
        self.LE_startjnt.setText(start_joint)
        self.LE_lastjnt.setText(last_joint)
        
        self.CB_prefix_suffix.clear()
        
        self.CB_prefix_suffix.addItem("FK_{0}".format(start_joint))
        self.CB_prefix_suffix.addItem("{0}_FK".format(start_joint))
        
    
    def create_fk_ik(self):
        
        self.IK_LIST_NAME = []
        self.FK_LIST_NAME = []
        self.BIND_JOINTS = []
        self.removed_list_obj = []
        numb = None
        
        cmds.select(cl=True)
        
        start_text = self.LE_startjnt.text()
        last_text = self.LE_lastjnt.text()
        
        current_index_CB = self.CB_prefix_suffix.currentIndex()
        example = "NAME_EXAMPLE"
        
        cmds.select(cl=True)
        
        if current_index_CB == 0:
            name_jnt_fk = "FK_{0}".format(example)
            name_jnt_ik = "IK_{0}".format(example)
        else:
            name_jnt_fk = "{0}_FK".format(example)
            name_jnt_ik = "{0}_IK".format(example)
        
        new_start_name_fk = name_jnt_fk.replace(example,start_text)
        new_start_name_ik = name_jnt_ik.replace(example,start_text)


        #check for existing ik and fk .

        if cmds.objExists(new_start_name_fk):
            self.numb = 0
        
        while cmds.objExists(new_start_name_fk):
            
            name_jnt_fk = "{0}_{1}".format(name_jnt_fk,self.numb)
            name_jnt_ik = "{0}_{1}".format(name_jnt_ik,self.numb)
            new_start_name_fk = "{0}_{1}".format(new_start_name_fk,self.numb)
            new_start_name_ik = "{0}_{1}".format(new_start_name_ik,self.numb)
            self.numb+=1
        if self.numb>=0:
            self.numb-=1
        
        if cmds.objExists(new_start_name_fk) or cmds.objExists(new_start_name_ik):
            QtWidgets.QMessageBox.critical(self,"Name Exists","When we want to create new names those names are exists ")
            raise 
        
        hierarchy_selected_fk = cmds.duplicate(start_text,n = new_start_name_fk,renameChildren=False)
        hierarchy_selected_ik = cmds.duplicate(start_text,n = new_start_name_ik,renameChildren=False)
        
        hierarchy_selected_fk.remove(hierarchy_selected_fk[0])
        hierarchy_selected_ik.remove(hierarchy_selected_ik[0])
        
        self.BIND_JOINTS.append(start_text)
        self.FK_LIST_NAME.append(new_start_name_fk)
        self.IK_LIST_NAME.append(new_start_name_ik)
        
        # Rename fk joint
        
        cmds.select(cl=True)
        cmds.select(new_start_name_fk,hierarchy=True)
        cmds.select(new_start_name_fk,deselect=True)
        
        for jnt_main_name_fk in hierarchy_selected_fk:
            last_numb_fk = None
            new_name_fk = name_jnt_fk.replace(example,jnt_main_name_fk)
            if cmds.objExists(new_name_fk):
                last_numb = new_name_fk.split("_")[-1]
                try:
                    last_numb_fk = int(last_numb)
                except:
                    last_numb_fk = 0
                
                jnt_renamed_fk = cmds.rename("{0}_{1}".format(new_name_fk,last_numb_fk))
            else:
                jnt_renamed_fk = cmds.rename(new_name_fk)
            self.BIND_JOINTS.append(jnt_main_name_fk)
            
            
            if jnt_main_name_fk != last_text:
                cmds.select(jnt_renamed_fk,deselect = True)
                self.FK_LIST_NAME.append(jnt_renamed_fk)
                
            else:
                self.FK_LIST_NAME.append(jnt_renamed_fk)
                cmds.select(cl=True)
                child_fk_last_joint = cmds.listRelatives(jnt_renamed_fk,children = True)
                if child_fk_last_joint:
                    cmds.select(cl=True)
                    cmds.select(jnt_renamed_fk,hierarchy=True)
                    cmds.select(jnt_renamed_fk,deselect=True)
                    cmds.delete()
                break
                
        
            
            
        # Rename ik joint
        
        cmds.select(cl=True)
        cmds.select(new_start_name_ik,hierarchy=True)
        cmds.select(new_start_name_ik,deselect=True)
            
        for jnt_main_name_ik in hierarchy_selected_ik:
            
            last_numb_ik = None
            new_name_ik = name_jnt_ik.replace(example,jnt_main_name_ik)
            if cmds.objExists(new_name_ik):
                last_numb_ik = new_name_ik.split("_")[-1]
                try:
                    last_numb_ik = int(last_numb_ik)
                except:
                    last_numb_ik = 0
                
                jnt_renamed_ik = cmds.rename("{0}_{1}".format(new_name_ik,last_numb_ik))
                jnt_renamed_ik = jnt_renamed_ik.split("|")[-1]

            else:
                jnt_renamed_ik = cmds.rename(new_name_ik)
                jnt_renamed_ik = jnt_renamed_ik.split("|")[-1]
                
            
            
            if jnt_main_name_ik != last_text :
                cmds.select(jnt_renamed_ik,deselect = True)
                self.IK_LIST_NAME.append(jnt_renamed_ik)

            else:
                self.IK_LIST_NAME.append(jnt_renamed_ik)
                cmds.select(cl=True)
                child_ik_last_joint = cmds.listRelatives(jnt_renamed_ik,children = True)
                if child_ik_last_joint:
                    cmds.select(cl=True)
                    cmds.select(jnt_renamed_ik,hierarchy=True)
                    cmds.select(jnt_renamed_ik,deselect=True)
                    cmds.delete()
                break    
        
        self.clean_garbage_obj(name_jnt_fk,name_jnt_ik,example)
        self.create_attr()
        self.create_constraint(name_jnt_fk,name_jnt_ik,example)
        
            
    def create_constraint(self,name_jnt_fk,name_jnt_ik,example):
        
        numbstr = self.numb
        if numbstr>=0:
            numbstr = str(numbstr)
        else:
            numbstr=""
        
        output_plug_switch_fkik = self.BIND_JOINTS[0]+".FK_IK_Auto_Create"+numbstr
        output_plug_mainjoint_visibility = self.BIND_JOINTS[0]+".Main_Visibility"+numbstr
        output_plug_fkjoint_visibility = self.BIND_JOINTS[0]+".FK_Visibility"+numbstr
        output_plug_ikjoint_visibility = self.BIND_JOINTS[0]+".IK_Visibility"+numbstr
           
        cmds.setAttr(output_plug_mainjoint_visibility,1)
        cmds.setAttr(output_plug_fkjoint_visibility,1)
        cmds.setAttr(output_plug_ikjoint_visibility,1)
           
        for joint in  self.BIND_JOINTS:
            
            name_reverse_node = "reverse_{0}{1}".format(joint,numbstr)
            if cmds.objExists(name_reverse_node):
                cmds.delete(name_reverse_node)
            
            reverse_node = cmds.createNode("reverse",name = "reverse_{0}{1}".format(joint,numbstr))
            input_x_reverse = reverse_node+".input.inputX"
            output_x_reverse =reverse_node+".output.outputX"
            
            index_joint = self.BIND_JOINTS.index(joint)
            joint_fk = self.FK_LIST_NAME[index_joint]
            joint_ik = self.IK_LIST_NAME[index_joint]
            
            
            #checking for exist constraint or not . if exist i get numb last const and add to it for set new const
            
            numb_ik_attr = None
            
            if self.RB_orient.isChecked():
                if cmds.objExists(joint+"_orientCOnstraint1"):
                    name_ik_attr = cmds.listAttr(joint+"_orientCOnstraint1",keyable=True)[-1]
                    split_name = name_ik_attr.split("W")[-1]
                    numb_ik_attr = int(split_name)                
                name_constraint = cmds.orientConstraint(joint_fk , joint_ik , joint , mo=True,weight=1)[0]
                
            elif self.RB_point.isChecked():
                if cmds.objExists(joint+"_pointConstraint1"):
                    name_ik_attr = cmds.listAttr(joint+"_pointConstraint1",keyable=True)[-1]
                    split_name = name_ik_attr.split("W")[-1]
                    numb_ik_attr = int(split_name)
                name_constraint = cmds.pointConstraint(joint_fk , joint_ik , joint , mo=True,weight=1)[0]
           
            else:
                if cmds.objExists(joint+"_parentConstraint1"):
                    name_ik_attr = cmds.listAttr(joint+"_parentConstraint1",keyable=True)[-1]
                    split_name = name_ik_attr.split("W")[-1]
                    numb_ik_attr = int(split_name)
                name_constraint = cmds.parentConstraint(joint_fk , joint_ik , joint , mo=True,weight=1)[0]
            
            
            if numb_ik_attr:
                fk_input_const = "{0}.{1}W{2}".format(name_constraint,joint_fk,numb_ik_attr+1)
                ik_input_const = "{0}.{1}W{2}".format(name_constraint,joint_ik,numb_ik_attr+2)
            
            else:
                fk_input_const = "{0}.{1}W{2}".format(name_constraint,joint_fk,0)
                ik_input_const = "{0}.{1}W{2}".format(name_constraint,joint_ik,1)
            
            fk_visibility = joint_fk+".visibility"
            ik_visibility = joint_ik+".visibility"
            main_joint_visibility = joint+".visibility"
            
            cmds.connectAttr(output_plug_fkjoint_visibility,fk_visibility)
            cmds.connectAttr(output_plug_ikjoint_visibility,ik_visibility)
            if not self.numb>=0:
                if not cmds.connectionInfo(main_joint_visibility,isDestination=True):
                    cmds.connectAttr(output_plug_mainjoint_visibility,main_joint_visibility)
                
            cmds.connectionInfo
            cmds.connectAttr(output_plug_switch_fkik,input_x_reverse)
            cmds.connectAttr(output_plug_switch_fkik,ik_input_const)
            cmds.connectAttr(output_x_reverse,fk_input_const)
            
            if numb_ik_attr:
                numb_ik_attr = None
            
        cmds.ikHandle( sj=self.IK_LIST_NAME[0], ee=self.IK_LIST_NAME[-1])
        
        numbstr = self.numb
        if numbstr>0:
            numbstr = str(numbstr-1)
        else:
            numbstr=""
        
        for obj_find_attr in self.FK_LIST_NAME:
            final_list_attr = cmds.listAttr(obj_find_attr,keyable=True)
            for attr_obj in final_list_attr:
                if attr_obj == "JOINTS_VISIBILITY":
                    index_attr_jnt = final_list_attr.index(attr_obj)
                    index_fk = self.FK_LIST_NAME.index(obj_find_attr)
                    for final_attr in final_list_attr[index_attr_jnt::]:
                            cmds.deleteAttr("{0}.{1}".format(self.FK_LIST_NAME[index_fk],final_attr))
                            cmds.deleteAttr("{0}.{1}".format(self.IK_LIST_NAME[index_fk],final_attr))
        
        self.IK_LIST_NAME = []
        self.FK_LIST_NAME = []
        self.BIND_JOINTS = []
        self.numb = None
        om.MGlobal.displayInfo("Joints FK IK has created")
        
        
        
    def create_attr(self):
        
        numbstr = self.numb
        if numbstr>=0:
            numbstr = str(numbstr)
        else:
            numbstr=""
        
        strat_main_joint = self.BIND_JOINTS[0]
        try:
            cmds.addAttr(strat_main_joint,ln="JOINTS_VISIBILITY"+numbstr,at="enum",en="_________:",keyable=True) 
            cmds.addAttr(strat_main_joint,ln="Main_Visibility"+numbstr,at="bool",keyable=True)
            cmds.addAttr(strat_main_joint,ln="FK_Visibility"+numbstr,at="bool",keyable=True)
            cmds.addAttr(strat_main_joint,ln="IK_Visibility"+numbstr,at="bool",keyable=True)
            cmds.addAttr(strat_main_joint,ln="IK_FK_SWITCH_AUTO_CREATE"+numbstr,at="enum",en="_________:",keyable=True)
            cmds.addAttr(strat_main_joint,ln="FK_IK_Auto_Create"+numbstr,at="double",min=0,max=1,keyable=True)
        except:
            QtWidgets.QMessageBox.critical(self,"Exists Attribute","Check Attr in start joint and delete optional attr \n.optional attr are = [JOINTS_VISIBILITY{0},Main_Visibility{0},FK_Visibility{0},IK_Visibility{0},IK_FK_SWITCH_AUTO_CREATE{0},FK_IK_Auto_Create{0}] If is not exists script worked correctly ".format(numbstr))
    def clean_garbage_obj(self,name_jnt_fk,name_jnt_ik,example):
        start_joint = self.BIND_JOINTS[0]
        last_joint = self.BIND_JOINTS[-1]
        full_path_last_obj = cmds.ls(last_joint,long=True)[0]
        
        list_path_last_obj = full_path_last_obj.split("|")
        index_start_joint = list_path_last_obj.index(start_joint)
        del list_path_last_obj[0:index_start_joint]
        
        numbstr = self.numb
        if numbstr>=0:
            numbstr = "_{0}".format(numbstr)
        else:
            numbstr=""
        
        self.removed_list_obj = []
        
        for garbage_obj in self.BIND_JOINTS:
            if  not garbage_obj in list_path_last_obj:
                
                self.removed_list_obj.append(garbage_obj)
     
   
        for remove_of_list in self.removed_list_obj:
            index_remove_of_list = self.BIND_JOINTS.index(remove_of_list)
            self.BIND_JOINTS.remove(remove_of_list)
            del self.FK_LIST_NAME[index_remove_of_list]
            del self.IK_LIST_NAME[index_remove_of_list]

        cmds.select(cl=True)
        cmds.select(self.FK_LIST_NAME[0],hierarchy=True)
        for fk_jnt in self.FK_LIST_NAME:
            cmds.select(fk_jnt,deselect=True)
        if cmds.ls(sl=True):
            cmds.delete()
        
        cmds.select(cl=True)
        cmds.select(self.IK_LIST_NAME[0],hierarchy=True)
        for ik_jnt in self.IK_LIST_NAME:
            cmds.select(ik_jnt,deselect=True)
        if cmds.ls(sl=True,absoluteName=True):
            cmds.delete()
            
        self.removed_list_obj = []

