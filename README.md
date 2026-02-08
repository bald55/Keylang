# Keylang
## - A programming language that runs on Python and embeds Lua!!! It puts a lot of emphasis on built in functions and KEYwords
##

## **v2.0.0 is OUT!!!** Working on v3.0.0 starting 2025/12/21

Latest version:
# Keylang v2.0.0 (NOT AS very early yes)

Keylang is a simple Python-like programming LANGuage that puts emphasis on built in functions and KEYwords.
It's quite similar to Python right now but it will evolve over time

***It's powered by Python, so you have to have that downloaded haha***

### More info on the website
### https://bald55.github.io/keylang-site/

----------------------------------------------------------------

## Upcoming v3.0.0 features
<sub><sup>
v3.0.0!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
</sub></sup>
<sub><sup>
PHILOSOPHY IS NOW... GAMES!!! Keylang wasn’t exactly supposed to be a general purpose programming language, and I only really care about games. So yeah Keylang is game oriented now (which means performance must be TOP NOTCH!!!!!!!!!! and stuff)
</sub></sup>

<sub><sup>
Changes
<sub><sup>
- Async functions automatically run. It’s a feature trust
<sub><sup>
- Keyword alias of EVERY syntax [TO DO]
<sub><sup>
  - (} = end)(== = is)() [TO DO]
<sub><sup>
- Variants added. Variants of a function accessed with a tilde (~)
<sub><sup>
  - “wait” function has variant “wait~async”. The async version of wait.
<sub><sup>
    - Also has the variant “wait~until”. Waits until a condition is met. [TO DO]
<sub><sup>
  - Default “wait” function changed to uses time.sleep()
<sub><sup>
- Lua embed changed to use LuaJIT
<sub><sup>
  - Scripts can be moved around now without Lua embedding breaking
<sub><sup>
- Uses NumPy for number stuff [TO DO]

<sub><sup>
Additions
<sub><sup>
- “when” keyword. Listens for WHEN an event occurs. Allows you to state how frequent it checks inside the parentheses
<sub><sup>
  - Also a “when~once” variant. Checks UNTIL the thing happens, then stops checking [TO DO]
<sub><sup>
- Keyboard input detectors. Use “if key(the_key) {}” to check if the key was pressed, if True, executes the code in the block
<sub><sup>
- “keyword” keyword. Makes a custom keyword that compiles (?) into the code it was assigned (ex. keyword yay = cube[x] += 1) [TO DO]
<sub><sup>
  - Can also have completely empty keywords (ex. keyword yay) for cosmetic purposes [TO DO]
<sub><sup>
- “print_python” keyword. Prints the unpreprocessed Python for when you’re confused or when I was confused and there’s a weird Keylang bug that you need to report
<sub><sup>
- Updated website… again! Somewhat extreme style revamp [TO DO]
