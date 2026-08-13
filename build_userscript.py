# -*- coding: utf-8 -*-
"""生成汉化油猴脚本 birb-zh.user.js（针对 birbplay.com 原版）。"""
import json, io

BASE = 'https://birbplay.com/assets/'

zh = json.load(open('zh_dict.json', encoding='utf-8'))
zh_source = json.dumps(zh, ensure_ascii=False, separators=(',', ':'))

# lang-zh 按钮（参照 lang-ru 按钮结构，16 个 \x20 缩进）
zh_button = (
    r"\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20"
    r"<button\x20id=\x22lang-zh\x22\x20class=\x22birb-btn\x20'+('zh'===Fr()?'primary':'secondary')"
    r"+'\x22\x20style=\x22padding:12px;\x20font-size:14px;\x22>'+Or('misc.languageChinese')+'</button>"
)

# (old, new) 替换规则，按顺序应用
rules = [
    # 语言注册
    ("Sr=['en','pt','es','de','fr','ru']",
     "Sr=['en','pt','es','de','fr','ru','zh']"),
    ("['en','pt','es','de','fr','ru']['includes']",
     "['en','pt','es','de','fr','ru','zh']['includes']"),
    ("}const Rr={'pt':",
     "}const Rr={'zh':async()=>{return xr(ZH_DICT);},'pt':"),
    ("'languageRussian':'Russian'",
     "'languageRussian':'Russian','languageChinese':'中文'"),
    ("Or('misc.languageRussian')+'</button>",
     "Or('misc.languageRussian')+'</button>" + zh_button),
    ("document['getElementById']('lang-ru')?.['addEventListener']('click',()=>{_0x1f2dda('ru');});",
     "document['getElementById']('lang-ru')?.['addEventListener']('click',()=>{_0x1f2dda('ru');}),document['getElementById']('lang-zh')?.['addEventListener']('click',()=>{_0x1f2dda('zh');});"),
    # P10-P27 硬编码文本
    (r"'Parrot\x20Aura'", "Or('misc.spiritAuraName')"),
    (r"_0x3dd76d['rarity']['toUpperCase']()", "Or('rarities.'+_0x3dd76d['rarity'])['toUpperCase']()"),
    (r"_0x483a45['rarity']['toUpperCase']()", "Or('rarities.'+_0x483a45['rarity'])['toUpperCase']()"),
    (r"_0x1c2278['targetRarity']['toUpperCase']()", "Or('rarities.'+_0x1c2278['targetRarity'])['toUpperCase']()"),
    (r"_0x4b1632['nextRarity']['toUpperCase']()", "Or('rarities.'+_0x4b1632['nextRarity'])['toUpperCase']()"),
    (r"'SATISFACTION:\x20'", "'满意度：'"),
    (r"'COMPLETED!'", "'完成！'"),
    (r"?'Spirit\x20Aura':'rare\x20spirit\x20trash'===", r"?'灵魂光环':'rare\x20spirit\x20trash'==="),
    (r"?'Rare\x20Spirit\x20Aura':", "?'稀有灵魂光环':"),
    (r"_0x5746ce['charAt'](0x0)['toUpperCase']()+_0x5746ce['slice'](0x1)", "Or('rarities.'+_0x5746ce)"),
    (r"_0x5f5cfd['toUpperCase']()", "Or('rarities.'+_0x5f5cfd)['toUpperCase']()"),
    (r"_0x4b5db8['targetRarity']['toUpperCase']()", "Or('rarities.'+_0x4b5db8['targetRarity'])['toUpperCase']()"),
    (r"_0x5a062b['toUpperCase']()+'\x20AURA'", "Or('rarities.'+_0x5a062b)['toUpperCase']()+Or('misc.auraWordPlural')"),
    (r"_0x4f439f['toUpperCase']()+'\x20EQUIP\x20CHEST'", "Or('rarities.'+_0x4f439f)['toUpperCase']()+Or('fishing.equipment')+Or('ui.chest')"),
    (r">INFUSION\x20+", r">'+Or('misc.infuseAction')+'\x20+"),
    (r"_0x384eeb[_0x5ab7d1]=_0x287051", "_0x384eeb[_0x5ab7d1]=_0x384eeb[_0x5ab7d1]||_0x287051"),
    (r"'damageMult'!==_0x479f40&&'damage'!==_0x479f40||(_0x52bb37=IM('misc.statDamageShort')),'maxHealthAdd'",
     r"'damageMult'!==_0x479f40&&'damage'!==_0x479f40||(_0x52bb37=IM('misc.statDamageShort')),'hpMult'!==_0x479f40&&'maxHealth'!==_0x479f40||(_0x52bb37=IM('misc.healthPercentLabel')),'maxHealthAdd'"),
    (r"'lifeRegenMult'===_0x479f40&&(_0x52bb37=IM('misc.statHpRegen'));",
     r"'lifeRegenMult'===_0x479f40&&(_0x52bb37=IM('misc.statHpRegen')),'attackSpeedMult'!==_0x479f40&&'attackSpeed'!==_0x479f40||(_0x52bb37=IM('misc.attackSpeedLabel')),'moveSpeedMult'!==_0x479f40&&'moveSpeed'!==_0x479f40||(_0x52bb37=IM('misc.moveSpeedLabel')),'critChance'===_0x479f40&&(_0x52bb37=IM('misc.critChanceLabel'));"),
    (r"_0x20d0ff=_0x473036?.['name']||_0x26f0db?.['name']||_0x3c0a76",
     r"_0x20d0ff=_0x473036?.['name']||(_0x3b825d?AM(_0x3b825d):_0x3c0a76)"),
]

