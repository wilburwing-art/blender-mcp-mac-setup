# Blender MCP — Mac Setup

Wire Blender to Claude Desktop via MCP, then drive it with voice.

Each phase is a natural stopping point if you hit friction.

## Phase 1: Install the pieces

1. **Blender**: download from [blender.org](https://www.blender.org/download/) and drag to Applications, or `brew install --cask blender`. Tested with Blender 5.1.x; the upstream addon also supports 4.x.
2. **Claude Desktop**: [claude.ai/download](https://claude.ai/download) — the mobile or web app can't run MCP servers, has to be desktop.
3. **uv** (provides the `uvx` command the MCP server needs): in Terminal run `brew install uv`, or if you don't have Homebrew: `curl -LsSf https://astral.sh/uv/install.sh | sh`.
4. Confirm `uvx` is installed: `which uvx`. Copy that full path somewhere, you'll need it.

## Phase 2: Install the Blender addon

### Option A — scripted (skips the GUI)

```bash
git clone https://github.com/wilburwing-art/blender-mcp-mac-setup.git
cd blender-mcp-mac-setup
curl -sSL -o ~/Desktop/addon.py https://raw.githubusercontent.com/ahujasid/blender-mcp/main/addon.py
/Applications/Blender.app/Contents/MacOS/Blender --python bootstrap_blender_mcp.py -- ~/Desktop/addon.py
```

`bootstrap_blender_mcp.py` installs the addon, enables it, saves prefs, and starts the MCP server on port 9876. Blender stays running with the server listening. Skip to Phase 3.

### Option B — manual GUI

1. Go to [github.com/ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp) and download `addon.py` from the repo.
2. Open Blender, go to **Edit > Preferences > Add-ons > Install from Disk**, pick `addon.py`.
3. Tick the checkbox to enable **Interface: Blender MCP**.
4. Close preferences, press **N** in the 3D viewport, you'll see a **BlenderMCP** tab in the sidebar. Don't click Start yet.

## Phase 3: Configure Claude Desktop

The config path is `~/Library/Application Support/Claude/claude_desktop_config.json`. It often already contains a `preferences` block — you need to **merge**, not replace.

### If the file doesn't exist yet

Create it with just this:

```json
{
  "mcpServers": {
    "blender": {
      "command": "/full/path/to/uvx",
      "args": ["blender-mcp"]
    }
  }
}
```

### If the file already exists

Use `jq` to merge safely (preserves everything else):

```bash
UVX_PATH="$(which uvx)"
CFG=~/Library/Application\ Support/Claude/claude_desktop_config.json
jq --arg uvx "$UVX_PATH" '.mcpServers.blender = {command: $uvx, args: ["blender-mcp"]}' "$CFG" > "$CFG.tmp" && mv "$CFG.tmp" "$CFG"
```

No `jq`? `brew install jq` first, or edit by hand — add a top-level `"mcpServers": { "blender": { "command": "...", "args": ["blender-mcp"] } }` entry alongside your existing keys.

Using the full path to `uvx` (instead of just `"uvx"`) avoids the most common macOS gotcha where Claude Desktop's PATH doesn't include Homebrew.

Fully quit Claude Desktop (**Cmd+Q**, not just close the window) and reopen it.

## Phase 4: First run

1. **If you used Option A**, the server is already listening — skip to step 2. **If Option B**, click **Start MCP Server** in the BlenderMCP sidebar. It should say `MCP Server started on port 9876`.
2. Confirm the server is actually listening, independent of Claude Desktop:

   ```bash
   lsof -iTCP:9876 -sTCP:LISTEN
   ```

   You should see `Blender` as the owning process. If nothing prints, the addon didn't start the server — check Blender's system console for errors.

   For an end-to-end socket smoke test (should print scene JSON):

   ```bash
   python3 -c 'import socket,json; s=socket.socket(); s.connect(("localhost",9876)); s.sendall(json.dumps({"type":"get_scene_info"}).encode()); print(s.recv(4096).decode()[:300])'
   ```

3. In Claude Desktop, start a new chat. You should see a tools icon indicating Blender MCP is connected.
4. Type `get scene information` as your first test. If that works, you're wired up.

## Phase 5: Voice

On macOS the fastest path is built-in dictation: **System Settings > Keyboard > Dictation**, turn on, set a shortcut (double-tap `fn` works well). Then in Claude Desktop, double-tap `fn` and talk.

Whisper-based alternatives like [Superwhisper](https://superwhisper.com/) or [MacWhisper](https://goodsnooze.gumroad.com/l/macwhisper) are better quality and worth upgrading to later.

## Phase 6: A file to play with

Grab the **Classroom** or **Junk Shop** demo from [blender.org/download/demo-files](https://www.blender.org/download/demo-files/), open it in Blender, then try voice commands like:

- "describe the scene"
- "add a bright orange cube floating above the main desk"
- "change the world background to a sunset HDRI from Poly Haven"

## Troubleshooting

**Claude Desktop shows no tools icon / says the `blender` server failed to start.**
Usually a PATH issue: Claude Desktop's environment doesn't include Homebrew. Make sure the config uses the full path from `which uvx` (e.g. `/opt/homebrew/bin/uvx`), not bare `uvx`. Fully quit (Cmd+Q) and reopen after editing the config.

**`lsof -iTCP:9876 -sTCP:LISTEN` prints nothing after Option A.**
The addon installed but `start_server` couldn't run. Look at Blender's system console: Window > Toggle System Console on macOS shows nothing helpful — instead re-run the bootstrap from Terminal so stderr prints in your shell. Common causes: the module name didn't match the filename (bootstrap now derives this automatically), or another process is already on port 9876 (`lsof -iTCP:9876` to find it).

**`addon_enable` fails with "module 'X' not found".**
Blender's `addon_install` copies the file to `~/Library/Application Support/Blender/<ver>/scripts/addons/` keeping the filename. If the filename contains hyphens or other non-identifier characters, Python can't import it. The bootstrap renames `-` to `_`; if you're installing manually, save the addon as `addon.py` or another valid Python module name.

**Blender 4.x vs 5.x.**
The upstream addon (ahujasid/blender-mcp) supports both. This guide is tested on 5.1.1. If you hit a 4.x-specific issue, pin to an older addon commit.

**Port 9876 is already in use.**
Another Blender instance is still running. `pgrep -l -i blender` to find it, quit or kill it, then retry.

**Changed the config, Claude Desktop still doesn't see the server.**
You didn't fully quit. Closing the window is not enough — use Cmd+Q or `osascript -e 'tell application "Claude" to quit'`, then reopen.
