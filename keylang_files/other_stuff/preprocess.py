def preprocess_source(src: str) -> str:
    import re, sys, builtins
    
    # wait_count = len(re.findall(r'^\s*wait(?:\([^)]*\))?\s*$', src, re.MULTILINE))
    # src = src + "\nwait_end" * wait_count

    # .\keylang.ps1 .\test.kl

    indent = 0
    prev_indent = 0
    
    block_stack = []
    current_func = None

    once_id = 0
    loop_id = 0
    
    output_lines = []
    
    declared2 = []
    
    var_pattern = re.compile(r"\b([A-Za-z_]\w*)\s*=")
    keyword_pattern = re.compile(r"\b([A-Za-z_]\w*)\s*=")
    
    keywords = {}
    
    async_funcs = []
        
    # in_string = False

    output_lines.append("__once_done = set()")
    output_lines.append("import asyncio")
    output_lines.append("import types")
    output_lines.append("import random")
    output_lines.append("import threading")
    output_lines.append("import subprocess")
    output_lines.append("import json")
    import json
    output_lines.append("import os")
    
    output_lines.append("key_down = {}")
    output_lines.append("from pynput import keyboard")
    output_lines.append("for k in keyboard.Key:")
    output_lines.append("\tkey_down[k.name] = False")
    output_lines.append("chars = \"abcdefghijklmnopqrstuvwxyz0123456789`-=[]\\\\;',./\"")
    output_lines.append("for c in chars:")
    output_lines.append("\tkey_down[c] = False")
    
    # output_lines.append("from lupa import LuaRuntime")
    # output_lines.append("lua = LuaRuntime(unpack_returned_tuples=True)")

    output_lines.append("def __on_press(key):")
    output_lines.append("\ttry:")
    output_lines.append("\t\tname = key.char")
    output_lines.append("\texcept AttributeError:")
    output_lines.append("\t\tname = key.name")
    output_lines.append("\tif name in key_down:")
    output_lines.append("\t\tkey_down[name] = True")

    output_lines.append("def __on_release(key):")
    output_lines.append("\ttry:")
    output_lines.append("\t\tname = key.char")
    output_lines.append("\texcept AttributeError:")
    output_lines.append("\t\tname = key.name")
    output_lines.append("\tif name in key_down:")
    output_lines.append("\t\tkey_down[name] = False")

    output_lines.append("_listener = keyboard.Listener(on_press=__on_press, on_release=__on_release)")
    output_lines.append("_listener.start()")
    # output_lines.append("from pynput.keyboard import Key")
        
    output_lines.append("import time")
    output_lines.append("__last_time = time.time()")

    output_lines.append("def get_looprate():")
    output_lines.append("\tglobal __last_time")
    output_lines.append("\tnow = time.time()")
    output_lines.append("\tdelta = now - __last_time")
    output_lines.append("\t__last_time = now")
    output_lines.append("\treturn 1.0 / delta if delta > 0 else 0")

    output_lines.append("def __print_nones(locals_dict):")
    output_lines.append("\tfor name, value in locals_dict.items():")
    output_lines.append("\t\tif value is None:")
    output_lines.append("\t\t\tprint(f\"{name} = None\")")

    output_lines.append("def __print_all(locals_dict):")
    output_lines.append("\tfor name, value in locals_dict.items():")
    output_lines.append("\t\tif value:")
    output_lines.append("\t\t\tprint(f\"{name} = {value!r}\")")

    output_lines.append("def __print_vars(locals_dict):")
    output_lines.append("\tfor name, value in locals_dict.items():")
    output_lines.append("\t\tif name.startswith('__'):")
    output_lines.append("\t\t\tcontinue")
    output_lines.append("\t\tif isinstance(value, types.FunctionType):")
    output_lines.append("\t\t\tcontinue")
    output_lines.append("\t\tif name == 'asyncio' or name == 'types':")
    output_lines.append("\t\t\tcontinue")
    output_lines.append("\t\tprint(f\"{name} = {value!r}\")")
    
    def collect_symbols(content):
        var_decl_pattern = re.compile(r'^\s*var\s+([A-Za-z_]\w*)')
        globals_found = set()
        for line in content.splitlines():
            m = var_decl_pattern.match(line)
            if m:
                globals_found.add(m.group(1))
        # print(globals_found)
        return list(globals_found)
        
    def collect_symbols2(content):
        keyword_decl_pattern = re.compile(r'^\s*keyword\s+([A-Za-z_]\w*)')
        globals_found2 = set()
        for line in content.splitlines():
            m = keyword_decl_pattern.match(line)
            if m:
                globals_found2.add(m.group(1))
        # print(globals_found2)
        return list(globals_found2)


    # def undeclared(line: str, declared: set):
        # assign_pattern = re.compile(r'^\s*([A-Za-z_]\w*)\s*=')

        # m = assign_pattern.match(line)
        # if m:
            # varname = m.group(1)
            # if varname not in declared2:
                # raise SyntaxError(f"Keylang error:'{varname}' not declared in current scope")
                
    # declared = collect_symbols(src)
    # undeclared(src, declared)

    globals_list = collect_symbols(src)

    def preprocess(line: str):
        for m in re.finditer(r"'([^']*)'", line):
            inner = m.group(1)
            end_index = m.end()
            if end_index < len(line) and line[end_index] == "s":
                continue
            if inner and inner.startswith("s") and not (block_stack and block_stack[-1] == "python"):
                sys.stderr.write("KeylangError: Strings that start with 's', specifically strings with single quotes, are not supported yet ok don't ask why it's so specific\nTry using double quotes instead\n")
                sys.exit(1)
        return line


    def replace_accessor(line: str) -> str:
        parts = re.split(r'(".*?"|\'(?!s\s).*?\')', line)
        out = []
        for p in parts:
            if not p:
                continue
            if (p.startswith('"') and p.endswith('"')) or (p.startswith("'") and p.endswith("'")):
                out.append(p)
            else:
                out.append(re.sub(r"'s\s+", ".", p))
        return "".join(out)
        
    # def split_strings(line):
        # parts = re.split(r'(".*?"|\'.*?\')', line)
        # out = []
        # for p in parts:
            # if not p:
                # continue
            # if (p.startswith('"') and p.endswith('"')) or (p.startswith("'") and p.endswith("'")):
                # out.append(p)
                # in_string = True
            # else:
                # out.append(p)
                # in_string = False
        # return "".join(out)

    def replace_random(m):
        arg = m.group(1).strip()
        parts = [p.strip() for p in arg.split(",")]

        if len(parts) == 1:
            var = parts[0]
            return (f"random.choice({var} if not isinstance({var}, dict) "
                    f"else list({var}.values()))")
        return f"random.choice([{arg}])"

    def strip_comment(line):
        in_string = False
        quote_char = None
        escape = False
        for i, ch in enumerate(line):
            if in_string:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == quote_char:
                    in_string = False
                    quote_char = None
            else:
                if ch in ("'", '"'):
                    in_string = True
                    quote_char = ch
                elif ch == "#":
                    return line[:i].rstrip()
        return line
        
    for raw in src.splitlines():
        
        line = raw.rstrip()
        
        # ignore if strings
        # ignore if strings
        stripped = re.sub(r'(".*?"|\'.*?\')', "", line)
        # ignore if strings
        # ignore if strings
        
        if line.lstrip().startswith("#"):
            output_lines.append("\t" * indent + line.lstrip())
            continue
        else:
            line = strip_comment(line)
        
        m_embed_lua = re.match(r'\s*embed_lua\s*{', line)
        if m_embed_lua:
            lua_block = []
            block_stack.append("lua")
            indent += 1
            continue
        
        m_python = re.match(r'\s*python\s*{', line)
        if m_python:
            python_block = []
            block_stack.append("python")
            # indent += 1
            continue

    # keyword stripper!!!
        m_key = re.match(r'^\s*keyword\s+([A-Za-z_]\w*)\s*=\s*(.+)$', line)
        if m_key:
            # global keywords
            name = m_key.group(1)
            value = m_key.group(2)
            keywords[name] = value
            continue
            
        for key, val in keywords.items():
            line = re.sub(rf'\b{key}\b', val, line)
            
    # lua embeder
        if block_stack and block_stack[-1] == "lua":
            if "}" in stripped:
                lua_block.append(line.split("}")[0])
                lua_code = "\n".join(lua_block)
                escaped_lua = json.dumps(lua_code)
                output_lines.append("\t" * (indent - 1) + f"__lua_code = {escaped_lua}")
                # output_lines.append("\t" * (indent - 1) + "lua.execute(__lua_code)")
                output_lines.append("\t" * (indent - 1) + "with open('temp_embed.lua', 'w') as __f:")
                output_lines.append("\t" * indent + "__f.write(__lua_code)")
                output_lines.append("\t" * (indent - 1) + "lua_dir = os.environ.get('KEYLANG_LUA_DIR', '')")
                output_lines.append("\t" * (indent - 1) + "lua_exe = os.path.join(lua_dir, 'luajit')")
                output_lines.append("\t" * (indent - 1) + "subprocess.run([lua_exe, 'temp_embed.lua'])")
                output_lines.append("\t" * (indent - 1) + "os.remove('temp_embed.lua')")
                block_stack.pop()
                indent -= 1
                continue
            else:
                lua_block.append(line)
                continue
        
    # python embedder
        if block_stack and block_stack[-1] == "python":
            if "}" in stripped:
                block_stack.pop()
                # indent -= 1

                # Emit the python code
                for py_line in python_block:
                    output_lines.append("\t" * indent + py_line)

                continue
            else:
                python_block.append(line)
                continue
        
        if "~" in stripped:
            line = line.replace("~", "_____")
            
        if "do" in stripped:
            line = re.sub(r'\bdo\b', '{', line)
        if "end" in stripped:
            line = re.sub(r'\bend\b', '}', line)
            stripped = re.sub(r'(".*?"|\'.*?\')', "", line)
        
        # var_thingy = re.compile(r'^\s*var\b')
        # if var_thingy.match(raw):
        if re.match(r'^\s*var\s+', line) or re.match(r'^\s*keyword\s+', line):
            name = line.split()[1]
            if name in declared2 and not (block_stack and block_stack[-1] == "python"):
                raise SyntaxError(f"Keylang error:'{name}' already declared in current scope")
            declared2.append(name)
            prev_indent = indent
            # print(f'[[[{declared2}]]]')
            
        if indent < prev_indent:
            if declared2:
                declared2.pop()
                
        if not (block_stack and block_stack[-1] == "lua") and not (block_stack and block_stack[-1] == "python"):
            assign_pattern = re.compile(r'^\s*([A-Za-z_]\w*)\s*=')
            m = assign_pattern.match(line)
            if m:
                varname = m.group(1)
                if varname not in declared2:
                    raise SyntaxError(f"Keylang error:'{varname}' not declared in current scope")
                    
        preprocess(line)
            
        line = replace_accessor(line)

        if not line.strip():
            output_lines.append("")
            continue

        # stripped = line.lstrip()

        # if line.lstrip().startswith("#"):
            # output_lines.append("\t" * indent + line.lstrip())
            # continue

        # if has_inline_comment(line):
            # sys.stderr.write("KeylangError: Inline comments are not supported in the current version. That sucks\n")
            # sys.exit(1)

    # re searches
    # re searches
    
    
        if not (block_stack and block_stack[-1] == "python"):
        # [] error
            if re.search(r'=\s*\[', line):
                sys.stderr.write("KeylangError: '[' and ']' are replaced with 'array()' btw >:)\n")
                sys.exit(1)
        # {} error
            if re.search(r'=\s*\{', stripped):
                sys.stderr.write("KeylangError: '{' and '}' are replaced with 'dict()' btw >:)\n")
                sys.exit(1)
            if re.search(r':\s*$', line):
                sys.stderr.write("KeylangError: ':' is replaced with curly brackets >:), use '{' and '}'\n")
                sys.exit(1)

        m = re.match(r'\s*loop\((.+)\)\s*{', line)
        if m:
            count = m.group(1).strip()
            loop_id += 1
            varname = f"__i{loop_id}"
            output_lines.append("\t" * indent + f"for {varname} in range(int({count})):")
            # output_lines.append("\t" * indent + f"for __i in range(int({count})):")
            indent += 1
            block_stack.append(None)
            continue

        m2 = re.match(r'\s*once\s*{', line)
        if m2:
            once_id += 1
            oid = once_id
            output_lines.append("\t" * indent + f"if {oid} not in __once_done:")
            indent += 1
            output_lines.append("\t" * indent + f"__once_done.add({oid})")
            block_stack.append(oid)
            continue

        m3 = re.match(r'\s*wait\((.+)\)\s*$', line)
        if m3:
            arg = m3.group(1).strip()
            output_lines.append("\t" * indent + f"time.sleep({arg})")
            continue
            
        # arg real wait function
        m_wait_p = re.match(r'^\s*wait_____thread\s*\((.*?)\)\s*(\{)?\s*$', line)
        if m_wait_p:
            arg = m_wait_p.group(1).strip()
            func_name = f"__wait_{len(output_lines)}"
            output_lines.append("\t" * indent + f"def {func_name}():")
            block_stack.append(("wait_p", func_name, indent, arg))
            indent += 1
            continue
            
        # real wait function
        m_wait = re.match(r'^\s*wait_____thread\s*(\{)?\s*$', line)
        if m_wait:
            func_name = f"__wait_{len(output_lines)}"
            output_lines.append("\t" * indent + f"def {func_name}():")
            # indent -= 1
            # output_lines.append("\t" * indent + f"threading.Timer(1, {func_name}).start()")
            block_stack.append(("wait", func_name, indent))
            indent += 1
            # output_lines.append("\t" * indent + "print('yay')")
            continue
            
        # nothing is real
        m_wait_u = re.match(r'^\s*wait_____until\s*\((.+)\)\s*$', line)
        if m_wait_u:
            arg = m_wait_u.group(1).strip()
            output_lines.append("\t" * indent + f"while not {arg}:")
            indent += 1
            output_lines.append("\t" * indent + f"time.sleep(0.01)")
            indent -= 1
            continue
            
        m33 = re.match(r'\s*(?:await\s+)?wait_____async\((.+)\)\s*$', line)
        if m33:
            arg = m33.group(1).strip()
            output_lines.append("\t" * indent + f"await asyncio.sleep({arg})")
            continue
            
    # var stripper!!!
        if re.match(r'^\s*var\s+', line):
            # print("OH YEAH IT RAN")
            line = line.replace("var ", "", 1)

        m4 = re.search(r'\barray\((.*?)\)', line)
        if m4:
            line = re.sub(r'\barray\((.*?)\)', r'[\1]', line)

        m5 = re.search(r'\bdict\((.*?)\)', line)
        if m5:
            line = re.sub(r'\bdict\((.*?)\)', r'{\1}', line)
            line = re.sub(r'({.*?})(.*)', 
                lambda m: re.sub(r'([\'"].+?[\'"]|\w+)\s*=\s*', r'\1: ', m.group(1)) + m.group(2),
                      line)
            output_lines.append("\t" * indent + line.lstrip())
            

        m_private = re.match(r"\s*private\s+func\s+(.+)", line)
        if m_private:
            header = m_private.group(1).rstrip("{").strip()
            if "(" not in header and ")" not in header:
                header += "()"
            func_name, _, params = header.partition("(")
            func_name = func_name.strip()
            params = params.rstrip(")")
            if not params.strip():
                params = ""
            else:
                params = ", " + params.strip()
            current_func = func_name
            output_lines.append("\t" * indent + f"def __{func_name}({params}):")
            indent += 1
            block_stack.append(None)
            continue

        m_protected = re.match(r"\s*protected\s+func\s+(.+)", line)
        if m_protected:
            header = m_protected.group(1).rstrip("{").strip()
            if "(" not in header and ")" not in header:
                header += "()"
            func_name, _, params = header.partition("(")
            func_name = func_name.strip()
            params = params.rstrip(")")
            if not params.strip():
                params = ""
            else:
                params = ", " + params.strip()
            current_func = func_name
            output_lines.append("\t" * indent + f"def _{func_name}({params}):")
            indent += 1
            block_stack.append(None)
            continue

        m_spawn = re.match(r'\s*spawn\s+(\w+)(?:\((.*?)\))?\s*$', line)
        if m_spawn:
            func = m_spawn.group(1)
            args = (m_spawn.group(2) or "").strip()
            if args:
                output_lines.append("\t" * indent + f"threading.Thread(target={func}, args=({args},), daemon=True).start()")
            else:
                output_lines.append("\t" * indent + f"threading.Thread(target={func}, daemon=True).start()")
            continue

            
        m_looprate = re.search(r'\blooprate\b', stripped)
        if m_looprate:
            line = re.sub(r'\blooprate\b', 'get_looprate()', line)
            # continue
            
    # when key(bleh some key) # when comes later
        # m_keypress = re.match(r'\s*key\((.+)\)\s*{', line)
        # if m_keypress:
            # unsafe_arg = m_keypress.group(1).strip()
            # arg = unsafe_arg.replace(".", "_")
            # func_name = f"__key_event_{arg}"
            # output_lines.append("\t" * indent + f"def {func_name}(key):")
            # indent += 1
            # if unsafe_arg.startswith("Key."):
                # output_lines.append("\t" * indent + f"if key == {unsafe_arg}:")
            # else:
                # output_lines.append("\t" * indent + f"if hasattr(key, 'char') and key.char == '{unsafe_arg}':")
            # indent += 1
            # block_stack.append(("key_event", func_name, indent - 2))
            # continue
            
        # if line.strip() == "key":
            # output_lines.append("\t" * indent + "async def main():")
            # indent += 1
            # output_lines.append("\t" * indent + "await asyncio.sleep(1)")
            # indent -= 1
            # output_lines.append("\t" * indent + "asyncio.run(main())")
            # continue
        m_keypress = re.match(r'\s*if\s+key\s*\(\s*(.+?)\s*\)\s*\{', line)
        if m_keypress:
            keyname = m_keypress.group(1).strip()
            if keyname.startswith("Key."):
                keyname = keyname[4:]

            output_lines.append("\t" * indent + f"if key_down['{keyname}']:")
            indent += 1
            block_stack.append(None)
            continue
            
        m_when = re.match(r'\s*when\s*\((.+?)\)\s+(.+?)\s*\{', line)
        m_when2 = re.match(r'\s*when\s+([^\{#]+?)\s*\{', line)
        m_once_when = re.match(r'\s*when_____once\s*\((.+?)\)\s+(.+?)\s*\{', line)
        m_once_when2 = re.match(r'\s*when_____once\s+([^\{#]+?)\s*\{', line)
        if m_when or m_when2 or m_once_when or m_once_when2:
            if m_when:
                interval = m_when.group(1).strip()
                condition = m_when.group(2).strip()
            elif m_when2:
                interval = "0"
                condition = m_when2.group(1).strip()
            elif m_once_when:
                interval = m_once_when.group(1).strip()
                condition = m_once_when.group(2).strip()
            elif m_once_when2:
                interval = "0"
                condition = m_once_when2.group(1).strip()
            func_name = f"__when_{len(output_lines)}"
            
            m_keycond = re.match(r'key\s*\(\s*(.+?)\s*\)', condition)
            if m_keycond:
                keyname = m_keycond.group(1).strip()
                if keyname.startswith("Key."):
                    keyname = keyname[4:]
                condition = f"key_down['{keyname}']"
            # output_lines.append("\t" * indent + f"async def {func_name}():")
            # indent += 1
            # output_lines.append("\t" * indent + "while True:")
            # indent += 1
            # output_lines.append("\t" * indent + f"await asyncio.sleep({interval})")
            # output_lines.append("\t" * indent + f"if {condition}:")
            # indent += 1
            # if m_once_when or m_once_when2:
                # block_stack.append(("once_when", func_name, indent))
            # else:
                # block_stack.append(("when", func_name, indent))
            # continue  
            output_lines.append("\t" * indent + f"def {func_name}():")
            indent += 1
            output_lines.append("\t" * indent + f"if {condition}:")
            indent += 1
            if m_once_when or m_once_when2:
                block_stack.append(("once_when", func_name, indent))
            else:
                block_stack.append(("when", func_name, indent))
            # output_lines.append("\t" * indent + "print('yay')")
            # indent += 1 + 2
            continue


    # error 'random.'
        if re.search(r'\brandom\.', line):
            sys.stderr.write("KeylangError: 'random.something' is simply just 'random()' or 'random_range()' btw >:)\n")
            sys.exit(1)

        line = re.sub(r'\brandom\s*\((.*?)\)', replace_random, line)

        line = re.sub(
            r'\brandom_range\s*\((.*?)\)',
            lambda m: f"random.randint({m.group(1).strip()})",
            line
        )

    # end of re searches
    # end of re searches


        if line.strip().startswith("def "):
            sys.stderr.write("KeylangError: 'def' is replaced with 'func' btw >:)\n")
            sys.exit(1)
            
            

    # functions
        m_func = re.match(r'^\s*((?:\w+\s+)*)func\s+(\w+)', line)
        m_async_func = re.match(r'^\s*async\s+func\s+(\w+)', line)
        if m_func:
            func_name = m_func.group(2)
            # if func_name == "main":
                # sys.stderr.write("KeylangError: 'main' is already used for the weird async stuff, use a different name >:)\n")
                # sys.exit(1)
            if m_async_func:
                async_funcs.append(func_name)
            modifiers = (m_func.group(1) or "").strip()
            idx = line.index("func") + len("func")
            header = line[idx:].rstrip("{").strip()
            if "(" not in header and ")" not in header:
                header += "()"
            name, _, params = header.partition("(")
            params = params.rstrip(")")
            if indent > 0:
                params = "" if not params.strip() else "self, " + params.strip()
            prefix = (modifiers + " ") if modifiers else ""
            output_lines.append("\t" * indent + f"{prefix}def {func_name}({params}):")
            indent += 1
            for g in declared2:
                output_lines.append("\t" * indent + f"global {g}")
            block_stack.append(None)
            continue


    # loop function
        if line.strip() == "loop {" or line.strip() == "loop{":
            output_lines.append("\t" * indent + "while True:")
            indent += 1
            block_stack.append(None)
            continue
            
            

    # once function
        # if line.strip() == "once {":
            # once_id += 1
            # oid = once_id
            # flag_name = f"__once_flag_{once_id}"
            # output_lines.append("\t" * indent + f"{flag_name} = True")
            # output_lines.append("\t" * indent + f"if {flag_name}:")
            # output_lines.append("\t" * indent + f"if {oid} not in __once_done:")
            # indent += 1
            # output_lines.append("\t" * indent + f"{flag_name} = False")
            # block_stack.append(oid)
            # block_stack.append(None)
            # continue
                

        if line.endswith("{") and not (block_stack and block_stack[-1] == "lua") and not (block_stack and block_stack[-1] == "python"):
            opener = line[:-1].strip()
            output_lines.append("\t" * indent + opener + ":")
            indent += 1
            block_stack.append(None)
            continue
            
            
            
    # keyboard input detector
        # placeholder


    # } closer
        if "}" in stripped and not (block_stack and block_stack[-1] == "lua"):
            parts = line.split("}")
            for i, part in enumerate(parts):
                if part.strip():
                    output_lines.append("\t" * indent + part.strip())
                if i < len(parts) - 1:
                    if block_stack:
                        top = block_stack[-1]
                        if top is None:
                            block_stack.pop()
                        elif isinstance(top, tuple) and top[0] == "when":
                            _, func_name, base_indent = block_stack.pop()
                            # indent = base_indent - 3
                            indent -= 1
                            output_lines.append("\t" * indent + f"threading.Timer({interval}, {func_name}).start()")
                            indent -= 1
                            # output_lines.append("\t" * indent + f"{func_name}()")
                            output_lines.append("\t" * indent + f"threading.Thread(target={func_name}, daemon=True).start()" )
                            continue
                        elif isinstance(top, tuple) and top[0] == "once_when":
                            _, func_name, base_indent = block_stack.pop()
                            output_lines.append("\t" * indent + "return")
                            # indent = base_indent - 3
                            indent -= 1
                            output_lines.append("\t" * indent + f"threading.Timer({interval}, {func_name}).start()")
                            indent -= 1
                            # output_lines.append("\t" * indent + f"{func_name}()")
                            output_lines.append("\t" * indent + f"threading.Thread(target={func_name}, daemon=True).start()" )
                            continue
                        elif isinstance(top, tuple) and top[0] == "wait":
                            _, func_name, base_indent = block_stack.pop()
                            indent -= 1
                            output_lines.append("\t" * indent + f"threading.Timer(1, {func_name}).start()")
                            # output_lines.append("\t" * indent + "time.sleep(1)")
                            # block_stack.append(("wait", func_name, indent))
                            # output_lines.append("\t" * indent + f"{func_name}()")
                            continue
                        elif isinstance(top, tuple) and top[0] == "wait_p":
                            _, func_name, base_indent, arg = block_stack.pop()
                            indent -= 1
                            output_lines.append("\t" * indent + f"threading.Timer({arg}, {func_name}).start()")
                            continue
                    indent = max(0, indent - 1)
            # if line.strip() == "}":
                # if block_stack and isinstance(block_stack[-1], tuple) and block_stack[-1][0] == "key_event":
                    # _, func_name, base_indent = block_stack.pop()
                    # indent = base_indent
                    # output_lines.append("\t" * indent + f"_listener = keyboard.Listener(on_press={func_name})")
                    # output_lines.append("\t" * indent + "_listener.start()")
            continue

        if "wait_end" in stripped and not (block_stack and block_stack[-1] == "lua"):
            parts = line.split("wait_end")
            for i, part in enumerate(parts):
                if part.strip():
                    output_lines.append("\t" * indent + part.strip())
                if i < len(parts) - 1:
                    if block_stack:
                        top = block_stack[-1]
                        if top is None:
                            block_stack.pop()
                        elif isinstance(top, tuple) and top[0] == "wait":
                            _, func_name, base_indent = block_stack.pop()
                            indent -= 1
                            output_lines.append("\t" * indent + f"threading.Timer(1, {func_name}).start()")
                            # output_lines.append("\t" * indent + "time.sleep(1)")
                            # block_stack.append(("wait", func_name, indent))
                            # output_lines.append("\t" * indent + f"{func_name}()")
                            continue
                        elif isinstance(top, tuple) and top[0] == "wait_p":
                            _, func_name, base_indent, arg = block_stack.pop()
                            indent -= 1
                            output_lines.append("\t" * indent + f"threading.Timer({arg}, {func_name}).start()")
                            continue
                    indent = max(0, indent - 1)
            continue

    # wait function
        if line.strip() == "wait":
            # output_lines.append("\t" * indent + "async def main():")
            # indent += 1
            # output_lines.append("\t" * indent + "await asyncio.sleep(1)")
            # indent -= 1
            # output_lines.append("\t" * indent + "asyncio.run(main())")
            output_lines.append("\t" * indent + "time.sleep(1)")
            continue
            
    # async_wait function
        m34 = re.match(r'\s*(?:await\s+)?wait_____async\s*$', line)
        if m34:
            output_lines.append("\t" * indent + "await asyncio.sleep(1)")
            continue

    # restart keyword
        # if line.strip() == "restart":
            # if current_func is None:
                # sys.stderr.write("KeylangError: 'restart' not in function\n")
                # sys.exit(1)
            # output_lines.append("\t" * indent + f"{current_func}()")
            # continue

    # print nones keyword
        if line.strip() == "print_nones":
            output_lines.append("\t" * indent + "__print_nones({**globals(), **locals()})")
            continue

    # print all keyword
        if line.strip() == "print_all":
            output_lines.append("\t" * indent + "__print_all({**globals(), **locals()})")
            continue

    # print vars keyword
        if line.strip() == "print_vars":
            output_lines.append("\t" * indent + "__print_vars({**globals(), **locals()})")
            continue
            
    # print python keyword
        if line.strip() == "print_python":
            python_code = "\n".join(output_lines)
            print(python_code)
            continue

        content = line.lstrip()
        output_lines.append("\t" * indent + content)
        
    # python_code = "\n".join(output_lines)

    # print(python_code)
    
# # print python keyword
    # if line.strip() == "print_python":
        # python_code = "\n".join(output_lines)
        # print(python_code)
        
    # output_lines.append("async def main():")
    # main_index = len(output_lines) - 1
    # insert_pos = main_index + 1
    # for the_thingies in async_funcs:
        # output_lines.insert(insert_pos, f"\tasyncio.create_task({the_thingies}())")
        # insert_pos += 1
    # output_lines.insert(insert_pos, "\tawait asyncio.Event().wait()")
    # output_lines.append("asyncio.run(main())")
    
    return "\n".join(output_lines)
    
if __name__ == "__main__":
    import sys
    src = sys.stdin.read()
    print(preprocess_source(src))