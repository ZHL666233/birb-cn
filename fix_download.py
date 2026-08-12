# -*- coding: utf-8 -*-
"""Fix missing resources: download to correct location (root / assets/buttons / assets-with-spaces)."""
import urllib.request, urllib.parse, ssl, os, shutil

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
BASE = 'https://birbplay.com'

def fetch(url, dest):
    try:
        req = urllib.request.Request(urllib.parse.quote(url, safe='/:'), headers={'User-Agent': 'Mozilla/5.0'})
        d = urllib.request.urlopen(req, context=ctx, timeout=60).read()
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, 'wb').write(d)
        return len(d)
    except Exception as e:
        return 'ERR %s' % e

# 1. root-level resources
root_files = [
    'birdsprite/pidgeon-sheet.png',
    'seagullsprite/Seagull-Sprite-Sheet.png',
    'meadow-grass.png',
]

# 2. buttons under assets/buttons/
buttons = ['config.png', 'fishing-inventory.png', 'fast-travel.png', 'leave-expedition.png', 'hold_to_reroll.png']

# 3. assets with spaces
space_files = [
    'Evil_Alien Creature_4_idle-Sheet-CWzma0Xu.png',
    'Frogfolk Brute Sprite Sheet-CAiyW9WM.png',
    'Frogfolk Chieftain Sprite Sheet-BJLXPIQc.png',
    'Doppelganger Sprite Sheet-DUwsAJnt.png',
    'Black Pudding Sprite Sheet-hx1Zy7pG.png',
    'Giant Black Pudding Sprite Sheet-CHG43NJ6.png',
    'Frogfolk Brute Sprite Sheet-pj0RL6Uj.json',
    'Frogfolk Chieftain Sprite Sheet-BoyWkGoa.json',
    'Small Hits Poofs Magic Particles Sprite Sheet-DTjLKgXm.png',
]

# remove the corrupted 0-byte truncated files first
for bad in ['Black', 'Doppelganger', 'Evil_Alien', 'Frogfolk', 'Giant', 'Small']:
    p = os.path.join('birbplay/assets', bad)
    if os.path.isdir(p):
        shutil.rmtree(p)
        print('removed corrupted dir', p)
    elif os.path.exists(p):
        os.remove(p)
        print('removed corrupted file', p)

ok = err = 0
for f in root_files:
    r = fetch(BASE + '/' + f, os.path.join('birbplay', f))
    print(('OK' if isinstance(r, int) else 'ERR'), 'root', f, r if not isinstance(r, int) else '')
    ok += isinstance(r, int); err += not isinstance(r, int)

for f in buttons:
    r = fetch(BASE + '/assets/buttons/' + f, os.path.join('birbplay/assets/buttons', f))
    print(('OK' if isinstance(r, int) else 'ERR'), 'buttons', f, r if not isinstance(r, int) else '')
    ok += isinstance(r, int); err += not isinstance(r, int)

for f in space_files:
    r = fetch(BASE + '/assets/' + f, os.path.join('birbplay/assets', f))
    print(('OK' if isinstance(r, int) else 'ERR'), 'space', f, r if not isinstance(r, int) else '')
    ok += isinstance(r, int); err += not isinstance(r, int)

print('done: OK', ok, 'ERR', err)
