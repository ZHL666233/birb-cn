import re, os, ssl, urllib.request

BASE = 'https://birbplay.com'
OUT = 'birbplay'
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch(url, dest):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        d = urllib.request.urlopen(req, context=ctx, timeout=120).read()
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, 'wb').write(d)
        return len(d)
    except Exception as e:
        return 'ERR %s' % e

# 1. assets referenced from JS (new URL / dynamic import, relative to /assets/)
js_files = [
    'birbplay/assets/main-7_LUcYxX.js',
    'birbplay/assets/maps-BILFrqKW.js',
    'birbplay/assets/vendor-Bjkrs06Y.js',
    'birbplay/assets/audio-DQ28Xj1A.js',
]
assets = set()
for f in js_files:
    txt = open(f, encoding='utf-8', errors='replace').read()
    for m in re.finditer(r"new URL\(['\"]([^'\"]+)['\"]", txt):
        assets.add(m.group(1))
    for m in re.finditer(r"import\(['\"]([^'\"]+)['\"]\)", txt):
        assets.add(m.group(1))

# 2. CSS url()
css = open('birbplay/assets/main-DA_7hnFA.css', encoding='utf-8', errors='replace').read()
for m in re.finditer(r"url\(([^)]+)\)", css):
    u = m.group(1).strip('"\'')
    if u.startswith('data:') or u.startswith('http'):
        continue
    assets.add(u)

# 3. HTML refs (root-relative)
html = open('birbplay_home.html', encoding='utf-8', errors='replace').read()
root_files = set()
for m in re.finditer(r'(?:src|href)=["\']([^"\']+)["\']', html):
    u = m.group(1)
    if u.startswith('http') or u.startswith('data:') or u.startswith('#'):
        continue
    root_files.add(u)

results = []
# download assets/ files
for u in sorted(assets):
    clean = u.lstrip('./')
    dest = os.path.join(OUT, 'assets', clean)
    size = fetch(BASE + '/assets/' + clean, dest)
    results.append(('assets', clean, size))

# download root files (html refs)
for u in sorted(root_files):
    clean = u.lstrip('./')
    dest = os.path.join(OUT, clean)
    size = fetch(BASE + '/' + clean, dest)
    results.append(('root', clean, size))

ok = 0
err = 0
total = 0
for cat, name, size in results:
    if isinstance(size, int):
        ok += 1
        total += size
    else:
        err += 1
        print('ERR', cat, name, size)
print('OK files:', ok, 'ERR:', err, 'total bytes:', total)
