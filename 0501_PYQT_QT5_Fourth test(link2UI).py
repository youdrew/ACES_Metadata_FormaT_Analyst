import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QToolTip,QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon,QFont

try:
  import xml.etree.cElementTree as ET
except ImportError:
  import xml.etree.ElementTree as ET

# QToolTip是控件的提示信息

#信息的定义


class MAINsolfware(QMainWindow):
    def __init__(self,parent=None):
        super(MAINsolfware,self).__init__(parent)

        loadUi('UI_file/0509_test.ui',self)
        #test

        # self.setFixedSize(self.sizeHint())                         # 这一条是用来调整窗口大小的
        self.setWindowIcon(QIcon('./UI_file/Pic/Golem.ico'))         # 设置窗口图标
        self.setWindowTitle('ACES Metadata Format Analyst')          # 设置主窗口名称
        self.statusBar.showMessage('This is a test version',5000)    # 设置一个存在5秒的底部提示


        # 下面两行让UI里的组建对应到相应的函数
        self.OUTPUTPanel_SaveAs_LineEdit.textChanged.connect(self.AMF_Save)
        self.OUTPUTPanel_PathSelect_PushButton.clicked.connect(self.I_was_clicked)

        # 设置按钮的提示信息
        self.OUTPUTPanel_SaveAs_LineEdit.setToolTip('我的路径是支持修改的')
        self.OUTPUTPanel_PathSelect_PushButton.setToolTip('点我会出现好可爱的啊啊啊啊啊')

        # 设置部件的边缘
        self.IMPORTPanel_Lift_QVBoxLayout.setContentsMargins(0,0,0,0)
        self.IMPORTPanel_Right_QVBoxLayout.setContentsMargins(0,0,0,0)
        self.IMPORTPanel_Right_QTabWidget.setContentsMargins(0,0,0,0)

        #设置AMFInfo文件下几个控件为只读
        self.ANALYSISPanel_Info_AMFInfo_TextEdit.setReadOnly(True)
        self.ANALYSISPanel_Info_Name_LineEdit.setReadOnly(True)
        self.ANALYSISPanel_Info_EmailAddress_LineEdit.setReadOnly(True)
        self.ANALYSISPanel_Info_AMFUUID_LineEdit.setReadOnly(True)

        self.pushButton_2.clicked.connect(self.IMPORTPanel_OpenAmffile)
        # self.findChild(QWidget, "ANALYSISPanel_Info_AMFInfo_TextEdit").setPlainText("test")




    def IMPORTPanel_OpenAmffile(self):
        '''点击[open amf file]按钮
             从文件管理系统选择amf文件
             解析amf文件'''
        # amf_filePath = QFileDialog.getOpenFileName(self,"open file dialog","D:\\","amf files(*.amf)")
        # global amf_filepath
        # amf_filepath = amf_filePath[0]
        # print(amf_filepath)

        # 调试代码
        global amf_filepath
        amf_filepath = 'D:/work/AMFTool/Isabella_trial.amf'

        self.Printinfo()
        # self.ANALYSISPanel_Info_AMFInfo_TextEdit.setPlainText(amfInfo_description)
        # self.ANALYSISPanel_Info_Name_LineEdit.setPlainText(amfInfo_name)


    def I_was_clicked(self):
        global AMF_Save_Path
        if(self.OUTPUTPanel_SaveAs_LineEdit.text()!=''):
            AMF_Save_Path = self.OUTPUTPanel_SaveAs_LineEdit.text()
        else:
            AMF_Save_Path = 'None'
        print('啊啊啊啊啊我被点击了')
        print("文件保存路径：" +AMF_Save_Path)

    def AMF_Save(self):
        global AMF_Save_Path
        AMF_Save_Path = self.OUTPUTPanel_SaveAs_LineEdit.text()
        print("文件保存路径：" + AMF_Save_Path)

    def get_AMFInfo(self,root):
        print('run...')
        '''解析AMFinfo部分的四个信息
           description
           name
           emailAdress
           amfUUID'''
        global amfInfo_description
        global amfInfo_name
        global amfInfo_emailAdress
        global amfInfo_amfUUID
        # 找到root节点下的所有amfInfo节点
        for amfInfo in root.findall('{urn:ampas:aces:amf:v1.0}amfInfo'):

            # 查找amfInfo节点下的 description 节点
            description = amfInfo.find('{urn:ampas:aces:amf:v1.0}description')
            if description is None:
                amfInfo_description = 'None'
            else:
                amfInfo_description = description.text

            # 查找amfInfo节点下的 name 节点
            name = amfInfo.find('{urn:ampas:aces:amf:v1.0}name')
            if name is None:
                amfInfo_name = 'None'
            else:
                amfInfo_name = name.text

            # 查找amfInfo节点下的 emailAdress 节点
            emailAdress = amfInfo.find('{urn:ampas:aces:amf:v1.0}emailAdress')
            if emailAdress is None:
                amfInfo_emailAdress = 'None'
            else:
                amfInfo_emailAdress = emailAdress.text

            # 查找amfInfo节点下的 amfUUID 节点
            amfUUID = amfInfo.find('{urn:ampas:aces:amf:v1.0}amfUUID')
            if amfUUID is None:
                amfInfo_amfUUID = 'None'
            else:
                amfInfo_amfUUID = amfUUID.text

        # 设置AMFINFO下的几个文本框信息
        self.ANALYSISPanel_Info_AMFInfo_TextEdit.setPlainText(amfInfo_description)
        self.ANALYSISPanel_Info_Name_LineEdit.setText(amfInfo_name)
        self.ANALYSISPanel_Info_EmailAddress_LineEdit.setText(amfInfo_emailAdress)
        self.ANALYSISPanel_Info_AMFUUID_LineEdit.setText(amfInfo_amfUUID)

    def get_ClipID(self, root):
        '''解析ClipID部分的五个信息
                   description
                   name
                   ClipIDUUID
                   ClipIDPath
                   ClipIDSequence'''
        global ClipID_description
        global ClipID_name
        global ClipID_UUID
        global ClipID_path
        global ClipID_sequence

        # 找到 root 节点下的所有 clipId 节点
        clipId = root.find('{urn:ampas:aces:amf:v1.0}clipId')
        if clipId is None:
            ClipID_description = 'None'
            ClipID_name = 'None'
            ClipID_UUID = 'None'
            ClipID_path = 'None'
            ClipID_sequence = 'None'
        else:
            # 查找 clipId 节点下的 description 节点
            description = clipId.find('{urn:ampas:aces:amf:v1.0}description')
            if description is None:
                ClipID_description = 'None'
            else:
                ClipID_description = description.text

            # 查找 clipId 节点下的 clipName 节点
            clipName = clipId.find('{urn:ampas:aces:amf:v1.0}clipName')
            if clipName is None:
                ClipID_name = 'None'
            else:
                ClipID_name = clipName.text

            # 查找 clipId 节点下的 UUID 节点
            UUID = clipId.find('{urn:ampas:aces:amf:v1.0}UUID')
            if UUID is None:
                ClipID_UUID = 'None'
            else:
                ClipID_UUID = UUID.text

            # 查找 clipId 节点下的 file 节点
            file = clipId.find('{urn:ampas:aces:amf:v1.0}file')
            if file is None:
                ClipID_path = 'None'
            else:
                ClipID_path = file.text

            # 查找 clipId 节点下的 sequence 节点
            sequence = clipId.find('{urn:ampas:aces:amf:v1.0}sequence')
            if sequence is None:
                ClipID_sequence = 'None'
            else:
                ClipID_sequence = sequence.text

        # 设置ClipID下的几个文本框信息
        self.ANALYSISPanel_Info_CilpID_TextEdit.setPlainText(ClipID_description)
        self.ANALYSISPanel_Info_CilpName_LineEdit.setText(ClipID_name)
        self.ANALYSISPanel_Info_CilpUUID_LineEdit.setText(ClipID_UUID)
        self.ANALYSISPanel_Info_FilePath_LineEdit.setText(ClipID_path)
        self.ANALYSISPanel_Info_Sequence_LineEdit.setText(ClipID_sequence)

    def Printinfo(self):
        '''解析并打印amf文件中的信息'''
        print("Printinfo run...")
        # 解析amf文件,获取根节点root
        tree = ET.parse(amf_filepath)
        global root
        root = tree.getroot()
        self.get_AMFInfo(root)
        self.get_ClipID(root)


if __name__ == '__main__':
    # 这条命令__name__ == '__main__'，如果是导入的方式，是默认不执行里面的语句的。
    # https://www.cnblogs.com/suguangti/p/12632119.html
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('./UI_file/Pic/Golem.ico'))               # 设置程序Logo，现在只是一个测试文件

    MAINsolfware=MAINsolfware()
    MAINsolfware.show()
    sys.exit(app.exec())


