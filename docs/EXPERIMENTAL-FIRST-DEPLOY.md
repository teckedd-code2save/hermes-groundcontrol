# Experimental repository-to-first-deploy rehearsal

This is a development profile, not the merged catalog's shipped capability.
Use only with a tested GroundControl build that advertises the three tools below
and an operator-enabled enrollment feature. Do not enable it on production as a
shortcut around review. No configuration is applied automatically.

Profiles are provided as `examples/experimental-proposal.yaml` and
`examples/experimental-first-launch.yaml`; `/groundcontrol experimental` explains the handoffs.
They are examples, never automatically installed or applied.

## 1. Proposal-only bootstrap

Keep native OAuth and verified Hermes write approval. Initially request only:

```yaml
mcp_servers:
  groundcontrol:
    url: https://YOUR-GROUNDCONTROL-INSTANCE/mcp
    auth: oauth
    oauth:
      redirect_port: 8765
      scope: deployment:propose offline_access
    trust: untrusted
    tools:
      include:
        - deployment.proposal.create
        - deployment.proposal.get
```

No workloads need to exist. Submit a public GitHub repository, full immutable SHA,
repository-relative Compose file and workload name. Do not put secrets in input.
The proposal itself neither fetches code nor creates an app. Open its owner-review
path on the configured GroundControl origin. The operator then fetches the pinned
Compose configuration, chooses the server and checks the actual configuration.

Current initial-launch limits: public repositories, explicit loopback port mapping
already in Compose, health endpoint, explicit owner-only encrypted runtime configuration, no arbitrary
host mounts or host-network mode. Host builds require explicit acknowledgement:
application runtime caps do not cap build CPU, RAM or daemon-side build duration.
A request timeout is an uncertain outcome, not proof the build stopped.

Enrollment is not launch. The owner acceptance creates a pending deployment and
immutable recipe without changing OAuth grants or executing host commands.

## 2. Explicit resource consent and first launch

With operator approval, replace the scope and tool selection below, reconnect
native OAuth, and select only the newly enrolled deployment. Keep redirect port
stable. Do not silently widen scope or select unrelated deployments.

```yaml
    oauth:
      redirect_port: 8765
      scope: deployment:read deployment:health deployment:logs deployment:redeploy operation:read offline_access
    trust: untrusted
    tools:
      include:
        - deployment.list
        - deployment.inspect
        - deployment.health
        - deployment.logs
        - deployment.first_launch
        - deployment.source.deploy
        - operation.get
```

Inspect the deployment to obtain its approved recipe hash and capability status.
Request `deployment.first_launch` with that exact hash, resource ID and stable
idempotency key. Verify Hermes actually prompts and use Approve Once. Track its
operation until a terminal result. Never substitute terminal/SSH for the tool.

Started, uncertain or failed launches are not automatically replayable. Inspect
and deliberately recover; a new idempotency key must not bypass the reservation.
After verified first launch, `deployment.source.deploy` can deploy a full immutable
commit SHA while preserving the approved Compose content, runtime config versions,
host, named volumes and domain binding. Changed Compose or configuration requires
owner review; branch-only updates are rejected for this recipe. Ordinary redeploy,
build/release adoption is not implied. Never use a new key to replay an unresolved
update. Prove this path in the joint rehearsal before recording.

## Evidence boundary

Loopback health proves only the selected app endpoint on that server. It is not a
public HTTPS URL. Public routing requires a separately authorized access plan;
this flow does not change DNS or firewall rules. Record the actual app interaction
and distinguish local tests, integration tests and live rehearsal results.

## Configuration and domain handoff

Use the owner configuration form for new values explicitly authorized for this
isolated deployment. The form returns names and saved versions, not values. Do not
copy current production credentials or data. Prepare the application domain through
the owner review page: DNS ownership and direct routing checks are read-only, and
DNS/firewall changes remain separate actions. Publish only the isolated app route
after its local health passes. Control-plane HTTPS checks are not an independent
customer browser journey. Preserve GC setup/access and SSH.
