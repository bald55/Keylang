import sys, os, traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
OTHER_STUFF_DIR = os.path.join(PARENT_DIR, "other_stuff")

sys.path.insert(0, OTHER_STUFF_DIR)

import preprocess

def run_kl(path: str):
    try:
        with open(path, encoding="utf-8") as f:
            kl_source = f.read()
        python_code = preprocess.preprocess_source(kl_source)
        exec(python_code, {"__name__": "__main__", "__builtins__": __builtins__})
    except Exception:
        print("[Keylang error]")
        print(traceback.format_exc())
        if sys.stdin.isatty():
            input("\nPress Enter to close...")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: keylang_runner.py <file.kl>")
        if sys.stdin.isatty():
            input("\nPress Enter to close...")
        sys.exit(1)

    src_file = sys.argv[1]
    if not os.path.exists(src_file):
        print(f"[File error] File not found: {src_file}")
        input("\nPress Enter to close...")
        sys.exit(1)

    run_kl(src_file)

if __name__ == "__main__":
    main()
    if sys.stdin.isatty():
        input("\nExecution finished. Press Enter to close...")
