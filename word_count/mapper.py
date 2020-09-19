#!/usr/bin/python
import sys

lines = sys.stdin.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()

for line in lines:
    words = line.split()
    for word in words:
        print(f"{word.strip()}\t 1")