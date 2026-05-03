import os
import hashlib
import json
from datetime import datetime

# 只扫描游戏资源目录
BASE_DIR = "Gamedata"

# 输出 manifest
OUTPUT = "manifest.json"

# 下载根地址（必须对应 BASE_DIR）
RAW_BASE = "https://raw.githubusercontent.com/ie9527/as2r-dataup-1106/main/Gamedata"


def md5(file_path):
    h = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def generate():
    manifest = {
        "version": datetime.utcnow().strftime("%Y.%m.%d.%H%M"),
        "base": "Gamedata",   # ⭐ 新增：标识根目录（很重要）
        "files": []
    }

    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            full_path = os.path.join(root, file)

            # 相对 Gamedata 的路径
            rel_path = os.path.relpath(full_path, BASE_DIR)
            rel_path = rel_path.replace("\\", "/")

            manifest["files"].append({
                "path": rel_path,
                "md5": md5(full_path),
                "url": f"{RAW_BASE}/{rel_path}"
            })

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("manifest generated")


if __name__ == "__main__":
    generate()
