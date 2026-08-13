# -*- coding: utf-8 -*-
import json, re, io

zh = json.load(open('zh_dict.json', encoding='utf-8'))
fish = zh.get('fish', {})

out = io.open('fish_mixed.txt', 'w', encoding='utf-8')
pat = re.compile(r'[A-Za-z]{2,}')

# 只关心 name 字段里残留的英文
count = 0
for k, v in fish.items():
    nm = v.get('name', '')
    words = pat.findall(nm)
    if words:
        out.write("%s :: %s  <英文: %s>\n" % (k, nm, ','.join(words)))
        count += 1

out.write("\n残留英文的鱼名: %d / %d\n" % (count, len(fish)))
out.close()
print("残留:", count, "/", len(fish))
