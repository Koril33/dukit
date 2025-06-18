import hashlib
import time

from PySide6.QtCore import QSize, QRect, Qt
from PySide6.QtGui import QFont, QPainter, QColor, QTextCharFormat, QTextFormat
from PySide6.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit


def hash_text(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def reconstruct(a, b, trace):
    if not trace:
        return []

    x, y = len(a), len(b)
    result = []

    for d in range(len(trace) - 1, -1, -1):
        current_v = trace[d]
        k = x - y

        # 获取前一步的k值
        if d == 0:
            prev_k = None  # d=0时无前一步
        else:
            if k == -d:
                prev_k = k + 1  # 边界情况：最左侧只能从k+1来
            elif k == d:
                prev_k = k - 1  # 边界情况：最右侧只能从k-1来
            else:
                # 使用d-1步的v数据进行比较
                prev_v = trace[d - 1]
                # 比较prev_v中k-1和k+1的值
                val_km1 = prev_v.get(k - 1, float('-inf'))
                val_kp1 = prev_v.get(k + 1, float('-inf'))
                if val_km1 < val_kp1:
                    prev_k = k + 1  # 从上方移动（插入）
                else:
                    prev_k = k - 1  # 从左侧移动（删除）

        # 计算前一步的坐标
        if d > 0:
            prev_x = trace[d - 1][prev_k]
            prev_y = prev_x - prev_k
        else:
            prev_x, prev_y = 0, 0  # d=0时起点为(0,0)

        # 回溯对角线（相同元素）
        while x > prev_x and y > prev_y:
            result.append("  " + a[x - 1])
            x -= 1
            y -= 1

        # 回溯非对角线移动（插入/删除）
        if d > 0:
            if prev_x == x:
                result.append("+ " + b[prev_y])  # 插入
            else:
                result.append("- " + a[prev_x])  # 删除
            x, y = prev_x, prev_y  # 更新为前一步坐标

    result.reverse()
    return result


def myers_diff(a, b):
    N, M = len(a), len(b)
    max_edit = N + M

    # 记录每一步到达的位置
    trace = []

    # v - 记录该 k 线上到达的最远的 x 坐标
    v = {1: 0}
    for d in range(0, max_edit + 1):
        current_v = {}
        # 从起点出发走出 d 步时，它只可能落在 k={-d, -d+2, ...., d-2, d} 的 k 线上
        # 循环，计算这一步可能落在的每条 k 线上的最远位置，直到碰到终点为止
        for k in range(-d, d + 1, 2):

            # 选择前一步 v 中 k 线上走得最远的 x
            # k == -d: 最左边的对角线，没有 k-1，只能从 k+1 下移过来
            # 如果当前不是最右边的对角线（否则没有 k+1）比较 v[k - 1] 和 v[k + 1]，谁的 x 更小
            if k == -d or (k != d and v.get(k - 1, -1) < v.get(k + 1, -1)):
                # 对 a 插入操作，向下移动 x 坐标不变
                x = v.get(k + 1, 0)
            else:
                # 对 a 删除操作 +1 表示向右移动，删除元素
                x = v.get(k - 1, 0) + 1
            # 通过 k 推算出 y 坐标
            y = x - k
            # 斜对角移动
            while x < N and y < M and a[x] == b[y]:
                x += 1
                y += 1

            current_v[k] = x

            # 找到最短编辑序列，结束搜索并且构造差异序列
            if x >= N and y >= M:
                trace.append(current_v)
                return reconstruct(a, b, trace)

        trace.append(current_v)
        v = current_v

    return []


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        # 根据行号位数计算宽度
        digits = len(str(max(1, self.editor.blockCount())))
        space = 3 + self.editor.fontMetrics().horizontalAdvance('9') * digits + 5
        return QSize(space, 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class CustomPlainTextEdit(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.lineNumberArea = LineNumberArea(self)
        self.setFont(QFont("Consolas", 12))
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.textChanged.connect(self.update_line_number_area_width)
        self.verticalScrollBar().valueChanged.connect(self.update_line_number_area_on_scroll)
        self.updateRequest.connect(self.update_line_number_area)
        self.update_line_number_area_width()
        self.cursorPositionChanged.connect(self.highlight_current_line)

    def highlight_current_line(self):
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(Qt.GlobalColor.yellow).lighter(160)  # 浅黄色背景
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def update_line_number_area_width(self):
        self.setViewportMargins(self.lineNumberArea.sizeHint().width(), 0, 0, 0)
        self.lineNumberArea.update()

    def update_line_number_area_on_scroll(self, value):
        self.lineNumberArea.update()

    def update_line_number_area(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberArea.sizeHint().width(), cr.height()))

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor("#f0f0f0"))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        font_metrics = self.fontMetrics()
        line_height = font_metrics.height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and top + line_height >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.GlobalColor.black)
                painter.drawText(0, int(top), self.lineNumberArea.width() - 3, line_height,
                                 Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, number)
            block = block.next()
            block_number += 1
            top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()


class FileCompareWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.clear_all_text_button = None
        self.clear_right_text_button = None
        self.clear_left_text_button = None
        self.compare_button = None
        self.diff_result = None
        self.right_text = None
        self.left_text = None
        self.setup_ui()

    def clear_all_texts(self):
        self.left_text.clear()
        self.right_text.clear()
        self.diff_result.clear()

    def setup_ui(self):
        layout = QVBoxLayout()

        editor_layout = QHBoxLayout()
        self.left_text = CustomPlainTextEdit()
        self.right_text = CustomPlainTextEdit()
        self.left_text.setPlaceholderText("旧文本")
        self.right_text.setPlaceholderText("新文本")
        editor_layout.addWidget(self.left_text)
        editor_layout.addWidget(self.right_text)

        self.diff_result = CustomPlainTextEdit()
        self.diff_result.setReadOnly(True)

        btn_layout = QHBoxLayout()

        self.compare_button = QPushButton("比较差异")
        self.compare_button.clicked.connect(self.run_diff)
        self.clear_left_text_button = QPushButton("清空左侧")
        self.clear_right_text_button = QPushButton("清空右侧")
        self.clear_all_text_button = QPushButton("清空所有")
        self.clear_left_text_button.clicked.connect(self.left_text.clear)
        self.clear_right_text_button.clicked.connect(self.right_text.clear)
        self.clear_all_text_button.clicked.connect(self.clear_all_texts)


        layout.addLayout(editor_layout)
        btn_layout.addWidget(self.compare_button)
        btn_layout.addWidget(self.clear_left_text_button)
        btn_layout.addWidget(self.clear_right_text_button)
        btn_layout.addWidget(self.clear_all_text_button)
        layout.addLayout(btn_layout)

        layout.addWidget(QLabel("对比结果："))
        layout.addWidget(self.diff_result)

        self.setLayout(layout)

    def run_diff(self):
        start_time = int(time.time() * 1000)
        self.diff_result.clear()
        cursor = self.diff_result.textCursor()

        a_text = self.left_text.toPlainText()
        b_text = self.right_text.toPlainText()

        if hash_text(a_text) == hash_text(b_text):
            cursor.insertText("两个文本完全一致")
        else:
            a_lines = a_text.splitlines()
            b_lines = b_text.splitlines()
            diff = myers_diff(a_lines, b_lines)
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
        end_time = int(time.time() * 1000)
        if self.main_window:
            self.main_window.update_status(f'文件对比完成，耗时: {end_time - start_time} 毫秒')