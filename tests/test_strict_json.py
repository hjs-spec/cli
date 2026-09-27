import io
import json

import pytest

from jep_cli import main as cli
from jep_cli import strict_json

BAD = [
    '{"x":1,"x":2}',
    '{"x":{"a":1,"\\u0061":2}}',
    '{"x":NaN}', '{"x":Infinity}', '{"x":-Infinity}',
    '{"x":1e400}', '{"x":9007199254740993}',
    '{"x":"\\ud800"}', '{"\\udfff":1}',
    '{"x":1,}', '{"x":1} {}',
]


@pytest.mark.parametrize('raw', BAD)
@pytest.mark.parametrize('source', ['inline', 'file', 'stdin'])
def test_all_input_sources_reject(raw, source, tmp_path, monkeypatch):
    argument = raw
    if source == 'file':
        path = tmp_path / 'event.json'
        path.write_bytes(raw.encode('utf-8'))
        argument = str(path)
    elif source == 'stdin':
        monkeypatch.setattr(cli.sys, 'stdin', io.StringIO(raw))
        argument = '-'
    with pytest.raises(ValueError):
        cli.parse_json_value(argument)


@pytest.mark.parametrize('source', ['file', 'stdin'])
def test_bad_utf8_rejected_before_text_replacement(source, tmp_path, monkeypatch):
    raw = b'{"x":"\xff"}'
    if source == 'file':
        path = tmp_path / 'event.json'
        path.write_bytes(raw)
        argument = str(path)
    else:
        stream = io.TextIOWrapper(io.BytesIO(raw), encoding='utf-8', errors='replace')
        monkeypatch.setattr(cli.sys, 'stdin', stream)
        argument = '-'
    with pytest.raises(ValueError):
        cli.parse_json_value(argument)


@pytest.mark.parametrize('raw', [
    '{"x":1000000000000000100}', '{"x":1000000000000000128}',
    '{"x":-1000000000000000100}', '{"x":100000000000000000000}',
    '{"x":"\\ud83d\\ude00","ext":{},"ext_crit":[],"sig":"keep..me"}',
    '{"x":"\\\\ud800","__proto__":{"ok":true}}',
])
def test_supported_values_preserve_members(raw):
    value = strict_json.loads(raw)
    assert value == json.loads(raw)
    assert strict_json.loads(strict_json.dumps(value)) == value


def test_duplicate_extension_is_not_silently_overwritten():
    with pytest.raises(ValueError):
        cli.parse_ext_items(['urn:test=1', 'urn:test=2'])


@pytest.mark.parametrize('legacy', [False, True])
def test_rejection_happens_before_network_and_never_falls_back(monkeypatch, legacy):
    def no_client(*args):
        pytest.fail('invalid input reached the client')
    monkeypatch.setattr(cli, 'build_client', no_client)
    args = ['verify', '{"who":"a","who":"b"}']
    if legacy:
        args.append('--legacy')
    assert cli.main(args) == 1


def test_outgoing_values_are_checked():
    with pytest.raises(ValueError):
        strict_json.dumps({'x': float('nan')})
    with pytest.raises(ValueError):
        strict_json.dumps({'x': '\ud800'})


def test_plain_text_and_long_inline_json_still_work():
    assert cli.parse_json_value('approve') == 'approve'
    raw = json.dumps({'x': 'a' * 10000})
    assert cli.parse_json_value(raw) == json.loads(raw)
