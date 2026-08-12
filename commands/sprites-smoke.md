---
description: Run a small end-to-end Sprites MCP check and preserve the created Sprite unless cleanup was explicitly approved.
---

Run an end-to-end Sprites MCP smoke test:

1. Call `list_sprites`; an empty list is valid.
2. Create a short-lived Sprite. If the OAuth prefix is unknown, prefer `mcp-smoke-<short-id>`. If the API returns a different required prefix, retry once with that exact prefix.
3. Run `echo smoke-ok` through `exec` and capture the exit status and one output line.
4. Keep the Sprite by default.
5. If the original request included cleanup, state the exact created Sprite name and irreversible impact, then ask for confirmation before destroying it. If cleanup was not requested, keep the Sprite and do not prompt for cleanup.

Report list, create, exec, cleanup, and learned-prefix results. Do not install packages, create services, change network policy, use the local shell as the Sprite, or call the REST API.
