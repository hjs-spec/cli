# Contributing to JEP CLI

This is a Python HTTP client for the JEP API. Use the [issue tracker](https://github.com/hjs-spec/cli/issues) and follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Develop

Python 3.9 or newer is required.

```sh
git clone https://github.com/hjs-spec/cli.git
cd cli
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
python -m pytest -q
jep --help
```

Keep each pull request focused. Test changed behavior and update CLI documentation. The command is `jep`; `jep-agent` and `jep-runtime` belong to separate packages. Protocol requirements stay in [Core](https://github.com/hjs-spec/jep-core).

Contact: signal@humanjudgment.org.
