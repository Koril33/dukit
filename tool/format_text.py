import re
import json
import xml.etree.ElementTree as ET
from PySide6.QtWidgets import (
    QWidget, QSplitter, QVBoxLayout, QPlainTextEdit, QComboBox,
    QLabel, QHBoxLayout, QApplication, QTextEdit
)
from PySide6.QtCore import Qt, QTimer
from pygments import lexers, highlight
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name


class FormatTextWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.original_edit = None
        self.detected_label = None
        self.language_combo = None
        self.formatted_document = None
        self.formatted_display = None
        self.setWindowTitle("代码格式化工具")
        # self.setMinimumSize(1000, 600)

        # 语言支持列表
        self.supported_languages = {
            "XML": "xml",
            "JSON": "json",
            "Python": "python",
            "C": "c",
            "C++": "cpp",
            "Java": "java",
            "Go": "go",
            "YAML": "yaml",
            "SQL": "sql",
            "Plain Text": "text"
        }

        self.init_ui()
        self.setup_connections()

        # 初始化高亮样式
        self.formatter = HtmlFormatter(
            style=get_style_by_name("monokai"),
            full=False,
            noclasses=True
        )

        # 防抖定时器
        self.update_timer = QTimer()
        self.update_timer.setInterval(500)
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self.update_formatted_text)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # 控制面板
        control_layout = QHBoxLayout()
        control_layout.addWidget(QLabel("语言检测:"))

        self.language_combo = QComboBox()
        self.language_combo.addItems(self.supported_languages.keys())
        self.language_combo.setCurrentText("Plain Text")
        self.language_combo.setMinimumWidth(150)
        control_layout.addWidget(self.language_combo)

        self.detected_label = QLabel("检测结果: 等待输入...")
        control_layout.addWidget(self.detected_label)

        control_layout.addStretch()
        main_layout.addLayout(control_layout)

        # 文本编辑区域
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # 原始文本编辑区
        self.original_edit = QPlainTextEdit()
        self.original_edit.setPlaceholderText("在此输入代码...")
        self.original_edit.setStyleSheet("""
            QPlainTextEdit {
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12pt;
                background-color: #2d2d2d;
                color: #f8f8f2;
            }
        """)
        splitter.addWidget(self.original_edit)

        # 格式化文本显示区
        # 右侧显示控件优化
        self.formatted_display = QTextEdit()
        self.formatted_display.setReadOnly(True)

        self.formatted_display.setStyleSheet("""
            QTextEdit {
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12pt;
                background-color: #2d2d2d;
                color: #f8f8f2;
            }
        """)

        # 提升富文本渲染性能
        self.formatted_document = self.formatted_display.document()
        self.formatted_document.setDefaultStyleSheet("""
                pre { 
                    font-family: 'Consolas', monospace; 
                    background-color: #2d2d2d;
                    padding: 10px;
                    border-radius: 4px;
                }
            """)
        splitter.addWidget(self.formatted_display)

        splitter.setSizes([500, 500])
        main_layout.addWidget(splitter, 1)

        self.setLayout(main_layout)

    def setup_connections(self):
        self.original_edit.textChanged.connect(self.start_update_timer)
        self.language_combo.currentTextChanged.connect(self.update_formatted_text)

    def start_update_timer(self):
        self.update_timer.start()

    def detect_language(self, text):
        """自动检测代码语言[1,4](@ref)"""
        if not text.strip():
            return "Plain Text"

        # 检测XML
        if re.match(r'^\s*<(\?xml|!DOCTYPE|html|root|soap|rss)', text, re.I):
            return "XML"

        # 检测JSON
        if re.match(r'^\s*[{\[]', text):
            try:
                json.loads(text)
                return "JSON"
            except:
                pass

        # 检测Python
        if re.search(r'^\s*(import|def|class|from)\s', text, re.M):
            return "Python"

        # 检测C/C++
        if re.search(r'^\s*#\s*include|^\s*(int|void|class)\s+\w+\s*\(', text, re.M):
            return "C++" if re.search(r'^\s*#\s*include\s*<iostream>', text) else "C"

        # 检测Java
        if re.search(r'^\s*(package|import|public\s+class)\s', text, re.M):
            return "Java"

        # 检测Go
        if re.search(r'^\s*(package|import|func)\s', text, re.M):
            return "Go"

        # 检测SQL
        if re.search(r'\b(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER)\b', text, re.I):
            return "SQL"

        # 检测YAML
        if re.search(r'^\s*[\w-]+\s*:', text) and not re.search(r'{\s*}', text):
            return "YAML"

        return "Plain Text"

    def format_text(self, text, language):
        """格式化不同语言的代码[1,4](@ref)"""
        if not text.strip():
            return ""

        # 格式化JSON
        if language == "JSON":
            try:
                parsed = json.loads(text)
                return json.dumps(parsed, indent=4)
            except Exception:
                return text  # 返回原始文本

        # 格式化XML
        if language == "XML":
            try:
                root = ET.fromstring(text)
                ET.indent(root, space="  ")
                return ET.tostring(root, encoding="unicode", method="xml")
            except Exception:
                return text  # 返回原始文本

        # 其他语言保持原样
        return text

    def highlight_code(self, text, language):
        """使用Pygments进行代码高亮[7](@ref)"""
        if not text.strip():
            return ""

        lang_alias = self.supported_languages[language]

        try:
            # 获取语言对应的词法分析器
            lexer = lexers.get_lexer_by_name(lang_alias)
            # 生成带样式的HTML
            highlighted = highlight(text, lexer, self.formatter)
            return highlighted
        except Exception:
            # 高亮失败时返回纯文本
            return f"<pre>{text}</pre>"

    def update_formatted_text(self):
        """更新右侧格式化后的文本"""
        text = self.original_edit.toPlainText()

        # 自动检测语言
        detected_lang = self.detect_language(text)
        self.detected_label.setText(f"检测结果: {detected_lang}")

        # 更新语言选择框
        if detected_lang != self.language_combo.currentText():
            self.language_combo.setCurrentText(detected_lang)

        # 格式化文本
        formatted = self.format_text(text, detected_lang)

        # 应用语法高亮
        highlighted = self.highlight_code(formatted, detected_lang)

        # 显示在右侧编辑框
        # self.formatted_display.textCursor().insertText(highlighted)
        self.formatted_display.setHtml(highlighted)


if __name__ == "__main__":
    app = QApplication()
    widget = FormatTextWidget()
    widget.show()
    app.exec()