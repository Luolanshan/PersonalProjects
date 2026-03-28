# 短视频数据分析应用
import gradio as gr
import pandas as pd
from deepseek import ai_bot
import os
from pprint import pprint

# 读取视频指标数据总表
df = pd.read_excel(r'.\整合数据\总表.xlsx')

# 读取文件夹中所有视频文件名称，生成下拉选择框数据
video_list = os.listdir('./投放数据')  # 读取文件夹中所有文件名称
video_path_list = [os.path.join(r'./投放数据/', video) for video in video_list if video.endswith('.mp4')]  # 筛选出mp4视频文件，并生成完整路径
video_title_list = [os.path.splitext(os.path.basename(video_path))[0] for video_path in video_path_list]  # 去掉路径和.mp4后缀，生成视频标题列表
video_tuples = list(zip(video_title_list, video_path_list))  # 生成(标题，路径)元组列表
# video_tuples = [(title, path) for title, path in zip(video_title_list, video_path_list)]  # 使用列表推导式组合成 (name, value) 元组列表


# 接收video_drop的值（视频文件路径）并直接返回它
def return_video_path(video_drop_value):
    return video_drop_value

# 清空历史对话函数
def clear_chat_history():
    return [], []  # 同时清空State和Chatbot

# 接受video_drop的值 → 提取视频标题（去掉.mp4后缀），返回筛选后的 视频标题行df
def filt_data(title):
    title = os.path.basename(title)[:-4]
    filt_df = df[df['视频标题']==title]
    return filt_df


# gradio界面设计
with gr.Blocks() as demo:
    # 页面标题
    gr.Image(r'项目2-1 标题.png', show_download_button=False)
    # 定义一个隐藏的DataFrame组件来存储筛选后的数据，初始值为空DataFrame
    filt_df = gr.DataFrame(visible=False)
    # 定义一个State组件来存储对话历史，初始值设为空列表[]
    chat_history_state = gr.State(value=[])

    with gr.Row():
        with gr.Column():
            # 视频名称 下拉选择框 → 元组(name, value)
            video_drop = gr.Dropdown(choices=video_tuples, value=video_tuples[0][1] if video_tuples else None, interactive=True, label='视频名称')
            # 视频展示区域 和下拉框联动
            video = gr.Video(height=395)
            video_drop.change(fn=return_video_path, inputs=video_drop, outputs=video)  # 事件监听器：下拉框的change事件 → 调用函数返回video_drop的value 视频路径，作为参数传给video组件，从而实现视频文件的切换

        with gr.Column():
            plot1 = gr.LinePlot(value=df, x='duration', y='点击指数', height=240)
            plot2 = gr.LinePlot(value=df, x='duration', y='流失指数', height=240)
            video_drop.change(fn=filt_data, inputs=video_drop, outputs=plot1)  # 事件监听器：下拉框的value传递给filt_data函数，返回筛选后的df，从而实现图表的联动
            video_drop.change(fn=filt_data, inputs=video_drop, outputs=plot2)
            video_drop.change(fn=filt_data, inputs=video_drop, outputs=filt_df)  # 输出给隐藏的DataFrame组件，供后续ai_bot函数调用

        with gr.Column():
            chatbot = gr.Chatbot(type="messages", max_height=350)
            msg = gr.Textbox()
            # 清空对话按钮
            clear_btn = gr.Button("清空对话")
            clear_btn.click(clear_chat_history, outputs=[chat_history_state, chatbot])

    # 监听文本框msg的submit事件(通常是用户按下回车键)
    msg.submit(
        fn=ai_bot,
        inputs=[msg, filt_df, chat_history_state],
        outputs=[msg, chat_history_state, chatbot]
    )


if __name__ == "__main__":
    demo.launch(share=True)





