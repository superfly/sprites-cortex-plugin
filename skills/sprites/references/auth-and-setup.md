# Authentication and setup

This plugin connects only to the Fly MCP at `https://mcp.fly.io`, requesting the `sprites:read` and `sprites:write` scopes. Cortex Code handles OAuth and stores resulting credentials in its configured credential store. Do not install the Sprites CLI or register a duplicate MCP server as a workaround.

The MCP configuration sets `authorization_server_url` to `https://fly.io/mcp/oauth` explicitly. As verified on 2026-11-13, that is the authorization server named by `https://mcp.fly.io/.well-known/oauth-protected-resource`, and the endpoint's unauthenticated `401` carries a `WWW-Authenticate` challenge pointing at that document. Recheck those live endpoints with [the release checklist](../../../docs/release-checklist.md) before changing this setting.

## First run

1. Install and enable the plugin.
2. Run `/plugin reload` or restart Cortex Code.
3. Run `/sprites-status` or ask Cortex to list Sprites.
4. Open `/mcp` if authorization is requested and complete browser OAuth for the intended Fly.io organization.
5. Review the consent screen's access level and any Sprite-name prefix and creation cap.

Releases up to 0.1.2 used `https://sprites.dev/mcp`. Its OAuth grant does not carry over: after updating, authorize `sprites` again in `/mcp` once.

An empty Sprite list means the integration is authenticated and working.

## Failure classes

### Tools missing

1. Confirm `sprites` is active with `/plugin` or `cortex plugin list`.
2. Run `/plugin reload`.
3. Inspect `/mcp` for the plugin-provided `sprites` server.
4. Ask an administrator whether plugin MCP servers are disabled or `https://mcp.fly.io` and its authorization server `https://fly.io/mcp/oauth` are absent from the managed URL allowlist. An allowlist written for `https://sprites.dev/mcp` does not cover them.

Do not use `sprite login`, raw API calls, `cortex mcp add`, or another MCP bridge to hide a plugin-loading or administrator-policy problem.

### OAuth incomplete

1. Open `/mcp` and authenticate `sprites`.
2. Select the correct organization and review connector restrictions.
3. Retry the original call once.

Never ask the user to paste tokens into prompts, shell commands, files, or Snowflake objects.

### Prefix or creation cap

Restricted tokens require a non-empty name prefix and may limit how many Sprites the connector can create.

- Read the required prefix from an API error; do not assume it.
- Retry a failed create once with the required prefix when the mapping is clear.
- Report the actual created name and remember the prefix for the session.
- Destroy only with explicit approval.
- Explain that Full access removes the prefix by granting organization-wide control.

### Wrong organization or hidden Sprite

Re-authenticate and verify the Fly.io organization. Restricted tokens can hide Sprites outside their configured prefix. Always operate on exact names returned by `list_sprites`.
