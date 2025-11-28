#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

# 需要安装的依赖
REQUIRED_PACKAGES = [
    "certifi",
    "python-socks",
    "websockets",
    "pyttsx3",
]

PROJECT_DIR = Path(__file__).resolve().parent
VENV_DIR = PROJECT_DIR / "venv"


def is_windows():
    return os.name == "nt"


def venv_python():
    """返回虚拟环境中的 python 可执行路径"""
    if is_windows():
        return VENV_DIR / "Scripts" / "python.exe"
    else:
        return VENV_DIR / "bin" / "python"


def venv_pip():
    """返回虚拟环境中的 pip 可执行路径"""
    if is_windows():
        return VENV_DIR / "Scripts" / "pip.exe"
    else:
        return VENV_DIR / "bin" / "pip"


def create_venv_if_needed():
    if VENV_DIR.exists():
        print(f"[INFO] 已检测到虚拟环境: {VENV_DIR}")
        return

    print("[INFO] 未检测到 venv，正在创建虚拟环境...")
    subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
    print("[INFO] 虚拟环境创建完成。")


def install_packages():
    pip_path = venv_pip()
    print(f"[INFO] 使用虚拟环境 pip 安装依赖: {pip_path}")
    # 可选：先升级 pip
    subprocess.run([str(pip_path), "install", "--upgrade", "pip"], check=True)
    # 安装必要依赖
    subprocess.run([str(pip_path), "install", *REQUIRED_PACKAGES], check=True)
    print("[INFO] 依赖安装完成。")


def run_douyu_script():
    py_path = venv_python()
    script_path = PROJECT_DIR / "douyu_obs_overlay.py"
    if not script_path.exists():
        print(f"[ERROR] 找不到脚本: {script_path}")
        sys.exit(1)

    # 拷贝一份当前环境变量
    env = os.environ.copy()

    # 等价于：HTTP_PROXY= HTTPS_PROXY= ALL_PROXY= python ...
    for key in ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
                "http_proxy", "https_proxy", "all_proxy"]:
        env.pop(key, None)

    print(f"[INFO] 使用虚拟环境 Python 运行: {script_path}")
    print("[INFO] 已清除 HTTP(S)/ALL_PROXY 环境变量。")

    # 运行斗鱼脚本
    subprocess.run([str(py_path), str(script_path)], env=env, check=True)


def main():
    create_venv_if_needed()
    # 如果刚创建 venv，需要安装依赖；已有 venv 时你可以根据需要决定是否总是安装
    # 这里简单处理：每次都尝试安装（pip 会跳过已安装版本）
    install_packages()
    run_douyu_script()


if __name__ == "__main__":
    main()