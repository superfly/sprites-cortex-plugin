from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
KEBAB_CASE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:[-+][0-9A-Za-z.-]+)?$")


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def scalar_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    block = text[4:].split("\n---\n", maxsplit=1)[0]
    return {
        match.group(1): match.group(2).strip(" \"'")
        for match in re.finditer(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.+)$", block, re.MULTILINE)
    }


class CortexPluginRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = load_json(ROOT / ".cortex-plugin/plugin.json")
        self.mcp = load_json(ROOT / ".mcp.json")

    def test_manifest_identity_and_version_are_valid(self) -> None:
        self.assertRegex(self.manifest["name"], KEBAB_CASE)
        self.assertRegex(self.manifest["version"], SEMVER)
        self.assertTrue(self.manifest["description"].strip())
        self.assertEqual(
            self.manifest["author"]["url"],
            "https://github.com/superfly/sprites-cortex-plugin",
        )

    def test_every_manifest_component_path_exists(self) -> None:
        expected_kinds = {
            "skills": "dir",
            "commands": "dir",
            "agents": "dir",
            "hooks": "file",
            "mcpServers": "file",
        }
        for field, kind in expected_kinds.items():
            values = self.manifest[field]
            if isinstance(values, str):
                values = [values]
            self.assertTrue(values, field)
            for value in values:
                target = ROOT / value
                self.assertTrue(target.is_dir() if kind == "dir" else target.is_file(), value)

    def test_mcp_uses_explicit_oauth_discovery(self) -> None:
        server = self.mcp["mcpServers"]["sprites"]
        parsed = urlparse(server["url"])
        self.assertEqual(server["type"], "http")
        self.assertEqual((parsed.scheme, parsed.netloc, parsed.path), ("https", "sprites.dev", "/mcp"))
        self.assertGreater(server["timeout"], 0)
        self.assertEqual(server["oauth"]["authorization_server_url"], "https://sprites.dev")
        self.assertTrue(server["oauth"]["client_name"])
        self.assertIn("sprites:read", server["oauth"]["scope"].split())
        self.assertIn("sprites:write", server["oauth"]["scope"].split())
        self.assertNotIn("client_id", server["oauth"])
        self.assertNotIn("headers", server)

    def test_all_commands_have_descriptions(self) -> None:
        commands = list((ROOT / "commands").glob("*.md"))
        self.assertGreaterEqual(len(commands), 2)
        for command in commands:
            self.assertRegex(command.stem, KEBAB_CASE)
            self.assertTrue(scalar_frontmatter(command).get("description"), command)

    def test_smoke_is_keep_by_default(self) -> None:
        text = (ROOT / "commands/sprites-smoke.md").read_text(encoding="utf-8")
        self.assertIn("Keep the Sprite by default", text)
        self.assertIn("original request included cleanup", text)
        self.assertIn("ask for confirmation before destroying", text)
        self.assertNotIn("argument-hint", text)
        self.assertNotIn("$ARGUMENTS", text)

    def test_hook_gates_each_high_risk_operation(self) -> None:
        hooks = load_json(ROOT / "hooks/hooks.json")
        entry = hooks["hooks"]["PreToolUse"][0]
        matcher = re.compile(entry["matcher"])
        for tool in (
            "destroy_sprite",
            "checkpoint_restore",
            "policy_network_update",
            "service_create",
            "service_start",
            "exec",
            "future_destructive_tool",
        ):
            self.assertIsNotNone(matcher.fullmatch(f"mcp__sprites__{tool}"), tool)
            self.assertIsNotNone(
                matcher.fullmatch(f"mcp__plugin_sprites_sprites__{tool}"), tool
            )
        prompt = entry["hooks"][0]["prompt"]
        self.assertIn("$ARGUMENTS", prompt)
        self.assertIn("explicit user confirmation", prompt)
        self.assertIn("offered a checkpoint of current state", prompt)
        self.assertIn("exact complete replacement rules", prompt)
        self.assertIn("existing service configuration was inspected", prompt)
        self.assertIn("cannot be classified confidently", prompt)
        self.assertEqual(entry["hooks"][0]["type"], "prompt")

    def test_runner_agent_is_bounded_and_cannot_destroy(self) -> None:
        path = ROOT / "agents/sprites-runner.md"
        text = path.read_text(encoding="utf-8")
        self.assertEqual(scalar_frontmatter(path)["name"], path.stem)
        self.assertIn("five minutes", text)
        self.assertIn("capped at 100 lines", text)
        self.assertIn("total deadline", text)
        self.assertIn("recorded PID", text)
        self.assertIn("do not use a broad process-name kill", text)
        self.assertIn("target/run_results.json", text)
        block = text[4:].split("\n---\n", maxsplit=1)[0]
        self.assertIn("mcp__sprites__exec", block)
        self.assertNotIn("destroy_sprite", block)
        self.assertNotIn("policy_network_update", block)
        self.assertNotIn("service_create", block)
        self.assertNotIn("service_start", block)

    def test_skill_reference_links_are_local_and_resolve(self) -> None:
        text = (ROOT / "skills/sprites/SKILL.md").read_text(encoding="utf-8")
        links = re.findall(r"\[[^\]]+\]\((references/[^)]+)\)", text)
        self.assertGreaterEqual(len(links), 6)
        for link in links:
            self.assertTrue((ROOT / "skills/sprites" / link).is_file(), link)

    def test_activation_metadata_exists(self) -> None:
        activation = ROOT / ".cortex-plugin/activation.md"
        self.assertTrue(activation.is_file())
        self.assertIn("/plugin enable sprites", activation.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
