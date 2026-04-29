#!/usr/bin/env python3
"""Validate that index.html has balanced braces/brackets in its JS block.
Run this after every edit. Exits 1 if unbalanced."""
import re, sys

with open('index.html') as f:
    content = f.read()

script = re.search(r'<script>(.*?)</script>', content, re.DOTALL).group(1)
braces = brackets = 0
in_string = False
string_char = None
i = 0
while i < len(script):
    c = script[i]
    if in_string:
        if c == '\\': i += 2; continue
        if c == string_char: in_string = False
    elif c in ('"', "'", '`'):
        in_string = True; string_char = c
    elif c == '{': braces += 1
    elif c == '}': braces -= 1
    elif c == '[': brackets += 1
    elif c == ']': brackets -= 1
    i += 1

if braces != 0 or brackets != 0:
    print(f"FAIL: braces={braces}, brackets={brackets}")
    sys.exit(1)
print("OK: balanced")
