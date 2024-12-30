from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QLabel, QFileDialog, QLineEdit,
                           QComboBox, QMessageBox, QTextEdit, QCheckBox)
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QFont
from ffmpeg_handler import FFmpegHandler
from logger import Logger
from i18n import I18n

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ffmpeg = FFmpegHandler()
        self.logger = Logger()
        self.logger.main_window = self
        self.i18n = I18n('zh_CN')  # 默认使用中文
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle(self.i18n.get('window_title'))
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 语言选择
        lang_layout = QHBoxLayout()
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(['简体中文', 'English'])
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        lang_layout.addWidget(QLabel('Language/语言:'))
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        layout.addLayout(lang_layout)
        
        # 输入视频选择
        input_layout = QHBoxLayout()
        self.input_path = QLineEdit()
        select_input_btn = QPushButton(self.i18n.get('select_video'))
        select_input_btn.clicked.connect(self.select_input_file)
        input_layout.addWidget(QLabel(self.i18n.get('input_video')))
        input_layout.addWidget(self.input_path)
        input_layout.addWidget(select_input_btn)
        layout.addLayout(input_layout)
        
        # 时间选择
        time_layout = QHBoxLayout()
        self.start_time = QLineEdit()
        self.end_time = QLineEdit()
        time_layout.addWidget(QLabel(self.i18n.get('start_time')))
        time_layout.addWidget(self.start_time)
        time_layout.addWidget(QLabel(self.i18n.get('end_time')))
        time_layout.addWidget(self.end_time)
        layout.addLayout(time_layout)
        
        # 输出设置
        output_layout = QHBoxLayout()
        self.output_path = QLineEdit()
        select_output_btn = QPushButton(self.i18n.get('select_save'))
        select_output_btn.clicked.connect(self.select_output_path)
        output_layout.addWidget(QLabel(self.i18n.get('output_path')))
        output_layout.addWidget(self.output_path)
        output_layout.addWidget(select_output_btn)
        layout.addLayout(output_layout)
        
        # 格式选择
        format_layout = QHBoxLayout()
        self.format_combo = QComboBox()
        self.format_combo.addItems([self.i18n.get('original_format'), 'MP4', 'AVI', 'MKV'])
        format_layout.addWidget(QLabel(self.i18n.get('output_format')))
        format_layout.addWidget(self.format_combo)
        
        # 添加音频选项
        self.audio_only_checkbox = QCheckBox(self.i18n.get('audio_only'))
        format_layout.addWidget(self.audio_only_checkbox)
        layout.addLayout(format_layout)
        
        # 剪辑按钮
        self.cut_btn = QPushButton(self.i18n.get('start_cutting'))
        self.cut_btn.clicked.connect(self.start_cutting)
        layout.addWidget(self.cut_btn)
        
        # 日志显示
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(QLabel(self.i18n.get('log')))
        layout.addWidget(self.log_text)
        
        # 添加作者信息标签
        self.author_label = QLabel('Author: C丶NOVICE', self)
        self.author_label.setStyleSheet('color: gray;')
        self.author_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        layout.addWidget(self.author_label)

    def change_language(self, index):
        # 切换语言
        self.i18n.language = 'en_US' if index == 1 else 'zh_CN'
        # 更新界面文本
        self.update_ui_texts()

    def update_ui_texts(self):
        # 更新窗口标题
        self.setWindowTitle(self.i18n.get('window_title'))
        
        # 更新所有标签文本
        for label in self.findChildren(QLabel):
            if label != self.author_label:  # 跳过作者信息标签
                text = label.text().rstrip(':')  # 移除可能的冒号
                # 查找对应的翻译键
                for key in self.i18n.translations['zh_CN'].keys():
                    if (self.i18n.translations['zh_CN'][key].rstrip(':') == text or 
                        self.i18n.translations['en_US'][key].rstrip(':') == text):
                        label.setText(self.i18n.get(key))
                        break

        # 更新按钮文本
        for button in self.findChildren(QPushButton):
            text = button.text()
            for key in self.i18n.translations['zh_CN'].keys():
                if (self.i18n.translations['zh_CN'][key] == text or 
                    self.i18n.translations['en_US'][key] == text):
                    button.setText(self.i18n.get(key))
                    break

        # 更新复选框文本
        self.audio_only_checkbox.setText(self.i18n.get('audio_only'))

        # 更新格式选择框
        current_format = self.format_combo.currentText()
        self.format_combo.clear()
        self.format_combo.addItems([
            self.i18n.get('original_format'),
            'MP4', 'AVI', 'MKV'
        ])
        
        # 处理格式选择的当前值
        if current_format in [
            self.i18n.translations['zh_CN']['original_format'], 
            self.i18n.translations['en_US']['original_format']
        ]:
            self.format_combo.setCurrentText(self.i18n.get('original_format'))
        else:
            self.format_combo.setCurrentText(current_format)

        # 更新剪辑按钮文本
        self.cut_btn.setText(self.i18n.get('start_cutting'))

    def select_input_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, self.i18n.get('select_video'), '',
                                                 'Video Files (*.mp4 *.avi *.mkv *.mov);;All Files (*)')
        if file_name:
            self.input_path.setText(file_name)
            self.logger.log(self.i18n.get('select_input_file', file_name))
            
            start_time, end_time = self.ffmpeg.get_video_duration(file_name, self.logger.log)
            if start_time and end_time:
                self.start_time.setText(start_time)
                self.end_time.setText(end_time)
                self.logger.log(self.i18n.get('set_time_range', start_time, end_time))
            
    def select_output_path(self):
        file_filter = 'Audio Files (*.mp3)' if self.audio_only_checkbox.isChecked() else 'Video Files (*.mp4 *.avi *.mkv *.mov);;All Files (*)'
        file_name, _ = QFileDialog.getSaveFileName(self, self.i18n.get('select_save'), '', file_filter)
        if file_name:
            if self.audio_only_checkbox.isChecked() and not file_name.lower().endswith('.mp3'):
                file_name += '.mp3'
            self.output_path.setText(file_name)
            self.logger.log(self.i18n.get('select_output_path', file_name))
            
    def start_cutting(self):
        input_file = self.input_path.text()
        output_file = self.output_path.text()
        start_time = self.start_time.text()
        end_time = self.end_time.text()
        audio_only = self.audio_only_checkbox.isChecked()
        
        if not all([input_file, output_file, start_time, end_time]):
            QMessageBox.warning(self, self.i18n.get('warning'),
                              self.i18n.get('fill_all'))
            return
            
        try:
            self.ffmpeg.cut_video(input_file, output_file, start_time, end_time,
                                audio_only, self.logger.log)
            QMessageBox.information(self, self.i18n.get('success'),
                                  self.i18n.get('process_complete'))
        except Exception as e:
            QMessageBox.critical(self, self.i18n.get('error'),
                               self.i18n.get('process_failed', str(e))) 

    def resizeEvent(self, event):
        # 确保作者信息始终在右下角
        super().resizeEvent(event)
        margin = 10
        label_width = 150
        label_height = 20
        self.author_label.setGeometry(
            self.width() - label_width - margin,
            self.height() - label_height - margin,
            label_width,
            label_height
        ) 