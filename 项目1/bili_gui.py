import gradio as gr
from bilibili import batch_data, parse_data
import pandas as pd

def data_for_gui(mid):
    data_list = batch_data(mid)
    df = parse_data(data_list)

    # 确保DataFrame中的Timestamp等类型被转换为字符串
    # 遍历DataFrame的每一列
    for col in df.columns:
        # 检查列数据类型是否为datetime64[ns]或包含Timestamp对象
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            # 将datetime/Timestamp列转换为字符串
            df[col] = df[col].dt.strftime('%Y-%m-%d')

    return df


with gr.Blocks() as demo:
    mid = gr.Textbox(label="输入up主的MID")
    df = gr.DataFrame()
    greet_btn = gr.Button("获取投稿数据")
    greet_btn.click(fn=data_for_gui, inputs=mid, outputs=df)

if __name__ == "__main__":
    demo.launch(share=True)
