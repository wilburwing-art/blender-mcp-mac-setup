# blender-mcp-mac-setup session backlog

The queue for one-item-per-session work. Written 2026-11-17 from measurements on that date: 6 tracked files (`README.md` 156 lines, `bootstrap_blender_mcp.py` 52, `.github/workflows/check.yml` 31), 17 commits all from 2026-04-19, CI green on the last push, `python3 -m py_compile bootstrap_blender_mcp.py` passes, no tests. The README pins upstream `ahujasid/blender-mcp` `addon.py` to commit `7636d13`; upstream `main` is at `b6a2ce3` (2026-11-15).

**How to read it**

- Take the first unticked item in "Queue" from the top that is not marked "Needs owner". One item per session.
- Estimates are hours for one session. Check with `python3 -m py_compile bootstrap_blender_mcp.py` and the CI workflow.

## Queue

- [ ] **1. Re-test the guide against current upstream.** ~2 h. Diff `addon.py` between `7636d13` and `main` (`gh api repos/ahujasid/blender-mcp/compare/7636d13...main`), read the changes that touch addon startup or the MCP port, run Phase 2 through Phase 4 on the installed Blender, and bump `ADDON_SHA` only if the scripted install still works. Done: the pin is either bumped to a tested commit or left with a dated note saying why, and the README states the Blender version tested.

- [ ] **2. Re-verify the Claude Desktop config section.** ~1 h. The README's `claude_desktop_config.json` snippet and the `uvx` path steps predate seven months of Claude Desktop changes. Done: the snippet matches what Claude Desktop reads today, checked by a real connection.

- [ ] **3. Add a smoke check to CI.** ~2 h. CI compiles the bootstrap and validates README JSON only. Add a step that confirms the pinned SHA still resolves on raw.githubusercontent.com. Done: the workflow fails when the pin 404s.

## Needs owner

- **Whether this guide stays maintained** or is archived once voice-to-blender supersedes it.
