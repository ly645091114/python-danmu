import os
import sys

class EmitMessage:
    def __init__(self):
        self.platform=""
        self.roomId=""
        self.type=""
        self.time=None
        self.data=None


def setup_proxy_environment(use_socks_proxy: bool):
    """
    处理代理相关问题：
    - 默认关闭环境变量中的 HTTP(S)/SOCKS 代理
    - 如果 use_socks_proxy=True，检查 python-socks 依赖
    """
    proxy_keys = [
        "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
        "http_proxy", "https_proxy", "all_proxy",
    ]

    if not use_socks_proxy:
        found = {}
        for k in proxy_keys:
            v = os.environ.get(k)
            if v:
                found[k] = v

        if found:
            print("检测到系统/环境中配置了代理，已自动清理：")
            for k, v in found.items():
                print(f"  {k} = {v}")
                os.environ.pop(k, None)
        else:
            print("未检测到代理环境变量，直接连接服务器。")
    else:
        print("已开启 SOCKS 代理模式")
        try:
            import python_socks  # noqa: F401
        except ImportError:
            print(
                "\n[错误] 你开启了 SOCKS 代理模式，但未安装 python-socks。\n"
                "请先安装依赖：\n"
                "    pip install python-socks\n"
            )
            sys.exit(1)