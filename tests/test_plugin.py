import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('groundcontrol', ROOT / '__init__.py')
plugin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plugin)

class PluginTests(unittest.TestCase):
    def test_registration(self):
        class Context:
            def register_command(self, name, handler, **kwargs):
                self.command = (name, handler)
            def register_skill(self, name, path, **kwargs):
                self.skill = (name, path)
        ctx = Context()
        plugin.register(ctx)
        self.assertEqual(ctx.command[0], 'groundcontrol')
        self.assertTrue(ctx.skill[1].is_file())
    def test_health_unknown_without_public_evidence(self):
        for value in ({}, {'healthy': True}, {'healthy': None}, {'healthy': True, 'public': {'checked': False}}):
            self.assertEqual(plugin.review_receipt(value)['health'], 'unknown')
    def test_only_explicit_2xx_verifies(self):
        for status in (200, 204, 299):
            self.assertEqual(plugin.review_receipt({'healthy': True, 'public': {'checked': True, 'healthy': True, 'status': status}})['health'], 'healthy')
        for status in (True, '200', 301, 399, 500, None):
            self.assertFalse(plugin.review_receipt({'healthy': True, 'public': {'checked': True, 'healthy': True, 'status': status}})['public_endpoint_verified'])
    def test_http_does_not_verify_customer_journey(self):
        self.assertFalse(plugin.review_receipt({'healthy': True, 'public': {'checked': True, 'healthy': True, 'status': 200}})['customer_journey_verified'])
    def test_uncertain_never_replays(self):
        r = plugin.review_receipt({'operation': {'status': 'uncertain'}})
        self.assertTrue(r['terminal'])
        self.assertFalse(r['replay_allowed'])
        self.assertFalse(r['action_completed'])
    def test_success_is_not_customer_verification(self):
        for status in ('pending', 'running', 'verifying', 'failed', 'uncertain', 'success'):
            self.assertFalse(plugin.review_receipt({'operation': {'status': status}})['public_endpoint_verified'])
    def test_explicit_verification(self):
        self.assertTrue(plugin.review_receipt({'operation': {'status': 'success', 'result': {'publicVerified': True, 'healthy': True}}})['public_endpoint_verified'])
    def test_operation_endpoint_is_not_customer_journey(self):
        self.assertFalse(plugin.review_receipt({'operation': {'status': 'success', 'result': {'publicVerified': True, 'healthy': True}}})['customer_journey_verified'])
    def test_malformed_input(self):
        for raw in ('receipt []', 'receipt secret', 'receipt null', 'receipt'):
            self.assertIn('Usage:', plugin.command(raw))
        self.assertEqual(plugin.review_receipt({'operation': {'status': []}})['status'], 'unknown')
    def test_no_untrusted_strings_echoed(self):
        raw = {'operation': {'status': 'unexpected-status-value', 'error': 'SECRET', 'result': {'token': 'SECRET'}}}
        result = json.dumps(plugin.review_receipt(raw))
        self.assertNotIn('SECRET', result)
        self.assertNotIn('unexpected-status-value', result)
    def test_setup_has_no_automatic_action(self):
        self.assertIn('does not change', plugin.command('setup'))
    def test_setup_starts_with_prerequisite_and_direct_install_guide(self):
        text = plugin.command('setup')
        self.assertTrue(text.startswith('Requires your own GroundControl instance'))
        self.assertIn('does not include a hosted account', text)
        self.assertIn('https://github.com/teckedd-code2save/groundcontrol/blob/main/docs/start-from-your-computer.md', text)
        self.assertIn('docs/projects-and-deployments.md', text)
    def test_setup_distinguishes_platforms_https_and_authentication(self):
        text = plugin.command('setup')
        for phrase in ('Docker Desktop/Engine', 'AMD64 Linux VPS', 'Windows uses WSL',
                       'not native Mac/Windows services', 'browser setup link',
                       'HTTPS', 'verify deployment.list', 'do not expand access automatically'):
            self.assertIn(phrase, text)
    def test_readme_prerequisite_precedes_feature_pitch(self):
        text = (ROOT / 'README.md').read_text()
        self.assertLess(text.index('Requires your own GroundControl instance'), text.index('Check deployment health'))
        for phrase in ('### 1. Get GroundControl', '### 2. Install the Hermes plugin',
                       '### 3. Connect and verify', 'localhost-only Hermes OAuth'):
            self.assertIn(phrase, text)
    def test_capability_catalog_is_explicitly_not_a_live_grant(self):
        value = json.loads(plugin.command('capabilities'))
        self.assertIn('not a live authorization check', value['source'])
        self.assertTrue(value['available_now'].startswith('unknown'))
    def test_catalog_contains_exact_typed_operations(self):
        value = json.loads(plugin.command('capabilities'))
        self.assertEqual(set(value['write_tools']), {'deployment.source.deploy','deployment.redeploy','deployment.restart','deployment.build_publish','deployment.release'})
        self.assertEqual(len(set(value['read_tools'] + value['write_tools'])), 11)
        self.assertEqual(value['write_scope'], 'deployment:redeploy')
    def test_optional_profile_matches_catalog_without_credentials(self):
        text = (ROOT / 'examples/full-capability.yaml').read_text()
        included = [line.strip()[2:] for line in text.splitlines() if line.strip().startswith('- ')]
        self.assertEqual(set(included), set(plugin.READ_TOOLS + plugin.WRITE_TOOLS))
        self.assertEqual(len(included), 11)
        self.assertNotIn('Authorization:', text)
        self.assertNotIn('Bearer ', text)
        self.assertIn('YOUR-GROUNDCONTROL-INSTANCE', text)
    def test_read_only_profile_remains_read_only(self):
        text = (ROOT / 'examples/read-only.yaml').read_text()
        included = [line.strip()[2:] for line in text.splitlines() if line.strip().startswith('- ')]
        self.assertEqual(set(included), set(plugin.READ_TOOLS))
        self.assertTrue(set(included).isdisjoint(plugin.WRITE_TOOLS))
    def test_capability_command_warns_about_effective_approval_bypasses(self):
        value = json.loads(plugin.command('capabilities'))
        for term in ('Approve Once', 'YOLO', 'approvals off', 'remembered'):
            self.assertIn(term, value['approval'])
        self.assertIn('not applied', value['enablement'])

