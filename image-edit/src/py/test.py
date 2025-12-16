# -*- coding: utf-8 -*-
# @Time    : 2025-12-16 15:09:17
# @Author  : hujiawei
# @File    : test.py

import requests
import json
import base64
import sys
from pathlib import Path


#  Base64 编码格式
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def check_env():
    env_path = Path(__file__).parent.parent.parent / ".env"
    if not env_path.exists():
        raise FileNotFoundError(".env file not found.")
    with open(env_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("MAAS_API_KEY="):
                return line.strip().split("=")[1]
    raise KeyError("MAAS_API_KEY not found in .env file.")


def check_image(image_path):
    try:
        with open(image_path, "rb") as f:
            return True
    except FileNotFoundError:
        raise FileNotFoundError(f"Image file {image_path} not found.")


def _guess_ext_from_data_url(data_url: str) -> str:
    try:
        header = data_url.split(",", 1)[0]  # data:image/jpeg;base64
        if "/" in header:
            mime = header.split(":", 1)[1].split(";", 1)[0]  # image/jpeg
            subtype = mime.split("/", 1)[1].lower()
            if subtype in ("jpeg", "jpg"):
                return ".jpg"
            if subtype in ("png",):
                return ".png"
            if subtype in ("webp",):
                return ".webp"
            if subtype in ("bmp",):
                return ".bmp"
            if subtype in ("tiff", "tif"):
                return ".tiff"
    except Exception:
        pass
    return ".png"


def _extract_b64_from_json(obj: dict) -> str | None:
    # 兼容常见结构：{"data":[{"b64_json":"data:image/...;base64,xxx"}]}
    if isinstance(obj, dict):
        if "data" in obj and isinstance(obj["data"], list):
            for item in obj["data"]:
                if isinstance(item, dict):
                    if item.get("b64_json"):
                        return item["b64_json"]
                    # 兜底字段
                    for key in ("image_base64", "image", "content"):
                        val = item.get(key)
                        if isinstance(val, str) and ("base64" in val or len(val) > 1000):
                            return val
        # 直接扁平结构
        if obj.get("b64_json"):
            return obj["b64_json"]
    return None


def save_response_image(resp_text: str, out_path: Path) -> Path | None:
    """从响应文本中提取图片并保存到 out_path（自动补扩展名）。"""
    try:
        obj = json.loads(resp_text)
    except Exception:
        print("无法解析响应为 JSON，跳过保存图片。")
        return None

    # 优先处理 base64
    b64_value = _extract_b64_from_json(obj)
    if b64_value:
        if b64_value.startswith("data:"):
            ext = _guess_ext_from_data_url(b64_value)
            out_path = out_path.with_suffix(ext)
            b64_value = b64_value.split(",", 1)[1]
        else:
            # 没有 data: 头时，默认 .png
            out_path = out_path.with_suffix(".png")

        try:
            img_bytes = base64.b64decode(b64_value)
        except Exception as e:
            print(f"base64 解码失败: {e}")
            return None

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(img_bytes)
        return out_path

    # 其次，如果返回了 url，可尝试下载
    try:
        data_list = obj.get("data") if isinstance(obj, dict) else None
        if isinstance(data_list, list) and data_list:
            url_val = data_list[0].get("url") if isinstance(data_list[0], dict) else None
            if url_val:
                # 默认使用 jpg 扩展名
                out_path = out_path.with_suffix(".jpg")
                r = requests.get(url_val, timeout=30, verify=False)
                r.raise_for_status()
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(r.content)
                return out_path
    except Exception as e:
        print(f"下载图片失败: {e}")
        return None

    print("未在响应中找到可用的图片数据。")
    return None


if __name__ == "__main__":
    url = "https://api.modelarts-maas.com/v1/images/generations"  # API地址
    api_key = check_env()  # 从.env文件中获取API Key
    # 默认图片路径：image-edit/data/image/test.jpg；支持通过命令行传入自定义路径
    default_image = Path(__file__).parent.parent.parent / "data" / "image" / "test.jpg"
    image_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_image
    if check_image(image_path):
        base64_image = encode_image(image_path)
    # Send request.
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    data = {
        "model": "qwen-image-edit-2509",  # model参数
        "prompt": "将花朵颜色修改成红色",  # 支持中英文
        "size": "1024x1024",
        # 生成图像尺寸qwen_image_edit要求介于[512x512,2048x2048]。
        # 推荐：2048x2048,1536x1536,1024x1024, 512x512，其中height和width需要被16整除，否则会向下兼容。
        "image": f"data:image/jpg;base64,{base64_image}",
        # 支持图片格式 ["png", "jpeg", "jpg", "webp", "bmp", "tiff"]，支持base64形式传递图片。
        "seed": 48,  # 取值范围在[0, 2147483648]， 随机种子
    }
    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    # 打印状态码与原始响应（便于调试）
    print(response.status_code)
    print(response.text)

    # 将返回图片保存到文件。第二个命令行参数可指定输出路径。
    default_out = Path(__file__).parent.parent.parent / "data" / "result" / "output"
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else default_out
    saved = save_response_image(response.text, out_path)
    if saved:
        print(f"已保存图片: {saved}")
    else:
        print("未能保存图片文件。")
