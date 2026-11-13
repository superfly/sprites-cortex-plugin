#!/usr/bin/env python3
"""Dependency-free semantic validation for the Cortex Code plugin repository."""

from __future__ import annotations

import json
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SKIPPED = {".git", "__pycache__", ".pytest_cache", ".ruff_cache"}
TEXT_SUFFIXES = {".json", ".md", ".py", ".svg", ".txt", ".yaml", ".yml"}
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
KEBAB_CASE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


class DuplicateKeyError(ValueError):
    """Raised when a JSON object contains duplicate keys."""


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate key {key!r}")
        result[key] = value
    return result


def repository_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file() and not SKIPPED.intersection(path.relative_to(ROOT).parts)
    )


def local_markdown_target(raw: str) -> str | None:
    value = raw.strip()
    if value.startswith("<") and value.endswith(">"):
        value = value[1:-1]
    elif " " in value:
        value = value.split(" ", maxsplit=1)[0]
    value = urllib.parse.unquote(value.split("#", maxsplit=1)[0])
    if not value or value.startswith(("http://", "https://", "mailto:")):
        return None
    return value


def frontmatter(path: Path, text: str, errors: list[str]) -> dict[str, Any] | None:
    relative = path.relative_to(ROOT)
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        errors.append(f"{relative}: missing YAML frontmatter")
        return None

    block = text[4:].split("\n---\n", maxsplit=1)[0]
    result: dict[str, Any] = {}
    current: str | None = None
    lines = block.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        key_match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s*(.*))?$", line)
        if key_match:
            key, raw_value = key_match.groups()
            if key in result:
                errors.append(f"{relative}: duplicate frontmatter key {key!r}")
                index += 1
                continue
            scalar = raw_value.strip() if raw_value else ""
            if scalar in {">", ">-", ">+", "|", "|-", "|+"}:
                block_lines: list[str] = []
                index += 1
                while index < len(lines) and (
                    not lines[index].strip() or lines[index][0].isspace()
                ):
                    block_lines.append(lines[index].lstrip())
                    index += 1
                if scalar.startswith(">"):
                    result[key] = " ".join(part for part in block_lines if part).strip()
                else:
                    result[key] = "\n".join(block_lines).strip()
                current = None
                continue
            result[key] = scalar.strip(" \"'") if scalar else []
            current = key
            index += 1
            continue
        list_match = re.match(r"^\s*-\s+(.+)$", line)
        if list_match and current is not None and isinstance(result[current], list):
            result[current].append(list_match.group(1).strip(" \"'"))
            index += 1
            continue
        if line.strip():
            errors.append(f"{relative}: unsupported frontmatter line {line!r}")
        index += 1
    return result


def validate_skill(path: Path, text: str, errors: list[str]) -> None:
    relative = path.relative_to(ROOT)
    data = frontmatter(path, text, errors)
    if data is None:
        return
    if data.get("name") != path.parent.name:
        errors.append(f"{relative}: name must match directory {path.parent.name!r}")
    if not data.get("description"):
        errors.append(f"{relative}: description must be non-empty")
    unsupported = set(data) - {"name", "description", "tools"}
    if unsupported:
        errors.append(
            f"{relative}: unsupported frontmatter keys: {', '.join(sorted(unsupported))}"
        )
    tools = data.get("tools")
    if tools is not None and not (
        tools == "*"
        or (
            isinstance(tools, list)
            and tools
            and all(isinstance(tool, str) and tool for tool in tools)
        )
    ):
        errors.append(f"{relative}: tools must be '*' or a non-empty YAML list")


def validate_command(path: Path, text: str, errors: list[str]) -> None:
    relative = path.relative_to(ROOT)
    data = frontmatter(path, text, errors)
    if data is None:
        return
    if not KEBAB_CASE.fullmatch(path.stem):
        errors.append(f"{relative}: command filename must be lowercase kebab-case")
    if not data.get("description"):
        errors.append(f"{relative}: description must be non-empty")


def validate_agent(path: Path, text: str, errors: list[str]) -> None:
    relative = path.relative_to(ROOT)
    data = frontmatter(path, text, errors)
    if data is None:
        return
    if data.get("name") != path.stem or not KEBAB_CASE.fullmatch(path.stem):
        errors.append(f"{relative}: name must match its lowercase kebab-case filename")
    if not data.get("description"):
        errors.append(f"{relative}: description must be non-empty")
    tools = data.get("tools")
    if not isinstance(tools, list) or not tools:
        errors.append(f"{relative}: tools must be a non-empty YAML list")
    if not data.get("model"):
        errors.append(f"{relative}: model must be non-empty")


def manifest_paths(
    manifest: dict[str, Any], field: str, kind: str, errors: list[str]
) -> None:
    raw_paths = manifest.get(field)
    if isinstance(raw_paths, str):
        raw_paths = [raw_paths]
    if not isinstance(raw_paths, list) or not raw_paths:
        errors.append(f".cortex-plugin/plugin.json: {field} must name at least one path")
        return
    for raw in raw_paths:
        if not isinstance(raw, str) or not raw.startswith("./"):
            errors.append(
                f".cortex-plugin/plugin.json: {field} path must start with './': {raw!r}"
            )
            continue
        target = (ROOT / raw).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f".cortex-plugin/plugin.json: {field} escapes repository: {raw!r}")
            continue
        valid = target.is_dir() if kind == "directory" else target.is_file()
        if not valid:
            errors.append(
                f".cortex-plugin/plugin.json: {field} {kind} does not exist: {raw!r}"
            )


