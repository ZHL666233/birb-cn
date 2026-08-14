# -*- coding: utf-8 -*-
"""游戏更新后同步汉化词典。

用法：
    python sync_zh.py [新版 main JS 路径]

省略路径时默认从 https://birbplay.com/assets/main-7_LUcYxX.js 下载。

功能：
    1. 提取新版英文源（Zt 对象）
    2. 与 zh_dict.json 对比，输出新增/删除/值变更清单
    3. 把新增 key 合并进 zh_dict.json（值暂用英文，待人工翻译）
    4. 缓存英文源到 en_full.json（下次对比基准）
"""
import json, os, re, ssl, subprocess, sys, tempfile, urllib.request

DICT = 'zh_dict.json'
CACHE = 'en_full.json'
REPORT = 'sync_report.txt'

# ---------- 获取 main JS ----------
def get_js(path=None):
    if path:
        return open(path, encoding='utf-8', errors='replace').read()
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(
        'https://birbplay.com/assets/main-7_LUcYxX.js',
        headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req, context=ctx, timeout=120).read().decode('utf-8', errors='replace')

# ---------- 提取英文源 Zt ----------
def extract_zt(js):
    start = js.find('Zt={')
    if start < 0:
        raise SystemExit('错误：未找到 Zt 定义（文件可能不是游戏 main JS）')
    i = start + 3
    depth, in_str, esc, end = 0, False, False, -1
    for j in range(i, len(js)):
        c = js[j]
        if in_str:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == "'":
                in_str = False
            continue
        if c == "'":
            in_str = True
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                end = j + 1
                break
    obj_src = js[start + 3:end]
    p = os.path.join(tempfile.gettempdir(), '_zt_sync.js')
    open(p, 'w', encoding='utf-8').write('(' + obj_src + ')')
    out = subprocess.run(
        ['node', '-e',
         "const z=require('fs').readFileSync(process.argv[1],'utf8');process.stdout.write(JSON.stringify(eval(z)))",
         p], capture_output=True)
    if out.returncode != 0:
        raise SystemExit('错误：Zt 解析失败\n' + out.stderr.decode('utf-8', 'replace'))
    return json.loads(out.stdout.decode('utf-8'))

# ---------- flatten（路径 -> 值） ----------
def flatten(obj, prefix='', out=None):
    if out is None:
        out = {}
    for k, v in obj.items():
        full = prefix + '.' + k if prefix else k
        if isinstance(v, dict):
            flatten(v, full, out)
        else:
            out[full] = v
    return out

# ---------- 合并新增 key 到词典 ----------
def set_path(root, path, value):
    parts = path.split('.')
    cur = root
    for p in parts[:-1]:
        cur = cur.setdefault(p, {})
    cur[parts[-1]] = value

def main():
    js = get_js(sys.argv[1] if len(sys.argv) > 1 else None)
    zt = extract_zt(js)

    # 新版英文源扁平化
    zt_flat = flatten(zt)
    zh = json.load(open(DICT, encoding='utf-8'))
    zh_flat = flatten(zh)

    zt_keys = set(zt_flat)
    zh_keys = set(zh_flat)

    added = sorted(zt_keys - zh_keys)          # 新增（游戏新文本，待翻译）
    removed = sorted(zh_keys - zt_keys)        # 已删除（游戏移除的文本）

    # 英文值变化：对比“上次缓存的英文源”和“新版英文源”
    en_changed = []
    if os.path.exists(CACHE):
        old_zt = flatten(json.load(open(CACHE, encoding='utf-8')))
        en_changed = sorted(k for k in (zt_keys & set(old_zt))
                            if zt_flat[k] != old_zt[k])

    # 合并新增（值暂用英文，待翻译）
    for k in added:
        set_path(zh, k, zt_flat[k])

    json.dump(zh, open(DICT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(zt, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False)

    # 同步后重新生成 zh-CHINESE.js（patch_main.py 依赖的语言文件）
    zh_chunk = 'const e=' + json.dumps(zh, ensure_ascii=False, separators=(',', ':')) + ';export{e as zh};'
    open('zh-CHINESE.js', 'w', encoding='utf-8', newline='\n').write(zh_chunk)

    # 报告
    lines = []
    lines.append('== 汉化词典同步报告 ==')
    lines.append('英文源分类数: %d' % len(zt))
    lines.append('新版英文 key 总数: %d' % len(zt_keys))
    lines.append('旧词典 key 总数: %d' % len(zh_keys))
    lines.append('')
    lines.append('【新增 key（已并入词典，值暂用英文，待翻译）】%d 条' % len(added))
    for k in added:
        v = zt_flat[k]
        lines.append('  + %s => %s' % (k, v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)))
    lines.append('')
    lines.append('【词典有但英文源没有的 key（游戏移除或汉化补丁自有，保留未删，请人工确认）】%d 条' % len(removed))
    for k in removed:
        lines.append('  - %s' % k)
    lines.append('')
    lines.append('【英文源值变化（翻译可能需复核）】%d 条' % len(en_changed))
    for k in en_changed:
        lines.append('  ~ %s  英文: %r' % (k, zt_flat[k]))

    report = '\n'.join(lines)
    open(REPORT, 'w', encoding='utf-8').write(report)
    print(report)
    print('\n报告已写入 %s，英文源缓存已写入 %s' % (REPORT, CACHE))

if __name__ == '__main__':
    main()
