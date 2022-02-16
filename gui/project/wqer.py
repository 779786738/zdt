import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class DialogDemo(QMainWindow):
    def __init__(self,parent=None):
        super(DialogDemo, self).__init__(parent)
        #设置主界面的标题及初始大小
        self.setWindowTitle('Dialog例子')
        self.resize(350,300)

        #创建按钮，注意()内的self必不可少，用于加载自身的一些属性设置
        self.btn=QPushButton(self)
        #设置按钮的属性：文本，移动位置，链接槽函数
        self.btn.setText('弹出对话框')
        self.btn.move(50,50)
        self.btn.clicked.connect(self.showdialog)

    def showdialog(self):
        #创建QDialog对象
        dialog=QDialog()
        #创建按钮到新创建的dialog对象中
        btn=QPushButton('ok',dialog)
        #移动按钮，设置dialog的标题
        btn.move(50,50)
        dialog.setWindowTitle("Dialog")
        #设置窗口的属性为ApplicationModal模态，用户只有关闭弹窗后，才能关闭主界面
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()
