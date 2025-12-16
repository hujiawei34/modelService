# -*- coding: utf-8 -*-
"""
从输出日志中提取 base64 图片并保存为可查看的图片文件。

用法：
  python -u image-edit/src/py/save_from_log.py [log_path] [output_path]

示例：
  python -u image-edit/src/py/save_from_log.py \
    image-edit/data/result/output.log \
    image-edit/data/result/output.jpg
"""

from __future__ import annotations

import base64
import json
import sys
from pathlib import Path


def guess_ext_from_data_url(data_url: str) -> str:
    try:
        header = data_url.split(",", 1)[0]  # e.g. data:image/jpeg;base64
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


def extract_b64(obj: dict) -> str | None:
    # 兼容常见结构：{"data":[{"b64_json":"data:image/...;base64,xxx"}]}
    if isinstance(obj, dict):
        if "data" in obj and isinstance(obj["data"], list):
            for item in obj["data"]:
                if isinstance(item, dict) and "b64_json" in item:
                    return item["b64_json"]
        # 其他可能字段
        for key in ("b64_json", "image_base64", "image", "content"):
            val = obj.get(key)
            if isinstance(val, str) and ("base64" in val or len(val) > 1000):
                return val
    return None


def main():
    default_log = Path(__file__).parent.parent.parent / "data" / "result" / "output.log"
    log_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_log

    if len(sys.argv) > 2:
        out_path = Path(sys.argv[2])
    else:
        # 默认输出到与日志同目录
        out_path = log_path.with_suffix("")  # 去掉 .log

    if not log_path.exists():
        print(f"日志不存在: {log_path}")
        sys.exit(1)

    text = log_path.read_text(encoding="utf-8", errors="ignore")

    # 从后往前找一行 JSON
    b64_value = None
    last_json_obj = None
    for line in reversed(text.splitlines()):
        s = line.strip()
        if not s or not s.startswith("{"):
            continue
        try:
            obj = json.loads(s)
            b64_value = extract_b64(obj)
            last_json_obj = obj
            if b64_value:
                break
        except Exception:
            continue

    if not b64_value:
        print("未在日志中找到 base64 图片数据。")
        sys.exit(2)

    # 如果是 data URL，拆掉头部
    if b64_value.startswith("data:"):
        # 推断扩展名
        ext = guess_ext_from_data_url(b64_value)
        out_path = out_path.with_suffix(ext)
        b64_value = b64_value.split(",", 1)[1]
    else:
        # 无前缀时默认 .png
        out_path = out_path.with_suffix(".png")

    # 解码并保存
    try:
        img_bytes = base64.b64decode(b64_value)
    except Exception as e:
        print(f"base64 解码失败: {e}")
        sys.exit(3)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(img_bytes)

    print(f"已保存图片: {out_path}")


if __name__ == "__main__":
    main()