# 生成 JS 替换语句
repl_lines = []
for old, new in rules:
    repl_lines.append(
        '    code = code.replace(%s, %s);' % (json.dumps(old), json.dumps(new))
    )
repl_block = '\n'.join(repl_lines)

script = r'''// ==UserScript==
// @name         Birb 汉化（简体中文）
// @namespace    birb-cn
// @version      1.0.0
// @description  汉化 Birb 网页游戏（birbplay.com 原版），自动切换为简体中文，可随时在设置里切回英文
// @author       ZHL666233
// @match        https://birbplay.com/*
// @match        https://www.birbplay.com/*
// @run-at       document-start
// @grant        GM_addElement
// @license      MIT
// ==/UserScript==

(function () {
  'use strict';

  var BASE = '__BASE__';
  var ZH_DICT_SOURCE = __ZH_DICT_SOURCE__;

  function patch(code) {
    // 1) 把相对资源路径改成绝对路径（因为内联注入后 import.meta.url 会变成页面地址）
    code = code.replace(/from'\.\//g, "from'" + BASE);
    code = code.replace(/import'\.\//g, "import'" + BASE);
    code = code.replace(/import\('\.\//g, "import('" + BASE);
    code = code.split('import.meta.url').join(JSON.stringify(BASE));

    // 2) 注入中文词典（模块作用域内可用）
    code = 'const ZH_DICT=' + ZH_DICT_SOURCE + ';\n' + code;

    // 3) 语言注册 + 硬编码文本汉化
__REPL_BLOCK__

    return code;
  }

  function intercept() {
    var scripts = document.querySelectorAll('script[type="module"][src]');
    for (var i = 0; i < scripts.length; i++) {
      var script = scripts[i];
      if (script.dataset.zhPatched) continue;
      script.dataset.zhPatched = '1';
      var src = script.getAttribute('src') || '';
      if (!/main-[\w-]+\.js/.test(src)) continue;
      // 立即把 module 改成 text/plain，阻止原版脚本执行（module 是 deferred，来得及）
      script.type = 'text/plain';
      var url = new URL(src, location.href).href;
      fetch(url).then(function (r) { return r.text(); }).then(function (code) {
        var parent = script.parentNode;
        script.remove();
        // 用 GM_addElement 绕过页面 CSP（birbplay.com 的 script-src 'self' 会阻止普通内联 script）
        GM_addElement(parent, 'script', {
          type: 'module',
          textContent: patch(code)
        });
      }).catch(function () {
        // 失败则恢复原脚本，保证游戏仍能运行
        script.type = 'module';
      });
    }
  }

  // 首次访问默认中文；用户手动切回英文后不再强制
  if (!localStorage.getItem('birb_language')) {
    try { localStorage.setItem('birb_language', 'zh'); } catch (e) {}
  }

  new MutationObserver(intercept).observe(document.documentElement, { childList: true, subtree: true });
  intercept();
})();
'''

script = script.replace('__BASE__', BASE)
script = script.replace('__ZH_DICT_SOURCE__', json.dumps(zh_source, ensure_ascii=False))
script = script.replace('__REPL_BLOCK__', repl_block)

with io.open('birb-zh.user.js', 'w', encoding='utf-8', newline='\n') as f:
    f.write(script)

print('written birb-zh.user.js, bytes:', len(script.encode('utf-8')))
print('rules:', len(rules))
