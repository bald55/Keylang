import re, sys

# .\keylang.ps1 .\test.kl

indent = 0
block_stack = []
current_func = None

once_id = 0
loop_id = 0


print("__once_done = set()")
print("import asyncio")
print("import types")
print("import random")
print("import threading")

print("def __print_nones(locals_dict):")
print("\tfor name, value in locals_dict.items():")
print("\t\tif value is None:")
print("\t\t\tprint(f\"{name} = None\")")

print("def __print_all(locals_dict):")
print("\tfor name, value in locals_dict.items():")
print("\t\tif value:")
print("\t\t\tprint(f\"{name} = {value!r}\")")

print("def __print_vars(locals_dict):")
print("\tfor name, value in locals_dict.items():")
print("\t\tif name.startswith('__'):")
print("\t\t\tcontinue")
print("\t\tif isinstance(value, types.FunctionType):")
print("\t\t\tcontinue")
print("\t\tif name == 'asyncio' or name == 'types':")
print("\t\t\tcontinue")
print("\t\tprint(f\"{name} = {value!r}\")")

def replace_random(m):
    arg = m.group(1).strip()
    parts = [p.strip() for p in arg.split(",")]

    if len(parts) == 1:
        var = parts[0]
        return (f"random.choice({var} if not isinstance({var}, dict) "
                f"else list({var}.values()))")
    return f"random.choice([{arg}])"

def has_inline_comment(line):
    in_string = False
    quote_char = None
    for i, ch in enumerate(line):
        if ch in ("'", '"'):
            if i > 0 and line[i-1] == "\\":
                continue
            if not in_string:
                in_string = True
                quote_char = ch
            elif ch == quote_char:
                in_string = False
                quote_char = None
        elif ch == "#" and not in_string:
            # '#' outside a string and not at start = inline comment
            if i > 0 and not line[:i].lstrip().startswith("#"):
                return True
    return False

for raw in sys.stdin:
    line = raw.rstrip()

    if not line.strip():
        print("")
        continue

    stripped = line.lstrip()

    if line.lstrip().startswith("#"):
        print("\t" * indent + line.lstrip())
        continue

    if has_inline_comment(line):
        sys.stderr.write("KeylangError: Inline comments are not supported in the current version. That sucks\n")
        sys.exit(1)

# re searches
# re searches

    if re.search(r':\s*$', line):
        sys.stderr.write("KeylangError: ':' is replaced with curly brackets >:), use '{' and '}'\n")
        sys.exit(1)

    m = re.match(r'\s*loop\((.+)\)\s*{', line)
    if m:
        count = m.group(1).strip()
        loop_id += 1
        varname = f"__i{loop_id}"
        print("\t" * indent + f"for {varname} in range(int({count})):")
        # print("\t" * indent + f"for __i in range(int({count})):")
        indent += 1
        block_stack.append(None)
        continue

    m2 = re.match(r'\s*once\s*{', line)
    if m2:
        once_id += 1
        oid = once_id
        print("\t" * indent + f"if {oid} not in __once_done:")
        indent += 1
        print("\t" * indent + f"__once_done.add({oid})")
        block_stack.append(oid)
        continue

    m3 = re.match(r'\s*wait\((.+)\)\s*$', line)
    if m3:
        arg = m3.group(1).strip()
        print("\t" * indent + "async def main():")
        indent += 1
        print("\t" * indent + f"await asyncio.sleep({arg})")
        indent -= 1
        print("\t" * indent + "asyncio.run(main())")
        continue

    m4 = re.search(r'\barray\((.*?)\)', line)
    if m4:
        line = re.sub(r'\barray\((.*?)\)', r'[\1]', line)
        print("\t" * indent + line.lstrip())
        continue

    m5 = re.search(r'\bdict\((.*?)\)', line)
    if m5:
        line = re.sub(r'\bdict\((.*?)\)', r'{\1}', line)
        line = re.sub(r'({.*?})(.*)', 
            lambda m: re.sub(r'([\'"].+?[\'"]|\w+)\s*=\s*', r'\1: ', m.group(1)) + m.group(2),
                  line)
        print("\t" * indent + line.lstrip())
        continue

    m_private = re.match(r"\s*private\s+func\s+(.+)", line)
    if m_private:
        header = m_private.group(1).rstrip("{").strip()
        if "(" not in header and ")" not in header:
            header += "()"
        func_name, _, params = header.partition("(")
        func_name = func_name.strip()
        params = params.rstrip(")")
        if not params.strip():
            params = "self"
        else:
            params = "self, " + params.strip()
        current_func = func_name
        print("\t" * indent + f"def __{func_name}({params}):")
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
            params = "self"
        else:
            params = "self, " + params.strip()
        current_func = func_name
        print("\t" * indent + f"def _{func_name}({params}):")
        indent += 1
        block_stack.append(None)
        continue

    m_spawn = re.match(r'\s*spawn\s+(\w+)(?:\((.*?)\))?\s*$', line)
    if m_spawn:
        func = m_spawn.group(1)
        args = (m_spawn.group(2) or "").strip()
        if args:
            print("\t" * indent + f"threading.Thread(target={func}, args=({args},), daemon=True).start()")
        else:
            print("\t" * indent + f"threading.Thread(target={func}, daemon=True).start()")
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
    if line.strip().startswith("func "):
        header = line.strip()[5:].rstrip("{").strip()
        if "(" not in header and ")" not in header:
            header += "()"
        name, _, params = header.partition("(")
        params = params.rstrip(")")
        func_name = name.strip()
        current_func = func_name
        if indent > 0:
            if not params.strip():
                params = "self"
            else:
                params = "self, " + params.strip()
            print("\t" * indent + f"def {func_name}({params}):")
        else:
            print("\t" * indent + f"def {func_name}({params}):")
        indent += 1
        block_stack.append(None)
        continue



