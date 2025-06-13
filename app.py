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
        list_layout = QVBoxLayout()
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.addWidget(self.list_widget)
        self.list_widget_frame.setLayout(list_layout)

        self.stack = QStackedWidget()
        self.stack.addWidget(FileCompareWidget())
        self.stack.addWidget(UnixTimestampWidget())
        self.stack.addWidget(UUIDGeneratorWidget())

        splitter.addWidget(self.list_widget_frame)
        splitter.addWidget(self.stack)
        splitter.setStretchFactor(1, 1)

        self.setCentralWidget(splitter)

        self.list_widget.currentRowChanged.connect(self.stack.setCurrentIndex)

    def keyPressEvent(self, event):
        # 用 Tab 键切换左侧面板显示/隐藏
        if event.key() == Qt.Key.Key_Tab:
            if self.list_widget_frame.isVisible():
                self.list_widget_frame.hide()
            else:
                self.list_widget_frame.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
