class I18n:
    translations = {
        'zh_CN': {
            'window_title': 'CutV - 视频剪辑工具',
            'input_video': '输入视频:',
            'select_video': '选择视频文件',
            'start_time': '起始时间(HH:MM:SS):',
            'end_time': '结束时间(HH:MM:SS):',
            'output_path': '输出路径:',
            'select_save': '选择保存路径',
            'output_format': '输出格式:',
            'audio_only': '仅导出音频',
            'start_cutting': '开始剪辑',
            'log': '日志:',
            'original_format': '原格式',
            'warning': '警告',
            'error': '错误',
            'success': '成功',
            'fill_all': '请填写所有必要信息！',
            'process_complete': '处理完成！',
            'process_failed': '处理失败: {}',
            'select_input_file': '选择输入文件: {}',
            'set_time_range': '设置默认时间范围: {} - {}',
            'select_output_path': '选择输出路径: {}',
            'command_success': '命令执行成功',
            'command_failed': '命令执行失败: {}',
            'ffmpeg_failed': 'FFmpeg执行失败: {}',
            'get_duration_failed': '获取视频时长失败: {}'
        },
        'en_US': {
            'window_title': 'CutV - Video Cutting Tool',
            'input_video': 'Input Video:',
            'select_video': 'Select Video',
            'start_time': 'Start Time(HH:MM:SS):',
            'end_time': 'End Time(HH:MM:SS):',
            'output_path': 'Output Path:',
            'select_save': 'Select Save Path',
            'output_format': 'Output Format:',
            'audio_only': 'Audio Only',
            'start_cutting': 'Start Cutting',
            'log': 'Log:',
            'original_format': 'Original Format',
            'warning': 'Warning',
            'error': 'Error',
            'success': 'Success',
            'fill_all': 'Please fill in all required information!',
            'process_complete': 'Process Complete!',
            'process_failed': 'Process Failed: {}',
            'select_input_file': 'Selected input file: {}',
            'set_time_range': 'Set default time range: {} - {}',
            'select_output_path': 'Selected output path: {}',
            'command_success': 'Command executed successfully',
            'command_failed': 'Command execution failed: {}',
            'ffmpeg_failed': 'FFmpeg execution failed: {}',
            'get_duration_failed': 'Failed to get video duration: {}'
        }
    }

    def __init__(self, language='zh_CN'):
        self.language = language

    def get(self, key, *args):
        text = self.translations.get(self.language, {}).get(key, key)
        if args:
            return text.format(*args)
        return text 