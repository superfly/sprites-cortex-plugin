# Changelog

All notable changes to this project are documented here.

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
