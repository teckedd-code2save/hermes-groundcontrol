# Real Hermes deployment rehearsal

This is an acceptance plan, not evidence of a completed live write. Use a separate
rehearsal run, then record genuinely new work in one continuous 20–60-minute take.
Do not substitute fixtures or terminal renderings for the actual Hermes session.

## Proposed story: ship an enrolled source application

Use a disposable, public-source HTTP application with a health route and a visible
version marker. Prefer an existing Compose recipe with no real customer data,
payment integration or production secrets. Operator prerequisites are disclosed:
the project/deployment, source linkage, server and environment values must already
be configured in GC. The current MCP contract cannot perform that enrollment.

Hermes inspects the selected deployment, identifies required configuration by name
without reading values, proposes a supported source build/deploy, requests approval,
tracks its durable operation and checks the visible application afterward. A small
new app change can be prepared with Hermes's coding tools, explicitly separate from
GC's MCP operations. Source deployment takes a branch; record the resolved commit,
and never claim immutable commit deployment unless the actual build/release path
used a full commit and verified image digest.

## Readiness gates

- Record actual GC image/revision, Hermes version, plugin revision/catalog pin and
  profile name. Catalog acceptance is not proof that all operations were tested.
- Use one disposable workload only. Confirm host budget and lifetime before work;
  do not silently keep a time-limited test VM running beyond approval.
- Confirm trusted reachable HTTPS, canonical OAuth issuer and registered callback
  port, then complete native OAuth. Do not put tokens in YAML or recordings.
- Discovery alone is insufficient: `deployment.list`, inspect and health must work
  in the actual Hermes session and show the expected workload.
- Verify source/recipe capabilities as supported, authorized and available. Check
  GitHub App access, Git/build tools, disk/RAM, dependencies and health-route settings.
- Explicitly approve the intended write-enabled profile/scopes. Confirm effective
  native approval guards in this installed Hermes build, with YOLO/approvals-off
  disabled and no remembered tool-wide grant for this test.
- Deny a test write prompt and verify no operation was dispatched. Do not infer
  gating from a version string or `trust: untrusted` alone. If it fails, stop writes.
- Plan and approve the actual exact write, its interruption/publishing impact and
  rollback. No shell fallback to bypass a missing GC capability or denied operation.

## Run and evidence

1. Establish current app version, health and expected outcome.
2. Ask Hermes for an evidence-backed deployment plan; correct assumptions aloud.
3. Approve Once for the specific write. Preserve one idempotency key for that intent.
4. Keep the operation ID and poll `operation.get`. On connection loss, reconnect
   and resume that operation; never create a replacement for uncertain work.
5. Check final operation evidence, fresh health and the resolved source revision.
6. Open the actual service and perform one user-visible action. A 2xx/health check
   is not proof of a complete customer journey. Check logs without exposing secrets.
7. Demonstrate a safe repeated read or operation recovery, not a second unintended
   deployment. Record failures honestly and fix blockers before claiming readiness.

Save sanitized actual tool evidence and the exact outcome. Approval denial, live
mutation, external verification, OAuth/MCP streaming and recovery are distinct test
results; do not infer one from another. Do not promise "no issues" after a rehearsal.

## Recording boundary

Show the real plugin, task instructions, tools and resulting application. Keep all
credentials, claim URLs, provider tokens, private logs and customer data off screen.
The application asks for one continuous take: do not edit out failures or reconstruct
results. A dry run validates infrastructure, not a script of fabricated agent behavior.
