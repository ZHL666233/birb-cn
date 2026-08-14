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

# P15/P16: monster overhead progress text (castle monster)
js = rep(js,
    "'SATISFACTION:\\x20'",
    "'满意度：'",
    1, 'P15 monster satisfaction')

js = rep(js,
    "'COMPLETED!'",
    "'完成！'",
    1, 'P16 monster completed')

# P17/P18: hardcoded aura display names in gy()
js = rep(js,
    "?'Spirit\\x20Aura':'rare\\x20spirit\\x20trash'===",
    "?'灵魂光环':'rare\\x20spirit\\x20trash'===",
    1, 'P17 spirit aura name')

js = rep(js,
    "?'Rare\\x20Spirit\\x20Aura':",
    "?'稀有灵魂光环':",
    1, 'P18 rare spirit aura name')

# P19: getAuraRarityLabel rarity capitalization -> translate
js = rep(js,
    "_0x5746ce['charAt'](0x0)['toUpperCase']()+_0x5746ce['slice'](0x1)",
    "Or('rarities.'+_0x5746ce)",
    1, 'P19 aura rarity label')

# P20: hotbar equipment slot title rarity (was showing e.g. "COMMON")
js = rep(js,
    "_0x5f5cfd['toUpperCase']()",
    "Or('rarities.'+_0x5f5cfd)['toUpperCase']()",
    1, 'P20 hotbar gear rarity')

# P21: fusion target rarity label
js = rep(js,
    "_0x4b5db8['targetRarity']['toUpperCase']()",
    "Or('rarities.'+_0x4b5db8['targetRarity'])['toUpperCase']()",
    1, 'P21 fusion target rarity')

# P22: loot aura float text "+N RARITY AURA"
js = rep(js,
    "_0x5a062b['toUpperCase']()+'\\x20AURA'",
    "Or('rarities.'+_0x5a062b)['toUpperCase']()+Or('misc.auraWordPlural')",
    1, 'P22 loot aura float text')

# P23: equipment chest float text "+N RARITY EQUIP CHEST"
js = rep(js,
    "_0x4f439f['toUpperCase']()+'\\x20EQUIP\\x20CHEST'",
    "Or('rarities.'+_0x4f439f)['toUpperCase']()+Or('fishing.equipment')+Or('ui.chest')",
    1, 'P23 equip chest float text')

# P24: artifact "INFUSION +N" label (tooltip + gear detail)
js = rep(js,
    ">INFUSION\\x20+",
    ">'+Or('misc.infuseAction')+'\\x20+",
    2, 'P24 infusion label')

# P25: xr() must keep zh translations for artifact/equipment names (fill missing only)
js = rep(js,
    "_0x384eeb[_0x5ab7d1]=_0x287051",
    "_0x384eeb[_0x5ab7d1]=_0x384eeb[_0x5ab7d1]||_0x287051",
    1, 'P25 xr name override -> fill missing')

# P26a: VM tooltip stat label for maxHealth/hpMult
js = rep(js,
    "'damageMult'!==_0x479f40&&'damage'!==_0x479f40||(_0x52bb37=IM('misc.statDamageShort')),'maxHealthAdd'",
    "'damageMult'!==_0x479f40&&'damage'!==_0x479f40||(_0x52bb37=IM('misc.statDamageShort')),'hpMult'!==_0x479f40&&'maxHealth'!==_0x479f40||(_0x52bb37=IM('misc.healthPercentLabel')),'maxHealthAdd'",
    1, 'P26a VM maxHealth/hpMult label')

