# -*- coding: utf-8 -*-
import json

en = json.load(open('en_zt.json', encoding='utf-8'))
zh = json.load(open('zh_dict.json', encoding='utf-8'))

missing = {}  # category -> list of missing keys

def collect(obj, prefix=''):
    """返回所有叶子 key 的路径列表"""
    keys = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            keys.extend(collect(v, prefix + '.' + k if prefix else k))
    else:
        keys.append(prefix)
    return keys

for cat, en_obj in en.items():
    en_keys = set(collect(en_obj))
    zh_obj = zh.get(cat, {})
    zh_keys = set(collect(zh_obj))
    miss = sorted(en_keys - zh_keys)
    if miss:
        missing[cat] = miss

total = 0
for cat, keys in sorted(missing.items()):
    print("===== %s (%d 缺失) =====" % (cat, len(keys)))
    for k in keys:
        # 取英文值
        cur = en[cat]
        for part in k.split('.'):
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                cur = None
                break
        if isinstance(cur, str):
            print(k + " :: " + repr(cur))
        else:
            print(k + " :: (非字符串)")
        total += 1
    print()

print("总缺失:", total)
