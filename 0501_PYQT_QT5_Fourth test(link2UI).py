import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QToolTip,QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon,QFont
import Function.read_info


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

        #设置ClipID文件下几个控件为只读
        self.ANALYSISPanel_Info_CilpID_TextEdit.setReadOnly(True)
        self.ANALYSISPanel_Info_CilpName_LineEdit.setReadOnly(True)
        self.ANALYSISPanel_Info_CilpUUID_LineEdit.setReadOnly(True)
        self.ANALYSISPanel_Info_FilePath_LineEdit.setReadOnly(True)
        self.ANALYSISPanel_Info_Sequence_LineEdit.setReadOnly(True)

        self.pushButton_2.clicked.connect(self.IMPORTPanel_OpenAmffile)
        # self.findChild(QWidget, "ANALYSISPanel_Info_AMFInfo_TextEdit").setPlainText("test")




    def IMPORTPanel_OpenAmffile(self):
        '''点击[open amf file]按钮
             从文件管理系统选择amf文件
             解析amf文件'''
        amf_filePath = QFileDialog.getOpenFileName(self,"open file dialog","D:\\","amf files(*.amf)")
        global amf_filepath
        amf_filepath = amf_filePath[0]
        # print(amf_filepath)

        # # 调试代码
        # global amf_filepath
        # amf_filepath = r'D:\work\AMFTool\test1.amf'

        rst1,rst2=Function.read_info.Printinfo(amf_filepath)

        # 设置AMFINFO下的几个文本框信息
        self.ANALYSISPanel_Info_AMFInfo_TextEdit.setPlainText(rst1[0])
        self.ANALYSISPanel_Info_Name_LineEdit.setText(rst1[1])
        self.ANALYSISPanel_Info_EmailAddress_LineEdit.setText(rst1[2])
        self.ANALYSISPanel_Info_AMFUUID_LineEdit.setText(rst1[3])

        # 设置ClipID下的几个文本框信息
        self.ANALYSISPanel_Info_CilpID_TextEdit.setPlainText(rst2[0])
        self.ANALYSISPanel_Info_CilpName_LineEdit.setText(rst2[1])
        self.ANALYSISPanel_Info_CilpUUID_LineEdit.setText(rst2[2])
        self.ANALYSISPanel_Info_FilePath_LineEdit.setText(rst2[3])
        self.ANALYSISPanel_Info_Sequence_LineEdit.setText(rst2[4])

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


if __name__ == '__main__':
    # 这条命令__name__ == '__main__'，如果是导入的方式，是默认不执行里面的语句的。
    # https://www.cnblogs.com/suguangti/p/12632119.html
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('./UI_file/Pic/Golem.ico'))               # 设置程序Logo，现在只是一个测试文件

    MAINsolfware=MAINsolfware()
    MAINsolfware.show()
    sys.exit(app.exec())


