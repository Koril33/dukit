import sys

from PySide6.QtGui import QTextCharFormat, QColor
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QSplitter, QListWidget, QListWidgetItem, QStackedWidget,
    QFrame, QHBoxLayout, QTextEdit, QPushButton
)
from PySide6.QtCore import Qt


def _reconstruct(a, b, trace):
    if not trace:  # 无差异时直接返回空列表
        return []

    x, y = len(a), len(b)
    result = []

    # 从最后一步开始回溯
    for d in range(len(trace) - 1, -1, -1):
        current_v = trace[d]  # 当前d层状态
        k = x - y  # 当前对角线位置

        # 确定上一步的k值 (使用安全比较)
        if k == -d or (k != d and current_v.get(k - 1, float('-inf')) < current_v.get(k + 1, float('-inf'))):
            prev_k = k + 1  # 上一步是向下移动(插入)
        else:
            prev_k = k - 1  # 上一步是向右移动(删除)

        # 获取上一步坐标 (关键修复)
        if d > 0:
            prev_v = trace[d-1]  # 上一步的状态字典
            prev_x = prev_v[prev_k]
        else:  # d=0时到达起点
            prev_x = 0
        prev_y = prev_x - prev_k

        # 处理对角线移动(相同字符)
        while x > prev_x and y > prev_y:
            result.append("  " + a[x - 1])  # 空格表示未修改
            x -= 1
            y -= 1

        # 记录差异操作
        if d > 0:  # 避免在起点(0,0)操作
            if prev_x == x:
                result.append("+ " + b[prev_y])  # 插入操作
            else:
                result.append("- " + a[prev_x])  # 删除操作
            x, y = prev_x, prev_y  # 更新当前位置

    result.reverse()  # 反转结果列表
    return result


def myers_diff(a, b):
    N, M = len(a), len(b)
    max_edit = N + M
    trace = []  # 存储每层的状态

    v = {1: 0}  # 初始状态
    for d in range(0, max_edit + 1):
        current_v = {}
        # 遍历k值范围(-d到d)，步长为2
        for k in range(-d, d + 1, 2):
            # 确定移动方向 (使用安全访问)
            if k == -d or (k != d and v.get(k - 1, -1) < v.get(k + 1, -1)):
                x = v.get(k + 1, 0)
            else:
                x = v.get(k - 1, 0) + 1
            y = x - k

            # 沿对角线移动(相同行)
            while x < N and y < M and a[x] == b[y]:
                x += 1
                y += 1

            current_v[k] = x  # 记录当前位置

            # 终点检测 (修复边界条件)
            if x >= N and y >= M:
                trace.append(current_v)
                return _reconstruct(a, b, trace)

        trace.append(current_v)
        v = current_v  # 更新状态

    return []  # 无差异时返回空列表


class FileCompareWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.compare_button = None
        self.diff_result = None
        self.right_text = None
        self.left_text = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        editor_layout = QHBoxLayout()
        self.left_text = QTextEdit()
        self.right_text = QTextEdit()
        self.left_text.setPlaceholderText("旧文本")
        self.right_text.setPlaceholderText("新文本")
        editor_layout.addWidget(self.left_text)
        editor_layout.addWidget(self.right_text)

        self.diff_result = QTextEdit()
        self.diff_result.setReadOnly(True)
        self.diff_result.setFontFamily("Courier New")

        self.compare_button = QPushButton("比较差异")
        self.compare_button.clicked.connect(self.run_diff)

        layout.addLayout(editor_layout)
        layout.addWidget(self.compare_button)
        layout.addWidget(QLabel("对比结果："))
        layout.addWidget(self.diff_result)

        self.setLayout(layout)

    def run_diff(self):
        a_lines = self.left_text.toPlainText().splitlines()
        b_lines = self.right_text.toPlainText().splitlines()

        diff = myers_diff(a_lines, b_lines)

        self.diff_result.clear()
        cursor = self.diff_result.textCursor()

        for line in diff:
            fmt = QTextCharFormat()
            if line.startswith("-"):
                fmt.setForeground(QColor("red"))
            elif line.startswith("+"):
                fmt.setForeground(QColor("green"))
            else:
                fmt.setForeground(QColor("gray"))

            cursor.setCharFormat(fmt)
            cursor.insertText(line + "\n")


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
