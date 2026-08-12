# Services

Use Sprite services for web servers, workers, databases, daemons, and previews. Do not leave a forever-blocking `exec` as the lifecycle mechanism.

1. Inspect existing services with `service_list`.
2. Choose a stable role name such as `web`, `api`, `worker`, or `db`.
3. Create the service with `service_create`, setting its name, command, arguments, and working directory deliberately.
4. Set `http_port` only when the service should answer on the Sprite URL. Explain what will be exposed and request confirmation first.
5. Start with `service_start`.
6. Verify with `service_get` and `service_logs`.
7. Report service name, port, URL, authentication expectation, and health.

For builds or tests that may exceed the plugin's five-minute MCP timeout, a service can act as a durable worker. Alternatively, start a detached process that writes a log and exit-status file, and poll those files with short `exec` calls. Never keep a single tool call blocked indefinitely.

Read logs before restarting or rewriting a failing service. Never expose environment dumps, arbitrary file browsers, credentials, raw logs, admin endpoints, or Snowflake data through the Sprite URL.
