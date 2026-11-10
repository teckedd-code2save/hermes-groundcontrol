# GroundControl for Hermes

Operate your own deployments through GroundControl's scoped MCP connection, with a clear operating workflow and conservative evidence receipts.

## What this package adds

- A native `/groundcontrol` command with setup guidance and a local JSON evidence receipt.
- A namespaced `groundcontrol:operate` skill covering capability discovery, exact approvals, idempotency, reconnecting to durable operations and honest public verification.
- A read-only MCP configuration example. Hermes owns OAuth and transport; GroundControl owns resource grants and execution.

This package does not automatically connect, modify configuration, enable write tools, create grants, install itself, or change your deployments. It is a workflow companion, not a second MCP implementation or autonomous SRE.

## Setup

Requires Hermes 0.17.0 or later for the native command/skill APIs. The source is published at https://github.com/teckedd-code2save/hermes-groundcontrol. Catalog admission is pending maintainer review. Install a reviewed revision through `hermes plugins install https://github.com/teckedd-code2save/hermes-groundcontrol --no-enable`, then explicitly enable `groundcontrol` using the installed version's plugin controls. Do not substitute an unreviewed repository URL.

Merge `examples/read-only.yaml` into the selected Hermes profile only after replacing its URL with your own HTTPS GroundControl endpoint. Preserve other settings. Run `hermes mcp login groundcontrol` interactively and approve only the workloads and read scopes you intend to expose. OAuth consent is a separate decision. Never put a bearer token in YAML or paste one into chat.

Use `/groundcontrol setup`, then ask Hermes to load `groundcontrol:operate` and inspect the named deployment. MCP names may be normalized by Hermes; use discovered tools, not invented names.

The six exposed tools are deployment.list, deployment.inspect, deployment.health, deployment.logs, deployment.config.check and operation.get. GroundControl grants enforce actual access. Tool filtering is not a security sandbox for other Hermes tools.

## Evidence receipts

`/groundcontrol receipt <JSON>` accepts an object returned by deployment.health or operation.get and emits only a bounded, conservative summary. It does not fetch anything, prove authenticity, or certify a customer journey. Missing public evidence remains unknown. An uncertain operation never recommends replay. An HTTP 2xx is endpoint evidence, not proof of login or checkout.

## Write-enabled use

The operating skill describes the complete workflow, but the default connection is read-only. Deliberately enabling mutations requires operator consent to the corresponding tools and GroundControl scope plus verified Hermes approval controls. Current Hermes supports untrusted MCP servers with write approval gates; the locally installed 0.17.0 was not found to implement that guard. Do not treat an ignored `trust` key as protection. Validate a supported Hermes release before enabling writes. GroundControl must still check exact workload, runtime capability and grant at execution.

## Safety and disclosure

The installed Python plugin reads only its own bundled skill and receives slash-command text. It makes no network calls, runs no shell, starts no background tasks, stores no state or credentials, has no telemetry, and imports no Hermes private modules. Native Hermes MCP separately connects to the configured GroundControl URL and manages its own OAuth tokens. Its tool responses can include infrastructure evidence; do not paste raw secrets or sensitive logs into receipts. A plugin is not a sandbox and has Hermes' process authority.

## Validation

Run `python -m unittest discover -s tests -v`. For current catalog admission run `hermes plugins validate /path/to/hermes-groundcontrol --install-deps` against a reviewed current Hermes checkout. There are no plugin Python dependencies beyond the standard library. See `validation/` for recorded results and `submission/DEMO.md` for the demo plan. No live mutation is part of the current acceptance run.

## GroundControl runtime

The tested server release is `25202bc11fc09b41c6d8a88c5b22721ca0e9a38c`. It supports runtime-aware capability discovery, scoped operations, durable idempotent mutations and honest health uncertainty. Runtime support varies by deployment and recorded recipe; inspect capabilities before proposing an operation.

MIT. GroundControl source: https://github.com/teckedd-code2save/groundcontrol
