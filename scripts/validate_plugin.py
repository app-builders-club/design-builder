#!/usr/bin/env python3
"""Validate both plugin packages and run local tools from an unrelated cwd."""
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def run(args, cwd, expected=(0,)):
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=60)
    assert result.returncode in expected, (args, result.returncode, result.stderr)
    return result.stdout


def main():
    manifests = [json.loads((ROOT / name / 'plugin.json').read_text())
                 for name in ('.claude-plugin', '.codex-plugin')]
    assert manifests[0]['name'] == manifests[1]['name'] == 'design-builder'
    assert manifests[0]['version'] == manifests[1]['version']
    for manifest in manifests:
        for key in ('skills', 'mcpServers'):
            assert (ROOT / manifest[key]).exists(), (key, manifest[key])
    assert (ROOT / manifests[0]['commands']).is_dir()
    for catalog in ('.claude-plugin/marketplace.json', '.agents/plugins/marketplace.json'):
        data = json.loads((ROOT / catalog).read_text())
        plugin = next(p for p in data['plugins'] if p['name'] == manifests[0]['name'])
        source = plugin['source']
        assert (ROOT / (source['path'] if isinstance(source, dict) else source)).resolve() == ROOT
    assert set(p.stem for p in (ROOT / 'commands').glob('*.md')) == {
        'setup', 'start', 'design_page', 'design_screen', 'build', 'improve', 'review'}
    assert (ROOT / 'agents/design-auditor.md').is_file()
    # Check operational entry links, excluding fenced examples and dynamic artifacts.
    files = [ROOT / 'README.md', *(ROOT / 'commands').glob('*.md'),
             *(ROOT / 'skills').rglob('SKILL.md'), *(ROOT / 'agents').glob('*.md')]
    for path in files:
        text = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
        for link in re.findall(r'\]\(([^)]+)\)', text):
            if '://' in link or link.startswith('#'):
                continue
            target = unquote(link.split('#')[0])
            assert (path.parent / target).exists(), (path.relative_to(ROOT), target)
    scripts = ROOT / 'skills/design/scripts'
    with tempfile.TemporaryDirectory(prefix='design-builder validation ') as tmp:
        cwd = Path(tmp)
        result = json.loads(run([sys.executable, str(scripts / 'search.py'),
                                'accessible form focus', '--domain', 'ux', '--json'], cwd))
        assert result['results'], 'Local CSV search must return real records'
        sys.path.insert(0, str(scripts))
        from compute_contrast import contrast_ratio
        assert contrast_ratio('#000000', '#FFFFFF') == 21.0
        candidates = [{
            'id': ident, 'name': 'Candidate ' + ident,
            'differentiation_hook': 'Use a 72px Serif heading above an asymmetric grid',
            'tone_one_liner': 'Quiet editorial layout',
            'fonts': {'display': {'family': 'Georgia'}, 'body': {'family': 'Arial'}},
            'palette': {'bg': '#FFFFFF', 'fg': '#000000', 'accent': '#245533'},
            'type': {'display_size_px': 72, 'body_size_px': 16, 'scale': [16, 24, 72]},
        } for ident in 'ABC']
        (cwd / 'candidates.json').write_text(json.dumps(candidates))
        for platform in ('web', 'ios', 'cross'):
            out = cwd / (platform + '.html')
            run([sys.executable, str(scripts / 'generate_system_preview.py'),
                 '--candidates', 'candidates.json', '--platform', platform,
                 '--project', 'Smoke <test>', '--out', str(out)], cwd)
            rendered = out.read_text()
            assert 'Candidate A' in rendered and 'Candidate C' in rendered
            assert 'Smoke &lt;test&gt;' in rendered, 'Project label must be HTML-escaped'
        assert shutil.which('node'), 'Node is needed to validate the bundled detector'
        (cwd / 'fixture.html').write_text('<html><body><h1>Fixture</h1><button>Save</button></body></html>')
        output = run(['node', str(scripts / 'detect-antipatterns.mjs'), '--fast',
                      '--json', str(cwd / 'fixture.html')], cwd, expected=(0, 2))
        json.loads(output)
    print('PASS: both manifests, marketplaces, command preservation, entry links, CSV search, contrast, 3 previews, Node detector')


if __name__ == '__main__':
    main()
