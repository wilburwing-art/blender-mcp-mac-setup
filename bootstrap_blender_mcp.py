import bpy
import os
import sys

DEFAULT_ADDON_FILE = os.path.expanduser("~/Desktop/addon.py")

if "--" in sys.argv:
    extra = sys.argv[sys.argv.index("--") + 1:]
    ADDON_FILE = os.path.expanduser(extra[0]) if extra else DEFAULT_ADDON_FILE
else:
    ADDON_FILE = DEFAULT_ADDON_FILE

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

# Defer start_server: --python runs before Blender's event loop is ready, so
# calling bpy.ops.blendermcp.start_server() now fails with a context error.
# The timer queues it onto the first UI tick after startup.
bpy.app.timers.register(start_server, first_interval=1.0)
