# Files inside a Sprite

As manually verified on 2026-08-12, the hosted Sprites MCP contract did not expose dedicated file upload, read, or write tools. Check the current `/mcp` tool list first; use a dedicated file tool if one is now available, otherwise perform filesystem work through `exec`. The [Remote MCP documentation](https://docs.sprites.dev/integrations/remote-mcp/#available-tools) notes that the Sprite-level tool list can change with environment versions.

## Preferred transfer methods

1. Clone or fetch a Git repository for real projects and multi-file trees.
2. Use base64 plus a space-free `python3 -c` expression for small generated files.
3. Use focused `cat`, `head`, `tail`, `wc`, and `ls` commands for reads.
4. Ask for an approved private-code transfer method when credentials are unavailable.

After any transfer, verify the destination and byte count or checksum. If a newly exposed dedicated file tool is absent from the tool map, hook, agent allowlist, or tests, use it directly only when its semantics are clear and report the contract drift for a plugin update.

The MCP `exec` command is represented as one string. Avoid heredocs, nested shell quoting, interactive prompts, and relying on stdin that the tool schema does not expose.

## Small-file write

Encode the content as base64 outside the Sprite, then run:

```text
mkdir -p /home/sprite/app
python3 -c __import__('pathlib').Path('/home/sprite/app/file.txt').write_bytes(__import__('base64').b64decode('BASE64_HERE'))
wc -c /home/sprite/app/file.txt
```

For many files, prefer Git or a base64-encoded archive followed by a simple extraction command. Never place credentials in HTTP-served paths, repository files, shell history, or world-readable files.
