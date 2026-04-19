import bpy
import os

ADDON_FILE = os.path.expanduser("~/Desktop/addon.py")
MODULE_NAME = "addon"

print(f"[bootstrap] installing {ADDON_FILE}")
bpy.ops.preferences.addon_install(overwrite=True, filepath=ADDON_FILE)

print(f"[bootstrap] enabling module {MODULE_NAME}")
bpy.ops.preferences.addon_enable(module=MODULE_NAME)

bpy.ops.wm.save_userpref()
print("[bootstrap] user prefs saved")

def start_server():
    try:
        print("[bootstrap] starting MCP server")
        bpy.ops.blendermcp.start_server()
        print("[bootstrap] MCP server start invoked")
    except Exception as e:
        print(f"[bootstrap] failed to start server: {e}")
    return None

bpy.app.timers.register(start_server, first_interval=1.0)
