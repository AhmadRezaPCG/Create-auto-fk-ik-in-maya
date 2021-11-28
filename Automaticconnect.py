import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.OpenMaya as om

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

def maya_main_window():
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window),QtWidgets.QWidget)

class Automatic_connect_class(QtWidgets.QDialog):
    
    dialog_window = None
    
    def __init__(self,parent=maya_main_window()):
        super(Automatic_connect_class,self).__init__(parent)
        
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_context)
        
        self.setWindowTitle("Connect automatic")
        self.createmessagebox()
        self.createaction()
        self.createwidget()
        self.createlayout()
        self.connectsignalslot()
    
    @classmethod
    def show_dialog(cls):
        if cls.dialog_window:
            if cls.dialog_window.isHidden():
                cls.dialog_window.show()
            else:
                cls.dialog_window.raise_()
                cls.dialog_window.activateWindow()
        else:
            cls.dialog_window = Automatic_connect_class()
            cls.dialog_window.show()
    
    def createmessagebox(self):
    
        PB_continue = QtWidgets.QPushButton("Continue")
        PB_cancel = QtWidgets.QPushButton("Cancel")
        PB_replace = QtWidgets.QPushButton("Replace")
    
        self.MS_error = QtWidgets.QMessageBox(self)
        self.MS_error.setWindowTitle("Exists Attr",)
        self.MS_error.setText("Youre Attrs object is exists in your list .")
        self.MS_error.setIcon(QtWidgets.QMessageBox.Question)
        self.MS_error.addButton("Replace",QtWidgets.QMessageBox.NoRole)
        self.MS_error.addButton("Cancel",QtWidgets.QMessageBox.RejectRole)
        self.MS_error.addButton("Continue",QtWidgets.QMessageBox.YesRole)
        

    
    def createaction(self):
        
        self.A_deleteitem = QtWidgets.QAction()
        self.A_deleteitem.setText("Delete")
        
        self.A_additem_output = QtWidgets.QAction()
        self.A_additem_output.setText("Add to output")
        
        self.A_additem_input = QtWidgets.QAction()
        self.A_additem_input.setText("Add to input")
    
    def createwidget(self):
        
        
        self.M_context = QtWidgets.QMenu()
        
        self.MB_edit = QtWidgets.QMenuBar()
        M_edit = self.MB_edit.addMenu("Edit")
        M_edit.addAction(self.A_deleteitem)
        M_edit.addSeparator()
        M_edit.addAction(self.A_additem_input)
        M_edit.addAction(self.A_additem_output)
        
        self.LW_output = QtWidgets.QListWidget()
        self.LW_output.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.L_countoutput = QtWidgets.QLabel()
        self.L_countoutput.setHidden(True)
        self.PB_output = QtWidgets.QPushButton("Output Attr")
        
        self.LW_input = QtWidgets.QListWidget()
        self.LW_input.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.L_countinput = QtWidgets.QLabel()
        self.L_countinput.setHidden(True)
        self.PB_input = QtWidgets.QPushButton("Input Attr")
        
        self.CB_typeconnection = QtWidgets.QComboBox()
        self.CB_typeconnection.setEditable(False)
        self.CB_typeconnection.addItem("Connect to all")
        self.CB_typeconnection.addItem("One by one")
        self.CB_typeconnection.addItem("By names Attrs")
        
        self.PB_cancel = QtWidgets.QPushButton("Cancel")
        self.PB_connect = QtWidgets.QPushButton("Connect")
        
    
    def createlayout(self):
        
        VL_output = QtWidgets.QVBoxLayout()
        VL_output.addWidget(self.LW_output)
        VL_output.addWidget(self.L_countoutput)
        VL_output.addWidget(self.PB_output)
        
        VL_input = QtWidgets.QVBoxLayout()
        VL_input.addWidget(self.LW_input)
        VL_input.addWidget(self.L_countinput)
        VL_input.addWidget(self.PB_input)
        
        HL_inputoutput = QtWidgets.QHBoxLayout()
        HL_inputoutput.addLayout(VL_output)
        HL_inputoutput.addLayout(VL_input)
        
        Fr_1 = QtWidgets.QFrame()
        Fr_1.setLineWidth(5)
        Fr_1.setFrameShape(QtWidgets.QFrame.HLine)
        
        Fr_2 = QtWidgets.QFrame()
        
        Fr_2.setFrameShape(QtWidgets.QFrame.HLine)
        Fr_2.setLineWidth(5)
        
        FL_typeconnect = QtWidgets.QFormLayout()
        FL_typeconnect.addRow("Type Connection : ",self.CB_typeconnection)
        
        HL_bottombutton = QtWidgets.QHBoxLayout()
        HL_bottombutton.addStretch()
        HL_bottombutton.addWidget(self.PB_cancel)
        
        MAIN_L = QtWidgets.QVBoxLayout(self)
        MAIN_L.setMenuBar(self.MB_edit)
        MAIN_L.addLayout(HL_inputoutput)
        MAIN_L.addWidget(Fr_1)
        MAIN_L.addLayout(FL_typeconnect)
        MAIN_L.addWidget(self.PB_connect)
        MAIN_L.addWidget(Fr_2)
        MAIN_L.addLayout(HL_bottombutton)
        
    def open_context(self,point):
        
        
        self.M_action = QtWidgets.QMenu()
        self.M_action.addAction(self.A_deleteitem)
        self.M_action.addSeparator()
        self.M_action.addAction(self.A_additem_input)
        self.M_action.addAction(self.A_additem_output)
        
        self.M_action.exec_(self.mapToGlobal(point))
        
    def connectsignalslot(self):
        
        self.CB_typeconnection.currentTextChanged.connect(self.CB_changed)
        self.PB_cancel.clicked.connect(self.close)
        self.PB_output.clicked.connect(self.to_output)
        self.PB_input.clicked.connect(self.to_input)
        self.A_deleteitem.triggered.connect(self.delete_item)
        self.A_additem_input.triggered.connect(self.add_iteminput)
        self.A_additem_output.triggered.connect(self.add_itemoutput)
        self.PB_connect.clicked.connect(self.connect_attr)
        
    def CB_changed(self,CB_text):
        
        if CB_text == "One by one":
            self.L_countinput.setHidden(False)
            self.L_countoutput.setHidden(False)
        
            self.L_countinput.setText("Input Count :"+self.int_to_str(self.get_count_LW(self.LW_input)))
            self.L_countoutput.setText("Output Count : "+self.int_to_str(self.get_count_LW(self.LW_output)))
        else:
            self.L_countinput.setHidden(True)
            self.L_countoutput.setHidden(True)
    
    def connect_attr(self):
        
        count_input = self.get_count_LW(self.LW_input)
        count_output = self.get_count_LW(self.LW_output)
        CB_text = self.gettextcombo()
        
        if count_input and count_output:
            
            if CB_text == "Connect to all" : 
                if count_output != 1 :
                    om.MGlobal.displayError("If you want to use ('connect to all') you should add one attr to output list.")
                    raise RuntimeError
                self.connect_to_all(count_input)
            
            if CB_text == "One by one":
                if count_input == count_output:
                    self.connect_one_by_one(count_input)
                else:
                    om.MGlobal.displayError("If you want to use ('One by one') type connection , your count input and out put should be equal by together.")
            
            if CB_text == "By names Attrs":
            
                self.connect_bynamesAttrs(count_input,count_output)
            
    
    def connect_bynamesAttrs(self,count_input,count_output):
        
        
        output_items = self.get_all_items(self.LW_output,count_output)
        input_items = self.get_all_items(self.LW_input,count_input)
        
        command_str = ""
        
        for item_output in output_items:
            
            data_item_output = self.get_data(item_output)
            attr_name = self.data_to_attrname(data_item_output)
            
            for item_input in input_items:
                
                data_item_input = self.get_data(item_input)
                if not self.check_input_plug(data_item_input):
                    om.MGlobal.displayWarning("({0}) plug input has connected to another plug".format(data_item_input))
                    continue
                
                if attr_name == self.data_to_attrname(data_item_input):
                    command_str+="cmds.connectAttr('{0}','{1}');".format(data_item_output,data_item_input)
        exec (command_str)
        om.MGlobal.displayInfo(" Your Attrs are connected")
    
    
    def connect_one_by_one(self,count):
        
        command_str=""
        for index_item in range(count):
            
            attr_output = self.get_data(self.LW_output.item(index_item))
            attr_input = self.get_data(self.LW_input.item(index_item))
            
            if not self.check_input_plug(attr_input):
                om.MGlobal.displayWarning("({0}) plug input has connected to another plug".format(attr_input))
                continue
                
            command_str+="cmds.connectAttr('{0}','{1}');".format(attr_output,attr_input)
            
        exec command_str
        om.MGlobal.displayInfo(" Your Attrs are connected")
        
    def connect_to_all(self,count_input):
        
        item_output = self.LW_output.item(0)
        attr_output = self.get_data(item_output)
    
        command_string = ""
    
        for index_item in range(count_input):
            
            item_input = self.LW_input.item(index_item)
            attr_input = self.get_data(item_input)
            
            if not self.check_input_plug(attr_input):
                om.MGlobal.displayWarning("({0}) plug input has connected to another plug".format(attr_input))
                continue
                
                
            command_string+="cmds.connectAttr('{0}','{1}');".format(attr_output,attr_input)
        
        exec command_string
        om.MGlobal.displayInfo(" Your Attrs are connected")
        
    def check_input_plug(self,attr):
        
        if cmds.listConnections(attr):
            return False
        return True
        
        
    def to_input(self):
        
        selected_objs_ls_long = cmds.ls(sl=True,long=True)
        selected_objs = cmds.ls(sl=True)
        attr_name_ls = cmds.channelBox("mainChannelBox",q=True,selectedMainAttributes=True)

        
        if selected_objs_ls_long and attr_name_ls :
            self.check_attr_exist(selected_objs_ls_long,attr_name_ls)
            self.delete_items(self.LW_input)
            self.add_attr(selected_objs_ls_long,selected_objs,attr_name_ls,self.LW_input)
        else:
            om.MGlobal.displayError("Select attr")
            return
        
        
        
    def to_output(self):
        
        
        selected_objs_ls_long = cmds.ls(sl=True,long=True)
        selected_objs = cmds.ls(sl=True)
        attr_name_ls = cmds.channelBox("mainChannelBox",q=True,selectedMainAttributes=True)

        
        if selected_objs_ls_long and attr_name_ls :
            self.check_attr_exist(selected_objs_ls_long,attr_name_ls)
            self.delete_items(self.LW_output)
            self.add_attr(selected_objs_ls_long,selected_objs,attr_name_ls,self.LW_output)
        else:
            om.MGlobal.displayError("Select attr")
            return
    
        
    def add_iteminput(self):
        
        
        selected_objs_ls_long = cmds.ls(sl=True,long=True)
        selected_objs = cmds.ls(sl=True)
        attr_name_ls = cmds.channelBox("mainChannelBox",q=True,selectedMainAttributes=True)

        
        if selected_objs_ls_long and attr_name_ls :
            self.check_attr_exist(selected_objs_ls_long,attr_name_ls)
            bool_check = self.check_attrinlist(selected_objs_ls_long,attr_name_ls,self.LW_input)
            if bool_check:
                self.add_attr(selected_objs_ls_long,selected_objs,attr_name_ls,self.LW_input)
        else:
            om.MGlobal.displayError("Select attr")
            return
            
            
            
    def add_itemoutput(self):
        
        
        selected_objs_ls_long = cmds.ls(sl=True,long=True)
        selected_objs = cmds.ls(sl=True)
        attr_name_ls = cmds.channelBox("mainChannelBox",q=True,selectedMainAttributes=True)

        
        if selected_objs_ls_long and attr_name_ls :
            self.check_attr_exist(selected_objs_ls_long,attr_name_ls)
            bool_check = self.check_attrinlist(selected_objs_ls_long,attr_name_ls,self.LW_output)
            if bool_check:
                self.add_attr(selected_objs_ls_long,selected_objs,attr_name_ls,self.LW_output)
        else:
            om.MGlobal.displayError("Select attr")
            return
            
            
        
    def check_attrinlist(self,selected_objs_ls_long,attr_name_ls,LW):
        
        long_datas = self.getdataitems(selected_objs_ls_long,attr_name_ls)
        
        all_items = self.get_all_items(self.LW_input,self.LW_input.count())
        bool_showmessage = True
        for item_exist in all_items:
            data_item = self.get_data(item_exist)
            if data_item in long_datas:
                if bool_showmessage:
                    MS_return = self.MS_error.exec_()
                    bool_showmessage = False
                if MS_return == 1:
                    return False
                    break
                elif MS_return == 2:
                    continue
                else:
                    self.delete_from_list(LW,[item_exist])
        
        return True
        
    def check_attr_exist(self,selected_obj,attr_names):
        
        for object_sl in selected_obj:
            for attr_name in attr_names:
                attrname_in_object = "{0}.{1}".format(object_sl,attr_name)
                if not cmds.objExists(attrname_in_object):
                    om.MGlobal.displayError("Your Attr doesn't math to object selected")
                    raise RuntimeError
     
    def delete_item(self):
        
        outputitemsselected = self.getitemsselected(self.LW_output)
        inputitemsselected = self.getitemsselected(self.LW_input)
        
        
        if outputitemsselected:
            self.delete_from_list(self.LW_output,outputitemsselected)
        if inputitemsselected:
            self.delete_from_list(self.LW_input,inputitemsselected)
        
    def delete_items(self,LW):


        count_item = LW.count()
        if count_item:
            for item_index in range(count_item):
                
                item = LW.itemAt(0,0)
                LW.takeItem(0)
                LW.removeItemWidget(item)
                
        self.LW_output.reset()
        
              
    def delete_from_list(self,LW,outputitemsselected):
        
        
        for item in outputitemsselected:
            row_item = LW.row(item)
            LW.takeItem(row_item)


                
    def add_attr(self,selected_objs_ls_long,selected_objs,attr_name_ls,LW):
    
        text_items = self.gettextitems(selected_objs,attr_name_ls)
        data_items = self.getdataitems(selected_objs_ls_long,attr_name_ls)

        
        self.setdatatext(text_items,data_items,LW)
        
    def setdatatext(self,text_items,data_items,LW):
        
        for index_item in range(len(text_items)):
            item = QtWidgets.QListWidgetItem(text_items[index_item])
            item.setData(QtCore.Qt.UserRole,data_items[index_item])
            LW.addItem(item)
    
    
    def get_all_items(self,LW,count_LW):
        
    
        list_items = [LW.item(x) for x in range(count_LW)]
        return list_items
        
            
            
    def getitemsselected(self,LW):
        
        list_items = []
        
        items_selected = LW.selectedItems()
        if items_selected:
            for item_selected in items_selected:
                
                list_items.append(item_selected)
                
            return list_items
        
        else:
            
            return False
        
    def gettextitems(self,selected_objs,attr_name_ls):
        
        text_items = []
        
        for selected_obj in selected_objs:
            for attr_name in attr_name_ls:
                
                text_item = "{0}.{1}".format(selected_obj,attr_name)
                text_items.append(text_item)
                
        return text_items
        
        
    def getdataitems(self,selected_objs_ls_long,attr_name_ls):
        
        data_items = []
        
        for selected_obj_long in selected_objs_ls_long:
            for attr_name in attr_name_ls:
                data_item = "{0}.{1}".format(selected_obj_long,attr_name)
                data_items.append(data_item)
                
        return data_items
        
        
    def get_data(self,item):
        
        return item.data(QtCore.Qt.UserRole)
        
    def get_count_LW(self,LW):
        
        return LW.count()
        
    def gettextcombo(self):
        
        return self.CB_typeconnection.currentText()
        
    def int_to_str(self,integer):
        
        return "{0}".format(integer)
        
    def data_to_attrname(self,name_data):
        
        split_data = name_data.split(".")
        if split_data:
            return split_data[-1]
        return 
    


