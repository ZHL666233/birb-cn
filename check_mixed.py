# -*- coding: utf-8 -*-
"""Scan zh_dict.json for values that still contain English letters (mixed/leftover)."""
import json, re, io

zh = json.load(open('zh_dict.json', encoding='utf-8'))

out = io.open('mixed_en.txt', 'w', encoding='utf-8')

# 英文单词/缩写：连续 2+ 个 ASCII 字母
pat = re.compile(r'[A-Za-z]{2,}')

count = 0
def scan(cat, obj, prefix=''):
    global count
    if isinstance(obj, dict):
        for k, v in obj.items():
            scan(cat, v, (prefix + '.' + k) if prefix else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            scan(cat, v, prefix + '[%d]' % i)
    elif isinstance(obj, str):
        words = set(pat.findall(obj))
        if words:
            out.write("[%s] %s :: %s\n" % (cat, prefix, obj))
            count += 1

for cat, obj in zh.items():
    scan(cat, obj)

out.write("\n总计含英文字母的值: %d\n" % count)
out.close()
print("总计:", count)
