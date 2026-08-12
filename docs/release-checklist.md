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

1. Record `cortex --version`.
2. Launch `cortex --plugin-dir .` and run `/plugin info sprites`.
3. Run `/plugin reload`, then open `/mcp`. Confirm the `sprites` server connects through browser OAuth.
4. Compare the exposed tool list with the tool map in `skills/sprites/SKILL.md`. As of 2026-08-12 the expected names were:
   - `list_sprites`, `create_sprite`, `destroy_sprite`
   - `exec`, `exec_list`, `exec_kill`
   - `checkpoint_create`, `checkpoint_list`, `checkpoint_get`, `checkpoint_restore`
   - `policy_network_get`, `policy_network_update`
   - `service_list`, `service_get`, `service_create`, `service_start`, `service_stop`, `service_logs`
5. If the contract changed, update the skill, hook matcher, agent tool allowlist, tests, and changelog together. Do not alias or guess changed names.

## Safe end-to-end checks

Use a restricted connector in a non-production organization.

1. Run `/sprites-status`; an empty list is success.
2. Run `/sprites-smoke` without requesting cleanup. Confirm create and exec succeed and the Sprite is kept.
3. Ask to clean up that exact smoke Sprite. Confirm the `PreToolUse` hook requires explicit approval before `destroy_sprite` and that the Sprite is removed only after approval.
4. On a disposable Sprite, attempt a checkpoint restore, complete network-policy replacement, and `service_create` with `http_port`. Cancel each at the hook gate; do not mutate the Sprite merely to test the prompt.
5. Delegate a verbose build to `sprites-runner`. Confirm full output remains inside the Sprite and the agent returns bounded output plus the log path.

## Publishing

1. Update `CHANGELOG.md` and the manifest version.
2. Confirm the repository URL in the manifest resolves to this repository.
3. Push the release commit and tag before documenting `cortex plugin install superfly/sprites-cortex-plugin` as generally available.
4. Verify a clean Git-based install, enable the plugin, and repeat `/sprites-status`.
