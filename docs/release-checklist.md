# Release checklist

Complete this checklist against the release commit. Record the Cortex Code version and date in the release notes because the Cortex plugin schema and hosted Sprite-level tool contract can change independently.

## Static validation

```sh
python3 scripts/check_repository.py
python3 -m unittest discover -s tests -v
cortex plugin validate
```

Confirm that all commands succeed and that the manifest version is the intended semantic version.

## OAuth discovery

1. Request `https://sprites.dev/mcp` without credentials. Confirm it returns `401`. If it still lacks `WWW-Authenticate`, keep `oauth.authorization_server_url` set to `https://sprites.dev`.
2. Fetch `https://sprites.dev/.well-known/oauth-protected-resource`. Confirm its `resource` is `https://sprites.dev/mcp`, its `authorization_servers` includes `https://sprites.dev`, and its scopes include `sprites:read` and `sprites:write`.
3. Fetch `https://sprites.dev/.well-known/oauth-authorization-server`. Confirm the issuer is `https://sprites.dev`, PKCE `S256` is supported, and authorization, token, and dynamic-registration endpoints are present.

## Cortex runtime

1. Update the pinned Cortex version, archive URL, and SHA-256 in `.github/workflows/ci.yml` to the current stable release using Snowflake's published manifest. Keep the archive checksummed so CI remains reproducible while each plugin release tests the latest supported schema.
2. Record `cortex --version` and confirm it matches the CI pin.
3. Launch `cortex --plugin-dir .` and run `/plugin list`; confirm `sprites` is active and its components are present.
4. Run `/plugin reload`, then open `/mcp`. Confirm the `sprites` server connects through browser OAuth.
5. Compare the exposed tool list with the tool map in `skills/sprites/SKILL.md`. As of 2026-08-12 the expected names were:
   - `list_sprites`, `create_sprite`, `destroy_sprite`
   - `exec`, `exec_list`, `exec_kill`
   - `checkpoint_create`, `checkpoint_list`, `checkpoint_get`, `checkpoint_restore`
   - `policy_network_get`, `policy_network_update`
   - `service_list`, `service_get`, `service_create`, `service_start`, `service_stop`, `service_logs`
6. If the contract changed, update the skill, hook matcher, agent tool allowlist, tests, and changelog together. Do not alias or guess changed names.

## Safe end-to-end checks

Use a restricted connector in a non-production organization.

1. Run `/sprites-status`; an empty list is success.
2. Run `/sprites-smoke` without requesting cleanup. Confirm create and exec succeed and the Sprite is kept.
3. Ask to clean up that exact smoke Sprite. Confirm the `PreToolUse` hook requires explicit approval before `destroy_sprite` and that the Sprite is removed only after approval.
4. On a disposable Sprite, attempt a checkpoint restore, complete network-policy replacement, and `service_create` with `http_port`. Cancel each at the hook gate; do not mutate the Sprite merely to test the prompt.
5. Delegate a verbose build to `sprites-runner`. Confirm full output remains inside the Sprite and the agent returns bounded output plus the log path.

## Publishing

The public source is `https://github.com/superfly/sprites-cortex-plugin`, and the documented install source is `superfly/sprites-cortex-plugin`.

For each release:

1. Update `CHANGELOG.md` and the manifest version.
2. Confirm the repository URL in the manifest still resolves to this repository.
3. Push the release commit and matching version tag.
4. From a clean environment, run `cortex plugin install superfly/sprites-cortex-plugin`, enable `sprites`, and confirm it appears in `cortex plugin list`.
5. Start a connected Cortex session and repeat `/sprites-status`. Record this separately when a Snowflake connection or browser OAuth is not available in CI.
