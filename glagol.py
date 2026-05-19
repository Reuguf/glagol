#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Глагол 0.3 Stable
Русский командный язык программирования поверх Python.
Файлы: .гл
"""

from __future__ import annotations

import sys
import os
import re
import json
import time
import random
import math
import traceback
import importlib
from pathlib import Path
from datetime import datetime
from typing import Any, List, Tuple, Dict, Set


VERSION = "0.3.0-stable"


# =========================
# Runtime helpers
# =========================

def gl_read_text(path: str, encoding: str = "utf-8") -> str:
    return Path(path).read_text(encoding=encoding)

def gl_write_text(path: str, text: Any, encoding: str = "utf-8") -> None:
    p = Path(path)
    if p.parent and str(p.parent) not in ("", "."):
        p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(str(text), encoding=encoding)

def gl_append_text(path: str, text: Any, encoding: str = "utf-8") -> None:
    p = Path(path)
    if p.parent and str(p.parent) not in ("", "."):
        p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding=encoding) as f:
        f.write(str(text))

def gl_file_exists(path: str) -> bool:
    return Path(path).exists()

def gl_read_json(path: str, encoding: str = "utf-8") -> Any:
    with open(path, "r", encoding=encoding) as f:
        return json.load(f)

def gl_write_json(path: str, data: Any, encoding: str = "utf-8") -> None:
    p = Path(path)
    if p.parent and str(p.parent) not in ("", "."):
        p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding=encoding) as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def gl_randint(a: Any, b: Any) -> int:
    return random.randint(int(a), int(b))

def gl_choice(seq: Any) -> Any:
    return random.choice(seq)

def gl_now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def gl_sleep(seconds: Any) -> None:
    time.sleep(float(seconds))


class GlagolGUI:
    """Простой и стабильный GUI-слой на tkinter/ttk."""

    def __init__(self) -> None:
        self.root = None
        self.frame = None
        self.widgets: Dict[str, Any] = {}
        self.widget_types: Dict[str, str] = {}
        self.theme = "светлая"
        self.colors = {
            "bg": "#f3f3f3",
            "fg": "#111111",
            "accent": "#3b82f6",
            "card": "#ffffff",
            "input": "#ffffff",
            "button": "#e5e7eb",
        }

    def _ensure_tk(self):
        try:
            import tkinter as tk
            from tkinter import ttk, messagebox
            return tk, ttk, messagebox
        except Exception as e:
            raise RuntimeError("GUI недоступен: tkinter не найден или не работает") from e

    def create_window(self, title: str = "Глагол", width: int = 640, height: int = 480) -> None:
        tk, ttk, _ = self._ensure_tk()
        self.root = tk.Tk()
        self.root.title(str(title))
        self.root.geometry(f"{int(width)}x{int(height)}")
        self.root.minsize(320, 240)
        self.root.configure(bg=self.colors["bg"])

        self._style_ttk(ttk)

        self.canvas = tk.Canvas(self.root, borderwidth=0, highlightthickness=0, bg=self.colors["bg"])
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.frame = ttk.Frame(self.canvas, padding=12, style="Glagol.TFrame")
        self.frame_id = self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        def _on_frame_configure(event=None):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        def _on_canvas_configure(event):
            try:
                self.canvas.itemconfigure(self.frame_id, width=event.width)
            except Exception:
                pass

        self.frame.bind("<Configure>", _on_frame_configure)
        self.canvas.bind("<Configure>", _on_canvas_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _style_ttk(self, ttk):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("Glagol.TFrame", background=self.colors["bg"])
        style.configure("Glagol.TLabel", background=self.colors["bg"], foreground=self.colors["fg"], font=("Segoe UI", 12))
        style.configure("Glagol.Title.TLabel", background=self.colors["bg"], foreground=self.colors["fg"], font=("Segoe UI", 20, "bold"))
        style.configure("Glagol.TButton", font=("Segoe UI", 12), padding=8)
        style.configure("Glagol.TEntry", font=("Segoe UI", 12), padding=6)
        style.configure("Glagol.TLabelframe", background=self.colors["bg"], foreground=self.colors["fg"])
        style.configure("Glagol.TLabelframe.Label", background=self.colors["bg"], foreground=self.colors["fg"], font=("Segoe UI", 12, "bold"))

    def set_theme(self, theme: str) -> None:
        theme = str(theme).lower().strip()
        self.theme = theme
        if "тём" in theme or "тем" in theme or "dark" in theme:
            self.colors.update({
                "bg": "#111827",
                "fg": "#f9fafb",
                "accent": "#60a5fa",
                "card": "#1f2937",
                "input": "#374151",
                "button": "#374151",
            })
        elif "фиолет" in theme:
            self.colors.update({
                "bg": "#1e1b4b",
                "fg": "#f5f3ff",
                "accent": "#a78bfa",
                "card": "#312e81",
                "input": "#3730a3",
                "button": "#4c1d95",
            })
        else:
            self.colors.update({
                "bg": "#f3f3f3",
                "fg": "#111111",
                "accent": "#3b82f6",
                "card": "#ffffff",
                "input": "#ffffff",
                "button": "#e5e7eb",
            })

        if self.root is not None:
            try:
                from tkinter import ttk
                self.root.configure(bg=self.colors["bg"])
                self.canvas.configure(bg=self.colors["bg"])
                self._style_ttk(ttk)
            except Exception:
                pass

    def _parent(self):
        if self.frame is None:
            self.create_window("Глагол", 640, 480)
        return self.frame

    def add_title(self, text: str, name: str | None = None):
        from tkinter import ttk
        w = ttk.Label(self._parent(), text=str(text), anchor="center", style="Glagol.Title.TLabel")
        w.pack(fill="x", pady=(8, 12))
        if name:
            self._store(name, w, "label")
        return w

    def add_text(self, text: str, name: str | None = None):
        from tkinter import ttk
        w = ttk.Label(self._parent(), text=str(text), anchor="center", wraplength=900, style="Glagol.TLabel")
        w.pack(fill="x", pady=5)
        if name:
            self._store(name, w, "label")
        return w

    def add_input(self, placeholder: str, name: str):
        from tkinter import ttk
        w = ttk.Entry(self._parent(), style="Glagol.TEntry")
        if placeholder:
            w.insert(0, str(placeholder))
            w.selection_range(0, "end")
        w.pack(fill="x", pady=6)
        self._store(name, w, "entry")
        return w

    def add_button(self, text: str, name: str):
        from tkinter import ttk
        w = ttk.Button(self._parent(), text=str(text), style="Glagol.TButton")
        w.pack(fill="x", pady=7)
        self._store(name, w, "button")
        return w

    def add_big_text(self, text: str, name: str, height: int = 7):
        import tkinter as tk
        w = tk.Text(self._parent(), height=int(height), wrap="word", font=("Segoe UI", 11),
                    bg=self.colors["card"], fg=self.colors["fg"], insertbackground=self.colors["fg"],
                    relief="flat", padx=10, pady=10)
        w.insert("1.0", str(text))
        w.pack(fill="both", expand=False, pady=7)
        self._store(name, w, "text")
        return w

    def add_canvas(self, width: int, height: int, name: str):
        import tkinter as tk
        w = tk.Canvas(self._parent(), width=int(width), height=int(height), bg=self.colors["card"], highlightthickness=0)
        w.pack(fill="x", pady=8)
        self._store(name, w, "canvas")
        return w

    def add_card(self, text: str, name: str | None = None):
        from tkinter import ttk
        card = ttk.Labelframe(self._parent(), text=str(text), padding=10, style="Glagol.TLabelframe")
        card.pack(fill="x", pady=8)
        if name:
            self._store(name, card, "card")
        return card

    def spacer(self, size: int = 8):
        from tkinter import ttk
        w = ttk.Frame(self._parent(), height=int(size), style="Glagol.TFrame")
        w.pack(fill="x")
        return w

    def _store(self, name: str, widget: Any, typ: str) -> None:
        self.widgets[str(name)] = widget
        self.widget_types[str(name)] = typ

    def value(self, name: str) -> str:
        name = str(name)
        w = self.widgets.get(name)
        typ = self.widget_types.get(name)
        if w is None:
            return ""
        try:
            if typ == "entry":
                return w.get()
            if typ == "text":
                return w.get("1.0", "end-1c")
            if typ == "label":
                return str(w.cget("text"))
        except Exception:
            return ""
        return ""

    def set(self, name: str, value: Any) -> None:
        name = str(name)
        w = self.widgets.get(name)
        typ = self.widget_types.get(name)
        if w is None:
            print(f"[Глагол GUI] Элемент не найден: {name}")
            return
        value = str(value)
        if typ == "label":
            w.configure(text=value)
        elif typ == "entry":
            w.delete(0, "end")
            w.insert(0, value)
        elif typ == "text":
            w.delete("1.0", "end")
            w.insert("1.0", value)
        elif typ == "button":
            w.configure(text=value)

    def clear(self, name: str) -> None:
        self.set(name, "")

    def on_click_decorator(self, name: str):
        def deco(func):
            def wrapped(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    self.show_error(f"Ошибка в событии кнопки '{name}'", e)
            w = self.widgets.get(str(name))
            if w is None:
                print(f"[Глагол GUI] Кнопка не найдена: {name}")
            else:
                try:
                    w.configure(command=wrapped)
                except Exception as e:
                    print(f"[Глагол GUI] Не удалось назначить событие {name}: {e}")
            return wrapped
        return deco

    def show_error(self, title: str, err: Exception) -> None:
        msg = f"{title}\n\n{type(err).__name__}: {err}"
        print(msg)
        traceback.print_exc()
        try:
            _, _, messagebox = self._ensure_tk()
            messagebox.showerror("Ошибка Глагола", msg)
        except Exception:
            pass

    def message(self, text: str, title: str = "Глагол") -> None:
        try:
            _, _, messagebox = self._ensure_tk()
            messagebox.showinfo(str(title), str(text))
        except Exception:
            print(text)

    def draw_rect(self, canvas_name: str, x1, y1, x2, y2, color: str = "#60a5fa") -> None:
        c = self.widgets.get(str(canvas_name))
        if c is not None:
            c.create_rectangle(float(x1), float(y1), float(x2), float(y2), fill=str(color), outline="")

    def draw_circle(self, canvas_name: str, x, y, r, color: str = "#60a5fa") -> None:
        c = self.widgets.get(str(canvas_name))
        if c is not None:
            x, y, r = float(x), float(y), float(r)
            c.create_oval(x-r, y-r, x+r, y+r, fill=str(color), outline="")

    def draw_text(self, canvas_name: str, x, y, text: str, color: str = None, size: int = 16) -> None:
        c = self.widgets.get(str(canvas_name))
        if c is not None:
            c.create_text(float(x), float(y), text=str(text), fill=color or self.colors["fg"], font=("Segoe UI", int(size), "bold"))

    def clear_canvas(self, canvas_name: str) -> None:
        c = self.widgets.get(str(canvas_name))
        if c is not None:
            c.delete("all")

    def run(self) -> None:
        if self.root is None:
            self.create_window("Глагол", 640, 480)
        self.root.mainloop()


__gl_gui = GlagolGUI()


class GlagolError(Exception):
    pass


def is_inside_string_aware_scan(text: str):
    quote = None
    escape = False
    for i, ch in enumerate(text):
        if quote:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == quote:
                quote = None
            yield i, ch, True
        else:
            if ch in ("'", '"'):
                quote = ch
                yield i, ch, True
            else:
                yield i, ch, False


def split_code_string_segments(text: str) -> List[Tuple[str, bool]]:
    parts: List[Tuple[str, bool]] = []
    buf = []
    quote = None
    escape = False

    def flush(flag):
        nonlocal buf
        if buf:
            parts.append(("".join(buf), flag))
            buf = []

    for ch in text:
        if quote:
            buf.append(ch)
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == quote:
                flush(True)
                quote = None
        else:
            if ch in ("'", '"'):
                flush(False)
                quote = ch
                buf.append(ch)
            else:
                buf.append(ch)
    flush(bool(quote))
    return parts


def replace_outside_strings(text: str, fn) -> str:
    out = []
    for part, is_str in split_code_string_segments(text):
        out.append(part if is_str else fn(part))
    return "".join(out)


def strip_final_dot(text: str) -> str:
    s = text.rstrip()
    if not s.endswith("."):
        return text
    quote = None
    escape = False
    for ch in s[:-1]:
        if quote:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == quote:
                quote = None
        else:
            if ch in ("'", '"'):
                quote = ch
    if quote is None:
        return s[:-1].rstrip()
    return text


def bracket_delta_outside_strings(text: str) -> int:
    delta = 0
    for _, ch, in_str in is_inside_string_aware_scan(text):
        if in_str:
            continue
        if ch in "([{":
            delta += 1
        elif ch in ")]}":
            delta -= 1
    return delta


def preprocess_logical_lines(source: str) -> List[Tuple[int, str]]:
    source = source.replace("\r\n", "\n").replace("\r", "\n").replace("\t", "    ")
    raw_lines = source.split("\n")
    logical: List[Tuple[int, str]] = []
    pending = ""
    pending_lineno = 1
    depth = 0

    for lineno, line in enumerate(raw_lines, start=1):
        if not pending:
            pending = line
            pending_lineno = lineno
        else:
            pending += " " + line.strip()

        depth += bracket_delta_outside_strings(line)

        if depth <= 0:
            logical.append((pending_lineno, pending))
            pending = ""
            depth = 0

    if pending:
        logical.append((pending_lineno, pending))
    return logical


IDENT_RE = r"[A-Za-zА-Яа-яЁё_][A-Za-zА-Яа-яЁё0-9_]*"


def get_indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def russian_suffix_replace(part: str) -> str:
    suffixes = {
        "млрд": 1_000_000_000,
        "мин": 60,
        "кб": 1024,
        "мб": 1024**2,
        "гб": 1024**3,
        "к": 1_000,
        "м": 1_000_000,
        "с": 1,
        "ч": 3600,
    }

    def repl(m):
        num_s = m.group(1).replace(",", ".")
        suffix = m.group(2).lower()
        num = float(num_s)
        val = num * suffixes[suffix]
        if val.is_integer():
            return str(int(val))
        return str(val)

    return re.sub(r"(?<![A-Za-zА-Яа-яЁё0-9_])(\d+(?:[\.,]\d+)?)(млрд|мин|кб|мб|гб|к|м|с|ч)\b", repl, part, flags=re.IGNORECASE)


def basic_expr_replacements(part: str) -> str:
    replacements = [
        (r"\bбольше\s+или\s+равно\b", ">="),
        (r"\bменьше\s+или\s+равно\b", "<="),
        (r"\bне\s+равно\b", "!="),
        (r"\bравно\b", "=="),
        (r"\bбольше\b", ">"),
        (r"\bменьше\b", "<"),
        (r"\bи\b", "and"),
        (r"\bили\b", "or"),
        (r"\bне\b", "not"),
        (r"\bда\b", "True"),
        (r"\bнет\b", "False"),
        (r"\bничего\b", "None"),
    ]
    for pat, rep in replacements:
        part = re.sub(pat, rep, part, flags=re.IGNORECASE)
    return part


def translate_special_exprs(expr: str) -> str:
    expr = expr.strip()

    # Whole-expression commands first. This correctly handles quoted filenames
    # like: прочитай файл "a.txt"
    m = re.match(r"^прочитай\s+файл\s+(.+)$", expr, re.IGNORECASE)
    if m:
        return f"gl_read_text({convert_expr(m.group(1))})"

    m = re.match(r"^прочитай\s+json\s+(.+)$", expr, re.IGNORECASE)
    if m:
        return f"gl_read_json({convert_expr(m.group(1))})"

    m = re.match(r"^файл\s+существует\s+(.+)$", expr, re.IGNORECASE)
    if m:
        return f"gl_file_exists({convert_expr(m.group(1))})"

    m = re.match(r"^случайное\s+число\s+от\s+(.+?)\s+до\s+(.+)$", expr, re.IGNORECASE)
    if m:
        return f"gl_randint({convert_expr(m.group(1))}, {convert_expr(m.group(2))})"

    m = re.match(r"^случайный\s+элемент\s+из\s+(.+)$", expr, re.IGNORECASE)
    if m:
        return f"gl_choice({convert_expr(m.group(1))})"

    if re.match(r"^текущее\s+время$", expr, re.IGNORECASE):
        return "gl_now()"

    def repl(part: str) -> str:
        part = re.sub(rf"\bзначение\s+({IDENT_RE})\b", r'__gl_gui.value("\1")', part)
        # Phrase replacements inside larger expressions.
        part = re.sub(r"\bтекущее\s+время\b", "gl_now()", part, flags=re.IGNORECASE)
        return part

    return replace_outside_strings(expr, repl)

def convert_expr(expr: str) -> str:
    expr = strip_final_dot(expr.strip())
    expr = replace_outside_strings(expr, russian_suffix_replace)
    expr = translate_special_exprs(expr)
    expr = replace_outside_strings(expr, basic_expr_replacements)
    return expr.strip()


class Translator:
    def __init__(self, source: str, filename: str = "<глагол>", safe: bool = False):
        self.source = source
        self.filename = filename
        self.safe = safe
        self.lines = preprocess_logical_lines(source)
        self.gui_elements: Set[str] = set()
        self.top_vars: Set[str] = set()
        self.block_globals: Dict[int, List[str]] = {}
        self.event_count = 0
        self.loop_count = 0
        self.scan()

    def scan(self) -> None:
        for idx, (lineno, line) in enumerate(self.lines):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            code = strip_final_dot(stripped)
            indent = get_indent(line)
            m = re.match(rf"пусть\s+({IDENT_RE})(?:\s*:\s*{IDENT_RE})?\s+буд(?:ет|ут)\s+(.+)$", code, re.IGNORECASE)
            if indent == 0 and m:
                self.top_vars.add(m.group(1))
            m = re.search(rf"\s+как\s+({IDENT_RE})\s*$", code, re.IGNORECASE)
            if code.lower().startswith("добавь ") and m:
                self.gui_elements.add(m.group(1))

        for idx, (lineno, line) in enumerate(self.lines):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            code = strip_final_dot(stripped)
            indent = get_indent(line)
            is_block = bool(re.match(rf"(действие\s+{IDENT_RE}|\bкогда\s+нажата\s+{IDENT_RE})", code, re.IGNORECASE))
            if not is_block:
                continue
            modified: Set[str] = set()
            j = idx + 1
            while j < len(self.lines):
                _, ln = self.lines[j]
                if ln.strip() and get_indent(ln) <= indent:
                    break
                c = strip_final_dot(ln.strip())
                for pat in [
                    rf"пусть\s+({IDENT_RE})(?:\s*:\s*{IDENT_RE})?\s+буд(?:ет|ут)\s+",
                    rf"измени\s+({IDENT_RE})\s+на\s+",
                    rf"увеличь\s+({IDENT_RE})\s+на\s+",
                    rf"уменьши\s+({IDENT_RE})\s+на\s+",
                    rf"умножь\s+({IDENT_RE})\s+на\s+",
                    rf"раздели\s+({IDENT_RE})\s+на\s+",
                ]:
                    mm = re.match(pat, c, re.IGNORECASE)
                    if mm:
                        name = mm.group(1)
                        if name in self.top_vars and name not in self.gui_elements:
                            modified.add(name)
                j += 1
            if modified:
                self.block_globals[idx] = sorted(modified)

    def check_safe(self, text: str, lineno: int) -> None:
        if not self.safe:
            return
        lowered = text.lower()
        dangerous = [
            "eval", "exec", "__import__", "subprocess", "os.system", "shutil.rmtree",
            "удали файл", "import ", "from ", "подключи python",
        ]
        for d in dangerous:
            if d in lowered:
                raise GlagolError(f"Безопасный режим: запрещённая конструкция '{d}' в строке {lineno}")

    def translate(self) -> str:
        out: List[str] = [
            "# -*- coding: utf-8 -*-",
            f"# Сгенерировано Глаголом {VERSION}",
        ]

        for idx, (lineno, line) in enumerate(self.lines):
            raw = line.rstrip()
            if not raw.strip():
                out.append("")
                continue

            indent = " " * get_indent(raw)
            stripped = raw.strip()
            if stripped.startswith("#"):
                out.append(raw)
                continue

            self.check_safe(stripped, lineno)

            try:
                translated = self.translate_statement(stripped, idx, lineno)
            except GlagolError:
                raise
            except Exception as e:
                raise GlagolError(f"Ошибка перевода в строке {lineno}: {e}") from e

            if isinstance(translated, list):
                for t in translated:
                    out.append(indent + t if t else "")
            else:
                out.append(indent + translated)

        return "\n".join(out) + "\n"

    def translate_statement(self, stripped: str, idx: int, lineno: int):
        code = strip_final_dot(stripped)

        m = re.match(r'подключи\s+python\s+["\'](.+?)["\']\s+как\s+(' + IDENT_RE + r')$', code, re.IGNORECASE)
        if m:
            return f'{m.group(2)} = importlib.import_module("{m.group(1)}")'

        m = re.match(rf"подключи\s+({IDENT_RE})$", code, re.IGNORECASE)
        if m:
            name = m.group(1).lower()
            if name in ("математика", "math"):
                return "математика = math"
            if name in ("случайность", "random"):
                return "случайность = random"
            if name in ("время", "time"):
                return "время = time"
            if name in ("json", "джсон"):
                return "json = json"
            if name in ("файлы", "файл"):
                return "# модуль файлов встроен"
            return f'{m.group(1)} = importlib.import_module("{m.group(1)}")'

        m = re.match(r'создай\s+окно\s+(.+?)\s+размером\s+(.+?)\s+на\s+(.+)$', code, re.IGNORECASE)
        if m:
            return f"__gl_gui.create_window({convert_expr(m.group(1))}, {convert_expr(m.group(2))}, {convert_expr(m.group(3))})"

        m = re.match(r'установи\s+тему\s+(.+)$', code, re.IGNORECASE)
        if m:
            return f"__gl_gui.set_theme({convert_expr(m.group(1))})"

        m = re.match(r'покажи\s+сообщение\s+(.+)$', code, re.IGNORECASE)
        if m:
            return f"__gl_gui.message({convert_expr(m.group(1))})"

        m = re.match(r'добавь\s+заголовок\s+(.+?)(?:\s+как\s+(' + IDENT_RE + r'))?$', code, re.IGNORECASE)
        if m:
            text, name = m.group(1), m.group(2)
            return f'__gl_gui.add_title({convert_expr(text)}, {repr(name) if name else "None"})'

        m = re.match(r'добавь\s+большой\s+текст\s+(.+?)\s+как\s+(' + IDENT_RE + r')$', code, re.IGNORECASE)
        if m:
            return f'__gl_gui.add_big_text({convert_expr(m.group(1))}, "{m.group(2)}")'

        m = re.match(r'добавь\s+текст\s+(.+?)(?:\s+как\s+(' + IDENT_RE + r'))?$', code, re.IGNORECASE)
        if m:
            text, name = m.group(1), m.group(2)
            return f'__gl_gui.add_text({convert_expr(text)}, {repr(name) if name else "None"})'

        m = re.match(r'добавь\s+поле\s+(.+?)\s+как\s+(' + IDENT_RE + r')$', code, re.IGNORECASE)
        if m:
            return f'__gl_gui.add_input({convert_expr(m.group(1))}, "{m.group(2)}")'

        m = re.match(r'добавь\s+кнопку\s+(.+?)\s+как\s+(' + IDENT_RE + r')$', code, re.IGNORECASE)
        if m:
            return f'__gl_gui.add_button({convert_expr(m.group(1))}, "{m.group(2)}")'

        m = re.match(r'добавь\s+карточку\s+(.+?)(?:\s+как\s+(' + IDENT_RE + r'))?$', code, re.IGNORECASE)
        if m:
            return f'__gl_gui.add_card({convert_expr(m.group(1))}, {repr(m.group(2)) if m.group(2) else "None"})'

        m = re.match(r'добавь\s+отступ\s+(.+)$', code, re.IGNORECASE)
        if m:
            return f"__gl_gui.spacer({convert_expr(m.group(1))})"

        m = re.match(r'добавь\s+холст\s+размером\s+(.+?)\s+на\s+(.+?)\s+как\s+(' + IDENT_RE + r')$', code, re.IGNORECASE)
        if m:
            return f'__gl_gui.add_canvas({convert_expr(m.group(1))}, {convert_expr(m.group(2))}, "{m.group(3)}")'

        m = re.match(r'нарисуй\s+прямоугольник\s+в\s+(' + IDENT_RE + r')\s+от\s+(.+?)\s*,\s*(.+?)\s+до\s+(.+?)\s*,\s*(.+?)\s+цветом\s+(.+)$', code, re.IGNORECASE)
        if m:
            return f'__gl_gui.draw_rect("{m.group(1)}", {convert_expr(m.group(2))}, {convert_expr(m.group(3))}, {convert_expr(m.group(4))}, {convert_expr(m.group(5))}, {convert_expr(m.group(6))})'

        m = re.match(r'нарисуй\s+круг\s+в\s+(' + IDENT_RE + r')\s+на\s+(.+?)\s*,\s*(.+?)\s+радиусом\s+(.+?)\s+цветом\s+(.+)$', code, re.IGNORECASE)
        if m:
            return f'__gl_gui.draw_circle("{m.group(1)}", {convert_expr(m.group(2))}, {convert_expr(m.group(3))}, {convert_expr(m.group(4))}, {convert_expr(m.group(5))})'

        m = re.match(r'нарисуй\s+надпись\s+в\s+(' + IDENT_RE + r')\s+на\s+(.+?)\s*,\s*(.+?)\s+текст\s+(.+?)(?:\s+цветом\s+(.+?))?$', code, re.IGNORECASE)
        if m:
            color = convert_expr(m.group(5)) if m.group(5) else "None"
            return f'__gl_gui.draw_text("{m.group(1)}", {convert_expr(m.group(2))}, {convert_expr(m.group(3))}, {convert_expr(m.group(4))}, {color})'

        m = re.match(r'очисти\s+холст\s+(' + IDENT_RE + r')$', code, re.IGNORECASE)
        if m:
            return f'__gl_gui.clear_canvas("{m.group(1)}")'

        m = re.match(r'запусти\s+окно$', code, re.IGNORECASE)
        if m:
            return "__gl_gui.run()"

        m = re.match(r'когда\s+нажата\s+(' + IDENT_RE + r')\s*:$', code, re.IGNORECASE)
        if m:
            self.event_count += 1
            func_name = f"__gl_event_{self.event_count}"
            lines = [f'@__gl_gui.on_click_decorator("{m.group(1)}")', f"def {func_name}():"]
            globs = self.block_globals.get(idx)
            if globs:
                lines.append("    global " + ", ".join(globs))
            return lines

        m = re.match(r'действие\s+(' + IDENT_RE + r')\s*\((.*?)\)\s*:$', code, re.IGNORECASE)
        if m:
            args = m.group(2).strip()
            lines = [f"def {m.group(1)}({args}):"]
            globs = self.block_globals.get(idx)
            if globs:
                lines.append("    global " + ", ".join(globs))
            return lines

        m = re.match(r'действие\s+(' + IDENT_RE + r')\s*:$', code, re.IGNORECASE)
        if m:
            lines = [f"def {m.group(1)}():"]
            globs = self.block_globals.get(idx)
            if globs:
                lines.append("    global " + ", ".join(globs))
            return lines

        m = re.match(r'действие\s+(' + IDENT_RE + r')\s+с\s+(.+?)\s*:$', code, re.IGNORECASE)
        if m:
            args = ", ".join([a.strip() for a in re.split(r"\s*,\s*|\s+и\s+", m.group(2)) if a.strip()])
            lines = [f"def {m.group(1)}({args}):"]
            globs = self.block_globals.get(idx)
            if globs:
                lines.append("    global " + ", ".join(globs))
            return lines

        m = re.match(r'если\s+(.+)\s*:$', code, re.IGNORECASE)
        if m:
            return f"if {convert_expr(m.group(1))}:"

        m = re.match(r'иначе\s+если\s+(.+)\s*:$', code, re.IGNORECASE)
        if m:
            return f"elif {convert_expr(m.group(1))}:"

        if re.match(r'иначе\s*:$', code, re.IGNORECASE):
            return "else:"

        m = re.match(r'пока\s+(.+)\s*:$', code, re.IGNORECASE)
        if m:
            return f"while {convert_expr(m.group(1))}:"

        m = re.match(r'повтори\s+(.+?)\s+раз\s*:$', code, re.IGNORECASE)
        if m:
            self.loop_count += 1
            return f"for __gl_i_{self.loop_count} in range(int({convert_expr(m.group(1))})):"

        m = re.match(r'для\s+(' + IDENT_RE + r')\s+от\s+(.+?)\s+до\s+(.+?)\s*:$', code, re.IGNORECASE)
        if m:
            return f"for {m.group(1)} in range(int({convert_expr(m.group(2))}), int({convert_expr(m.group(3))}) + 1):"

        m = re.match(r'для\s+каждого\s+(' + IDENT_RE + r')\s+из\s+(.+?)\s*:$', code, re.IGNORECASE)
        if m:
            return f"for {m.group(1)} in {convert_expr(m.group(2))}:"

        if re.match(r'попробуй\s*:$', code, re.IGNORECASE):
            return "try:"
        m = re.match(r'поймай\s+ошибку\s+как\s+(' + IDENT_RE + r')\s*:$', code, re.IGNORECASE)
        if m:
            return f"except Exception as {m.group(1)}:"
        if re.match(r'поймай\s+ошибку\s*:$', code, re.IGNORECASE):
            return "except Exception:"
        if re.match(r'всегда\s*:$', code, re.IGNORECASE):
            return "finally:"

        m = re.match(r'выведи(?:\s+(?:текст|число|значение|строку))?\s+(.+)$', code, re.IGNORECASE)
        if m:
            return f"print({convert_expr(m.group(1))})"

        m = re.match(r'спроси\s+текст\s+(.+?)\s+и\s+запомни\s+как\s+(' + IDENT_RE + r')$', code, re.IGNORECASE)
        if m:
            return f"{m.group(2)} = input({convert_expr(m.group(1))})"

        m = re.match(r'пусть\s+(' + IDENT_RE + r')(?:\s*:\s*' + IDENT_RE + r')?\s+буд(?:ет|ут)\s+(.+)$', code, re.IGNORECASE)
        if m:
            return f"{m.group(1)} = {convert_expr(m.group(2))}"

        m = re.match(r'измени\s+(' + IDENT_RE + r')\s+на\s+(.+)$', code, re.IGNORECASE)
        if m:
            name = m.group(1)
            if name in self.gui_elements:
                return f'__gl_gui.set("{name}", {convert_expr(m.group(2))})'
            return f"{name} = {convert_expr(m.group(2))}"

        m = re.match(r'очисти\s+(' + IDENT_RE + r')$', code, re.IGNORECASE)
        if m:
            name = m.group(1)
            if name in self.gui_elements:
                return f'__gl_gui.clear("{name}")'
            return f"{name}.clear()"

        m = re.match(r'увеличь\s+(' + IDENT_RE + r')\s+на\s+(.+)$', code, re.IGNORECASE)
        if m:
            return f"{m.group(1)} += {convert_expr(m.group(2))}"

        m = re.match(r'уменьши\s+(' + IDENT_RE + r')\s+на\s+(.+)$', code, re.IGNORECASE)
        if m:
            return f"{m.group(1)} -= {convert_expr(m.group(2))}"

        m = re.match(r'умножь\s+(' + IDENT_RE + r')\s+на\s+(.+)$', code, re.IGNORECASE)
        if m:
            return f"{m.group(1)} *= {convert_expr(m.group(2))}"

        m = re.match(r'раздели\s+(' + IDENT_RE + r')\s+на\s+(.+)$', code, re.IGNORECASE)
        if m:
            return f"{m.group(1)} /= {convert_expr(m.group(2))}"

        m = re.match(r'добавь\s+(.+?)\s+в\s+(' + IDENT_RE + r')$', code, re.IGNORECASE)
        if m:
            return f"{m.group(2)}.append({convert_expr(m.group(1))})"

        m = re.match(r'удали\s+(.+?)\s+из\s+(' + IDENT_RE + r')$', code, re.IGNORECASE)
        if m:
            return f"{m.group(2)}.remove({convert_expr(m.group(1))})"

        m = re.match(r'запиши\s+текст\s+(.+?)\s+в\s+файл\s+(.+)$', code, re.IGNORECASE)
        if m:
            return f"gl_write_text({convert_expr(m.group(2))}, {convert_expr(m.group(1))})"

        m = re.match(r'добавь\s+текст\s+(.+?)\s+в\s+файл\s+(.+)$', code, re.IGNORECASE)
        if m:
            return f"gl_append_text({convert_expr(m.group(2))}, {convert_expr(m.group(1))})"

        m = re.match(r'запиши\s+json\s+(.+?)\s+в\s+файл\s+(.+)$', code, re.IGNORECASE)
        if m:
            return f"gl_write_json({convert_expr(m.group(2))}, {convert_expr(m.group(1))})"

        m = re.match(r'подожди\s+(.+)$', code, re.IGNORECASE)
        if m:
            return f"gl_sleep({convert_expr(m.group(1))})"

        m = re.match(r'верни(?:\s+(.+))?$', code, re.IGNORECASE)
        if m:
            return "return" if not m.group(1) else f"return {convert_expr(m.group(1))}"

        if re.match(r'останови$', code, re.IGNORECASE):
            return "break"

        if re.match(r'пропусти$', code, re.IGNORECASE):
            return "continue"

        m = re.match(r'выбрось\s+ошибку\s+(.+)$', code, re.IGNORECASE)
        if m:
            return f"raise Exception({convert_expr(m.group(1))})"

        direct = convert_expr(code)
        if direct:
            return direct

        raise GlagolError(f"Ошибка перевода в строке {lineno}: неизвестная команда '{stripped}'")


def translate_source(source: str, filename: str = "<глагол>", safe: bool = False) -> str:
    return Translator(source, filename, safe=safe).translate()


def runtime_globals() -> Dict[str, Any]:
    env = {
        "__name__": "__main__",
        "VERSION": VERSION,
        "importlib": importlib,
        "json": json,
        "time": time,
        "random": random,
        "math": math,
        "Path": Path,
        "datetime": datetime,
        "gl_read_text": gl_read_text,
        "gl_write_text": gl_write_text,
        "gl_append_text": gl_append_text,
        "gl_file_exists": gl_file_exists,
        "gl_read_json": gl_read_json,
        "gl_write_json": gl_write_json,
        "gl_randint": gl_randint,
        "gl_choice": gl_choice,
        "gl_now": gl_now,
        "gl_sleep": gl_sleep,
        "__gl_gui": __gl_gui,
        "корень": math.sqrt,
        "синус": math.sin,
        "косинус": math.cos,
        "тангенс": math.tan,
        "округли": round,
        "длина": len,
        "число": int,
        "дробь": float,
        "текст": str,
        "список": list,
        "словарь": dict,
    }
    return env


def run_file(path: str, *, show_python: bool = False, check_only: bool = False, safe: bool = False) -> int:
    p = Path(path)
    if not p.exists():
        print(f"Ошибка: файл не найден: {path}")
        return 1
    try:
        source = p.read_text(encoding="utf-8-sig")
        py = translate_source(source, filename=str(p), safe=safe)

        if show_python:
            print(py)
            return 0

        try:
            compile(py, str(p), "exec")
        except SyntaxError as e:
            print("Ошибка Глагола:")
            print("Сгенерированный Python-код содержит синтаксическую ошибку.")
            print(f"Строка Python: {e.lineno}, {e.msg}")
            if e.text:
                print(e.text.rstrip())
            return 1

        if check_only:
            print("Проверка завершена: ошибок перевода не найдено.")
            return 0

        env = runtime_globals()
        exec(compile(py, str(p), "exec"), env, env)
        return 0
    except GlagolError as e:
        print("Ошибка Глагола:")
        print(e)
        return 1
    except Exception as e:
        print("Ошибка выполнения Глагола:")
        print(f"{type(e).__name__}: {e}")
        traceback.print_exc()
        return 1


TEMPLATES = {
    "консоль": """выведи текст "Привет из Глагола 0.3".
