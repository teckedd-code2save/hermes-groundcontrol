# Experimental candidate validation

Plugin code: `5361616fb4e158f66d010b502175c802ef87b9bd`.
Official Hermes checkout: `78abaafcccec20a546c94e8734a70e38c08a6a69`.

- 26 plugin unit tests pass.
- Official `validate_plugin_dir` passes all checks. The isolated registration probe
  succeeds and reports plugin-host readiness.
- Native local-file installation was attempted in a throwaway HOME/HERMES_HOME,
  using a separate Python virtual environment, never the user's profile.
- Installer stopped at its caution scan. Findings refer to existing prerequisite
  documentation mentioning administrator privileges and a test fixture containing
  an injection string. No scanner override was used. Full installer publication
  is therefore **not verified**.
- No OAuth, authenticated tool discovery, approval prompt, deployment, or live
  Hermes-to-GroundControl rehearsal is claimed by these checks.

The official public catalog fetched during this check still advertised version
`0.2.0`, pinned to `d2905e9cdd710aaa20217e1c24a8091cdf8b9dcc`.
The catalog and published pin were not changed.

## Follow-up: stock installer passed

Candidate `f780995` was installed successfully by the unmodified official Hermes
`cmd_install` entry point into a new throwaway HOME/HERMES_HOME with `enable=False`.
No force flag, scanner override, scanner configuration change, or user-profile
change was used. The plugin remains disabled in that test home.

The runtime setup command now points to the installation guide for host permission
details rather than duplicating privilege setup advice. The exact elevated-access
prerequisite remains in README. The invalid-status non-echo test uses an ordinary
unknown status instead of an unrelated attack sentence. Tests remain distributed.
The stock scanner reports **safe**, retaining the README prerequisite as an
informational finding.

The native install also exposed an existing manifest compatibility warning:
`capabilities` was a mapping while the native loader expects a list. The candidate
now uses native top-level `provides_tools` / `provides_hooks` fields and an empty
capabilities list. Commands and skills still register through the plugin context.

Final results: 27 unit tests pass; native validation passes without warnings;
isolated registration reports host readiness; stock installation completes without
manifest warnings. This still does not establish live OAuth, native approval
behavior, connection to GroundControl, or a real deployment.

## Pinned remote installation

The stock Hermes installer also fetched and installed candidate commit
`71f2f795b1cd9a6fac730d220daca35ff85a6344` from the public GitHub repository
into a fresh isolated HOME with `enable=False`. It completed without scanner
bypass or force. This proves packaging/installability, not live OAuth or deployment.
The next candidate adds existing `deployment.source.deploy` to the opt-in profile;
real VM installation and rehearsal remain owner-attended steps.
