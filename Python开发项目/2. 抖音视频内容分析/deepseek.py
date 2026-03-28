from openai import OpenAI  # 导入OpenAI库，这里用于与DeepSeek的API进行交互
from fuzzywuzzy import fuzz

def ai_bot(question, df, chat_history):
    """
    处理用户提问，并调用DeepSeek模型生成回复。
    同时会更新并返回累积的对话历史。

    参数:
        question: 用户输入的问题
        df: 用于数据分析的DataFrame
        chat_history: 之前的对话历史列表

    返回:
        str: 要清空输入框，所以返回空字符串
        list: 更新后的完整对话历史（用于更新gr.State）
        list: 更新后的完整对话历史（用于更新gr.Chatbot的显示）
    """

    # 识别question中是否含有关键字视频数据（不用连续，可出现在任意位置）
    target_keywords = "视频数据"
    similarity_score = fuzz.partial_ratio(question, target_keywords)
    if similarity_score >= 60:
        # 将DataFrame转换为字符串格式（不包含索引），并追加到原始问题后面
        question = question + '\n具体数据如下:' + df.to_string(index=False)

    # 初始化OpenAI客户端，配置API密钥和基础URL（指向DeepSeek的服务）
    client = OpenAI(api_key="sk-7f815f50eae243c8a56c092907b7fb87", base_url="https://api.deepseek.com")

    # <构建发送给大模型的消息列表，这是一个多轮对话的上下文结构>
    # <msg：首先添加系统消息，然后添加所有历史对话，最后是当前用户问题> → 输入给DS模型
    # 系统消息，设定AI的角色
    msg = [{"role": "system", "content": "You are a helpful assistant"}]
    # 将存储的对话历史（通常是元组列表）转换为API所需的字典格式并添加到messages中
    for user_turn, assistant_turn in chat_history:
        msg.append({"role": "user", "content": user_turn})
        msg.append({"role": "assistant", "content": assistant_turn})
    # 将当前用户的最新问题也加入
    msg.append({"role": "user", "content": question})

    # 调用DeepSeek API
    response = client.chat.completions.create(
        model="deepseek-chat",  # 指定使用的模型
        messages=msg,  # 传入对话上下文
        stream=False  # 非流式输出（等待完整响应）
    )
    bot_response = response.choices[0].message.content
    # 打印模型的回复内容到控制台（用于调试或日志）
    # print(response.choices[0].message.content)

    # 更新对话历史 chat_history
    # 将当前一轮的对话（用户问题, AI回复）追加到历史列表中[()()]
    updated_chat_history = chat_history + [(question, bot_response)]
    # 将本轮对话的AI回复追加到msg中，以字典形式返回给chatbot
    d = {'role': 'assistant', 'content': response.choices[0].message.content}
    msg.append(d)

    # 函数返回三个值
    return "", updated_chat_history, msg


if __name__ == '__main__':
    ai_bot('你认识米老鼠吗？')

