# blender-mcp-mac-setup

Guide plus bootstrap script that wires Blender to Claude Desktop over MCP on a Mac. README.md is the guide.

## Workflow

Read by the user-level `/spec`, `/next` and `/gaps` commands. One backlog item per fresh session.

- **Backlog files:** `BACKLOG.md` (the "Queue" section, top to bottom).
- **Session rules:** none beyond this block.
- **Verify:** `python3 -m py_compile bootstrap_blender_mcp.py`, then the guide steps on a real Blender install for any change to a command in the README. A claimed version or SHA comes from a command run that session.
- **Blocked markers:** "Needs owner" in an item text or under the "Needs owner" heading.
- **Commit and push:** stage by named path only. Push straight to main after `git fetch` shows nothing new upstream. No attribution lines.
- **Standing rules:** the upstream addon is pinned to a tested commit SHA and bumped only after a real run. Every command in the README has been executed on a Mac.
- **Lenses for `/gaps`:**
  1. `upstream`: pinned SHA versus upstream main, API changes.
  2. `versions`: Blender and Claude Desktop versions the guide was tested on.
  3. `commands`: README commands that fail when run.
  4. `ci`: what the workflow actually checks.