class RehearsalBoundaryTests(unittest.TestCase):
    def test_catalog_does_not_imply_enrollment(self):
        value = json.loads(plugin.command('capabilities'))
        self.assertIn('does not create projects', value['enrollment'])
        self.assertIn('enroll deployments', value['enrollment'])
    def test_setup_does_not_claim_temporary_is_durable(self):
        text = plugin.command('setup')
        self.assertIn('temporary HTTPS by default', text)
        self.assertIn('verify a durable HTTPS endpoint', text)

class ExperimentalProfilesTests(unittest.TestCase):
    def profile(self, name):
        text = (ROOT / 'examples' / name).read_text()
        return text, [line.strip()[2:] for line in text.splitlines() if line.strip().startswith('- ')]
    def test_proposal_profile_has_no_existing_workload_or_execution_scope(self):
        text, tools = self.profile('experimental-proposal.yaml')
        self.assertEqual(tools, ['deployment.proposal.create', 'deployment.proposal.get'])
        self.assertIn('scope: deployment:propose offline_access', text)
        self.assertNotIn('deployment:redeploy', text)
        self.assertIn('trust: untrusted', text)
    def test_first_launch_profile_does_not_offer_unimplemented_updates(self):
        text, tools = self.profile('experimental-first-launch.yaml')
        self.assertEqual(set(tools), set(plugin.READ_TOOLS) | {'deployment.first_launch'})
        self.assertTrue(set(tools).isdisjoint(plugin.WRITE_TOOLS))
        self.assertIn('select only the new deployment', text)
        self.assertIn('redirect_port: 8765', text)
    def test_experimental_guidance_has_human_handoffs_and_no_action(self):
        text = plugin.command('experimental')
        for phrase in ('candidate-only', 'verify live tool discovery', 'owner', 'does not launch or grant',
                       'explicit operator consent', 'Approve Once', 'Never replay',
                       'Loopback health is not public HTTPS', 'does not change profiles'):
            self.assertIn(phrase, text)
    def test_experimental_capability_separate_from_released_catalog(self):
        value = json.loads(plugin.command('capabilities'))
        self.assertEqual(len(value['read_tools']), 6)
        self.assertEqual(len(value['write_tools']), 5)
        self.assertEqual(len(value['experimental']['tools']), 3)
        self.assertIn('disabled by default', value['experimental']['status'])
        self.assertTrue(set(value['experimental']['tools']).isdisjoint(value['read_tools'] + value['write_tools']))
    def test_manifest_uses_native_declaration_fields(self):
        text = (ROOT / 'plugin.yaml').read_text()
        self.assertIn('provides_tools: []', text)
        self.assertIn('provides_hooks: []', text)
        self.assertIn('capabilities: []', text)
        self.assertNotIn('  commands:', text)
    def test_experimental_examples_have_no_embedded_credentials(self):
        for name in ('experimental-proposal.yaml', 'experimental-first-launch.yaml'):
            text, _ = self.profile(name)
            for secret in ('Authorization:', 'Bearer ', 'access_token:', 'client_secret:'):
                self.assertNotIn(secret, text)

if __name__ == '__main__':
    unittest.main()
