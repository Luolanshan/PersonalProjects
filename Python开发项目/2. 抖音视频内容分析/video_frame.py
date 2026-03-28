# 画面截图+存储
from moviepy.editor import VideoFileClip
import imageio
import os
from stt import stt

# 返回视频指定秒数的画面截图 存储路径
def frame(video_clip, video_path, second):

    frame = video_clip.get_frame(second)  # 截取第n秒的画面
    video_name = os.path.basename(video_path)[:-4]  # 视频文件名
    save_path = rf'./画面存储/{video_name}'  # 截图存储路径

    # 如果文件夹不存在，则创建
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    # 将截图写入jpg文件
    imageio.imwrite(rf"{save_path}/frame_at_{second}s.jpg", frame)

    return rf"{save_path}/frame_at_{second}s.jpg"


# 获取每段文字内容+对应视频截图，存入列表（元组形式：图片路径,文字内容）
def text_and_frame(segments, video_path):
    # 加载视频
    video = VideoFileClip(video_path)

    # 遍历segments列表中的字典
    gallery_list = []
    for seg in eval(segments):  # eval将字符串转换为数据类型(即可作为python代码执行) ← stt_seg中的输入为字符串
        mid = (seg['start'] + seg['end']) / 2  # 取每段文字的中间时间点，作为截图参数
        text = seg['text']  # 视频文本
        img_path = frame(video_clip=video, video_path=video_path, second=mid)  # 视频截图 存储路径
        tp = (img_path, text)
        gallery_list.append(tp)  # 元组添加到列表

    return gallery_list


if __name__ == '__main__':
    path = r'./投放数据/50亿研发值不值？现场实测OPPO全场景1nit明眸护眼屏#oppofindx9.mp4'
    segments, full_text = stt(path)
    text_and_frame(segments, path)