# P26b: VM tooltip stat label for attackSpeed/moveSpeed/critChance
js = rep(js,
    "'lifeRegenMult'===_0x479f40&&(_0x52bb37=IM('misc.statHpRegen'));",
    "'lifeRegenMult'===_0x479f40&&(_0x52bb37=IM('misc.statHpRegen')),'attackSpeedMult'!==_0x479f40&&'attackSpeed'!==_0x479f40||(_0x52bb37=IM('misc.attackSpeedLabel')),'moveSpeedMult'!==_0x479f40&&'moveSpeed'!==_0x479f40||(_0x52bb37=IM('misc.moveSpeedLabel')),'critChance'===_0x479f40&&(_0x52bb37=IM('misc.critChanceLabel'));",
    1, 'P26b VM attackSpeed/moveSpeed/critChance label')

# P27: hotbar equipment slot title uses translated name (AM) instead of raw English name
js = rep(js,
    "_0x20d0ff=_0x473036?.['name']||_0x26f0db?.['name']||_0x3c0a76",
    "_0x20d0ff=_0x473036?.['name']||(_0x3b825d?AM(_0x3b825d):_0x3c0a76)",
    1, 'P27 hotbar equipment name')

# P28: third seagull (specialist) name was hardcoded 'SPECIALIST'
js = rep(js,
    "?'SPECIALIST':Or('misc.seagullN')",
    "?'专家海鸥':Or('misc.seagullN')",
    1, 'P28 specialist seagull name')

# P29: shiny-fish tracker seagull labels were hardcoded 'Gull N'
js = rep(js,
    "VU('Gull\\x20'+(_0x3507c1+0x1),_0x253b95,",
    "VU(Or('misc.seagullN')['replace']('{n}',String(_0x3507c1+0x1)),_0x253b95,",
    1, 'P29 shiny tracker seagull label')

# P30: mobile tap -> synthesize mousedown (fix touch tapping/clicking, e.g. feeding monster)
js = rep(js,
    "['joystick']={'active':!0x1,'x':0x0,'y':0x0,'startX':0x0,'startY':0x0};",
    "['joystick']={'active':!0x1,'x':0x0,'y':0x0,'startX':0x0,'startY':0x0,'startClientX':0x0,'startClientY':0x0,'startTime':0x0};",
    1, 'P30a joystick tap fields')

js = rep(js,
    "this['joystick']['startX']=_0x541a5f['clientX']-_0x36cdf1['left'],this['joystick']['startY']=_0x541a5f['clientY']-_0x36cdf1['top'],this['joystick']['x']=0x0,this['joystick']['y']=0x0,_0x421194['preventDefault']();",
    "this['joystick']['startX']=_0x541a5f['clientX']-_0x36cdf1['left'],this['joystick']['startY']=_0x541a5f['clientY']-_0x36cdf1['top'],this['joystick']['startClientX']=_0x541a5f['clientX'],this['joystick']['startClientY']=_0x541a5f['clientY'],this['joystick']['startTime']=Date['now'](),this['joystick']['x']=0x0,this['joystick']['y']=0x0,_0x421194['preventDefault']();",
    1, 'P30b touchstart tap record')

js = rep(js,
    "['handleTouchEnd']=()=>{this['joystick']['active']=!0x1,this['joystick']['x']=0x0,this['joystick']['y']=0x0;};",
    "['handleTouchEnd']=()=>{const _0x7a9b1=Math['hypot'](this['joystick']['x'],this['joystick']['y']),_0x8b2c3=Date['now']()-this['joystick']['startTime'];this['joystick']['active']=!0x1,this['joystick']['x']=0x0,this['joystick']['y']=0x0;if(_0x7a9b1<0xf&&_0x8b2c3<0x258){const _0x9c4d5={'clientX':this['joystick']['startClientX'],'clientY':this['joystick']['startClientY'],'button':0x0,'bubbles':!0x0,'cancelable':!0x0,'view':window};this['canvas']['dispatchEvent'](new MouseEvent('mousedown',_0x9c4d5)),this['canvas']['dispatchEvent'](new MouseEvent('mouseup',_0x9c4d5));}};",
    1, 'P30c touchend tap dispatch')

open('patched_main.js', 'w', encoding='utf-8').write(js)
print('patched_main.js written, size:', len(js))
