# Sorcar Validation Scripts

## Smoke test (headless Blender)

1. Package addon:

```bash
python tests/smoke/package_addon.py --output sorcar-smoke.zip
```

2. Run smoke test:

```bash
blender -b --factory-startup -P tests/smoke/smoke_addon.py -- --addon-zip sorcar-smoke.zip --cycles 3
```

## Execution benchmark (headless Blender)

```bash
blender -b --factory-startup -P tests/perf/benchmark_execute.py -- --addon-zip sorcar-smoke.zip --tree-count 5 --cycles 5 --output sorcar-bench.json
```
