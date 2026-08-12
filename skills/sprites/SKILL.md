---
name: sprites
description: Use Sprites from Cortex Code for persistent isolated Linux compute, remote builds and tests, generated or untrusted code, preview services, checkpoints, and Snowflake project development. Invoke when the user mentions Sprites, remote sandboxes, cloud development environments, agent compute, running work away from the local machine, or asks to test dbt, Streamlit, Snowpark, Native App, or other Snowflake projects in an isolated environment.
---

# Sprites

Use the hosted Sprites MCP tools as the control plane for remote environments. Cortex Code remains outside the Sprite.

## Golden path

1. Call Sprites MCP tools directly. Do not use the local shell, curl, the Sprites CLI, `cortex mcp add`, or a second MCP bridge for normal Sprite work.
2. Keep contexts separate:
   - Cortex workspace: local project files and Cortex's Snowflake connection.
   - Sprites MCP: operations against the hosted control plane.
   - Sprite filesystem: remote state reached only through Sprite-scoped tools.
3. Discover read-only state first. Reuse a clear task-specific Sprite or create one when requested or when isolation matters.
4. Use `exec` for finite commands that will finish well within the five-minute MCP timeout. Use a Sprite service, detached process, or bounded polling for longer work.
5. Create a checkpoint before package upgrades, migrations, bulk edits, service rewrites, network changes, or generated-code experiments.
6. Verify with tests, health checks, service status, or logs. Report exact Sprite, service, checkpoint, and URL identifiers.

After selecting or creating the exact Sprite, taking any required checkpoint, and establishing the working directory, delegate long, verbose, or multi-step builds and tests to the `sprites-runner` agent. Give it a self-contained task with a total deadline and expected result format. Perform file transfer in the main conversation when the current dedicated file tool is not in the runner's allowlist.

If tools are missing or OAuth fails, read [references/auth-and-setup.md](references/auth-and-setup.md) and stop workaround attempts. Empty `list_sprites` is authenticated success.

## Tool map

The names below were manually verified against the hosted server on 2026-08-12. The [Sprites Remote MCP documentation](https://docs.sprites.dev/integrations/remote-mcp/#available-tools) is the source of truth for categories, and the tools exposed in the current Cortex session are authoritative when names change.

- Organization: `list_sprites`, `create_sprite`, and `destroy_sprite`.
- Commands: `exec`, `exec_list`, and `exec_kill`.
- Services: `service_list`, `service_get`, `service_create`, `service_start`, `service_stop`, and `service_logs`.
- Checkpoints: `checkpoint_create`, `checkpoint_list`, `checkpoint_get`, and `checkpoint_restore`.
- Network: `policy_network_get` and `policy_network_update`.

Do not guess a replacement tool name. When the hosted server exposes a different contract, inspect `/mcp`, select the clearly corresponding available tool, and report the drift. Sprite-scoped tools normally take `sprite`; create and destroy normally take `name`.

Restricted OAuth access normally enforces a non-empty name prefix and may cap creation. Try a user-supplied name exactly once. If the API returns a required prefix, retry once with that prefix when unambiguous and report the actual name. Full access removes the prefix but grants organization-wide control; never present it as a harmless naming option.

## Snowflake division of responsibility

Use Cortex Code's Snowflake tools for SQL, RBAC, catalog inspection, stages, and deployment. Use Sprites for Linux tooling, builds, tests, native dependencies, generated code, and preview services.

Do not copy Cortex's current Snowflake session, browser SSO state, or credentials into a Sprite. Connecting a Sprite to Snowflake requires separately configured, least-privileged authentication and explicit user intent. Keep governed data in Snowflake; transfer only narrowly scoped fixtures or staged artifacts.

Read [references/snowflake-workflows.md](references/snowflake-workflows.md) for dbt, Streamlit, Snowpark, Native App, or integration-test work.

## References

- Read [references/compute.md](references/compute.md) for builds, tests, and environment bootstrapping.
- Read [references/files.md](references/files.md) before transferring or generating files in a Sprite.
- Read [references/services.md](references/services.md) before creating or changing long-running services.
- Read [references/safety.md](references/safety.md) before destructive, restore, exposure, credential, or network-policy work.
