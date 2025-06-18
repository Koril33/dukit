import uuid
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                               QPlainTextEdit, QComboBox, QWidget, QSpinBox,
                               QFrame, QSizePolicy)
from PySide6.QtCore import Qt


class UUIDGeneratorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.uuid_display = None
        self.generate_button = None
        self.count_spin = None
        self.version_combo = None
        self.init_ui()
        self.setup_logic()

        # 设置窗口初始大小
        self.setMinimumSize(500, 400)

    def init_ui(self):
        # 主垂直布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        # 顶部设置区域
        settings_frame = QFrame()
        settings_frame.setFrameShape(QFrame.Shape.StyledPanel)
        settings_layout = QVBoxLayout(settings_frame)
        settings_layout.setContentsMargins(15, 15, 15, 15)

        # 版本选择
        version_layout = QHBoxLayout()
        version_layout.addWidget(QLabel("UUID 版本:"))
        self.version_combo = QComboBox()
        self.version_combo.addItems(["UUID v1", "UUID v4"])
        version_layout.addWidget(self.version_combo)
        settings_layout.addLayout(version_layout)

        # 数量选择
        count_layout = QHBoxLayout()
        count_layout.addWidget(QLabel("生成数量:"))
        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 100)  # 限制1-100个
        self.count_spin.setValue(5)  # 默认生成5个
        count_layout.addWidget(self.count_spin)
        settings_layout.addLayout(count_layout)

        # 生成按钮
        self.generate_button = QPushButton("生成 UUID")
        self.generate_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        settings_layout.addWidget(self.generate_button, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(settings_frame)

        # 结果显示区域
        results_frame = QFrame()
        results_frame.setFrameShape(QFrame.Shape.StyledPanel)
        results_layout = QVBoxLayout(results_frame)
        results_layout.setContentsMargins(15, 15, 15, 15)

        results_layout.addWidget(QLabel("生成的 UUID:"))

        # 使用QPlainTextEdit作为多行文本框[6,7](@ref)
        self.uuid_display = QPlainTextEdit()
        self.uuid_display.setReadOnly(True)
        self.uuid_display.setPlaceholderText("点击上方按钮生成UUID...")
        self.uuid_display.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)  # 不自动换行
        self.uuid_display.setStyleSheet("font-family: monospace;")  # 等宽字体
        results_layout.addWidget(self.uuid_display)

        main_layout.addWidget(results_frame, stretch=1)  # 结果区域占据剩余空间

        self.setLayout(main_layout)

    def setup_logic(self):
        self.generate_button.clicked.connect(self.generate_uuid)

    def generate_uuid(self):
        version_index = self.version_combo.currentIndex()
        count = self.count_spin.value()

        try:
            uuids = []
            for _ in range(count):
                if version_index == 0:
                    uuids.append(str(uuid.uuid1()))
                else:
                    uuids.append(str(uuid.uuid4()))

            # 将生成的UUID显示在多行文本框中[6](@ref)
            self.uuid_display.setPlainText("\n".join(uuids))

        except Exception as e:
            self.uuid_display.setPlainText(f"错误: {str(e)}")