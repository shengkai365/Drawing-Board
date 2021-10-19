from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from paint_board import PaintBoard

class MainWidget(QWidget):
    def __init__(self, Parent=None):
        '''
        Constructor
        '''
        super().__init__(Parent)
        
        self.__InitData() #先初始化数据，再初始化界面
        self.__InitView()
    
    def __InitData(self):
        '''
                  初始化成员变量
        '''
        self.__paintBoard = PaintBoard(self)
        
        
    def __InitView(self):
        '''
                  初始化界面
        '''
        self.setGeometry(300, 300, 800, 600)
        # self.setFixedSize(800,600)
        self.setWindowTitle("  Drawing Board")
        self.setWindowIcon(QIcon('./img/icon.png'))     
        # 设置背景颜色
        mainWindowColor="background-color:#E6E6FA"
        self.setStyleSheet(mainWindowColor)


        #新建一个水平布局作为本窗体的主布局
        main_layout = QHBoxLayout(self) 
        #设置主布局内边距以及控件间距为15px
        main_layout.setSpacing(15) 



        #在主界面左侧放置画板
        main_layout.addWidget(self.__paintBoard) 
        

        #新建垂直子布局用于放置按键
        sub_layout = QVBoxLayout() 
        #设置此子布局和内部控件的间距为13px
        #setContentsMargins(左, 上, 右, 下)，设置控件内容展示区域到边框的距离
        sub_layout.setContentsMargins(13, 13, 13, 13) 


        line1_layout = QHBoxLayout()
        line2_layout = QHBoxLayout()
        line3_layout = QHBoxLayout()
        line4_layout = QHBoxLayout()

        
        self.__btn_pen = QPushButton()
        self.__btn_pen.setFixedSize(70,40)
        self.__btn_pen.setIcon(QIcon('./img/pen.png'))
        self.__btn_pen.setParent(self)
        
        self.__btn_pen.clicked.connect(self.on_btn_pen_clicked)
        

        self.__btn_line = QPushButton()
        self.__btn_line.setFixedSize(70,40)
        self.__btn_line.setIcon(QIcon('./img/line.png'))
        self.__btn_line.setParent(self)
        self.__btn_line.clicked.connect(self.on_btn_line_clicked)

        line1_layout.addWidget(self.__btn_pen)
        line1_layout.addWidget(self.__btn_line)



        self.__btn_ellipse = QPushButton()
        self.__btn_ellipse.setFixedSize(70,40)
        self.__btn_ellipse.setIcon(QIcon('./img/ellipse.png'))
        self.__btn_ellipse.setParent(self)
        self.__btn_ellipse.clicked.connect(self.on_btn_circle_clicked)
        
        self.__btn_rect = QPushButton()
        self.__btn_rect.setFixedSize(70,40)
        self.__btn_rect.setIcon(QIcon('./img/rect.png'))
        self.__btn_rect.setParent(self)
        self.__btn_rect.clicked.connect(self.on_btn_rect_clicked)

        line2_layout.addWidget(self.__btn_ellipse)
        line2_layout.addWidget(self.__btn_rect)


        self.__cbtn_Eraser = QCheckBox("  ")
        self.__cbtn_Eraser.setFixedSize(70,40)
        self.__cbtn_Eraser.setIcon(QIcon('./img/erase.png'))
        self.__cbtn_Eraser.setParent(self)
        self.__cbtn_Eraser.clicked.connect(self.on_cbtn_Eraser_clicked)
        

        self.__btn_color = QPushButton()
        self.__btn_color.setFixedSize(70,40)
        self.__btn_color.setIcon(QIcon('./img/color.png'))
        self.__btn_color.setParent(self)
        self.__btn_color.clicked.connect(self.on_PenColorChange)

        line3_layout.addWidget(self.__cbtn_Eraser)
        line3_layout.addWidget(self.__btn_color)


        self.__label_penThickness = QLabel(self)
        self.__label_penThickness.setText("Thickness")
        self.__label_penThickness.setFixedSize(70,30)
        
        
        self.__spinBox_penThickness = QSpinBox(self)
        self.__spinBox_penThickness.setPrefix(" ")
        self.__spinBox_penThickness.setSuffix(" Pixel")
        self.__spinBox_penThickness.setMaximum(20)
        self.__spinBox_penThickness.setMinimum(1)
        self.__spinBox_penThickness.setValue(10) #默认粗细为10
        self.__spinBox_penThickness.setSingleStep(1) #最小变化值为2
        self.__spinBox_penThickness.valueChanged.connect(self.on_PenThicknessChange)#关联spinBox值变化信号和函数on_PenThicknessChange
        

        line4_layout.addWidget(self.__label_penThickness)
        line4_layout.addWidget(self.__spinBox_penThickness)

        sub_layout.addLayout(line1_layout)
        sub_layout.addLayout(line2_layout)
        sub_layout.addLayout(line3_layout)
        sub_layout.addLayout(line4_layout)
        

        splitter = QSplitter(self) #占位符
        sub_layout.addWidget(splitter)
        

        self.__btn_Clear = QPushButton("Clear")
        self.__btn_Save = QPushButton("Save")
        self.__btn_Quit = QPushButton("Exit")


        #设置父对象为本界面
        self.__btn_Clear.setParent(self) 
        self.__btn_Save.setParent(self)
        self.__btn_Quit.setParent(self) 
        
        
        #关联函数
        self.__btn_Clear.clicked.connect(self.__paintBoard.Clear) 
        self.__btn_Save.clicked.connect(self.on_btn_Save_Clicked)
        self.__btn_Quit.clicked.connect(self.Quit)
               
        sub_layout.addWidget(self.__btn_Clear)
        sub_layout.addWidget(self.__btn_Save)
        sub_layout.addWidget(self.__btn_Quit)
        #将按键按下信号与画板清空函数相关联

        main_layout.addLayout(sub_layout) #将子布局加入主布局
        
        
    
    def on_PenColorChange(self):
        self.__paintBoard.ChangePenColor()


    def on_PenThicknessChange(self):
        penThickness = self.__spinBox_penThickness.value()
        self.__paintBoard.ChangePenThickness(penThickness)


    def on_btn_Save_Clicked(self):
        savePath = QFileDialog.getSaveFileName(self, 'Save Your Paint', '.\\', '*.png')
        print(savePath)
        if savePath[0] == "":
            print("Save cancel")
            return
        image = self.__paintBoard.GetContentAsQImage()
        image.save(savePath[0])


    def on_cbtn_Eraser_clicked(self):
        if self.__cbtn_Eraser.isChecked():
            self.__paintBoard.Mode = "erase" #进入橡皮擦模式
        else:
            self.__paintBoard.Mode = "pen" #退出橡皮擦模式
    
    def on_btn_pen_clicked(self):
        if self.__cbtn_Eraser.isChecked(): return 
        print("pen")
        self.__paintBoard.Mode = "pen"
    
    def on_btn_line_clicked(self):
        if self.__cbtn_Eraser.isChecked(): return 
        print("line")
        self.__paintBoard.Mode = "line"

    def on_btn_circle_clicked(self):
        if self.__cbtn_Eraser.isChecked(): return 
        print("circle")
        self.__paintBoard.Mode = "circle"
    
    def on_btn_rect_clicked(self):
        if self.__cbtn_Eraser.isChecked(): return 
        print("rect")
        self.__paintBoard.Mode = "rect"

        
    def Quit(self):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        print('----')
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()   