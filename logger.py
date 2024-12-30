from datetime import datetime

class Logger:
    def __init__(self):
        self.logs = []
        self.main_window = None
        
    def log(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f'[{timestamp}] {message}'
        self.logs.append(log_entry)
        
        # 直接更新主窗口的日志文本框
        if hasattr(self, 'main_window') and self.main_window and hasattr(self.main_window, 'log_text'):
            self.main_window.log_text.append(log_entry)
            # 滚动到最新的日志
            self.main_window.log_text.verticalScrollBar().setValue(
                self.main_window.log_text.verticalScrollBar().maximum()
            )