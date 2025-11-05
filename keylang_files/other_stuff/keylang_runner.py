import sys
import os
import subprocess
import traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    if len(sys.argv) < 2:
        print("Usage: keylang_runner.py <file.kl>")
        sys.exit(1)

    src_file = sys.argv[1]
    if not os.path.exists(src_file):
        print(f"[File error] File not found: {src_file}")
        sys.exit(1)

    try:
        with open(src_file, encoding="utf-8") as f:
            src = f.read()
    except OSError as e:
        print(f"[File error] {e}")
        sys.exit(1)

    # Run the preprocessor to transpile Keylang → Python
    try:
        proc = subprocess.run(
            [sys.executable, os.path.join(BASE_DIR, "preprocess.py")],
            input=src.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if proc.returncode != 0:
            print("[Preprocessor error]")
            print(proc.stderr.decode())
            sys.exit(1)

        python_code = proc.stdout.decode()
    except Exception:
        print("[Transpile error]")
        print(traceback.format_exc())
        sys.exit(1)

    # Execute the transpiled Python code
    try:
        exec(python_code, {"__name__": "__main__", "__builtins__": __builtins__})
    except Exception:
        print("[Execution error]")
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
