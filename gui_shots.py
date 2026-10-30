# -*- coding: utf-8 -*-
"""真实浏览器窗口截图（带地址栏）：发布证明 + 跨浏览器测试证明"""
import os, sys
SKILL = r"C:\Users\zzh\.workbuddy\skills\browser-window-shot\scripts"
sys.path.insert(0, SKILL)
from gui_shot import shot, CHROME, EDGE

OUT = r"C:/Users/zzh/WorkBuddy/2026-10-27-21-51-44/zzh-shop/docs"
DEPLOY = "https://235df5aaa2eb4d7cba0715028a32291a.app.workbuddy.host/"
LOCAL = "http://127.0.0.1:8765/index.html#home"

TASKS = [
    ("shot_deploy",            DEPLOY, 520, 900, CHROME),
    ("shot_deploy_edge",       DEPLOY, 520, 900, EDGE),
    ("shot_browser_home_edge", LOCAL,  420, 900, EDGE),
    ("shot_browser_home_chrome", LOCAL, 420, 900, CHROME),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    for name, page, w, h, br in TASKS:
        if only and name not in only:
            continue
        try:
            shot(page, os.path.join(OUT, name + ".png"), w, h, browser=br)
            print("OK", name)
        except Exception as e:
            print("  !! %s  %s" % (name, e))
    print("done")
