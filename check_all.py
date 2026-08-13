# -*- coding: utf-8 -*-
"""精确扫描：去掉 HTML 标签和 {占位符} 后，找真正的英文单词残留。"""
import json, re, io

zh = json.load(open('zh_dict.json', encoding='utf-8'))
out = io.open('real_mixed.txt', 'w', encoding='utf-8')

ALLOWED = set('''FPS HP XP SP BOSS Boss STEAM Steam Discord WASD ESC Tab TAB Shift SHIFT OK
Birb BIRB Dave Monetaria Moneta Pombo Fishdex Tiny5 AUTO ON OFF MAX DMG ATK DEF SPD LV
I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII XVIII Ctrl Alt G L E P C M T R F
UP DOWN LEFT RIGHT EXIT UNLOCK LOCK PIN NEXT STOP
'''.split())

def clean(s):
    # 去 HTML 标签
    s = re.sub(r'<[^>]+>', '', s)
    # 去占位符 {xxx}
    s = re.sub(r'\{[^}]*\}', '', s)
    return s

pat = re.compile(r'[A-Za-z]{2,}')
count = 0
lines = []
for cat, obj in zh.items():
    def scan(o, prefix=''):
        global count
        if isinstance(o, dict):
            for k, v in o.items():
                scan(v, (prefix + '.' + k) if prefix else k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                scan(v, prefix + '[%d]' % i)
        elif isinstance(o, str):
            cleaned = clean(o)
            words = [w for w in pat.findall(cleaned) if w not in ALLOWED]
            if words and re.search(r'[\u4e00-\u9fff]', cleaned):
                lines.append("[%s] %s :: %s   <英文:%s>" % (cat, prefix, o, ','.join(words)))
                count += 1
    scan(obj)

for l in lines:
    out.write(l + "\n")
out.write("\n总计: %d\n" % count)
out.close()
print("真正的英文残留:", count)
