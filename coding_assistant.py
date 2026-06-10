import pyautogui
import pyperclip
import random
import time
import subprocess
import os
import sys

# ============ 配置 ============
TYPING_SPEED_RANGE = (0.02, 0.12)   # 单次按键间隔(秒)
PAUSE_PROB = 0.03                    # 思考停顿概率
PAUSE_DURATION = (1.0, 4.0)         # 停顿时长
TYPO_PROB = 0.04                     # 打错字概率
BACKSPACE_PROB = 0.02                # 退格概率
WORK_DIR = os.path.join(os.environ.get("USERPROFILE", "C:\\Users\\Default"), "coding_assistant_workspace")
PYTHON_EXE = sys.executable

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0


# ============ 代码模板库 ============
CODE_TEMPLATES = [
    # ---------- Python 项目 ----------
    {
        "language": "python",
        "files": {
            "calculator.py": '''"""
简易计算器模块
"""
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Calculator:
    """科学计算器实现"""

    def __init__(self, precision: int = 10):
        self.precision = precision
        self.history: list[str] = []
        self._last_result: Optional[float] = None

    def _record(self, expression: str, result: float) -> None:
        entry = f"{expression} = {round(result, self.precision)}"
        self.history.append(entry)
        self._last_result = result
        logger.info(f"Recorded: {entry}")

    def add(self, a: float, b: float) -> float:
        result = a + b
        self._record(f"{a} + {b}", result)
        return round(result, self.precision)

    def subtract(self, a: float, b: float) -> float:
        result = a - b
        self._record(f"{a} - {b}", result)
        return round(result, self.precision)

    def multiply(self, a: float, b: float) -> float:
        result = a * b
        self._record(f"{a} * {b}", result)
        return round(result, self.precision)

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        result = a / b
        self._record(f"{a} / {b}", result)
        return round(result, self.precision)

    def power(self, base: float, exponent: float) -> float:
        result = base ** exponent
        self._record(f"{base} ^ {exponent}", result)
        return round(result, self.precision)

    def sqrt(self, value: float) -> float:
        if value < 0:
            raise ValueError("Cannot calculate square root of negative number")
        result = value ** 0.5
        self._record(f"sqrt({value})", result)
        return round(result, self.precision)

    def percentage(self, value: float, percent: float) -> float:
        result = value * (percent / 100)
        self._record(f"{value} * {percent}%", result)
        return round(result, self.precision)

    def undo(self) -> Optional[float]:
        if len(self.history) > 1:
            self.history.pop()
        return self._last_result

    def clear_history(self) -> None:
        self.history.clear()
        self._last_result = None
        logger.info("History cleared")


def main():
    calc = Calculator()
    print("=== Calculator Demo ===")
    print(f"3 + 5 = {calc.add(3, 5)}")
    print(f"10 - 4 = {calc.subtract(10, 4)}")
    print(f"6 * 7 = {calc.multiply(6, 7)}")
    print(f"15 / 3 = {calc.divide(15, 3)}")
    print(f"2 ^ 8 = {calc.power(2, 8)}")
    print(f"sqrt(144) = {calc.sqrt(144)}")
    print(f"200 of 15% = {calc.percentage(200, 15)}")
    print(f"\\nHistory: {calc.history}")


if __name__ == "__main__":
    main()
''',
            "test_calculator.py": '''"""
计算器单元测试
"""
import pytest
from calculator import Calculator


class TestCalculatorBasic:
    """基础运算测试"""

    def setup_method(self):
        self.calc = Calculator()

    def test_add(self):
        assert self.calc.add(2, 3) == 5.0
        assert self.calc.add(-1, 1) == 0.0
        assert self.calc.add(0.1, 0.2) == pytest.approx(0.3)

    def test_subtract(self):
        assert self.calc.subtract(5, 3) == 2.0
        assert self.calc.subtract(1, 5) == -4.0

    def test_multiply(self):
        assert self.calc.multiply(3, 4) == 12.0
        assert self.calc.multiply(-2, 3) == -6.0

    def test_divide(self):
        assert self.calc.divide(10, 2) == 5.0
        assert self.calc.divide(7, 2) == 3.5

    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="Division by zero"):
            self.calc.divide(1, 0)

    def test_power(self):
        assert self.calc.power(2, 10) == 1024.0
        assert self.calc.power(5, 0) == 1.0

    def test_sqrt(self):
        assert self.calc.sqrt(9) == 3.0
        assert self.calc.sqrt(2) == pytest.approx(1.4142135623)

    def test_sqrt_negative(self):
        with pytest.raises(ValueError, match="negative number"):
            self.calc.sqrt(-1)

    def test_percentage(self):
        assert self.calc.percentage(200, 15) == 30.0

    def test_history(self):
        self.calc.add(1, 2)
        self.calc.add(3, 4)
        assert len(self.calc.history) == 2

    def test_clear_history(self):
        self.calc.add(1, 2)
        self.calc.clear_history()
        assert len(self.calc.history) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
''',
        },
        "run_cmd": lambda f: [PYTHON_EXE, f],
        "test_cmd": lambda: [PYTHON_EXE, "-m", "pytest", "test_calculator.py", "-v"],
    },
    {
        "language": "python",
        "files": {
            "todo_app.py": '''"""
命令行 Todo 应用
"""
from datetime import datetime
from typing import Optional
import json
import os


class TodoItem:
    def __init__(self, title: str, description: str = "", priority: int = 0):
        self.id: int = 0
        self.title = title
        self.description = description
        self.priority = priority
        self.completed = False
        self.created_at = datetime.now().isoformat()
        self.completed_at: Optional[str] = None

    def mark_done(self) -> None:
        self.completed = True
        self.completed_at = datetime.now().isoformat()

    def mark_undone(self) -> None:
        self.completed = False
        self.completed_at = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TodoItem":
        item = cls(data["title"], data.get("description", ""), data.get("priority", 0))
        item.id = data["id"]
        item.completed = data["completed"]
        item.created_at = data["created_at"]
        item.completed_at = data.get("completed_at")
        return item


class TodoList:
    def __init__(self, filepath: str = "todos.json"):
        self.filepath = filepath
        self.items: list[TodoItem] = []
        self._next_id = 1
        self._load()

    def add(self, title: str, description: str = "", priority: int = 0) -> TodoItem:
        item = TodoItem(title, description, priority)
        item.id = self._next_id
        self._next_id += 1
        self.items.append(item)
        self._save()
        return item

    def remove(self, item_id: int) -> bool:
        for i, item in enumerate(self.items):
            if item.id == item_id:
                self.items.pop(i)
                self._save()
                return True
        return False

    def toggle(self, item_id: int) -> Optional[TodoItem]:
        for item in self.items:
            if item.id == item_id:
                if item.completed:
                    item.mark_undone()
                else:
                    item.mark_done()
                self._save()
                return item
        return None

    def list_all(self, show_all: bool = True) -> list[TodoItem]:
        if show_all:
            return sorted(self.items, key=lambda x: (-x.priority, x.completed))
        return sorted(
            [i for i in self.items if not i.completed],
            key=lambda x: -x.priority,
        )

    def _save(self) -> None:
        data = [item.to_dict() for item in self.items]
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _load(self) -> None:
        if not os.path.exists(self.filepath):
            return
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            for d in data:
                item = TodoItem.from_dict(d)
                self.items.append(item)
                self._next_id = max(self._next_id, item.id + 1)
        except (json.JSONDecodeError, KeyError):
            pass


def main():
    todo = TodoList()
    todo.add("Learn Python", "Study advanced features", priority=3)
    todo.add("Build CLI app", "Create a todo application", priority=2)
    todo.add("Write tests", "Add unit tests for all modules", priority=1)

    print("=== Todo List ===")
    for item in todo.list_all():
        status = "[x]" if item.completed else "[ ]"
        print(f"  {status} #{item.id} {item.title} (priority={item.priority})")

    todo.toggle(1)
    print("\\n=== After toggle #1 ===")
    for item in todo.list_all():
        status = "[x]" if item.completed else "[ ]"
        print(f"  {status} #{item.id} {item.title}")


if __name__ == "__main__":
    main()
''',
        },
        "run_cmd": lambda f: [PYTHON_EXE, f],
        "test_cmd": lambda: [PYTHON_EXE, "-c", "print('no tests')"],
    },
]


