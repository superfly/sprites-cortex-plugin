# Snowflake workflows

Use Cortex Code and Sprites as two coordinated execution planes. Cortex supplies Snowflake-aware authoring and governed account access; Sprites supplies persistent, isolated Linux compute.

## General workflow

1. Inspect the project and Snowflake context locally with Cortex tools.
2. Identify the work that actually requires remote Linux compute.
3. Create or reuse a task-specific Sprite and establish a baseline checkpoint.
4. Clone the project's original Git remote into the Sprite. A Snowflake Workspace or Snowflake Git repository filesystem is not automatically mounted in a Sprite.
5. Install only required tooling and run focused tests.
6. Use Cortex's Snowflake tools for SQL and account changes unless the user explicitly authorizes a separate remote Snowflake connection.
7. Return source changes through Git and return generated artifacts through an approved repository, Snowflake stage, or narrowly scoped transfer.

## dbt and database-change projects

- Distinguish standard dbt Core workflows from Snowflake-native dbt Project objects.
- Use a Sprite for dbt Core dependency resolution, compilation, linting, unit tests, and multi-runtime validation. Prefer the sequence `dbt debug`, dependency resolution, compilation, then tests so connection and parse failures are isolated early.
- Use Cortex's bundled Snowflake skills for deploying or operating Snowflake-native dbt and DCM objects.
- When integration tests mutate Snowflake, use a dedicated role and per-task database or schema with explicit cleanup approval.
- Keep complete dbt logs in the Sprite and return failure names, relevant paths, summary counts, and bounded excerpts. Do not enable database-side failure tables unless the user approves them.

## Streamlit, Snowflake Apps, and Native Apps

- Use a Sprite for local builds, package installation, browser-facing previews, and tests that require arbitrary system dependencies.
- Use Cortex's bundled application skills for Snowflake manifests, deployment, grants, and account-side validation.
- Do not represent a Sprite preview as equivalent to Snowflake authentication, RBAC, networking, or runtime behavior.

## Snowpark, connectors, and packaging

- Use a Sprite to build wheels, test supported Python versions, run linters, or exercise external connectors.
- Validate Snowflake runtime compatibility separately; a successful Linux build does not prove availability in Snowpark, SPCS, or a Notebook runtime.
- Keep credentials out of built artifacts and checkpoints.

## Integration authentication

Do not reuse Cortex's active connection. If a test must connect from the Sprite, ask the user to choose an approved authentication method and scope. Prefer short-lived or revocable credentials, least-privileged roles, explicit Snowflake hostname access, and temporary test objects.
