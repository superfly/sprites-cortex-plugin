# Contributing

Thanks for helping improve Sprites for Cortex Code. By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Before opening a change

- Search existing issues and pull requests before filing a duplicate.
- Use the bug or feature issue form for changes that need design discussion.
- Do not open a public issue for a security vulnerability; follow [SECURITY.md](SECURITY.md).

Small, focused pull requests are easiest to review. Explain the user-facing problem, why the change belongs in this plugin, and any Cortex or Sprites contract assumptions it introduces.

## Pull requests

1. Fork or branch from `main`.
2. Make the smallest coherent change.
3. Add or update semantic tests and documentation.
4. Run the development checks below.
5. Open a pull request and complete its checklist.

Contributions are licensed under the repository's [MIT License](LICENSE). By submitting a contribution, you agree that it may be distributed under that license.

## Development checks

Run these commands before opening a pull request:

```sh
python3 scripts/check_repository.py
python3 -m unittest discover -s tests -v
cortex plugin validate
```

Changes to MCP tool names, OAuth, hooks, agents, commands, or safety guidance must also complete the relevant parts of [the release checklist](docs/release-checklist.md). Keep the skill concise and move detailed workflow guidance into its existing reference files.

Do not commit tokens, Snowflake credentials, MCP credential caches, logs containing secrets, or generated test data. End-to-end tests must use a restricted connector and a non-production organization.

## Review and merging

Pull requests must pass required CI, resolve review conversations, and receive the approvals required by the `main` branch protection. Maintainers generally squash-merge changes and delete merged branches.
