# Contributing

Contributions are welcome through the repository's normal issue and pull-request workflow.

## Development checks

Run these commands before opening a pull request:

```sh
python3 scripts/check_repository.py
python3 -m unittest discover -s tests -v
cortex plugin validate
```

Changes to MCP tool names, OAuth, hooks, agents, commands, or safety guidance must also complete the relevant parts of [the release checklist](docs/release-checklist.md). Keep the skill concise and move detailed workflow guidance into its existing reference files.

Do not commit tokens, Snowflake credentials, MCP credential caches, logs containing secrets, or generated test data. End-to-end tests must use a restricted connector and a non-production organization.
