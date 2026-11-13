# Changelog

All notable changes to this project are documented here.

## Unreleased

- Connect to the Fly MCP at `https://mcp.fly.io` instead of `https://sprites.dev/mcp`, as part of the transition to the new Fly MCP server. The server key, tool names, and requested scopes (`sprites:read sprites:write`) are unchanged.
- Pin the OAuth authorization server to `https://fly.io/mcp/oauth`, the issuer named by the new endpoint's protected-resource metadata.
- Upgrade note: the two endpoints have separate OAuth grants, so every existing user must authorize `sprites` again in `/mcp` once after updating.
- Upgrade note: administrators of managed environments must allow `https://mcp.fly.io` and `https://fly.io/mcp/oauth` before users update.

## 0.1.2 - 2026-08-12

- Add public contribution, support, conduct, security-reporting, ownership, and issue/PR guidance.
- Add automated GitHub Actions dependency updates and repository checks for community-health files.
- Make tests independent of the caller's working directory and refresh pinned CI actions.
- Document reproducible Cortex CLI pin maintenance in the release checklist.

## 0.1.1 - 2026-08-12

- Use Cortex's documented `mcp__sprites__*` namespace consistently in hooks, agents, and tests.
- Classify Sprite creation explicitly while retaining catch-all protection for new MCP tools.
- Document the prompt-hook latency tradeoff and the now-public Git installation flow.
- Pin the optional Cortex CI validation to a checksummed CLI archive.
- Accept documented skill tool allowlists and YAML block descriptions in repository validation.

## 0.1.0 - 2026-08-12

- Add hosted Sprites MCP configuration with explicit OAuth authorization-server discovery.
- Add Cortex commands for status and a safe, keep-by-default smoke test.
- Add Snowflake-aware Sprites workflow guidance and bounded long-running execution guidance.
- Add the `sprites-runner` agent and `PreToolUse` safety hook.
- Add repository validation, semantic tests, Cortex CLI validation in CI, and a live release checklist.
