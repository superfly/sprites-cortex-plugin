# Remote compute

Use Sprites for isolated Linux builds, tests, generated or untrusted code, preview environments, native dependencies, and long-running services.

## Choose local, Snowflake, or Sprite compute

| Work | Prefer |
| --- | --- |
| Quick local reads and repository edits | Cortex workspace tools |
| SQL, RBAC, catalog, stages, governed data | Cortex Snowflake tools |
| Explicit remote or isolated execution | Sprite |
| Heavy installs, native binaries, generated code | Sprite |
| Persistent preview server or worker | Sprite service |
| Whole-environment rollback | Sprite checkpoint |

## Bootstrap

1. Call `list_sprites`; reuse a clear task match or create a descriptive task-scoped Sprite.
2. Probe only required tools with short commands such as `git --version`, `python3 --version`, or `node --version`.
3. Create a baseline checkpoint before large installs or risky execution.
4. Bring code in with `git clone` when possible. Ask how to access private code rather than inventing credentials.
5. Run finite work with `exec`; use services or a detached process plus bounded polling for processes that may exceed five minutes.
6. Verify with tests, status, logs, or health checks.

[Cortex Code caps MCP tool results at 50 KB](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-mcp#using-mcp-tools). Keep command output focused. For verbose builds or tests, redirect output to a file inside the Sprite and return a summary, failing section, or bounded `tail`.

The plugin configures a five-minute MCP call timeout. Do not use one blocking `exec` for a build that may exceed it. Prefer a service for a durable worker, or start a detached process that writes its exit status and log to files, then poll with short `exec` calls and bounded `tail` output. Set a clear maximum polling period, report when it is exceeded, and leave the process running only when the user wants that.

Use non-interactive flags so remote commands do not hang. Stop services that are no longer needed. Destroy a Sprite only with explicit intent.
