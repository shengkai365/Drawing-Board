from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 


class PaintBoard(QWidget):
    def __init__(self, Parent=None):
        '''
        Constructor
        '''
        super().__init__(Parent)

        self.__InitData() #先初始化数据，再初始化界面
        self.__InitView()
        
    def __InitData(self):
        
        # self.__size = QSize(480, 460)
        self.__size = QSize(600, 580)
        
        #新建QPixmap作为画板，尺寸为__size
        self.__board = QPixmap(self.__size)
        self.__board.fill(Qt.white) #用白色填充画板
        self.__tmpBoard = QPixmap(self.__board)
        self.__IsEmpty = True #默认为空画板 

        #模式: "pen","erase","circle","rect","line"
        self.Mode = "pen"
        
        self.__startPos = QPoint(0,0)#摁下鼠标的起始位置
        self.__lastPos = QPoint(0,0)#上一次鼠标位置
        self.__currentPos = QPoint(0,0)#当前的鼠标位置
        
        self.__painter = QPainter()#新建绘图工具
        self.__painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing) # 反走样

        self.__thickness = 10       #默认画笔粗细为10px
        self.__penColor = QColor("black")#设置默认画笔颜色为黑色
        
     
    def __InitView(self):
        #设置界面的尺寸为__size
        self.setFixedSize(self.__size)
        
    def Clear(self):
        #清空画板
        self.__board.fill(Qt.white)
        self.__tmpBoard.fill(Qt.white)
        self.update()
        self.__IsEmpty = True
        
    def ChangePenColor(self):
        #改变画笔颜色
        color= QColorDialog.getColor()
        if color.isValid():
            self.__penColor = QColor(color)
        
    def ChangePenThickness(self, thickness=10):
        #改变画笔粗细
        self.__thickness = thickness
        
    def IsEmpty(self):
        #返回画板是否为空
        return self.__IsEmpty
    
    def GetContentAsQImage(self):
        #获取画板内容（返回QImage）
        image = self.__board.toImage()
        return image
        
    def paintEvent(self, paintEvent):
        #绘图事件
        #绘图时必须使用QPainter的实例，此处为__painter
        #绘图在begin()函数与end()函数间进行
        #begin(param)的参数要指定绘图设备，即把图画在哪里
        #drawPixmap用于绘制QPixmap类型的对象
        self.__painter.begin(self)
        # 0,0为绘图的左上角起点的坐标，__board即要绘制的图
        
        if self.Mode in ["pen","erase"]:
            print('--board')
            self.__painter.drawPixmap(0,0,self.__board)
        else:
            self.__painter.drawPixmap(0,0,self.__tmpBoard)
            print('tmp---board')
        self.__painter.end()
        
    def mousePressEvent(self, mouseEvent):
        #鼠标按下时，获取鼠标的当前位置保存为上一次位置
        self.__currentPos =  mouseEvent.pos()
        self.__lastPos = self.__currentPos
        self.__startPos = self.__currentPos 
        
        
    def mouseMoveEvent(self, mouseEvent):
        #鼠标移动时，更新当前位置，并在上一个位置和当前位置间画线
        self.__currentPos =  mouseEvent.pos()
        self.__tmpBoard = QPixmap(self.__board)
        x = self.__startPos.x()
        y = self.__startPos.y()
        w = self.__currentPos.x() - x
        h = self.__currentPos.y() - y

        
        
        if self.Mode=='pen':
            self.__painter.begin(self.__board)
            #pen
            self.__painter.setPen(QPen(self.__penColor,self.__thickness)) #设置画笔颜色，粗细
            self.__painter.drawLine(self.__lastPos, self.__currentPos)
            self.__painter.end()
        
        elif self.Mode=='erase':
            self.__painter.begin(self.__board)
            #erase
            self.__painter.setPen(QPen(Qt.white,self.__thickness))
            self.__painter.drawLine(self.__lastPos, self.__currentPos)
            self.__painter.end()
    
            
        elif self.Mode == 'line':
            self.__painter.begin(self.__tmpBoard)
            self.__painter.setPen(QPen(self.__penColor,self.__thickness)) #设置画笔颜色，粗细
            self.__painter.drawLine(self.__startPos, self.__currentPos)
            self.__painter.end()

        elif self.Mode == 'circle':
            self.__painter.begin(self.__tmpBoard)
            self.__painter.setPen(QPen(self.__penColor,self.__thickness)) #设置画笔颜色，粗细
            self.__painter.drawEllipse(x,y,w,h)
            self.__painter.end()
        else:
            self.__painter.begin(self.__tmpBoard)
            self.__painter.setPen(QPen(self.__penColor,self.__thickness)) #设置画笔颜色，粗细
            self.__painter.drawRect(x,y,w,h)
            self.__painter.end()
       

        self.__lastPos = self.__currentPos
        self.update() #更新显示
        
    def mouseReleaseEvent(self, mouseEvent):
        self.__lastPos = mouseEvent.pos()
        self.__IsEmpty = False #画板不再为空
        x = self.__startPos.x()
        y = self.__startPos.y()
        w = self.__lastPos.x() - x
        h = self.__lastPos.y() - y

        
        if self.Mode in ["pen","erase"]: return 
        self.__painter.begin(self.__board)

        self.__painter.setPen(QPen(self.__penColor,self.__thickness)) #设置画笔颜色，粗细

        if self.Mode == "line":
            self.__painter.drawLine(self.__startPos, self.__currentPos)
            
        elif self.Mode == "circle":
            self.__painter.drawEllipse(x,y,w,h)
        else: #rect 
            self.__painter.drawRect(x,y,w,h)
            
        self.__painter.end()
        self.__lastPos = self.__currentPos    
        self.update() #更新显示