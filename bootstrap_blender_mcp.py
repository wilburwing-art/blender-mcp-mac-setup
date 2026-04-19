import bpy
import os
import sys

ADDON_FILE = os.path.expanduser("~/Desktop/addon.py")
MODULE_NAME = os.path.splitext(os.path.basename(ADDON_FILE))[0].replace("-", "_")

def die(msg):
    print(f"[bootstrap] FATAL: {msg}", file=sys.stderr)
    sys.exit(1)

if not os.path.isfile(ADDON_FILE):
    die(f"addon file not found: {ADDON_FILE}")

print(f"[bootstrap] installing {ADDON_FILE}")
try:
    bpy.ops.preferences.addon_install(overwrite=True, filepath=ADDON_FILE)
except Exception as e:
    die(f"addon_install failed: {e}")

print(f"[bootstrap] enabling module {MODULE_NAME}")
try:
    bpy.ops.preferences.addon_enable(module=MODULE_NAME)
except Exception as e:
    die(f"addon_enable(module={MODULE_NAME!r}) failed: {e}")

try:
    bpy.ops.wm.save_userpref()
    print("[bootstrap] user prefs saved")
except Exception as e:
    die(f"save_userpref failed: {e}")

def start_server():
    try:
        print("[bootstrap] starting MCP server")
        bpy.ops.blendermcp.start_server()
        print("[bootstrap] MCP server start invoked")
    except Exception as e:
        print(f"[bootstrap] failed to start server: {e}", file=sys.stderr)
    return None

bpy.app.timers.register(start_server, first_interval=1.0)