def validate_manifest(errors: list[str]) -> None:
    path = ROOT / ".cortex-plugin/plugin.json"
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    except (OSError, json.JSONDecodeError, DuplicateKeyError):
        return
    if not isinstance(manifest, dict):
        errors.append(".cortex-plugin/plugin.json: manifest must be an object")
        return

    name = manifest.get("name")
    if not isinstance(name, str) or not KEBAB_CASE.fullmatch(name):
        errors.append(".cortex-plugin/plugin.json: name must be lowercase kebab-case")
    version = manifest.get("version")
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        errors.append(".cortex-plugin/plugin.json: version must be valid semantic versioning")
    if not isinstance(manifest.get("description"), str) or not manifest["description"].strip():
        errors.append(".cortex-plugin/plugin.json: description must be non-empty")

    author = manifest.get("author")
    if not isinstance(author, dict) or not author.get("name"):
        errors.append(".cortex-plugin/plugin.json: author.name must be non-empty")
    else:
        parsed = urllib.parse.urlparse(str(author.get("url", "")))
        if parsed.scheme != "https" or not parsed.netloc:
            errors.append(".cortex-plugin/plugin.json: author.url must be an HTTPS URL")

    manifest_paths(manifest, "skills", "directory", errors)
    manifest_paths(manifest, "commands", "directory", errors)
    manifest_paths(manifest, "agents", "directory", errors)
    manifest_paths(manifest, "hooks", "file", errors)
    manifest_paths(manifest, "mcpServers", "file", errors)


def validate_mcp(errors: list[str]) -> None:
    path = ROOT / ".mcp.json"
    try:
        document = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        server = document["mcpServers"]["sprites"]
    except (OSError, KeyError, TypeError, json.JSONDecodeError, DuplicateKeyError):
        return
    if server.get("type") != "http" or server.get("url") != "https://mcp.fly.io":
        errors.append(".mcp.json: sprites must use HTTP at https://mcp.fly.io")
    timeout = server.get("timeout")
    if not isinstance(timeout, int) or timeout <= 0:
        errors.append(".mcp.json: timeout must be a positive integer")
    oauth = server.get("oauth")
    if not isinstance(oauth, dict):
        errors.append(".mcp.json: sprites OAuth configuration is required")
        return
    if oauth.get("authorization_server_url") != "https://fly.io/mcp/oauth":
        errors.append(
            ".mcp.json: oauth.authorization_server_url must be https://fly.io/mcp/oauth"
        )
    if not oauth.get("client_name") or not oauth.get("scope"):
        errors.append(".mcp.json: OAuth client_name and scope must be non-empty")
    if "client_id" in oauth or "headers" in server:
        errors.append(".mcp.json: do not commit OAuth client credentials or auth headers")


def main() -> int:
    errors: list[str] = []
    files = repository_files()

    required = {
        ROOT / ".cortex-plugin/plugin.json",
        ROOT / ".cortex-plugin/activation.md",
        ROOT / ".mcp.json",
        ROOT / "agents/sprites-runner.md",
        ROOT / "commands/sprites-status.md",
        ROOT / "commands/sprites-smoke.md",
        ROOT / "hooks/hooks.json",
        ROOT / "skills/sprites/SKILL.md",
        ROOT / "docs/release-checklist.md",
        ROOT / "CHANGELOG.md",
        ROOT / "CODE_OF_CONDUCT.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / "SECURITY.md",
        ROOT / "SUPPORT.md",
        ROOT / ".github/CODEOWNERS",
        ROOT / ".github/dependabot.yml",
        ROOT / ".github/pull_request_template.md",
        ROOT / ".github/ISSUE_TEMPLATE/bug_report.yml",
        ROOT / ".github/ISSUE_TEMPLATE/config.yml",
        ROOT / ".github/ISSUE_TEMPLATE/feature_request.yml",
    }
    for path in sorted(required):
        if not path.is_file():
            errors.append(f"missing required file {path.relative_to(ROOT)}")

    for path in files:
        relative = path.relative_to(ROOT)
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"{relative}: invalid UTF-8 ({exc})")
            continue
        if text and not text.endswith("\n"):
            errors.append(f"{relative}: missing final newline")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if line != line.rstrip():
                errors.append(f"{relative}:{line_number}: trailing whitespace")

        if path.suffix == ".json":
            try:
                json.loads(text, object_pairs_hook=unique_object)
            except (json.JSONDecodeError, DuplicateKeyError) as exc:
                errors.append(f"{relative}: invalid JSON ({exc})")
        elif path.suffix == ".svg":
            try:
                ET.fromstring(text)
            except ET.ParseError as exc:
                errors.append(f"{relative}: invalid SVG ({exc})")

        if path.suffix == ".md":
            for match in MARKDOWN_LINK.finditer(text):
                target = local_markdown_target(match.group(1))
                if target is not None and not (path.parent / target).resolve().exists():
                    errors.append(f"{relative}: broken local link {target!r}")
        if path.name == "SKILL.md":
            validate_skill(path, text, errors)
        elif path.parent == ROOT / "commands" and path.suffix == ".md":
            validate_command(path, text, errors)
        elif path.parent == ROOT / "agents" and path.suffix == ".md":
            validate_agent(path, text, errors)

    validate_manifest(errors)
    validate_mcp(errors)

    if errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(files)} repository files and plugin semantics.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
