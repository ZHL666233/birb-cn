# -*- coding: utf-8 -*-
"""Fix fish/junk/treasure names that still contain untranslated English words."""
import json

zh = json.load(open('zh_dict.json', encoding='utf-8'))
fish = zh['fish']

FIX = {
    'fish_tan_red_fins': '红鳍鱼',
    'ghost_angel_purple': '紫灵魂天使',
    'ghost_skeleton_green': '苔藓骷髅',
    'ocean_blue_pale': '浅海鱼',
    'ocean_whale_maroon': '栗色鲸',
    'eel_garden': '花园鳗',
    'gulper_eel': '吞噬鳗',
    'sea_angel': '深渊天使',
    'fish_white_fresh': '淡水白鱼',
    'goldfish_black_moor': '黑龙睛金鱼',
    'rockfish_spiky_red': '多刺红岩鱼',
    'ocean_blue_dark': '深海泳者',
    'ocean_blue_green': '青绿海鱼',
    'ocean_blue_longfin': '长鳍蓝鱼',
    'ocean_blue_tiny': '迷你蓝海鱼',
    'ocean_grey_blue': '风暴海鱼',
    'ocean_lavender_round': '圆薰衣草海鱼',
    'ocean_purple_tiny': '迷你紫海鱼',
    'ocean_purple_white': '紫白海鱼',
    'ocean_red_blue': '双色海泳者',
    'ocean_white_blue': '白蓝海鱼',
    'whale_blue_green_ocean': '泛绿蓝鲸',
    'dead_fish': '死鱼',
    'hermit_crab_small': '小寄居蟹',
    'runic_moonfish': '符文月亮鱼',
    'damselfish_blue_tail': '蓝尾雀鲷',
    'ghost_angel_white': '纯净灵魂天使',
    'ghost_fish_tan': '沙灵',
    'ghost_fish_yellow_small': '迷你火花灵',
    'ghost_skeleton_green_long': '苔藓巨蛇',
    'cosmic_fish_green': '星斑鱼',
    'clock_compass': '航海钟',
    'mech_shell_gold': '镀金机甲鱼',
    'sea_watch': '潜水员表',
    'torpedo_mini': '迷你鱼雷',
    'crab_hermit_standard': '寄居蟹',
    'crab_red': '红盐蟹',
    'crayfish_brown': '河螯虾',
    'crayfish_red': '信号螯虾',
    'plankton_cloud': '浮游云',
    'fish_tan_fresh': '棕黄淡水鱼',
    'ocean_blue_navy': '藏青海鱼',
    'ocean_grey_blue_alt': '风暴海鱼',
    'pipe_joint': '铜管接头',
    'abyssal_blob_brown': '泥水滴',
    'abyssal_spine_dark': '棘鱼',
    'abyssal_worm_dark': '影蠕虫',
    'bobbit_worm': '博比特虫',
    'dragonfish_black': '黑龙',
    'lanternfish_blue': '灯笼鱼',
    'prawn_red': '岩浆虾',
    'tube_worm_red': '巨管虫',
    'junk_boot': '旧靴子',
    'junk_net': '破网',
    'junk_seaweed': '湿海藻',
    'junk_moss_clump': '苔藓团',
    'junk_stone_grey': '光滑石头',
    'junk_sea_ribbons': '海丝带',
    'junk_sea_vine': '海藤蔓',
    'junk_bottle_jar': '空罐子',
    'junk_bottle_potion': '空药水瓶',
    'junk_boots_pair': '一双靴子',
    'junk_spectacles': '旧眼镜',
    'treasure_chest_wood': '木宝箱',
    'treasure_chest_mossy': '苔藓宝箱',
    'treasure_crown': '失落王冠',
    'exp_f1_dewscale_sproutfish': '露鳞芽鱼',
    'exp_f1_emerald_glenperch': '翡翠幽谷鲈',
    'exp_f1_whisperleaf_piran': '低语叶食人鱼',
    'exp_f2_violet_hexfin': '紫罗兰咒鳍',
    'exp_f2_lilac_runelet': '丁香小符文',
    'exp_f2_amethyst_driftling': '紫晶漂灵',
    'exp_f4_riptide_hexfin': '激流咒鳍',
    'exp_f6_polar_flicker': '极地闪烁',
}

applied = 0
for k, v in FIX.items():
    if k in fish:
        fish[k]['name'] = v
        applied += 1
    else:
        print('未找到 key:', k)

print('已修正:', applied, '/', len(FIX))

# 保存
json.dump(zh, open('zh_dict.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# 重新生成 zh chunk
body = json.dumps(zh, ensure_ascii=False, separators=(',', ':'))
js = 'const e=' + body + ';export{e as zh};'
open('zh-CHINESE.js', 'w', encoding='utf-8').write(js)
open('birbplay/assets/zh-CHINESE.js', 'w', encoding='utf-8').write(js)
print('zh-CHINESE.js 已更新:', len(js.encode('utf-8')), '字节')
