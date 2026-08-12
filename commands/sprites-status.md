---
description: Check whether the Sprites MCP server is loaded and authenticated without changing remote state.
---

Perform a read-only Sprites health check:

1. Confirm that the plugin-provided Sprites MCP tools are available.
2. If they are missing, tell the user to check `/plugin`, run `/plugin reload`, and inspect `/mcp`. Do not install the Sprites CLI or register a second MCP server.
3. Call `list_sprites`.
4. If authorization is required, direct the user to `/mcp` to complete browser OAuth for the intended Fly.io organization, then retry once.
5. Report MCP availability, authentication state, and a compact list of Sprite names, states, and URLs. An empty list is a successful authenticated result.

Do not create, mutate, restore, stop, or destroy anything.
