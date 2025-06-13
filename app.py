import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QSplitter, QListWidget, QListWidgetItem, QStackedWidget,
    QFrame
)
from PySide6.QtCore import Qt


class FileCompareWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("文件对比功能待开发。")
        layout.addWidget(label)
        self.setLayout(layout)
        self.setup_logic()

    def setup_logic(self):
        pass  # TODO: 文件对比逻辑


class UnixTimestampWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Unix 时间戳转换功能待开发。")
        layout.addWidget(label)
        self.setLayout(layout)
        self.setup_logic()

    def setup_logic(self):
        pass  # TODO: Unix 时间戳转换逻辑


class UUIDGeneratorWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("UUID 生成器功能待开发。")
        layout.addWidget(label)
        self.setLayout(layout)
        self.setup_logic()

    def setup_logic(self):
        pass  # TODO: UUID 生成逻辑


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DUKIT-Dev Utilities Kit")

        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.list_widget = QListWidget()
        self.list_widget.setMaximumWidth(200)
        self.list_widget.addItem(QListWidgetItem("文件对比"))
        self.list_widget.addItem(QListWidgetItem("Unix 时间戳转换"))
        self.list_widget.addItem(QListWidgetItem("UUID 生成器"))

        # 可折叠左侧菜单
        self.list_widget_frame = QFrame()
        self.list_widget_frame.setMinimumWidth(0)  # 允许完全隐藏左侧面板
        self.list_widget_frame.setMaximumWidth(200)  # 设置最大宽度限制
        list_layout = QVBoxLayout()
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.addWidget(self.list_widget)
        self.list_widget_frame.setLayout(list_layout)

        self.stack = QStackedWidget()
        self.stack.addWidget(FileCompareWidget())
        self.stack.addWidget(UnixTimestampWidget())
        self.stack.addWidget(UUIDGeneratorWidget())
        self.stack.setMinimumWidth(400)  # 确保右侧内容区域有最小宽度

        splitter.addWidget(self.list_widget_frame)
        splitter.addWidget(self.stack)
        splitter.setCollapsible(0, True)  # 允许左侧面板被完全折叠
        splitter.setSizes([200, 600])  # 初始分割比例

        self.setCentralWidget(splitter)
        self.list_widget.currentRowChanged.connect(self.stack.setCurrentIndex)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