# ============ 工具函数 ============

def human_type(text: str) -> None:
    """拟真逐字打字，包含随机速度、停顿、打错改错"""
    i = 0
    while i < len(text):
        ch = text[i]

        # 概率性思考停顿
        if random.random() < PAUSE_PROB:
            time.sleep(random.uniform(*PAUSE_DURATION))

        # 概率性打错一个相邻键并退格修正
        if random.random() < TYPO_PROB and ch.isalpha():
            neighbor = get_neighbor_key(ch)
            if neighbor:
                pyautogui.write(neighbor, interval=random.uniform(*TYPING_SPEED_RANGE))
                time.sleep(random.uniform(0.15, 0.4))
                pyautogui.press('backspace')
                time.sleep(random.uniform(0.1, 0.25))

        # 处理特殊字符
        if ch == '\n':
            pyautogui.press('enter')
        elif ch == '\t':
            pyautogui.press('tab')
        elif ch == '\\':
            pyperclip.copy('\\')
            pyautogui.hotkey('ctrl', 'v')
        else:
            if ch in '{}[]()_|~^<>':
                pyperclip.copy(ch)
                pyautogui.hotkey('ctrl', 'v')
            else:
                try:
                    pyautogui.write(ch, interval=0)
                except Exception:
                    pyperclip.copy(ch)
                    pyautogui.hotkey('ctrl', 'v')

        delay = random.uniform(*TYPING_SPEED_RANGE)
        # 大括号/复杂符号后多停顿
        if ch in '{}()[]':
            delay *= random.uniform(1.5, 3.0)
        time.sleep(delay)
        i += 1


