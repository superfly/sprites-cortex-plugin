# Security policy

## Supported versions

Security fixes are applied to the latest release and the current `main` branch. Older plugin versions might not receive separate patches.

## Reporting a vulnerability

Do not report security vulnerabilities in a public issue, pull request, discussion, or Fly.io community post.

Use one of these private channels:

- Open a [private GitHub security advisory](https://github.com/superfly/sprites-cortex-plugin/security/advisories/new).
- Email [security@fly.io](mailto:security@fly.io) with `sprites-cortex-plugin` in the subject.

Include affected versions, reproduction steps, expected impact, and whether the issue concerns plugin instructions, OAuth, hooks, the hosted Sprites MCP server, or an interaction with Cortex Code. Do not send active tokens, browser cookies, Snowflake connection files, or production data. If a minimal secret-like fixture is essential, use an obviously fake value.

Fly.io's security contact is also documented in the [Fly.io security documentation](https://fly.io/docs/security/#talk-to-the-security-team).

## Scope

This repository stores no Sprites or Snowflake credentials. Cortex Code owns the OAuth credential flow and storage. Vulnerabilities in Snowflake Cortex Code itself should also be reported through Snowflake's security process; issues in the hosted Sprites MCP service can be reported through the Fly.io channels above.
