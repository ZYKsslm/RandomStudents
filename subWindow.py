from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon

from qfluentwidgets import PrimaryPushButton, TableWidget, RoundMenu, MenuAnimationType, LineEdit
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        
    def setupUI(self):
        self.resize(500, 600)
        self.setObjectName("MainWindow")
        self.name_label = QLabel("点击开始")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setStyleSheet("font-size: 40px")
        
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.button = PrimaryPushButton("开始")
        
        self.info_label = QLabel("哇，贞德食泥鸭~~~")
        self.info_label.setStyleSheet("font-size: 20px")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setVisible(False)
        
        self.box = QVBoxLayout()
        self.setLayout(self.box)
        
        self.box.setSpacing(50)
        self.box.addWidget(self.icon_label)
        self.box.addWidget(self.name_label)
        self.box.setSpacing(50)
        self.box.addWidget(self.button)
        self.box.addWidget(self.info_label)
        self.box.addSpacing(50)


class CustomTableWidget(TableWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
    def setFunc(self, func):
        self.func = func 
    
    def contextMenuEvent(self, event):
        if self.rowCount() == 0 and self.columnCount() == 0:
            return
        menu = RoundMenu("", self)
        
        # 获取当前行数和内容
        current_row = self.currentRow()
        current_content = self.item(current_row, 0).text()
        current_weight = self.item(current_row, 1).text()
        
        weight_action = QAction("修改权重", self)
        
        weight_action.triggered.connect(lambda: self.func(current_row, current_content, current_weight))
        
        menu.addAction(weight_action)
        menu.exec(event.globalPos(), MenuAnimationType.PULL_UP)


class SettingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
    
    def setupUi(self):
        self.setObjectName("SettingWindow")
        self.table = CustomTableWidget(self)
        self.table.setGeometry(20, 50, 400, 520)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        

class WeightWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi()
        
    def setupUi(self):
        self.setWindowTitle("修改权重")
        self.setWindowOpacity(0.9)
        self.setWindowIcon(QIcon("icon.ico"))
        self.edit = LineEdit()
        self.box = QVBoxLayout()
        self.setLayout(self.box)
        self.box.addSpacing(10)
        self.box.addWidget(self.edit)
        self.box.addSpacing(10)