def get_neighbor_key(ch: str) -> str | None:
    """获取键盘上相邻的键（模拟打错）"""
    neighbors = {
        'a': 'sq', 'b': 'vn', 'c': 'xv', 'd': 'sf', 'e': 'wr',
        'f': 'dg', 'g': 'fh', 'h': 'gj', 'i': 'uo', 'j': 'hk',
        'k': 'jl', 'l': 'k;', 'm': 'n,', 'n': 'bm', 'o': 'ip',
        'p': 'o[', 'q': 'wa', 'r': 'et', 's': 'ad', 't': 'ry',
        'u': 'yi', 'v': 'cb', 'w': 'qe', 'x': 'zc', 'y': 'tu',
        'z': 'xa',
    }
    if ch in neighbors:
        return random.choice(neighbors[ch])
    return None


def random_mouse_move() -> None:
    """随机鼠标微移"""
    x, y = pyautogui.position()
    dx = random.randint(-100, 100)
    dy = random.randint(-50, 50)
    pyautogui.moveTo(
        max(0, min(1920, x + dx)),
        max(0, min(1080, y + dy)),
        duration=random.uniform(0.3, 1.0),
    )


def random_scroll() -> None:
    """随机滚动"""
    amount = random.choice([-3, -2, -1, 1, 2, 3])
    pyautogui.scroll(amount)
    time.sleep(random.uniform(0.3, 0.8))


def take_break() -> None:
    """随机休息（模拟阅读/思考）"""
    action = random.choice(["scroll", "mouse", "pause", "pause"])
    if action == "scroll":
        for _ in range(random.randint(2, 5)):
            random_scroll()
    elif action == "mouse":
        for _ in range(random.randint(1, 3)):
            random_mouse_move()
            time.sleep(random.uniform(0.5, 2.0))
    else:
        time.sleep(random.uniform(3.0, 15.0))