# loop function
    if line.strip() == "loop {":
        print("\t" * indent + "while True:")
        indent += 1
        block_stack.append(None)
        continue

# once function
    # if line.strip() == "once {":
        # once_id += 1
        # oid = once_id
        # flag_name = f"__once_flag_{once_id}"
        # print("\t" * indent + f"{flag_name} = True")
        # print("\t" * indent + f"if {flag_name}:")
        # print("\t" * indent + f"if {oid} not in __once_done:")
        # indent += 1
        # print("\t" * indent + f"{flag_name} = False")
        # block_stack.append(oid)
        # block_stack.append(None)
        # continue

    if line.endswith("{"):
        opener = line[:-1].strip()
        print("\t" * indent + opener + ":")
        indent += 1
        block_stack.append(None)
        continue

# [] error
    if re.search(r'=\s*\[', line):
        sys.stderr.write("KeylangError: '[' and ']' are replaced with 'array()' btw >:)\n")
        sys.exit(1)
# {} error
    if re.search(r'=\s*\{', line):
        sys.stderr.write("KeylangError: '{' and '}' are replaced with 'dict()' btw >:)\n")
        sys.exit(1)

# error thingy
    if "}" in line and not re.match(r'^\s*}\s*(#.*)?$', line):
        sys.stderr.write("KeylangError: Either '}' is not on its own line, or you're accessing a dictionary value with {} instead of [].\n")
        sys.exit(1)

    if line.endswith("}"):
        block_stack.pop()
        indent -= 1
        if indent < 0:
            indent = 0
        continue

# wait function
    if line.strip() == "wait":
        print("\t" * indent + "async def main():")
        indent += 1
        print("\t" * indent + "await asyncio.sleep(1)")
        indent -= 1
        print("\t" * indent + "asyncio.run(main())")
        continue

# restart keyword
    # if line.strip() == "restart":
        # if current_func is None:
            # sys.stderr.write("KeylangError: 'restart' not in function\n")
            # sys.exit(1)
        # print("\t" * indent + f"{current_func}()")
        # continue

# print nones keyword
    if line.strip() == "print_nones":
        print("\t" * indent + "__print_nones({**globals(), **locals()})")
        continue

# print all keyword
    if line.strip() == "print_all":
        print("\t" * indent + "__print_all({**globals(), **locals()})")
        continue

# print vars keyword
    if line.strip() == "print_vars":
        print("\t" * indent + "__print_vars({**globals(), **locals()})")
        continue


    content = line.lstrip()
    print("\t" * indent + content)