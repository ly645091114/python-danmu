#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
import shutil

PROJECT_DIR = Path(__file__).resolve().parent
VENV_DIR = PROJECT_DIR / "venv"
REQUIREMENTS_FILE = PROJECT_DIR / "requirements.txt"


def is_windows() -> bool:
    return os.name == "nt"


def find_python311_cmd() -> list[str]:
    """
    找到“能运行出 3.11.x”的命令行（带参数），例如：
    - ["python3.11"]
    - ["py", "-3.11"]
    - ["python311"]
    找不到就退出提示安装 3.11。
    """
    candidates = []

    if is_windows():
        # 优先精确 3.11
        candidates += [
            ["py", "-3.11"],
            ["python3.11"],
            ["python311"],
            ["python"],
        ]
    else:
        candidates += [
            ["python3.11"],
            ["python3"],
            ["python"],
        ]

    for cmd in candidates:
        try:
            out = subprocess.check_output(cmd + ["--version"], stderr=subprocess.STDOUT)
            text = out.decode("utf-8").lower()
            if "3.11" in text:
                print(f"[INFO] 使用 Python 3.11 命令: {' '.join(cmd)}")
                return cmd
        except Exception:
            continue

    print("\n[ERROR] 未找到 Python 3.11 可用命令，无法创建 XTTS 兼容环境。")
    print("请先安装 Python 3.11： https://www.python.org/downloads/release/python-3119/")
    if is_windows():
        input("按回车退出...")
    sys.exit(1)


PY311_CMD = find_python311_cmd()


def venv_python() -> Path:
    return VENV_DIR / ("Scripts/python.exe" if is_windows() else "bin/python")


def venv_pip_cmd() -> list[str]:
    return [str(venv_python()), "-m", "pip"]


def ensure_venv():
    """
    1. 如果没有 venv：用 3.11 创建
    2. 如果已有 venv：检查里面的 python 版本
       - 不是 3.11 → 删除整个 venv，重新用 3.11 创建
    """
    need_create = False

    if not VENV_DIR.exists():
        need_create = True
    else:
        py = venv_python()
        if not py.exists():
            need_create = True
        else:
            try:
                out = subprocess.check_output([str(py), "-c", "import sys; print(sys.version)"])
                if "3.11" not in out.decode("utf-8"):
                    print("[WARN] 当前 venv 不是 Python 3.11，将重新创建。")
                    need_create = True
            except Exception:
                need_create = True

    if need_create:
        if VENV_DIR.exists():
            print(f"[INFO] 删除旧虚拟环境: {VENV_DIR}")
            shutil.rmtree(VENV_DIR, ignore_errors=True)

        print("[INFO] 使用 Python 3.11 创建新的虚拟环境 venv ...")
        # 这里非常关键：保留完整命令，比如 ["py", "-3.11", "-m", "venv", "venv"]
        subprocess.run(PY311_CMD + ["-m", "venv", str(VENV_DIR)], check=True)
        print("[INFO] 虚拟环境创建完成。")
    else:
        print(f"[INFO] 已检测到 Python 3.11 虚拟环境: {VENV_DIR}")


def install_requirements():
    if not REQUIREMENTS_FILE.exists():
        print(f"[WARN] 未找到 {REQUIREMENTS_FILE}，跳过依赖安装。")
        return

    pip_cmd = venv_pip_cmd()

    print("[INFO] 升级 pip、setuptools、wheel ...")
    try:
        subprocess.run(pip_cmd + ["install", "--upgrade", "pip"], check=True)
        subprocess.run(pip_cmd + ["install", "--upgrade", "setuptools", "wheel"], check=True)
    except Exception as e:
        print("[WARN] pip / setuptools / wheel 升级失败（忽略）:", e)

    # 最后安装 requirements.txt
    if REQUIREMENTS_FILE.exists():
        print(f"[INFO] 安装 requirements.txt: {REQUIREMENTS_FILE}")
        try:
            subprocess.run(pip_cmd + ["install", "-r", str(REQUIREMENTS_FILE)], check=True)
        except subprocess.CalledProcessError as e:
            print("[ERROR] 安装依赖失败:", e)
            if is_windows():
                input("按回车退出...")
            sys.exit(1)
    else:
        print(f"[WARN] 未找到 {REQUIREMENTS_FILE}，跳过依赖安装。")

    print("[INFO] 所有依赖安装完成。")


def run_main():
    py_path = venv_python()
    script_path = PROJECT_DIR / "main.py"

    if not script_path.exists():
        print(f"[ERROR] 找不到脚本: {script_path}")
        if is_windows():
            input("按回车退出...")
        sys.exit(1)

    env = os.environ.copy()
    for key in ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
                "http_proxy", "https_proxy", "all_proxy"]:
        env.pop(key, None)

    print(f"[INFO] 使用 venv Python 运行: {script_path}")
    try:
        subprocess.run([str(py_path), str(script_path)], env=env)
    except subprocess.CalledProcessError as e:
        print("[ERROR] 脚本运行中断:", e)
    finally:
        if is_windows():
            input("按回车退出...")


def main():
    print(f"[INFO] 项目目录: {PROJECT_DIR}")
    ensure_venv()
    install_requirements()
    run_main()


if __name__ == "__main__":
    main()