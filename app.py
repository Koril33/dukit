import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QSplitter, QListWidget, QListWidgetItem, QStackedWidget,
    QFrame
)

from tool.file_diff import FileCompareWidget
from tool.format_text import FormatTextWidget
from tool.unix_timestamp import UnixTimestampWidget
from tool.uuid_generator import UUIDGeneratorWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DUKIT-Dev Utilities Kit")

        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.list_widget = QListWidget()
        self.list_widget.setMaximumWidth(200)
        self.list_widget.addItem(QListWidgetItem("文件对比"))
        self.list_widget.addItem(QListWidgetItem("UUID 生成器"))
        self.list_widget.addItem(QListWidgetItem("Unix 时间戳转换"))
        self.list_widget.addItem(QListWidgetItem("文本格式化"))

        # 可折叠左侧菜单
        self.list_widget_frame = QFrame()
        self.list_widget_frame.setMinimumWidth(0)  # 允许完全隐藏左侧面板
        self.list_widget_frame.setMaximumWidth(200)  # 设置最大宽度限制
        list_layout = QVBoxLayout()
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.addWidget(self.list_widget)
        self.list_widget_frame.setLayout(list_layout)

        self.stack = QStackedWidget()

        self.file_compare_widget = FileCompareWidget(main_window=self)
        self.stack.addWidget(self.file_compare_widget)

        self.uuid_generator_widget = UUIDGeneratorWidget()
        self.stack.addWidget(self.uuid_generator_widget)

        self.unix_timestamp_widget = UnixTimestampWidget()
        self.stack.addWidget(self.unix_timestamp_widget)

        self.format_text_widget = FormatTextWidget()
        self.stack.addWidget(self.format_text_widget)

        self.stack.setMinimumWidth(400)  # 确保右侧内容区域有最小宽度

        splitter.addWidget(self.list_widget_frame)
        splitter.addWidget(self.stack)
        splitter.setCollapsible(0, True)  # 允许左侧面板被完全折叠
        splitter.setSizes([200, 600])  # 初始分割比例

        self.setCentralWidget(splitter)
        self.list_widget.currentRowChanged.connect(self.stack.setCurrentIndex)

    def update_status(self, message: str) -> None:
        self.statusBar().showMessage(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
