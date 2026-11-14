"""GroundControl operating guide. Credentials and transport stay in Hermes MCP."""
from pathlib import Path
import json

READ_TOOLS = ('deployment.list', 'deployment.inspect', 'deployment.health',
              'deployment.logs', 'deployment.config.check', 'operation.get')
WRITE_TOOLS = ('deployment.source.deploy', 'deployment.redeploy', 'deployment.restart',
               'deployment.build_publish', 'deployment.release')

def command(raw_args: str = '') -> str:
    action, _, payload = raw_args.strip().partition(' ')
    if action == 'capabilities':
        return json.dumps({
            'source': 'GroundControl tool catalog, not a live authorization check',
            'read_tools': READ_TOOLS,
            'write_tools': WRITE_TOOLS,
            'write_scope': 'deployment:redeploy',
            'experimental': {'tools': ['deployment.proposal.create', 'deployment.proposal.get', 'deployment.first_launch'], 'status': 'candidate-only, disabled by default; not included in the released catalog profile', 'guide': '/groundcontrol experimental'},
            'available_now': 'unknown; inspect the selected deployment through native MCP',
            'enrollment': 'Operator setup required: this catalog does not create projects, enroll deployments or configure source and secret values',
            'enablement': 'examples/full-capability.yaml is optional and is not applied by this command',
            'approval': 'Verify effective per-call approval in the installed Hermes build; use Approve Once. YOLO, approvals off, or remembered grants can bypass prompts.',
        }, indent=2)
    if action == 'experimental':
        return ('Experimental candidate-only repository-to-first-launch workflow. Not a claim about the released catalog plugin or your connected server.\n'
                '1. Operator installs a tested GroundControl candidate and explicitly enables its enrollment feature; verify live tool discovery first. Never enable it silently.\n'
                '2. Deliberately use examples/experimental-proposal.yaml in a separate Hermes profile. Native OAuth requests only deployment:propose offline_access; no existing deployment is needed.\n'
                '3. Submit public GitHub repository, immutable SHA, Compose path and workload name through deployment.proposal.create. No secret values. Present ownerReviewPath on your configured GroundControl origin.\n'
                '4. The owner reviews fetched pinned Compose, host, loopback mapping, health, runtime budget and build risks. Acceptance reserves a pending deployment; it does not launch or grant agent access.\n'
                '5. With explicit operator consent, replace the profile using examples/experimental-first-launch.yaml, reconnect OAuth and select only that deployment. Inspect its approved recipe hash and first-launch capability.\n'
                '6. Verify effective Hermes Approve Once for deployment.first_launch; use the exact approved hash and one stable idempotency key. Save operation ID and poll operation.get. Never replay started/failed/uncertain work.\n'
                'Loopback health is not public HTTPS. Environment provisioning and ordinary source-update/adoption are not supplied by this experimental path. Builds run untrusted code; runtime caps do not bound build CPU/RAM or daemon-side build duration.\n'
                'Missing discovered tools means stop and explain the missing candidate/configuration, not use shell or another transport. This command does not change profiles, authenticate, grant access or run deployment actions. See docs/EXPERIMENTAL-FIRST-DEPLOY.md.')
    if action == 'receipt':
        try:
            value = json.loads(payload)
            if not isinstance(value, dict):
                raise ValueError('Expected an object')
            return json.dumps(review_receipt(value), indent=2)
        except (ValueError, TypeError):
            return 'Usage: /groundcontrol receipt <health or operation JSON object>. Do not include credentials.'
    if action == 'setup':
        return ('Requires your own GroundControl instance and an enrolled deployment; this plugin does not include a hosted account or provision infrastructure.\n\n'
                'New to GroundControl? Install and claim your instance: '
                'https://github.com/teckedd-code2save/groundcontrol/blob/main/docs/start-from-your-computer.md\n'
                'Choose local Docker Desktop/Engine (Linux containers; Windows uses WSL; Apple Silicon uses AMD64 emulation) '
                'or an AMD64 Linux VPS with SSH and root/passwordless sudo. Local mode manages Docker workloads, not native Mac/Windows services.\n'
                'Add a project and enroll or launch a deployment; importing a repository alone does not deploy it: '
                'https://github.com/teckedd-code2save/groundcontrol/blob/main/docs/projects-and-deployments.md\n\n'
                'Connect your own HTTPS GroundControl /mcp endpoint using Hermes native MCP OAuth. '
                'A browser setup link alone does not establish Hermes connectivity. '
                'Remote setup offers temporary HTTPS by default; verify a durable HTTPS endpoint and native OAuth/MCP before ongoing agent use. Do not expose the raw management port. '
                'Localhost-only Hermes OAuth is not claimed as tested here.\n'
                'Start with the six read-only tools in examples/read-only.yaml. '
                'The operator chooses exact deployments during OAuth consent. '
                'Authenticate through Hermes native MCP OAuth; never paste tokens into chat. '
                'Discovery alone is not proof of authentication: verify deployment.list returns authorized data. '
                'If empty, check enrollment and the workloads selected in your grant; do not expand access automatically. '
                'For a rejected refresh token, restore OAuth consent and then reload the MCP connection. '
                'This command does not change configuration, sign in, or grant access.')
    return ('Load skill groundcontrol:operate before operating a deployment. '
            'Inspect -> confirm runtime capability -> propose one exact change -> approval -> '
            'durable operation -> verify. Read-only is the default. Never use shell to bypass an unavailable operation. '
            'Commands: /groundcontrol setup; /groundcontrol capabilities; /groundcontrol experimental; /groundcontrol receipt <JSON>. '
            'A receipt reviews supplied evidence; it does not independently verify the server.')

def review_receipt(value: dict) -> dict:
    """Conservative projection only: never return logs, URLs, secrets or arbitrary strings."""
    operation = value.get('operation')
    if isinstance(operation, dict):
        status = operation.get('status')
        allowed = {'pending', 'running', 'verifying', 'success', 'failed', 'uncertain', 'cancelled'}
        result = operation.get('result')
        result = result if isinstance(result, dict) else {}
        return {
            'source': 'supplied operation evidence, not an independent live check',
            'status': status if isinstance(status, str) and status in allowed else 'unknown',
            'terminal': status in {'success', 'failed', 'uncertain', 'cancelled'} if isinstance(status, str) else False,
            'replay_allowed': False,
            'action_completed': status == 'success',
            'public_endpoint_verified': status == 'success' and result.get('publicVerified') is True and result.get('healthy') is True,
            'customer_journey_verified': False,
            'next_step': 'inspect and reconcile; do not replay' if status == 'uncertain' else 'check fresh deployment health and public evidence',
        }
    public = value.get('public')
    public = public if isinstance(public, dict) else {}
    status = public.get('status')
    verified = (public.get('checked') is True and public.get('healthy') is True
                and type(status) is int and 200 <= status < 300)
    return {
        'source': 'supplied health evidence, not an independent live check',
        'health': 'healthy' if value.get('healthy') is True and verified else 'unhealthy' if value.get('healthy') is False else 'unknown',
        'public_endpoint_verified': verified,
        'customer_journey_verified': False,
        'next_step': 'A successful HTTP endpoint is not proof of an authenticated customer journey.',
    }

def register(ctx):
    ctx.register_command('groundcontrol', command, description='GroundControl setup, capability catalog and evidence receipts', args_hint='[setup|capabilities|experimental|receipt JSON]')
    ctx.register_skill('operate', Path(__file__).parent / 'skills' / 'operate' / 'SKILL.md', description='Operate granted GroundControl workloads through native MCP with explicit capability checks and verified outcomes.')
