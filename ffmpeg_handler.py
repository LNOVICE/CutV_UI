import subprocess
import json

class FFmpegHandler:
    def get_video_duration(self, input_file, logger_callback):
        command = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            input_file
        ]
        
        logger_callback(f'执行命令: {" ".join(command)}')
        
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            duration = float(data['format']['duration'])
            
            # 将秒数转换为 HH:MM:SS 格式
            hours = int(duration // 3600)
            minutes = int((duration % 3600) // 60)
            seconds = int(duration % 60)
            
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            logger_callback(f'获取视频时长成功: {time_str}')
            return "00:00:00", time_str
        except Exception as e:
            logger_callback(f'获取视频时长失败: {str(e)}')
            return None, None

    def cut_video(self, input_file, output_file, start_time, end_time, audio_only, logger_callback):
        command = ['ffmpeg', '-i', input_file, '-ss', start_time, '-to', end_time]
        
        if audio_only:
            # 导出音频（mp3格式）
            command.extend(['-vn', '-acodec', 'libmp3lame'])
        else:
            # 导出视频（保持原有编码）
            command.extend(['-c', 'copy'])
            
        command.append(output_file)
        
        # 记录完整的命令
        command_str = ' '.join(command)
        logger_callback(f'执行命令: {command_str}')
        
        try:
            result = subprocess.run(command, 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            logger_callback('命令执行成功')
            if result.stdout:
                logger_callback(f'输出信息: {result.stdout}')
            return True
        except subprocess.CalledProcessError as e:
            error_msg = f'命令执行失败: {e.stderr}'
            logger_callback(error_msg)
            raise Exception(error_msg) 