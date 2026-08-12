# Birb 汉化版（单机离线版）

《Birb》网页游戏的简体中文汉化版，已移除多人联机与云存档，仅保留单机模式。

## 在线游玩

GitHub Pages：https://zhl666233.github.io/birb-cn/

> 首次进入后：设置（ESC）→ Language → **中文**，即可切换为中文界面。

## 本地运行

```bash
cd birbplay
node server.js
# 浏览器打开 http://localhost:8642/
```

## 汉化说明

- 基于游戏自带的 i18n 多语言系统，新增 `zh` 语言（可随时切回英文）
- 全量汉化 39 个分类、约 4300 条文本（界面 / 教程 / 钓鱼 / 鱼市 / 伙伴 / 升级 / 429 种鱼名 / 水族馆 / 敌人 / 地图编辑器等）
- 未翻译的后台管理（admin）文本保留英文

## 离线化说明

- `request()` 直接返回 401 → 云存档、账户、排行榜、公告、在线状态全部禁用，纯本地存档
- WebSocket 不连接，多人房间/聊天失效
- 主菜单隐藏 MULTIPLAYER，仅保留 SOLO 单人

## 目录结构

- `birbplay/` — 游戏本体（GitHub Pages 部署源）
- `build_zh.py` + `zh_dict.json` — 中文词典构建脚本与词典源
- `en_zt.json` — 提取的英文源文本（4466 条）
- `patch_main.py` — main JS 补丁脚本（汉化 + 离线化）
- `download.py` / `fix_download.py` — 资源下载脚本

## 重新构建

1. 重新下载原始 `main-7_LUcYxX.js` 覆盖到 `birbplay/assets/`
2. `python build_zh.py` 重新生成 `zh-CHINESE.js`
3. `python patch_main.py` 打补丁，`cp patched_main.js birbplay/assets/main-7_LUcYxX.js`
