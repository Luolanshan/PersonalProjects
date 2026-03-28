# ❗项目核心：comfyui生图
import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse
import random
import os

# ComfyUI服务器地址和客户端ID
server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

# 将prompt加入ComfyUI的处理队列
def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())

# 获取生成的图片数据
def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()  # 返回图片的二进制数据

# 获取指定prompt_id的历史记录
def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())

# 通过WebSocket监听ComfyUI的执行状态，并获取生成的所有图片 → 每次执行 返回包含所有图片数据的字典和最后一张图片的路径
def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
        else:
            # If you want to be able to decode the binary stream for latent previews, here is how you can do it:
            # bytesIO = BytesIO(out[8:])
            # preview_image = Image.open(bytesIO) # This is your preview in PIL image format, store it in a global
            continue #previews are binary data

    history = get_history(prompt_id)[prompt_id]
    for node_id in history['outputs']:
        node_output = history['outputs'][node_id]
        images_output = []
        if 'images' in node_output:
            for image in node_output['images']:
                # 下载每张生成的图片
                image_data = get_image(image['filename'], image['subfolder'], image['type'])
                images_output.append(image_data)
        output_images[node_id] = images_output
    full_path = os.path.join(r'D:\ComfyUI_windows_portable\ComfyUI\output', image['filename'])
    return output_images, full_path


# 预设的prompt模板（JSON格式）
prompt_text = """
{
  "3": {
    "inputs": {
      "seed": 382163076554969,
      "steps": 20,
      "cfg": 8,
      "sampler_name": "euler",
      "scheduler": "normal",
      "denoise": 0.7500000000000001,
      "model": [
        "26",
        0
      ],
      "positive": [
        "6",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "17",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "K采样器"
    }
  },
  "6": {
    "inputs": {
      "text": [
        "24",
        0
      ],
      "clip": [
        "26",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP文本编码"
    }
  },
  "7": {
    "inputs": {
      "text": "text, watermark",
      "clip": [
        "26",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP文本编码"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "3",
        0
      ],
      "vae": [
        "26",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE解码"
    }
  },
  "11": {
    "inputs": {
      "image": "00221-1774265606-lingluanhoutu,1girl,solo,blonde hair,looking at viewer,blue eyes,long hair,eyelashes,bangs,lips,closed mouth,realistic,braid,rib.png"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "加载图像"
    }
  },
  "17": {
    "inputs": {
      "pixels": [
        "11",
        0
      ],
      "vae": [
        "26",
        2
      ]
    },
    "class_type": "VAEEncode",
    "_meta": {
      "title": "VAE编码"
    }
  },
  "23": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": [
        "8",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "保存图像"
    }
  },
  "24": {
    "inputs": {
      "query": "briefly describe the image",
      "debug": "enable",
      "url": "http://127.0.0.1:11434",
      "model": "moondream:1.8b",
      "keep_alive": 0,
      "format": "text",
      "seed": 358278486,
      "images": [
        "11",
        0
      ]
    },
    "class_type": "OllamaVision",
    "_meta": {
      "title": "Ollama Vision"
    }
  },
  "26": {
    "inputs": {
      "ckpt_name": "pixelArtDiffusionXL_spriteShaper.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Checkpoint加载器（简易）"
    }
  },
  "35": {
    "inputs": {
      "text": [
        "24",
        0
      ]
    },
    "class_type": "JjkShowText",
    "_meta": {
      "title": "ShowText"
    }
  }
}
"""

# AI生图主函数 → 返回生成图片的路径列表
def gen_image(loop_num, path):  # loop_num: 每张图生成的变体数量, path: 图片所在路径
    ws = websocket.WebSocket()  # 创建WebSocket对象
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))  # 连接ComfyUI websockets API
    prompt = json.loads(prompt_text)  # 加载预设的prompt模板 → 正向提示词

    img_list = [path + '\\' + x for x in os.listdir(path)]   # 获取路径下所有图片的完整路径
    path_list = []
    for img in img_list:  # 遍历文件夹中的每一张图片
        prompt['11']['inputs']['image'] = img  # 替换加载图像节点的图片路径
        for num in range(int(loop_num)):  # 同一张图生成多张变体
            prompt["3"]["inputs"]["seed"] = random.randint(1, 88888888)  # k采样器 随机seed
            images, img_path = get_images(ws, prompt)  # 获取生成的所有图片数据和路径
            path_list.append(img_path)
            yield path_list  # 返回当前已生成的图片路径列表 → 不会中断，而是累计存储
    ws.close()  # 关闭连接
    # return path_list  # 只能一次性返回，无法边生成边返回


if __name__ == '__main__':
    loop_num = 1
    path = r'D:\OneDrive\college again\戴师兄\Python课\【Python】6期\项目3\图片下载\不在京都…在上海…严重被低估的小众寺庙🍁 - 小红书'
    images = gen_image(path, loop_num)


# for in case this example is used in an environment where it will be repeatedly called, like in a Gradio app. otherwise, you'll randomly receive connection timeouts
# Commented out code to display the output images:

# for node_id in images:
#     for image_data in images[node_id]:
#         from PIL import Image
#         import io
#         image = Image.open(io.BytesIO(image_data))
#         image.show()

