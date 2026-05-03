import os
import hashlib
import json
from datetime import datetime

# 你的资源目录（改这里）
BASE_DIR = "Gamedata"

# 输出
OUTPUT = "manifest.json"

# 改成你的仓库地址
RAW_BASE = "https://raw.githubusercontent.com/你的用户名/你的仓库/main/Gamedata"

def md5(file_path):
    h = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def generate():
    manifest = {
        "version": datetime.utcnow().strftime("%Y.%m.%d.%H%M"),
        "files": []
    }

    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            full_path = os.path.join(root, file)

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
