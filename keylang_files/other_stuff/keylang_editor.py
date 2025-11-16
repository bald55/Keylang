import tkinter as tk
from tkinter import ttk
import re
import subprocess
import traceback
import sys
import threading
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

keywords = ["False", "None", "True", "and", "as", "assert", "async", "await", "break", "class", "continue", "def", "del", "elif", "else", "except", "finally", "for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try", "while", "with", "yield", "func", "print_vars", "print_nones", "print_all", "protected", "private", "self", "spawn", "'s", "f", "embed_lua"]

symbols = sorted(set([
"False", "None", "True", "and", "as", "assert", "async", "await", "break", "class", "continue", "del", "elif", "else", "except", "finally", "for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try", "while", "with", "yield", "func", "print_vars", "print_nones", "print_all", "protected", "private", "self", "loop", "wait", "once", "array", "dict", "random", "random_range", "spawn", "'s", "f", "embed_lua",

"abs", "aiter", "all", "anext", "any", "ascii", "bin", "bool", "breakpoint", "bytearray", "bytes", "callable", "chr", "classmethod", "compile", "complex", "delattr", "dir", "divmod", "enumerate", "eval", "exec", "filter", "float", "format", "frozenset", "getattr", "globals", "hasattr", "hash", "help", "hex", "id", "input", "int", "isinstance", "issubclass", "iter", "len", "list", "locals", "map", "max", "memoryview", "min", "next", "object", "oct", "open", "ord", "pow", "print", "property", "range", "repr", "reversed", "round", "set", "setattr", "slice", "sorted", "staticmethod", "str", "sum", "super", "tuple", "type", "vars", "zip", "__import__",

"Ellipsis", "NotImplemented",

"BaseException", "Exception", "ArithmeticError", "BufferError", "LookupError", "AssertionError", "AttributeError", "EOFError", "FloatingPointError", "GeneratorExit", "ImportError", "ModuleNotFoundError", "IndexError", "KeyError", "KeyboardInterrupt", "MemoryError", "NameError", "NotImplementedError", "OSError", "OverflowError", "RecursionError", "ReferenceError", "RuntimeError", "StopIteration", "StopAsyncIteration", "SyntaxError", "IndentationError", "TabError", "SystemError", "SystemExit", "TypeError", "UnboundLocalError", "UnicodeError", "UnicodeEncodeError", "UnicodeDecodeError", "UnicodeTranslateError", "ValueError", "ZeroDivisionError"
]))

var_pattern  = re.compile(r"\b([A-Za-z_]\w*)\s*=")
func_pattern = re.compile(r"\bfunc\s+([A-Za-z_]\w*)")


popup = None
text = None

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, s):
        if not self.widget.winfo_exists():
            return
        try:
            def _append():
                if self.widget.winfo_exists():
                    self.widget.config(state="normal")
                    self.widget.insert("end", s)
                    self.widget.see("end")
                    self.widget.config(state="disabled")
            self.widget.after(0, _append)
        except tk.TclError:
            pass
    def flush(self):
        pass
        
def collect_symbols():
    content = text.get("1.0", "end-1c")
    found = set()
    for m in var_pattern.finditer(content):
        found.add(m.group(1))
    for m in func_pattern.finditer(content):
        found.add(m.group(1))
    return list(found)


