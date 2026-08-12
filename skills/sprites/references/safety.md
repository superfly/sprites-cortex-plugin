# Safety

Sprites are persistent. Files, packages, databases, services, checkpoints, policies, and credentials can outlive the Cortex Code session.

## Confirm first

- Destroying a Sprite, which permanently deletes its state, services, checkpoints, and URL.
- Restoring a checkpoint, which discards filesystem changes made afterward.
- Replacing the outbound network policy.
- Creating a service with an HTTP port.
- Broad destructive filesystem, database, or package-manager operations.

Name the exact Sprite and impact before requesting approval.

The plugin's `PreToolUse` hook adds a second gate for these operations and for services that set `http_port`. The hook does not replace a clear explanation or the user's explicit intent.

## Checkpoint first

Create a labeled checkpoint before package upgrades, lockfile churn, database migrations, bulk file operations, service rewrites, network changes, and experiments with generated or untrusted code.

Before restoring an older checkpoint, offer to checkpoint the current state so the user has an explicit recovery point. Then confirm the exact target checkpoint and explain that restore rewinds the filesystem and stops or restarts affected services.

## Network policy

`policy_network_update` replaces the complete rule set. Read the current policy first, merge the requested change, and send the full intended policy. Do not silently discard existing rules.

## Snowflake credentials and data

- Do not copy Cortex session state, browser cookies, SSO tokens, `connections.toml`, keychain contents, or local credential files into a Sprite.
- Use a separately authorized, least-privileged Snowflake identity when remote integration testing is necessary.
- Scope access to the required account, role, warehouse, database, schema, and temporary objects.
- Prefer synthetic fixtures and stage references over unloading governed production data.
- Never print credentials or include them in MCP tool arguments, service definitions, logs, checkpoints, or URLs.

## Exposure

A Sprite URL is authenticated by default, but users can change that outside this plugin. Treat every URL as potentially exposed. Never serve secrets, environment variables, arbitrary files, debug endpoints, unfiltered logs, or user data.
