## 环境要求

- Windows 10/11
- Python 3.10+

## 安装

```bash
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

### 3. 切换编辑器

默认使用 Notepad。如果想用 VS Code，修改 `coding_assistant.py` 中的 `open_in_notepad` 函数：

```python
# 将 "notepad" 改为 "code"
subprocess.Popen(["code", filepath])
```

同时调整 `close_notepad` 函数：

```python
# VS Code 关闭当前文件
pyautogui.hotkey('ctrl', 'w')
```

## 工作流程

脚本会无限循环以下流程：

```
选择代码模板
    |
    v
注入随机错误 (1-3个)
    |
    v
打开编辑器，逐字输入代码（含拟真打字节奏）
    |
    v
Ctrl+S 保存
    |
    v
运行代码，检查输出
    |
    v
如果报错 --> Ctrl+G 跳转到错误行 --> 阅读思考 --> 修复 --> 重新运行验证
    |
    v
运行单元测试
    |
    v
随机休息（鼠标移动 / 滚动 / 停顿思考）
    |
    v
回到开头，选择下一个模板
```

## 拟真特性

| 特性 | 说明 |
|------|------|
| 随机打字速度 | 每次按键间隔 20-120ms |
| 思考停顿 | 3% 概率停顿 1-4 秒 |
| 打错修正 | 4% 概率按到相邻键，然后退格修正 |
| 符号停顿 | 输入 `{}()[]` 后额外停顿 |
| 错误注入 | 随机注入缺冒号、变量拼错、缩进错误 |
| 编译-修复循环 | 运行报错后自动跳转修复 |
| 鼠标活动 | 随机微移、滚动 |
| 休息间隔 | 随机 5-20 秒停顿 |

## 可调参数

在文件顶部的配置区域修改：

```python
TYPING_SPEED_RANGE = (0.02, 0.12)  # 打字速度范围（秒）
PAUSE_PROB = 0.03                   # 停顿概率
PAUSE_DURATION = (1.0, 4.0)        # 停顿时长范围
TYPO_PROB = 0.04                    # 打错概率
```

## 文件说明

```
coder/
  ├── coding_assistant.py  # 主脚本
  └── README.md          # 本文件
```

运行时会在用户目录下自动创建 `coding_assistant_workspace/` 存放临时代码文件。
