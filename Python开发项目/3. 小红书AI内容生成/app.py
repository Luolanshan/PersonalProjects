# 小红书AI生图应用
import gradio as gr
import os
from xhs_image import xhs_img
from websockets_api_example import gen_image


# 小红书路径返回函数（占位函数）
def return_xhs_path(xhs_text_value):
    return xhs_text_value

# 图片路径列表
def return_img_list(xhs_text):
    img_list = os.listdir(return_xhs_path(xhs_text))  # 读取文件夹中所有文件名称
    img_path_list = [os.path.join(return_xhs_path(xhs_text), img) for img in img_list]  # 拼接成完整路径列表
    return img_path_list

# 预设Gradio主题
theme = gr.themes.Default(
    primary_hue="red",
    secondary_hue="neutral",
    neutral_hue="red",
).set(
    button_secondary_background_fill='*neutral_500',
    button_secondary_border_color_hover_dark='*neutral_50',
    button_secondary_text_color='white'
)

# Gradio界面搭建
with gr.Blocks(theme=theme) as demo:  # 传入主题
    gr.Image(r'XHS2.png')
    with gr.Row():
        with gr.Column():
            gr.Markdown("""
            # 📕小红书笔记下载参考图
            > 输入小红书笔记链接, 下载图片
            """)
            with gr.Row():
                xhs_url = gr.Textbox(label="小红书笔记链接")
                xhs_text = gr.Textbox(label='笔记路径')
            with gr.Row():
                xhs_btn = gr.Button(value='获取链接图片')
                xhs_btn2 = gr.Button(value='获取路径图片')
            xhs_gallery = gr.Gallery(columns=[4])

            xhs_btn.click(fn=xhs_img, inputs=xhs_url, outputs=xhs_gallery)
            xhs_btn2.click(fn=return_img_list, inputs=xhs_text, outputs=xhs_gallery)
            # [(图片路径, 标签), (图片路径, 标签), (图片路径, 标签)]
            # [图片路径, 图片路径, 图片路径]

        with gr.Column():
            gr.Markdown("""
                        # 🎨AI利用参考图作图
                        > 输入图片所在的路径, 以及期望每张参考图生成的张数
                        """)
            with gr.Row():
                num = gr.Textbox(label='每张参考图的生图数量')
                path_text = gr.Textbox(label='图片路径')
            ai_btn = gr.Button(value='AI图生图')
            ai_gallery = gr.Gallery(columns=[4])
            ai_btn.click(fn=gen_image, inputs=[num, path_text], outputs=ai_gallery)


if __name__ == '__main__':
    demo.launch(allowed_paths=[r'D:\ComfyUI_windows_portable\ComfyUI\output'], share=True, debug=True, show_error=True)   # 允许访问的路径
    # demo.launch(debug=True, show_error=True)  # 调试模式

