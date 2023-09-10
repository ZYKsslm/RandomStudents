import sys
import random
import os
from time import sleep

from PySide6.QtWidgets import *
from PySide6.QtCore import QObject, Signal, QThread
from PySide6.QtGui import QIcon, QPixmap
from qfluentwidgets import SplitFluentWindow, FluentIcon, NavigationItemPosition, Dialog
from ujson import load, dump

from subWindow import MainWindow, SettingWindow, WeightWindow


class Window(SplitFluentWindow):
    def __init__(self):
        super().__init__()
        self.config()
        self.setupUi()
        self.bind()
        
    def config(self):
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                self.data: dict = load(f)
                self.names = list(self.data.keys())
                self.weights = list(self.data.values())
        except:
            Dialog("读取数据失败", "读取json数据失败，请检查json文件位置和完整性！", self).show()

    def setupUi(self):
        self.setWindowTitle("超级整活系统 ver 0.2.0")
        self.setWindowOpacity(0.9)
        self.setWindowIcon(QIcon("icon.ico"))
        self.setFixedSize(500, 600)
        
        self.subWindow = MainWindow()
        self.settingWindow = SettingWindow()
        self.weightWindow = WeightWindow()
        self.addSubInterface(self.subWindow, FluentIcon.HOME, "主页")
        self.addSubInterface(self.settingWindow, FluentIcon.SETTING, "权重设置", NavigationItemPosition.BOTTOM)
        self.settingWindow.table.setFunc(self.setWeight)

        image_path =os.path.join(os.getcwd(), "image")
        self.image_list = os.listdir(image_path)
        self.subWindow.icon_label.setPixmap(QPixmap(f"image/{random.choice(self.image_list)}").scaled(300, 300))
        
        self.settingWindow.table.setColumnCount(2)
        self.settingWindow.table.setColumnWidth(0, 200)
        self.settingWindow.table.setColumnWidth(1, 200)
        self.settingWindow.table.setRowCount(len(self.names))
        self.settingWindow.table.setHorizontalHeaderLabels(["信息", "权重"])
        for i, info in enumerate(self.names):
            self.settingWindow.table.setItem(i, 0, QTableWidgetItem(info))
        for i, weight in enumerate(self.weights):
            self.settingWindow.table.setItem(i, 1, QTableWidgetItem(str(weight)))
        
    def bind(self):
        self.subWindow.button.clicked.connect(self.start)
        self.weightWindow.edit.textChanged.connect(self.set_weight)
        
    def start(self):
        self.result = random.choices(self.names, weights=self.weights)[0]
        self.subWindow.button.setEnabled(False)
        self.counter = Counter(self.names, self.subWindow.name_label)
        self.count_thread = QThread()
        self.counter.moveToThread(self.count_thread)
        self.count_thread.started.connect(self.counter.count)
        self.counter.count_signal.connect(self.end)
        
        self.count_thread.start()
        
    def end(self):
        self.count_thread.quit()
        self.subWindow.button.setEnabled(True)
        self.subWindow.icon_label.setPixmap(QPixmap(f"image/{random.choice(self.image_list)}").scaled(300, 300))
        self.subWindow.name_label.setText(self.result)
        self.subWindow.info_label.setVisible(True)
        
    def setWeight(self, current_row, current_content, current_weight):
        self.current_row = current_row
        self.current_weight = current_weight
        self.current_content = current_content
        self.weightWindow.open()
        
    def set_weight(self, num):
        try:
            int(num)
        except ValueError:
            self.weightWindow.edit.setText(self.current_weight)
        else:
            weight = self.weightWindow.edit.text()
            self.data[self.current_content] = int(weight)
            self.settingWindow.table.setItem(self.current_row, 1, QTableWidgetItem(str(weight)))
            self.weights = list(self.data.values())
            
    def closeEvent(self, event):
        with open("data.json", "w", encoding="utf-8") as f:
            dump(self.data, f)
            
        event.accept()


class Counter(QObject):
    count_signal = Signal()

    def __init__(self, name_list, label: QLabel):
        super().__init__()
        self.name_list = name_list
        self.label = label
        
    def count(self):
        for _ in range(5):
            for n in self.name_list:
                self.label.setText(n)
                sleep(0.001)
            sleep(0.001)
        self.count_signal.emit()


if __name__ == "__main__":
    app = QApplication()
    window = Window()
    window.show()
    sys.exit(app.exec())