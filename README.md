<img src="assets/sprites-logo.svg" alt="Sprites" width="72" height="58">

# Sprites for Cortex Code

[![CI](https://github.com/superfly/sprites-cortex-plugin/actions/workflows/ci.yml/badge.svg)](https://github.com/superfly/sprites-cortex-plugin/actions/workflows/ci.yml)
[![Latest tag](https://img.shields.io/github/v/tag/superfly/sprites-cortex-plugin?label=version)](https://github.com/superfly/sprites-cortex-plugin/tags)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Use [Sprites](https://sprites.dev) from Snowflake Cortex Code as persistent, isolated Linux environments for builds, tests, sandboxes, previews, and Snowflake development workflows.

This Cortex Code plugin connects to the hosted Sprites MCP server with browser OAuth. It also contributes operating guidance, a long-work runner agent, a safety hook, and read-only status and end-to-end smoke commands. No Sprites CLI or pasted API token is required.

## Install

### Requirements

- [Cortex Code CLI](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-cli) with plugin and remote HTTP MCP support.
- A Fly.io account with access to a Sprites organization.
- A browser available for the first-run OAuth flow.

Install from GitHub and enable the plugin:

```sh
cortex plugin install superfly/sprites-cortex-plugin
cortex plugin enable sprites
```

Run `/plugin reload` inside an existing session or restart Cortex Code. Both workflows are documented in the [Cortex Code plugin guide](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-plugins#managing-plugins).

For local development from a checkout instead:

```sh
cortex --plugin-dir /path/to/sprites-cortex-plugin
```

## First use

1. Run `/sprites-status` or ask Cortex Code to list your Sprites.
2. Open `/mcp` if authorization is requested.
3. Authenticate with Fly.io, select the intended organization, and review the access you are granting, including any Sprite name-prefix and creation-cap restrictions.
4. Treat an empty list as success: the connector is authenticated and no Sprites are visible under its policy.

The plugin connects to the Fly MCP at `https://mcp.fly.io` and requests only the `sprites:read` and `sprites:write` scopes. The Fly MCP can also serve other Fly.io tools when broader access is granted at consent; this plugin does not request it.

`.mcp.json` pins the OAuth authorization server, `https://fly.io/mcp/oauth`, explicitly. That is the issuer the endpoint's protected-resource metadata names, and pinning it keeps authorization independent of how Cortex handles the `401` discovery challenge.

### Upgrading from 0.1.2 or earlier

Earlier releases connected to `https://sprites.dev/mcp`. We are transitioning to the new Fly MCP server at `https://mcp.fly.io`. The two endpoints have separate OAuth grants, so after updating the plugin every user must open `/mcp` and authorize `sprites` once more. Tool names are unchanged, so existing permission rules for `mcp__sprites__*` keep working. Administrators must allow the new URLs first; see [Enterprise deployment](#enterprise-deployment).

## What it provides

- Hosted MCP access to Sprites through the Fly MCP at `https://mcp.fly.io`.
- Persistent, isolated Linux compute without treating the local Cortex shell as the Sprite.
- Guidance for commands, services, files, checkpoints, and network policy.
- `sprites-runner`, a bounded-output agent for long builds and tests.
- A `PreToolUse` hook that gates destructive, restore, policy, exposure, and broad persistent operations.
- Snowflake-aware boundaries for SQL, RBAC, stages, credentials, and governed data.
- `/sprites-status` for a read-only integration check.
- `/sprites-smoke` for list, create, and exec; the created Sprite is kept unless cleanup was explicitly requested and confirmed.

## Example prompts

- "Create a Sprite for this dbt Core project and run compilation and unit tests."
- "Use the sprites-runner agent to build this Snowpark wheel for every supported Python version."
- "Run generated migration code in a checkpointed Sprite before we review it."
- "Start this Streamlit project as a Sprite preview, without copying production data."
- "List the services and recent logs on my integration-test Sprite."

## How Cortex Code and Sprites divide the work

Cortex Code's local and Snowflake-native tools remain responsible for project editing, SQL, RBAC, catalog inspection, stages, and deployments. Sprites provide remote Linux execution for dependency-heavy, persistent, generated, or untrusted workloads.

The plugin does not copy Cortex's Snowflake session or credentials into a Sprite. If an integration test must connect from a Sprite, configure a separate least-privileged identity intentionally and keep governed data in Snowflake.

## OAuth restrictions

Restricted connector tokens use a non-empty Sprite-name prefix and may cap how many Sprites the connector can create. The common default is `mcp-`, but the plugin learns the actual rule from the API instead of assuming it.

Full access removes the prefix by granting control over every Sprite in the organization. Prefer restricted access for day-to-day agent work. See the [Sprites Remote MCP documentation](https://docs.sprites.dev/integrations/remote-mcp/) for the live connector contract.

## Safety

- Destroying a Sprite is irreversible.
- Restoring a checkpoint discards newer filesystem state.
- Network-policy updates replace the full policy.
- Services with an HTTP port can expose content through the Sprite URL.
- Checkpoint before risky package installs, migrations, bulk edits, and generated-code execution.
- Never expose secrets, environment dumps, arbitrary files, raw logs, or Snowflake data through a Sprite service.

Cortex Code's normal MCP permission flow still applies. The plugin hook adds a policy check; it does not weaken or auto-approve Cortex permissions. The hook intentionally evaluates every `mcp__sprites__*` call, including read-only calls, so a new or renamed destructive tool cannot bypass the guard. This adds one prompt-hook model evaluation per Sprites call, with a 30-second hook timeout. Organizations can further restrict the plugin and `https://mcp.fly.io` through connection profiles and managed settings.

## Long-running work and output

The plugin sets a five-minute MCP call timeout. Work that might outlast it should use a Sprite service or detached process and bounded polling instead of one blocking `exec`. Cortex also [caps MCP tool results at 50 KB](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-mcp#using-mcp-tools), so verbose output should remain in a Sprite log file while Cortex receives a summary and small failure excerpt.

## Enterprise deployment

Plugin-declared MCP servers can be disabled by administrators. Managed environments should allow the MCP endpoint `https://mcp.fly.io` and its OAuth authorization server under `https://fly.io/mcp/oauth`, and may distribute the plugin or an equivalent MCP definition through a Snowflake connection profile. [Cortex Extensions can also store plugins with role-governed access](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/plugins).

Environments that allowlisted `https://sprites.dev/mcp` for 0.1.2 or earlier must add the new URLs before users update; the old entry can be removed once no user remains on an earlier release.

## Troubleshooting

If tools are missing:

1. Confirm `sprites` is active with `cortex plugin list` or `/plugin`.
2. Run `/plugin reload` in the active session or restart Cortex Code.
3. Inspect `/mcp` for the `sprites` server and its last error.
4. Ask whether administrator settings disable plugin MCP servers or block the endpoint URL.

If OAuth is stale, remove and reinstall the plugin-provided MCP configuration through the supported Cortex plugin/MCP flow, then authenticate again. Do not install the Sprites CLI, add a duplicate MCP server, or paste tokens into a shell.

## Support and feedback

- Report reproducible plugin bugs with the [bug report form](https://github.com/superfly/sprites-cortex-plugin/issues/new?template=bug_report.yml).
- Propose workflow or integration improvements with the [feature request form](https://github.com/superfly/sprites-cortex-plugin/issues/new?template=feature_request.yml).
- Ask general Sprites questions in the [Fly.io community](https://community.fly.io/) after checking the [Sprites documentation](https://docs.sprites.dev/).
- Report security issues privately as described in [SECURITY.md](SECURITY.md). Never include credentials or production data in an issue.

## Development

```sh
python3 scripts/check_repository.py
python3 -m unittest discover -s tests -v
cortex plugin validate
```

The first two checks are dependency-free. The final check requires Cortex Code CLI. Before a release, also complete [the live contract checklist](docs/release-checklist.md).

## Repository layout

```text
.cortex-plugin/       Cortex manifest and inactive-plugin activation text
.mcp.json             Hosted Sprites MCP and OAuth configuration
agents/               Long-running Sprites runner
commands/             /sprites-status and /sprites-smoke
hooks/                PreToolUse safety policy
skills/sprites/       Core operating guidance and Snowflake references
assets/               Sprites logo
docs/                 Release and live-contract checklist
scripts/              Repository validation
tests/                Semantic and structural tests
```

## Project policies

See [CONTRIBUTING.md](CONTRIBUTING.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), [SECURITY.md](SECURITY.md), [SUPPORT.md](SUPPORT.md), and [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE) © Fly.io, Inc.
