# load_config_txt.py
def load_config_txt(path="config.txt"):
    config = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                # 自动识别数字
                if value.isdigit():
                    value = int(value)
                # 自动识别 true/false
                elif value.lower() in ("true", "false"):
                    value = value.lower() == "true"

                config[key] = value

    return config
