import vim
import re

print(len(vim.current.buffer))
for line in vim.current.buffer:
    print("line: " + line)
