import argparse
import importlib
import sys
from pathlib import Path

KEYMAP_OPS = {
    "sorcar.execute_node",
    "sorcar.clear_preview",
    "sorcar.group_nodes",
    "sorcar.edit_group",
}

def parse_args() -> argparse.Namespace:
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = argv[1:]

    parser = argparse.ArgumentParser(description="Sorcar smoke test.")
    parser.add_argument("--addon-module", default="", help="Addon module name (optional).")
    parser.add_argument("--addon-zip", default="", help="Addon zip to install before running tests.")
    parser.add_argument("--cycles", type=int, default=3, help="Enable/disable cycles.")
    return parser.parse_args(argv)

def detect_addon_module(module_hint: str, addon_utils_module) -> str:
    if module_hint:
        return module_hint

    for module in addon_utils_module.modules():
        info = getattr(module, "bl_info", {})
        if info.get("name") == "Sorcar":
            return module.__name__
    return ""

def count_sorcar_keymaps(bpy_module) -> int:
    kc = bpy_module.context.window_manager.keyconfigs.addon
    if not kc:
        return 0
    km = kc.keymaps.get("Node Generic")
    if not km:
        return 0
    return sum(1 for item in km.keymap_items if item.idname in KEYMAP_OPS)

def count_update_handlers(bpy_module) -> int:
    return sum(1 for handler in bpy_module.app.handlers.frame_change_post if getattr(handler, "__name__", "") == "update_each_frame")

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

    for _ in range(args.cycles):
        bpy.ops.preferences.addon_disable(module=module_name)
        bpy.ops.preferences.addon_enable(module=module_name)
        assert_true(count_update_handlers(bpy) <= 1, "Duplicate frame_change_post handlers detected")
        assert_true(count_sorcar_keymaps(bpy) <= len(KEYMAP_OPS), "Duplicate Sorcar keymaps detected")

    tree = bpy.data.node_groups.new("SorcarSmokeTree", "ScNodeTree")
    create_cube = tree.nodes.new("ScCreateCube")
    tree.set_preview(create_cube.name)

    active_object = bpy.context.active_object
    assert_true(active_object is not None, "No object created after tree execution")
    assert_true(active_object.type == "MESH", "Expected MESH output object")

    bpy.data.node_groups.remove(tree)
    if active_object and active_object.name in bpy.data.objects:
        bpy.data.objects.remove(active_object, do_unlink=True)

    print("SMOKE_PASS")

if __name__ == "__main__":
    run()
