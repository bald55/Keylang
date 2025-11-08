## This key lime pie is half-baked :| ↓
### This is an early release. Expect bugs and glitches

Latest version:
# Keylang v0.2.0 (NOT AS very early yes)

Keylang is a simple Python-like programming LANGuage that puts emphasis on built in functions and KEYwords.
It's quite similar to Python right now but it will evolve over time

***It's powered by Python, so you have to have that downloaded haha***


If you want to load a script, you can use this and change it a little
```Python
import subprocess
with open("test.kl", "r") as f: # replace with the script you want to run
    kl_source = f.read()
result = subprocess.run(["python", "other_stuff/preprocess.py"], input=kl_source, text=True, capture_output=True) # replace with actual file path if different
python_code = result.stdout
exec(python_code, {"__name__": "__main__"})
```

### More info on the website
### https://bald55.github.io/keylang-site/
