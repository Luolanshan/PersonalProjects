# 短视频语音识别应用
from stt import stt
import gradio as gr
from video_download import douyin_video, xhs_video
from video_frame import text_and_frame

# 创建Gradio界面
with gr.Blocks() as demo:
    gr.Image(r'项目2-2 标题.png', show_download_button=False)

    with gr.Row():
        with gr.Column():
            gr.Markdown("""
            # 📽️ 抖音/小红书 视频下载
            > 输入DY视频的ID or XHS视频链接
            """)
            with gr.Row():
                dy_video_id = gr.Textbox(label='抖音视频ID')
                xhs_link = gr.Textbox(label='小红书笔记链接')

            with gr.Row():
                dy_video_bt = gr.Button(value='获取抖音视频')
                xhs_video_bt = gr.Button(value='获取小红书视频')

            video = gr.Video()  # 接收视频存储路径
            stt_text = gr.Textbox(label='语音识别结果', lines=5)
            stt_btn = gr.Button(value='语音识别')

        with gr.Column():
            gr.Markdown("""
            # 🧩 视频脚本生成
            > 语音识别后才能生成视频脚本
            """)
            gallery = gr.Gallery(columns=[5])  # 5列图片
            jiaoben = gr.Button(value='生产视频脚本')

    # 点击视频获取按钮，结果输出到video组件
    dy_video_bt.click(fn=douyin_video, inputs=dy_video_id, outputs=video)
    xhs_video_bt.click(fn=xhs_video, inputs=xhs_link, outputs=video)

    # 点击语音识别按钮，结果输出到stt_text组件和隐藏框stt_seg
    stt_seg = gr.Textbox(label='segment信息', visible=False)  # 存储segment信息的隐藏框，作为脚本按钮的输入
    stt_btn.click(fn=stt, inputs=video, outputs=[stt_seg, stt_text])  # 点击语音识别按钮，segment输出到stt_seg隐藏框，全文本输出到语音识别框
    # 点击视频脚本生成按钮，结果输出到gallery组件
    jiaoben.click(fn=text_and_frame, inputs=[stt_seg, video], outputs=gallery)  # stt_seg中的输入为字符串，需通过eval转换为列表


if __name__ == '__main__':
    demo.launch(share=True)

    # http://xxxxxxx:7860