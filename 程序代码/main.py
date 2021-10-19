from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from main_widget import MainWidget

import sys



def main():
    # 创建QApplication类的实例
    app = QApplication(sys.argv) 
    
    # 创建自定义的窗口, 继承于QWidget
    mainWidget = MainWidget() 

    # 显示窗口
    mainWidget.show()    
    
    # 进入程序的主循环, 并通过exit函数确保主循环安全结束。
    exit(app.exec_()) 
    
    
if __name__ == '__main__':
    main()
