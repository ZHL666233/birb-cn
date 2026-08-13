import re, io

js = open('birbplay/assets/main-7_LUcYxX.js', encoding='utf-8', errors='replace').read()
out = io.open('hardcoded.txt', 'w', encoding='utf-8')

# showCinematicDialogue 调用（剧情对话，常硬编码）
out.write("=== showCinematicDialogue 调用 ===\n")
for m in re.finditer(r'showCinematicDialogue', js):
    s = max(0, m.start()-100)
    out.write(js[s:m.start()+700].replace('\n',' '))
    out.write("\n=====\n")

out.close()
print("done")