def open_editor(filepath=None):

    current_proc = None

    match_positions = []
    current_match_index = -1
    def run_script():
        nonlocal current_proc
        autosave()
        target = filepath if filepath else "script.kl"

        # im old! geheheheh
        if current_proc and current_proc.poll() is None:
            current_proc.terminate()
            
        exe = sys.executable
        if exe.endswith("pythonw.exe"):
            exe = exe.replace("pythonw.exe", "python.exe")

        current_proc = subprocess.Popen(
            [exe, "-u", os.path.join(BASE_DIR, "..", "runner", "keylang_runner.py"), target],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        output_text = show_output()
        redirector = TextRedirector(output_text)

        def pump_output():
            for line in current_proc.stdout:
                redirector.write(line)

        threading.Thread(target=pump_output, daemon=True).start()

# run keylang
# run keylang
# run keylang end
# run keylang end

    def show_output():
        output_win = tk.Toplevel(editor)
        output_win.title("Output")
        output_win.config(bg="#1e1e1e")

        output_text = tk.Text(
            output_win, wrap="word",
            bg="#1e1e1e", fg="#d4d4d4",
            font=("Consolas", 12)
        )
        output_text.pack(expand=True, fill="both")
        return output_text

    def update_line_numbers():
        line_numbers.config(state="normal")
        line_numbers.delete("1.0", "end")   # clear old numbers
        line_count = int(text.index("end-1c").split(".")[0])
        line_text = "\n".join(str(i) for i in range(1, line_count + 1))
        line_numbers.insert("1.0", line_text)
        line_numbers.config(state="disabled")


    style = ttk.Style()
    style.theme_use("default")
    style.configure("Vertical.TScrollbar",
        background="#2a2a2a",
        troughcolor="#1e1e1e",
        bordercolor="#1e1e1e",
        arrowcolor="#d4d4d4"
)

    style.map(
        "Vertical.TScrollbar",
        background=[("disabled", "#2a2a2a")],
        arrowcolor=[("disabled", "#888888")]
    )

    editor = tk.Toplevel()
    editor.title("Keylang Editor")
    editor.iconbitmap(os.path.join(BASE_DIR, "Keylang_logo.ico"))
    editor.config(bg="#1e1e1e")
    container = tk.Frame(editor)
    container.pack(side="top", fill="both", expand=True)

    global text
    text = tk.Text(
        container,
        wrap="none",
        font=("Consolas", 12),
        bg="#1e1e1e",
        fg="#d4d4d4",
        insertbackground="white",
        undo=True,
        autoseparators=True,
        maxundo=-1
    )

    line_numbers = tk.Text(
        container,
        width=4,
        padx=4,
        takefocus=0,
        border=0, 
        background="#f0f0f0",
        state="disabled"
    )

    line_numbers.config(
    background="#1e1e1e",
    fg="grey",
    font=("Consolas", 12)
    )

    line_numbers.pack(side="left", fill="y")

    text.pack(side="right", fill="both", expand=True)

    text.bind("<Control-z>", lambda e: text.edit_undo())
    text.bind("<Control-y>", lambda e: text.edit_redo())
    text.bind("<Control-Shift-Z>", lambda e: text.edit_redo())


    scrollbar = ttk.Scrollbar(container, orient="vertical", command=text.yview, style="Vertical.TScrollbar")
    scrollbar.pack(side="right", fill="y")

    def sync_scroll(first, last):
        scrollbar.set(first, last)
        line_numbers.yview_moveto(first)
    text.config(yscrollcommand=sync_scroll)

    def block_scroll(event):
        return "break"
    line_numbers.bind("<MouseWheel>", block_scroll)
    line_numbers.bind("<Button-4>", block_scroll)
    line_numbers.bind("<Button-5>", block_scroll)
    line_numbers.bind("<Shift-MouseWheel>", block_scroll)

    run_button = tk.Button(editor, text="▶ Run", bg="#2a2a2a", fg="#ffffff", activebackground="#80ef80", activeforeground="white", relief="flat", font=("Consolas", 12), borderwidth=0, command=run_script)
    run_button.pack(side="right", fill="x", padx=4, pady=4)

    find_entry = tk.Entry(editor, font=("Consolas", 12), bg="#2a2a2a", fg="white", insertbackground="white")
    find_entry.pack(side="left", fill="x", expand=True, padx=4, pady=4)

    def find_text(event=None):
        SHIFT_MASK = 0x0001
        nonlocal match_positions, current_match_index
        query = find_entry.get()
        if not hasattr(find_text, "last_query"):
            find_text.last_query = ""
        if query != find_text.last_query:
            match_positions.clear()
            current_match_index = -1
            find_text.last_query = query
        if not query:
            return
        if not match_positions:
            text.tag_remove("found", "1.0", tk.END)
            text.tag_remove("active_match", "1.0", tk.END)
            match_positions = []
            start = "1.0"
            match_len = tk.IntVar()
            start = "1.0"
            while True:
                pos = text.search(query, start, stopindex=tk.END, count=match_len, nocase=True)
                if not pos or match_len.get() == 0:
                    break
                end = f"{pos}+{match_len.get()}c"
                match_positions.append((pos, end))
                text.tag_add("found", pos, end)
                start = end

            text.tag_config("found", background="#444444")
            text.tag_config("active_match", background="#ffcc00", foreground="black")
            current_match_index = -1

        text.tag_remove("active_match", "1.0", tk.END)
        if match_positions:
            if event.state & SHIFT_MASK:
                current_match_index = (current_match_index - 1) % len(match_positions)
            else:
                current_match_index = (current_match_index + 1) % len(match_positions)
            pos, end = match_positions[current_match_index]
            text.tag_add("active_match", pos, end)
            text.see(pos)

    find_entry.bind("<KeyRelease>", find_text)

    find_button = tk.Button(editor, text="Find", bg="#2a2a2a", fg="#ffffff", activebackground="#80ef80", activeforeground="white", relief="flat", font=("Consolas", 12), borderwidth=0)
    find_button.pack(side="left", padx=4, pady=4)
    find_button.bind("<Button-1>", find_text)

# comment!!!
# yeah the setup done now
# comment!!! comment!!!
# yeah the setup done now YEAH I KNOW
    if filepath:
        text.config(undo=False)
        with open(filepath, "r") as f:
            text.insert("1.0", f.read())
        text.config(undo=True)

    # autosave
    def autosave(event=None):
        target = filepath if filepath else "script.kl"
        content = text.get("1.0", "end-1c")
        with open(target, "w") as f:
            f.write(content)

    # highlighting
   # highlighting
  # highlighting
 # highlighting
# highlighting

# keywords actually nope later
    def highlight(event=None):

# variables
        text.tag_remove("var", "1.0", tk.END)
        text.tag_config("var", foreground="#ffffff", font=("Consolas", 12, "bold"))

        lines = text.get("1.0", tk.END).splitlines()
        for i, line in enumerate(lines):
            for match in re.finditer(r"\b\w+\b", line):
                word = match.group()
                if word not in symbols:
                    col = match.start()
                    start = f"{i + 1}.{col}"
                    end = f"{i + 1}.{col + len(word)}"
                    text.tag_add("var", start, end)



# numbers
        text.tag_remove("number", "1.0", tk.END)
        text.tag_config("number", foreground="#61afef",
        font=("Consolas", 12))

        lines = text.get("1.0", tk.END).splitlines()
        for i, line in enumerate(lines):
            for match in re.finditer(r"\b\d+(\.\d+)?\b", line):
                start = f"{i + 1}.{match.start()}"
                end   = f"{i + 1}.{match.end()}"
                text.tag_add("number", start, end)


# real keywords
        text.config(undo=False)

        text.tag_remove("keyword", "1.0", tk.END)

        for f in keywords:
            start = "1.0"
            while True:
                if f == "'s":
                    pos = text.search("'s", start, stopindex=tk.END)
                else:
                    pos = text.search(rf"\m{f}\M", start, stopindex=tk.END, regexp=True)
                if not pos:
                    break
                end = f"{pos}+{len(f)}c"
                text.tag_add("keyword", pos, end)
                start = end
        text.tag_config("keyword", foreground="#ff5555", font=("Consolas", 12, "bold"))

        for kw in symbols:
            if kw in keywords:
                continue
            start = "1.0"
            while True:
                pos = text.search(rf"\m{kw}\M", start, stopindex=tk.END, regexp=True)

                if not pos:
                    break
                end = f"{pos}+{len(kw)}c"
                text.tag_add("keywordscam", pos, end)
                start = end
        text.tag_config("keywordscam", foreground="#c586c0", font=("Consolas", 12))



# functions
        text.tag_remove("function", "1.0", tk.END)
        text.tag_config("function", foreground="#c586c0", font=("Consolas", 12,))

        lines = text.get("1.0", tk.END).splitlines()
        for i, line in enumerate(lines):
            for match in re.finditer(r"\b\w+(?=\s*\()"
, line):
                word = match.group()
                col = match.start()
                start = f"{i + 1}.{col}"
                end = f"{i + 1}.{col + len(word)}"
                text.tag_add("function", start, end)



# function names
        text.tag_remove("name", "1.0", tk.END)
        text.tag_config("name", foreground="#93c47d",
        font=("Consolas", 12,))

        lines = text.get("1.0", tk.END).splitlines()
        for i, line in enumerate(lines):
            curly_index = line.find("{")
            if curly_index != -1:
                before = line[:curly_index]
                cleaned = re.sub(r"\(.*?\)", "", before)
                cleaned = re.sub(r"[^\w\s]", " ", cleaned).strip()
                match = re.search(r"\b\w+$", cleaned)

                match = re.search(r"\b\w+$", cleaned)
                if match:
                    word = match.group()
                    if word == "s":
                        continue
                    col = line.find(word)
                    start = f"{i + 1}.{col}"
                    end = f"{i + 1}.{col + len(word)}"
                    text.tag_add("name", start, end)
                    


# embed lua
        text.tag_remove("embed_lua", "1.0", tk.END)
        text.tag_config("embed_lua", foreground="#1E90FF", font=("Fira Mono", 12,))

        for match in re.finditer(r"\bembed_lua\b", text.get("1.0", tk.END)):
            start = f"1.0+{match.start()}c"
            end   = f"1.0+{match.end()}c"
            text.tag_add("embed_lua", start, end)    


# strings
        text.tag_remove("string", "1.0", tk.END)
        text.tag_config("string", foreground="#ffee8c", font=("Consolas", 12, "italic"))

        code = text.get("1.0", tk.END)

        for match in re.finditer(r'(["\'])(.*?)(\1)', code):
            inner = match.group(2)
            inner_start = match.start(2)
            after = code[match.end():]
            
            if after.startswith("s"):
                continue

            last = 0
            for brace_match in re.finditer(r'(?<!\{)\{[^{}]*\}(?!\})', inner):
                brace_start = brace_match.start()
                brace_end = brace_match.end()

                if brace_start > last:
                    gap_start = inner_start + last
                    gap_end = inner_start + brace_start
                    text.tag_add("string", f"1.0+{gap_start}c", f"1.0+{gap_end}c")

                last = brace_end

            text.tag_add("string", f"1.0+{match.start()}c", f"1.0+{match.start(2)}c")

            text.tag_add("string", f"1.0+{match.start(2) + len(inner)}c", f"1.0+{match.end()}c")

            if last < len(inner):
                final_start = inner_start + last
                final_end = inner_start + len(inner)
                text.tag_add("string", f"1.0+{final_start}c", f"1.0+{final_end}c")



# comments
        text.tag_remove("comment", "1.0", tk.END)
        text.tag_config("comment", foreground="grey", font=("Consolas", 12,))

        lines = text.get("1.0", tk.END).splitlines()
        for i, line in enumerate(lines):
            string_spans = []
            for match in re.finditer(r'(["\'])(.*?)(\1)', line):
                string_spans.append((match.start(), match.end()))
            for match in re.finditer(r"#.*"
, line):
                word = match.group()
                col = match.start()
                inside_string = any(start <= col < end for start, end in
        string_spans)
                if inside_string == True:
                    continue
                start = f"{i + 1}.{col}"
                end = f"{i + 1}.{col + len(word)}"
                text.tag_add("comment", start, end)



# lua contents
        text.tag_remove("contents", "1.0", tk.END)
        text.tag_config("contents", foreground="white", font=("Fira Mono", 12,))
        
        start = line.find("{")
        end = line.find("}", start)

        code = text.get("1.0", tk.END)

        for match in re.finditer(r"\bembed_lua\s*\{[^{}]*\}", code):
            line_start = code.rfind("\n", 0, match.start()) + 1
            line = code[line_start:match.start()]
            if re.match(r"^\s*#", line):
                continue

            full_start = match.start()
            full_end = match.end()

            real_start = code.find("{", full_start, full_end)
            real_end = code.find("}", real_start, full_end)

            text.tag_add("contents", f"1.0+{real_start}c", f"1.0+{real_end}c")


        text.config(undo=True)


    def get_current_token():
        cursor_index = text.index("insert")
        line, col = map(int, cursor_index.split("."))
        line_text = text.get(f"{line}.0", f"{line}.end")
        prefix = re.findall(r"[\w']+$", line_text[:col])
        return prefix[0] if prefix else ""

    def show_popup(matches):
        global popup
        if popup:
           popup.destroy()

        popup = tk.Toplevel(editor)
        popup.wm_overrideredirect(True)
        popup.config(bg="#2a2a2a")
        bbox = text.bbox("insert")
        if bbox:
            x, y, width, height = bbox
            x += text.winfo_rootx()
            y += text.winfo_rooty() + height
            popup.geometry(f"+{x}+{y}")

        frame = tk.Frame(popup, bg="#3a3a3a", bd=3)
        frame.pack()

        lb = tk.Listbox(
        frame,
            bg="#2a2a2a",
            fg="white",
            font=("Consolas", 12),
            borderwidth=0,
            highlightthickness=0
        )
        lb.pack()
        for m in matches:
            lb.insert("end", m)
        lb.selection_set(0)
        lb.activate(0)
        lb.pack()
        lb.bind("<Return>", lambda e: select(lb.get("active")))
        lb.bind("<Tab>", lambda e: select(lb.get("active")))
        lb.bind("<Double-Button-1>", lambda e: select(lb.get("active")))


    def hide_popup():
        global popup
        if popup:
            popup.destroy()
            popup = None

# important
# important
# important
    def on_key(event=None):
        autosave()
        highlight()
        update_line_numbers()

        dynamic_symbols = collect_symbols()
        better_symbols = list(symbols)
        better_symbols.extend(dynamic_symbols)
        
        token = get_current_token()
        if token:
            if token in better_symbols:
                hide_popup()
                return
            matches = [s for s in better_symbols if s.startswith(token) and s != token]
            if matches:
                show_popup(matches)
            else:
                hide_popup()
        else:
            hide_popup()
    highlight()
    update_line_numbers()
# important
# important
# important

    def select(choice):
        token = get_current_token()
        if token:
            text.delete(f"insert-{len(token)}c", "insert")
        text.insert("insert", choice)
        hide_popup()

    def confirm_top_suggestion(event=None):
        global popup
        if popup and popup.winfo_exists():
            # descend into the frame to get the listbox
            frame = popup.winfo_children()[0]
            lb = frame.winfo_children()[0]
            if lb.size() > 0:
                select(lb.get("active"))
            return "break"

    def double_pairs(event):
        pairs = {
            "(": ")",
            "[": "]",
            "{": "}",
            "\"": "\"",
            #"'": "'"
        }
        char = event.char
        if char in pairs:
            text.insert("insert", char + pairs[char])
            text.mark_set("insert", "insert-1c")
            return "break"

# shortcuts
 # shortcuts
  # shortcuts
   # shortcuts
    # shortcuts

    def comment_out(event=None):
        if text.tag_ranges("sel"):
            start_line = int(text.index("sel.first").split(".")[0])
            end_line   = int(text.index("sel.last").split(".")[0])
            for line_num in range(start_line, end_line + 1):
                line_start = f"{line_num}.0"
                if text.get(line_start, f"{line_start}+1c") == "#":
                    text.delete(line_start, f"{line_start}+1c")
                else:
                    text.insert(line_start, "#")
        else:
            line_start = text.index("insert linestart")
            if text.get(line_start, f"{line_start}+1c") == "#":
                text.delete(line_start, f"{line_start}+1c")
            else:
                text.insert(line_start, "#")
        return "break"


    def select_line(event=None):
        start = text.index("insert linestart")
        end = text.index("insert lineend +1c")
        text.tag_remove("sel", "1.0", "end")
        text.tag_add("sel", start, end)
        return "break"

    def line_up(event=None):
        start = text.index("insert linestart")
        end = text.index("insert lineend +1c")
        line_text = text.get(start, end)
        text.delete(start, end)
        target = text.index(f"{start} -1line linestart")
        text.insert(target, line_text)
        text.mark_set("insert", target)
        return "break"
    def line_down(event=None):
        start = text.index("insert linestart")
        end = text.index("insert lineend +1c")
        if text.compare(end, "==", "end-1c"):
            return "break"
        line_text = text.get(start, end)
        text.delete(start, end)
        target = text.index(f"{start} +1line linestart")
        text.insert(target, line_text)
        text.mark_set("insert", target)
        return "break"

    def duplicate_line(event=None):
        start = text.index("insert linestart")
        end = text.index("insert lineend +1c")
        line_text = text.get(start, end)
        text.insert(end, line_text)
        return "break"

    def select_word(event=None):
        text.mark_set("insert", "insert -1c")
        start = text.index("insert wordstart")
        end = text.index("insert wordend")
        text.tag_remove("sel", "1.0", "end")
        text.tag_add("sel", start, end)
        return "break"

    def tabtabtab(event=None):
        if text.tag_ranges("sel"):
            start = text.index("sel.first linestart")
            end = text.index("sel.last lineend")
            line = start
            while text.compare(line, "<=", end):
                text.insert(line, "\t")
                line = text.index(f"{line}+1line")
            return "break"
        else:
            text.insert("insert", "\t")
            return "break"
    def untabuntabuntab(event=None):
        if text.tag_ranges("sel"):
            start = text.index("sel.first linestart")
            end = text.index("sel.last lineend")
            line = start
            while text.compare(line, "<=", end):
                if text.get(line, f"{line}+1c") == "\t":
                    text.delete(line, f"{line}+1c")
                elif text.get(line, f"{line}+4c") == "    ": text.delete(line, f"{line}+4c")
                line = text.index(f"{line}+1line")
            return "break"

    def focus_find_entry(event=None):
        find_entry.focus_set()
        return "break"


    # text.bind("<Tab>", confirm_top_suggestion)
    text.bind("<Return>", confirm_top_suggestion, add="+")

    text.unbind_class("Text", "<Control-k>")
    text.bind("<Control-k>", comment_out)
    text.bind("<Control-slash>", comment_out)
    text.bind("<Control-l>", select_line)
    text.bind("<Alt-Up>", line_up)
    text.bind("<Alt-Down>", line_down)
    text.bind("<Control-Shift-D>", duplicate_line)
    text.unbind_class("Text", "<Control-d>")
    text.bind("<Control-d>", select_word)
    text.bind("<Tab>", tabtabtab)
    text.bind("<Shift-Tab>", untabuntabuntab)
    text.bind("<Control-f>", focus_find_entry)

    text.bind("<KeyRelease>", on_key)
    text.bind("<KeyPress>", double_pairs)
