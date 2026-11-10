"""GroundControl operating guide. Credentials and transport stay in Hermes MCP."""
from pathlib import Path
import json

READ_TOOLS = ('deployment.list', 'deployment.inspect', 'deployment.health',
              'deployment.logs', 'deployment.config.check', 'operation.get')

def command(raw_args: str = '') -> str:
    action, _, payload = raw_args.strip().partition(' ')
    if action == 'receipt':
        try:
            value = json.loads(payload)
            if not isinstance(value, dict):
                raise ValueError('Expected an object')
            return json.dumps(review_receipt(value), indent=2)
        except (ValueError, TypeError):
            return 'Usage: /groundcontrol receipt <health or operation JSON object>. Do not include credentials.'
    if action == 'setup':
        return ('Connect your own HTTPS GroundControl /mcp endpoint using Hermes native MCP OAuth. '
                'Start with the six read-only tools in examples/read-only.yaml. '
                'The operator chooses exact deployments during OAuth consent. '
                'Use hermes mcp login groundcontrol for interactive consent; never paste tokens into chat. '
                'This command does not change configuration, sign in, or grant access.')
    return ('Load skill groundcontrol:operate before operating a deployment. '
            'Inspect -> confirm runtime capability -> propose one exact change -> approval -> '
            'durable operation -> verify. Read-only is the default. Never use shell to bypass an unavailable operation. '
            'Commands: /groundcontrol setup; /groundcontrol receipt <JSON>. '
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
    ctx.register_command('groundcontrol', command, description='GroundControl setup, safe operating guide and evidence receipts', args_hint='[setup|receipt JSON]')
    ctx.register_skill('operate', Path(__file__).parent / 'skills' / 'operate' / 'SKILL.md', description='Operate granted GroundControl workloads through native MCP with explicit capability checks and verified outcomes.')