пусть имя будет "Мир".
выведи "Привет, " + имя.
""",
    "окно": """создай окно "Приложение на Глаголе" размером 600 на 400.
установи тему "тёмная".

добавь заголовок "Моё приложение".
добавь поле "Введи имя" как имя.
добавь кнопку "Поздороваться" как кнопка.
добавь текст "" как ответ.

когда нажата кнопка:
    если значение имя равно "":
        измени ответ на "Введи имя."
    иначе:
        измени ответ на "Привет, " + значение имя.

запусти окно.
""",
    "графика": """создай окно "Графика Глагола" размером 800 на 600.
установи тему "тёмная".

добавь заголовок "Холст и фигуры".
добавь холст размером 740 на 360 как холст.

нарисуй прямоугольник в холст от 30, 40 до 250, 170 цветом "#2563eb".
нарисуй круг в холст на 430, 150 радиусом 90 цветом "#7c3aed".
нарисуй надпись в холст на 370, 300 текст "Глагол 0.3" цветом "#f9fafb".

запусти окно.
""",
}


def create_template(kind: str) -> int:
    kind = kind.lower().strip()
    if kind not in TEMPLATES:
        print("Неизвестный шаблон. Доступно: консоль, окно, графика")
        return 1
    name = {
        "консоль": "main.гл",
        "окно": "window.гл",
        "графика": "graphics.гл",
    }[kind]
    Path(name).write_text(TEMPLATES[kind], encoding="utf-8")
    print(f"Создан файл: {name}")
    return 0


def print_help() -> None:
    print(f"""Глагол {VERSION}

Использование:
  glagol файл.гл
  glagol файл.гл --python
  glagol файл.гл --безопасно
  glagol проверить файл.гл
  glagol создать консоль
  glagol создать окно
  glagol создать графика
  glagol версия
""")


def main(argv: List[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    if not argv:
        print_help()
        return 0

    if argv[0].lower() in ("версия", "--version", "-v"):
        print(VERSION)
        return 0

    if argv[0].lower() in ("помощь", "--help", "-h"):
        print_help()
        return 0

    if argv[0].lower() == "создать":
        if len(argv) < 2:
            print("Укажи шаблон: консоль, окно, графика")
            return 1
        return create_template(argv[1])

    if argv[0].lower() == "проверить":
        if len(argv) < 2:
            print("Укажи файл для проверки.")
            return 1
        return run_file(argv[1], check_only=True, safe=("--безопасно" in argv))

    path = argv[0]
    show_python = "--python" in argv
    safe = "--безопасно" in argv
    return run_file(path, show_python=show_python, safe=safe)


if __name__ == "__main__":
    raise SystemExit(main())
