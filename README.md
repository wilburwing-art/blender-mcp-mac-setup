# Blender MCP — Mac Setup

Wire Blender to Claude Desktop via MCP, then drive it with voice.

Each phase is a natural stopping point if you hit friction.

## Phase 1: Install the pieces

1. **Blender**: download from [blender.org](https://www.blender.org/download/) and drag to Applications (grab 4.x).
2. **Claude Desktop**: [claude.ai/download](https://claude.ai/download) — the mobile or web app can't run MCP servers, has to be desktop.
3. **uv** (provides the `uvx` command the MCP server needs): in Terminal run `brew install uv`, or if you don't have Homebrew: `curl -LsSf https://astral.sh/uv/install.sh | sh`.
4. Confirm `uvx` is installed: `which uvx`. Copy that full path somewhere, you'll need it.

## Phase 2: Install the Blender addon

1. Go to [github.com/ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp) and download `addon.py` from the repo.
2. Open Blender, go to **Edit > Preferences > Add-ons > Install from Disk**, pick `addon.py`.
3. Tick the checkbox to enable **Interface: Blender MCP**.
4. Close preferences, press **N** in the 3D viewport, you'll see a **BlenderMCP** tab in the sidebar. Don't click Start yet.

## Phase 3: Configure Claude Desktop

Open the config file in Terminal:

```bash
open -e ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

If it doesn't exist, create it. Paste:

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

Replace `/full/path/to/uvx` with what `which uvx` gave you. Using the full path instead of just `"uvx"` avoids the most common macOS gotcha where Claude Desktop can't find it.

Fully quit Claude Desktop (**Cmd+Q**, not just close the window) and reopen it.

## Phase 4: First run

1. In Blender, click **Start MCP Server** in the BlenderMCP sidebar. It should say `MCP Server started on port 9876`.
2. In Claude Desktop, start a new chat. You should see a tools icon indicating Blender MCP is connected.
3. Type `get scene information` as your first test. If that works, you're wired up.

## Phase 5: Voice

On macOS the fastest path is built-in dictation: **System Settings > Keyboard > Dictation**, turn on, set a shortcut (double-tap `fn` works well). Then in Claude Desktop, double-tap `fn` and talk.

Whisper-based alternatives like [Superwhisper](https://superwhisper.com/) or [MacWhisper](https://goodsnooze.gumroad.com/l/macwhisper) are better quality and worth upgrading to later.

## Phase 6: A file to play with

Grab the **Classroom** or **Junk Shop** demo from [blender.org/download/demo-files](https://www.blender.org/download/demo-files/), open it in Blender, then try voice commands like:

- "describe the scene"
- "add a bright orange cube floating above the main desk"
- "change the world background to a sunset HDRI from Poly Haven"

## Troubleshooting

Work through Phase 1 to 4 first. If something breaks, the error message usually tells the story — capture it and work from there.
