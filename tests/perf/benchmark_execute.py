import argparse
import importlib
import json
import sys
import time
from pathlib import Path

def parse_args() -> argparse.Namespace:
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = argv[1:]

    parser = argparse.ArgumentParser(description="Sorcar execution benchmark.")
    parser.add_argument("--addon-module", default="", help="Addon module name (optional).")
    parser.add_argument("--addon-zip", default="", help="Addon zip to install before benchmark.")
    parser.add_argument("--tree-count", type=int, default=5, help="Number of trees.")
    parser.add_argument("--cycles", type=int, default=5, help="Execution cycles.")
    parser.add_argument("--output", default="", help="Optional JSON output filepath.")
    return parser.parse_args(argv)

def detect_addon_module(module_hint: str, addon_utils_module) -> str:
    if module_hint:
        return module_hint
    for module in addon_utils_module.modules():
        info = getattr(module, "bl_info", {})
        if info.get("name") == "Sorcar":
            return module.__name__
    return ""

def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)

def run() -> None:
    args = parse_args()
    try:
        import addon_utils
        import bpy
    except ModuleNotFoundError as err:
        raise RuntimeError("This script must run inside Blender's Python: {}".format(err))

    if args.addon_zip:
        addon_zip = Path(args.addon_zip).resolve()
        assert_true(addon_zip.exists(), "Addon zip not found: {}".format(addon_zip))
        bpy.ops.preferences.addon_install(filepath=addon_zip.as_posix(), overwrite=True)

    module_name = detect_addon_module(args.addon_module, addon_utils)
    assert_true(module_name != "", "Sorcar module could not be detected")
    bpy.ops.preferences.addon_enable(module=module_name)
    importlib.import_module(module_name)

    trees = []
    for index in range(args.tree_count):
        tree = bpy.data.node_groups.new("SorcarBenchTree{}".format(index), "ScNodeTree")
        create_cube = tree.nodes.new("ScCreateCube")
        tree.set_preview(create_cube.name)
        trees.append(tree)

    start = time.perf_counter()
    for _ in range(args.cycles):
        for tree in trees:
            tree.execute_node()
    elapsed = time.perf_counter() - start

    stats = {
        "tree_count": args.tree_count,
        "cycles": args.cycles,
        "total_seconds": elapsed,
        "seconds_per_cycle": elapsed / max(args.cycles, 1),
        "seconds_per_tree_exec": elapsed / max(args.cycles * args.tree_count, 1),
    }

    for tree in trees:
        bpy.data.node_groups.remove(tree)

    output = json.dumps(stats, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    print(output)

if __name__ == "__main__":
    run()
