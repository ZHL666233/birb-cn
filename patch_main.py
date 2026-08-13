# -*- coding: utf-8 -*-
"""Offline patch of main JS: inject zh language. Validates each replacement."""
import io

SRC = 'birbplay/assets/main-7_LUcYxX.js'
js = open(SRC, encoding='utf-8', errors='replace').read()

ZH_CHUNK = './zh-CHINESE.js'

def rep(s, old, new, expect, label):
    n = s.count(old)
    if n != expect:
        print('[FAIL] %s: expected %d occurrences, found %d' % (label, expect, n))
        return s
    s = s.replace(old, new)
    print('[OK] %s: %d replacements' % (label, n))
    return s

# P1a: game language list Sr - add zh (1 occurrence)
js = rep(js,
    "Sr=['en','pt','es','de','fr','ru']",
    "Sr=['en','pt','es','de','fr','ru','zh']",
    1, 'P1a Sr lang list')

# P1b: settings validation list - add zh (1 occurrence)
js = rep(js,
    "['en','pt','es','de','fr','ru']['includes']",
    "['en','pt','es','de','fr','ru','zh']['includes']",
    1, 'P1b settings validation')

# NOTE: OR (chat channel language list) intentionally NOT modified - the chat
# text table has no 'zh' entry and adding zh would throw on undefined.global

# P2: register zh loader in Rr
js = rep(js,
    "}const Rr={'pt':",
    "}const Rr={'zh':async()=>{return xr((await Er(async()=>{const {zh:z}=await import('" + ZH_CHUNK + "');return{'zh':z};},[],import.meta.url))['zh']);},'pt':",
    1, 'P2 Rr zh loader')

# P3: language display name
js = rep(js,
    "'languageRussian':'Russian'",
    "'languageRussian':'Russian','languageChinese':'中文'",
    1, 'P3 lang name')

# P4: add zh button HTML after lang-ru button
btn_zh = "\\x0a\\x20\\x20\\x20\\x20\\x20\\x20\\x20\\x20\\x20\\x20\\x20\\x20\\x20\\x20\\x20\\x20\\x20\\x20\\x20\\x20<button\\x20id=\\x22lang-zh\\x22\\x20class=\\x22birb-btn\\x20'+('zh'===Fr()?'primary':'secondary')+'\\x22\\x20style=\\x22padding:12px;\\x20font-size:14px;\\x22>'+Or('misc.languageChinese')+'</button>"
js = rep(js,
    "Or('misc.languageRussian')+'</button>",
    "Or('misc.languageRussian')+'</button>" + btn_zh,
    1, 'P4 zh button HTML')

# P5: add zh click handler after lang-ru handler
js = rep(js,
    "document['getElementById']('lang-ru')?.['addEventListener']('click',()=>{_0x1f2dda('ru');});",
    "document['getElementById']('lang-ru')?.['addEventListener']('click',()=>{_0x1f2dda('ru');}),document['getElementById']('lang-zh')?.['addEventListener']('click',()=>{_0x1f2dda('zh');});",
    1, 'P5 zh click handler')

# P6: disable all backend API calls (offline single-player only).
# request() throws 401 immediately so auth/cloud-save/leaderboard/announcements
# all degrade to guest/local, and no network requests are ever sent.
js = rep(js,
    "async['request'](_0x2a785f,_0x2e8dc2={},_0x499848=0x2710){",
    "async['request'](_0x2a785f,_0x2e8dc2={},_0x499848=0x2710){throw new up(0x191,{});",
    1, 'P6 disable API request')

# P7: hide the MULTIPLAYER tab on the start screen (solo only)
js = rep(js,
    "<button\\x20id=\\x22tab-multi\\x22\\x20class=\\x22tab-btn\\x22>",
    "<button\\x20id=\\x22tab-multi\\x22\\x20class=\\x22tab-btn\\x22\\x20style=\\x22display:none\\x22>",
    1, 'P7 hide multiplayer tab')

# P8: force chat disabled (WR() always takes the hide-chat branch)
js = rep(js,
    "_0x51be10=!!_0x2eeb7b['state']['settings']?.['disableChat']",
    "_0x51be10=!0x0",
    1, 'P8 force disable chat')

# P9: hide the chat toggle button in settings
js = rep(js,
    "<button\\x20id=\\x22settings-game-chat-btn\\x22\\x20class=\\x22birb-btn\\x20primary\\x22\\x20style=\\x22width:100%;\\x20padding:12px;\\x20font-size:14px;\\x22>",
    "<button\\x20id=\\x22settings-game-chat-btn\\x22\\x20class=\\x22birb-btn\\x20primary\\x22\\x20style=\\x22display:none;\\x20width:100%;\\x20padding:12px;\\x20font-size:14px;\\x22>",
    1, 'P9 hide chat toggle button')

# P10: translate hardcoded 'Parrot Aura' equipment name
js = rep(js,
    "'Parrot\\x20Aura'",
    "Or('misc.spiritAuraName')",
    1, 'P10 Parrot Aura name')

# P11-P14: translate rarity quality names (rarity.toUpperCase -> Or('rarities.'+rarity))
js = rep(js,
    "_0x3dd76d['rarity']['toUpperCase']()",
    "Or('rarities.'+_0x3dd76d['rarity'])['toUpperCase']()",
    1, 'P11 gear upgrade rarity')

js = rep(js,
    "_0x483a45['rarity']['toUpperCase']()",
    "Or('rarities.'+_0x483a45['rarity'])['toUpperCase']()",
    1, 'P12 upgrade toast rarity')

js = rep(js,
    "_0x1c2278['targetRarity']['toUpperCase']()",
    "Or('rarities.'+_0x1c2278['targetRarity'])['toUpperCase']()",
    1, 'P13 fusion rarity')

js = rep(js,
    "_0x4b1632['nextRarity']['toUpperCase']()",
    "Or('rarities.'+_0x4b1632['nextRarity'])['toUpperCase']()",
    1, 'P14 slot evolve rarity')

open('patched_main.js', 'w', encoding='utf-8').write(js)
print('patched_main.js written, size:', len(js))