def open_in_notepad(filepath: str) -> None:
    """用 notepad 打开文件"""
    subprocess.Popen(["notepad", filepath])
    time.sleep(1.5)


def save_file() -> None:
    """模拟 Ctrl+S 保存"""
    pyautogui.hotkey('ctrl', 's')
    time.sleep(0.5)


def close_notepad() -> None:
    """关闭 notepad"""
    pyautogui.hotkey('alt', 'f4')
    time.sleep(0.8)


def focus_editor() -> None:
    """点击编辑器窗口使其获得焦点"""
    time.sleep(0.5)
    pyautogui.click(960, 540)
    time.sleep(0.3)


def run_command(cmd: list[str], cwd: str) -> tuple[int, str, str]:
    """运行命令并返回 (returncode, stdout, stderr)"""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30, cwd=cwd
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)


# ============ 错误注入 & 修复 ============

def inject_errors(code: str) -> str:
    """在代码中注入一些常见错误，以便后续'发现并修复'"""
    lines = code.split('\n')
    errors_injected = 0
    max_errors = random.randint(1, 3)
    targets = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith('#') and not stripped.startswith('"""') and not stripped.startswith("'''"):
            targets.append(i)

    random.shuffle(targets)
    for idx in targets:
        if errors_injected >= max_errors:
            break
        line = lines[idx]

        # 缺少冒号
        if line.strip().endswith(':') and random.random() < 0.4:
            lines[idx] = line.rstrip()[:-1]
            errors_injected += 1
            continue

        # 拼写错误
        if 'self.' in line and random.random() < 0.3:
            import re
            match = re.search(r'self\.(\w+)', line)
            if match:
                var = match.group(1)
                if len(var) > 2:
                    pos = random.randint(0, len(var) - 1)
                    wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                    wrong_var = var[:pos] + wrong_char + var[pos + 1:]
                    lines[idx] = line.replace(f'self.{var}', f'self.{wrong_var}')
                    errors_injected += 1
                    continue

        # 缩进错误
        if line.startswith('    ') and random.random() < 0.2:
            spaces = len(line) - len(line.lstrip())
            lines[idx] = ' ' * (spaces + 4) + line.lstrip()
            errors_injected += 1

    return '\n'.join(lines)


def analyze_errors(stderr: str, filename: str) -> list[dict]:
    """解析 Python 错误输出"""
    errors = []
    for line in stderr.split('\n'):
        line = line.strip()
        if f'File "{filename}' in line or f'File "./{filename}' in line:
            parts = line.split(',')
            line_no = None
            for p in parts:
                if 'line' in p:
                    try:
                        line_no = int(p.strip().split()[-1])
                    except (ValueError, IndexError):
                        pass
            if line_no:
                errors.append({"line": line_no, "context": line})
    return errors


def show_fix_process(errors: list[dict], code_lines: list[str]) -> list[str]:
    """模拟在编辑器中定位错误、查看、修复的过程"""
    for err in sorted(errors, key=lambda x: x["line"]):
        line_no = err["line"]

        # Ctrl+G 跳转到错误行
        pyautogui.hotkey('ctrl', 'g')
        time.sleep(0.3)
        pyautogui.write(str(line_no), interval=0.05)
        pyautogui.press('enter')
        time.sleep(0.5)

        # 滚动查看上下文
        random_scroll()
        time.sleep(random.uniform(0.5, 1.5))

        # 模拟阅读/思考
        time.sleep(random.uniform(2.0, 5.0))

        # 选中当前行
        pyautogui.hotkey('home')
        time.sleep(0.1)
        pyautogui.hotkey('shift', 'end')
        time.sleep(0.2)

        # 修复：用正确内容替换
        if line_no <= len(code_lines):
            fixed_line = code_lines[line_no - 1]
            pyperclip.copy(fixed_line)
            pyautogui.hotkey('ctrl', 'v')

        time.sleep(random.uniform(0.3, 0.8))
        pyautogui.press('enter')

    return code_lines


