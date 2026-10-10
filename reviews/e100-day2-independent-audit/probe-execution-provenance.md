# Probe execution and independent verification provenance

The prospective probe plan was committed at `30aa31d` before execution. The exact fenced code in `probes.md` was extracted and invoked by the root executor with Python 3.9.6 using the following orchestration command; return code 0, empty stderr, complete raw output in `probes.stdout.json`. The original probe invocation did not record wall-clock start/end. **Original probe timestamps UNKNOWN**; do not infer them from file timestamps or the instrument execution interval. `execution-metadata.json` covers the five instrument invocations, not this probe invocation.

```python
import pathlib, subprocess, sys
root = pathlib.Path('reviews/e100-day2-independent-audit')
text = (root / 'probes.md').read_text()
code = text.split('```python\n', 1)[1].split('\n```', 1)[0]
p = subprocess.run([sys.executable, '-c', code], capture_output=True,
                   text=True, timeout=30)
(root / 'probes.stdout.json').write_text(p.stdout)
(root / 'probes.stderr.txt').write_text(p.stderr)
print('Probe return code:', p.returncode)
print(p.stdout)
print(p.stderr)
if p.returncode:
    raise SystemExit(p.returncode)
```

Distinct internal reviewer invocations independently executed the retained fenced code: Python reviewer `/root/python_probe_review` executed twice and scientific referee `/root/scientific_review` executed once. Each reported return code 0 and parsed JSON equal to the original retained output. These are reproduced probe observations, not independent environment/model/agent-efficacy replications or new accepted contributions. The scientific referee records its own review provenance separately. No historical timestamps were synthesized and no target code was changed.
