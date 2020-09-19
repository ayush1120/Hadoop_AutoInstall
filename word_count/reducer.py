#!/usr/bin/python
import sys

word = ''
count = 0

lines = sys.stdin.readlines()
for i, line in enumerate(lines):
    wordcount = line.strip()
    w, c = wordcount.split()
    if i==0:
        word = w
        count = int(c)
    else:
        if w == word :
            count = count +  int(c)
        else:
            print(word, count)
            word = w
            count = int(c)
print(word, count)
