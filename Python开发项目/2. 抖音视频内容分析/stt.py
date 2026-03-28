# 调用语音识别模型 whisper：音频转文本（speech to text）
import whisper
from pprint import pprint

# 加载模型
model = whisper.load_model("medium", download_root=r'D:\openai')

# 返回segments和全文本
def stt(video_path):
    # 识别音频并获取时间戳
    result = model.transcribe(video_path, word_timestamps=True)
    segments = result['segments']

    # 提取segments中的文本数据，进行拼接
    full_text = ''
    for seg in segments:
        full_text = full_text + seg['text'] + '。'
    # print(full_text)

    return segments, full_text

if __name__ == '__main__':
    video_path = r'./视频下载/7552144381940796735.mp4'
    seg, text = stt(video_path)
    pprint(seg)
    print(text)