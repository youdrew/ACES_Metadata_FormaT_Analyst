import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QToolTip
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon,QFont
# QToolTip是控件的提示信息


class MAINsolfware(QMainWindow):
    def __init__(self,parent=None):
        super(MAINsolfware,self).__init__(parent)

        loadUi('UI_file/0424_test.ui',self)

        # self.setFixedSize(self.sizeHint())                           # 这一条是用来调整窗口大小的
        self.setWindowIcon(QIcon('./UI_file/Pic/Golem.ico'))         # 设置窗口图标
        self.setWindowTitle('ACES Metadata Format Analyst')          # 设置主窗口名称
        self.statusBar.showMessage('This is a test version',5000)    # 设置一个存在5秒的底部提示


        # 下面两行让UI里的组建对应到相应的函数
        self.OUTPUTPanel_SaveAs_LineEdit.textChanged.connect(self.AMF_Save)
        self.OUTPUTPanel_PathSelect_PushButton.clicked.connect(self.I_was_clicked)

        # 设置按钮的提示信息
        self.OUTPUTPanel_SaveAs_LineEdit.setToolTip('我的路径是支持修改的')
        self.OUTPUTPanel_PathSelect_PushButton.setToolTip('点我会出现好可爱的啊啊啊啊啊')

        #设置部件的边缘
        self.IMPORTPanel_Lift_QVBoxLayout.setContentsMargins(0,0,0,0)
        self.IMPORTPanel_Right_QVBoxLayout.setContentsMargins(0,0,0,0)
        self.IMPORTPanel_Right_QTabWidget.setContentsMargins(0,0,0,0)

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