# ============ 主流程 ============

def ensure_workspace() -> None:
    """创建工作目录"""
    os.makedirs(WORK_DIR, exist_ok=True)


def write_file_to_disk(filepath: str, content: str) -> None:
    """写入文件到磁盘"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def main() -> None:
    ensure_workspace()
    print(f"[Coding Assistant] 工作目录: {WORK_DIR}")
    print("[Coding Assistant] 5 秒后开始，请切换到编辑器窗口...")
    time.sleep(5)

    cycle = 0
    while True:
        cycle += 1
        template = random.choice(CODE_TEMPLATES)
        print(f"\n[Cycle {cycle}] 选择模板: {list(template['files'].keys())}")

        # ---- Phase 1: 写代码 ----
        for filename, original_code in template["files"].items():
            filepath = os.path.join(WORK_DIR, filename)

            # 注入错误
            buggy_code = inject_errors(original_code)

            # 写入文件
            write_file_to_disk(filepath, buggy_code)

            # 打开文件
            open_in_notepad(filepath)
            focus_editor()

            # 清空内容后逐字输入
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.press('delete')
            time.sleep(0.2)

            print(f"  [Typing] 正在输入 {filename}...")
            human_type(buggy_code)

            # 保存
            save_file()
            print(f"  [Saved] {filename} 已保存")

            # 随机休息
            take_break()

            # ---- Phase 2: 运行 / 检查 ----
            print(f"  [Running] 执行 {filename}...")
            returncode, stdout, stderr = run_command(
                template["run_cmd"](filename), WORK_DIR
            )

            if returncode != 0 and stderr:
                print(f"  [Error] 发现错误！正在分析...")
                time.sleep(random.uniform(1.0, 3.0))

                errors = analyze_errors(stderr, filename)
                if errors:
                    print(f"  [Fixing] 定位到 {len(errors)} 个错误，开始修复")
                    focus_editor()
                    original_lines = original_code.split('\n')
                    show_fix_process(errors, original_lines)
                    save_file()
                    time.sleep(0.5)

                    # 写入修正后的代码
                    write_file_to_disk(filepath, original_code)
                    print(f"  [Fixed] {filename} 已修复")

                    # 重新运行验证
                    time.sleep(random.uniform(1.0, 2.0))
                    rc2, out2, err2 = run_command(
                        template["run_cmd"](filename), WORK_DIR
                    )
                    if rc2 == 0:
                        print(f"  [OK] {filename} 运行成功！")
                    else:
                        print(f"  [Retry] 仍有错误，再试一次")
                else:
                    print(f"  [Skip] 错误无法自动定位")
            else:
                print(f"  [OK] {filename} 运行正常")

            # 关闭 notepad
            close_notepad()
            time.sleep(random.uniform(0.5, 1.5))

        # ---- Phase 3: 运行测试 ----
        print(f"  [Testing] 运行测试...")
        time.sleep(random.uniform(1.0, 3.0))
        try:
            rc, out, err = run_command(template["test_cmd"](), WORK_DIR)
            if rc == 0:
                print(f"  [Tests] 全部通过")
            else:
                print(f"  [Tests] 部分失败，模拟排查")
                time.sleep(random.uniform(3.0, 8.0))
        except Exception:
            pass

        # ---- Phase 4: 随机活动 ----
        print(f"  [Break] 休息一会儿...")
        for _ in range(random.randint(2, 6)):
            random_mouse_move()
            time.sleep(random.uniform(1.0, 4.0))
            if random.random() < 0.3:
                random_scroll()

        time.sleep(random.uniform(5.0, 20.0))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[Coding Assistant] 已停止")
