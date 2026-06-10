## 环境要求

- Windows 10/11
- Python 3.10+
- VS Code

## 安装

```bash
python -m venv venv
venv\Scripts\activate
pip install pyautogui pyperclip
```

## 使用方法

### 1. 基本启动

```bash
python coding_assistant.py
```

启动后有 **5 秒缓冲时间**，切换到编辑器窗口即可。

### 2. 停止脚本

```
Ctrl + C
```

## 可调参数

在文件顶部的配置区域修改：

```python
TYPING_SPEED_RANGE = (0.02, 0.12)
PAUSE_PROB = 0.03
PAUSE_DURATION = (1.0, 4.0)
TYPO_PROB = 0.04
```

## 文件说明

```
coder/
  ├── coding_assistant.py  # 主脚本
  └── README.md            # 本文件
```

运行时会在用户目录下自动创建 `coding_assistant_workspace/` 存放临时代码文件。
