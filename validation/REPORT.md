# Validation record, 10 November 2026

## Passed

- Eleven deterministic unit tests: command and skill registration, malformed input, strict 2xx evidence, missing public evidence, uncertain operations, conservative completion, and rejection of arbitrary strings. Operation receipts now distinguish endpoint verification from customer-journey verification.
- Official catalog CLI: `hermes plugins validate /path/to/hermes-groundcontrol --install-deps` passed against NousResearch/hermes-agent source `9dcf7714df7a0d49c335925d12d4b017274ee355`, using its isolated runtime. Security scan: safe; no warnings; host readiness true. No plugin dependencies beyond Python's standard library.
- Fresh live read-only acceptance through installed Hermes 0.17.0 and its existing native MCP OAuth: list returned four granted deployments; inspect returned runtime capabilities; health returned healthy=true, public.checked=true and public.status=200. A synthetic nonexistent identifier was rejected. Zero mutation calls.
- The demo capture invokes the actual registered command handler through Hermes PluginContext, connects using Hermes' native MCP client, and feeds sanitized fresh health into the actual receipt command. Uncertain-operation evidence is a labelled fixture. This is an acceptance-harness demonstration, not an LLM conversation or a live mutation recording.

## Limits and reproducibility

The plugin does not automatically enable itself, alter persistent Hermes configuration, install MCP credentials, expand grants, or enable writes. The six-tool read-only configuration is an example; the operator chooses the active connection's tools. The nonexistent-ID check proves fail-closed lookup, not cross-tenant isolation against another real deployment.

No live write, disconnect/reconnect mutation, or authenticated browser journey is claimed. Existing GroundControl server mutation tests are separate from this plugin's acceptance. Hermes 0.17.0 lacks the newer native MCP trust gate; write-enabled use requires a supported release and verified approval controls.

An attempted fresh acceptance with the isolated catalog runtime failed before connection because that environment's HTTP MCP transport was not initialized/available to the standalone harness. The matching installed Hermes runtime then passed the read-only acceptance. The catalog validator itself passed; the isolated catalog runtime is not claimed as a tested live MCP environment.

The demo video presents a readable rendering of captured output. It does not reconstruct or invent successful calls. `submission/demo-capture.json` records its sanitized inputs and outputs; uncertain-operation data is labelled synthetic. No credentials or raw infrastructure logs are distributed.
