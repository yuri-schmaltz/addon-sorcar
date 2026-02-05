import ast
import re

import bpy
from mathutils import Vector

ID_REFERENCE_PATTERN = re.compile(
    r"""^bpy\.data\.(objects|curves|collections|materials|node_groups)\[(?P<quote>['"])(?P<name>.+)(?P=quote)\]$"""
)
ID_REFERENCE_SCAN_PATTERN = re.compile(
    r"""bpy\.data\.(objects|curves|collections|materials|node_groups)\[(['"])(.+?)\2\]"""
)

def sc_poll_op(context):
    space = context.space_data
    if hasattr(space, "node_tree"):
        if (space.node_tree):
            return space.tree_type == "ScNodeTree"
    return False

def sc_poll_mesh(self, object):
    return object.type == "MESH"

def sc_poll_curve(self, object):
    return object.type == "CURVE"

def sc_poll_curve_font(self, object):
    return object.type in ["CURVE", "FONT"]

def sc_poll_lattice(self, object):
    return object.type == "LATTICE"

def safe_literal_eval(data, fallback=None):
    if isinstance(data, str):
        try:
            return ast.literal_eval(data)
        except (ValueError, SyntaxError):
            return fallback
    if (data is None):
        return fallback
    return data

def resolve_data_reference(data):
    if not isinstance(data, str):
        return None
    match = ID_REFERENCE_PATTERN.match(data.strip())
    if not match:
        return None
    collection = getattr(bpy.data, match.group(1), None)
    if not collection:
        return None
    return collection.get(match.group("name"))

def extract_data_references(data, collection_name=None):
    refs = []
    if not isinstance(data, str):
        return refs
    for match in ID_REFERENCE_SCAN_PATTERN.finditer(data):
        current_collection = match.group(1)
        if (collection_name and current_collection != collection_name):
            continue
        collection = getattr(bpy.data, current_collection, None)
        if not collection:
            continue
        ref = collection.get(match.group(3))
        if (ref):
            refs.append(ref)
    return refs

def safe_parse_array(data, fallback=None):
    parsed = safe_literal_eval(data, None)
    if isinstance(parsed, (list, tuple, set)):
        return list(parsed)
    if (fallback is None):
        return None
    return list(fallback)

def safe_parse_int_list(data):
    out = []
    for i in safe_parse_array(data, []):
        try:
            out.append(int(i))
        except (TypeError, ValueError):
            pass
    return out

def safe_parse_object_array(data):
    out = extract_data_references(data, "objects")
    if (len(out) > 0):
        return out
    for i in safe_parse_array(data, []):
        if isinstance(i, bpy.types.Object):
            out.append(i)
        elif isinstance(i, str):
            ref = resolve_data_reference(i)
            if (ref is None):
                ref = bpy.data.objects.get(i)
            if (ref):
                out.append(ref)
    return out

def focus_on_object(obj, edit=False):
    if (bpy.ops.object.mode_set.poll()):
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action="DESELECT")
    if (obj):
        if (obj.name in bpy.context.view_layer.objects):
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            if (edit):
                bpy.ops.object.mode_set(mode="EDIT")

def remove_object(obj):
    if (obj):
        try:
            data = obj.data
            type = obj.type
        except AttributeError:
            return
        bpy.data.objects.remove(obj, do_unlink=True, do_id_user=True)
        if hasattr(data, "users"):
            if data.users == 0:
                if (type == 'MESH'):
                    bpy.data.meshes.remove(data, do_unlink=True, do_id_user=True)
                elif (type in ['CURVE', 'FONT']):
                    bpy.data.curves.remove(data, do_unlink=True, do_id_user=True)

def apply_all_modifiers(object):
    if (object):
        if (object.name in bpy.context.view_layer.objects):
            bpy.context.view_layer.objects.active = object
            while(object.modifiers):
                bpy.ops.object.modifier_apply(modifier=object.modifiers[0].name)

def get_override(active=None, edit=False, selected=[], type='VIEW_3D'):
    override = bpy.context.copy()
    if (type == 'VIEW_3D'):
        override["active_object"] = active
        if (edit):
            override["edit_object"] = active
        if (active not in selected):
            selected.append(active)
        override["selected_object"] = selected
    flag = False
    for window in bpy.data.window_managers[0].windows:
        for area in window.screen.areas:
            if area.type == type:
                override["area"] = area
                override["region"] = [i for i in area.regions if i.type == 'WINDOW'][0]
                flag = True
                break
        if (flag):
            break
    return override

def print_log(parent=None, child=None, func=None, msg=""):
    log = "SORCAR: "
    if (parent):
        log += parent + ": "
    if (child):
        log += child + ": "
    if (func):
        log += func + "(): "
    log += msg
    print(log)

def update_each_frame(scene):
    for i in bpy.data.node_groups:
        if (i.bl_idname == "ScNodeTree"):
            if (i.prop_realtime):
                i.execute_node()

def convert_data(data, from_type=None, to_type=None):
    if (data == None or from_type == None or to_type == None):
        return False, None
    try:
        if (to_type == "NUMBER"):
            if (from_type == "NUMBER"):
                val = data
            elif (from_type == "BOOL"):
                val = float(data)
            elif (from_type == "STRING"):
                parsed = safe_literal_eval(data, None)
                if (parsed is None):
                    return False, None
                val = float(parsed)
            elif (from_type == "VECTOR"):
                val = Vector(data).magnitude
            elif (from_type == "OBJECT"):
                val = bpy.data.objects.find(data.name)
            elif (from_type == "CURVE"):
                val = bpy.data.curves.find(data.name)
            elif (from_type == "ARRAY"):
                val = len(safe_parse_array(data, []))
            elif (from_type == "SELECTION_TYPE"):
                return False, None
        elif (to_type == "BOOL"):
            if (from_type == "NUMBER"):
                val = bool(data)
            elif (from_type == "BOOL"):
                val = data
            elif (from_type == "STRING"):
                val = bool(data)
            elif (from_type == "VECTOR"):
                val = bool(data)
            elif (from_type == "OBJECT"):
                val = bool(data)
            elif (from_type == "CURVE"):
                val = bool(data)
            elif (from_type == "ARRAY"):
                val = bool(safe_parse_array(data, []))
            elif (from_type == "SELECTION_TYPE"):
                val = len(data) != 0
        elif (to_type == "STRING"):
            if (from_type == "NUMBER"):
                val = str(data)
            elif (from_type == "BOOL"):
                val = str(data)
            elif (from_type == "STRING"):
                val = data
            elif (from_type == "VECTOR"):
                val = str(Vector(data).to_tuple())
            elif (from_type == "OBJECT"):
                val = str(repr(data))
            elif (from_type == "CURVE"):
                val = str(repr(data))
            elif (from_type == "ARRAY"):
                val = data
            elif (from_type == "SELECTION_TYPE"):
                val = str(data)
        elif (to_type == "VECTOR"):
            if (from_type == "NUMBER"):
                val = (data, data, data)
            elif (from_type == "BOOL"):
                val = (float(data), float(data), float(data))
            elif (from_type == "STRING"):
                parsed = safe_literal_eval(data, None)
                if (parsed is None):
                    return False, None
                val = Vector(parsed).to_tuple()
            elif (from_type == "VECTOR"):
                val = data
            elif (from_type == "OBJECT"):
                return False, None
            elif (from_type == "CURVE"):
                return False, None
            elif (from_type == "ARRAY"):
                data_arr = safe_parse_array(data, [])
                if (len(data_arr) < 3):
                    return False, None
                val = Vector((data_arr[0], data_arr[1], data_arr[2])).to_tuple()
            elif (from_type == "SELECTION_TYPE"):
                val = Vector(float("VERT" in data), float("EDGE" in data), float("FACE" in data)).to_tuple()
        elif (to_type == "OBJECT"):
            if (from_type == "NUMBER"):
                val = bpy.data.objects[data]
            elif (from_type == "BOOL"):
                return False, None
            elif (from_type == "STRING"):
                ref = resolve_data_reference(data)
                if (ref is None):
                    ref = bpy.data.objects.get(str(data))
                if (ref is None):
                    return False, None
                val = ref
            elif (from_type == "VECTOR"):
                return False, None
            elif (from_type == "OBJECT"):
                val = data
            elif (from_type == "CURVE"):
                return False, None
            elif (from_type == "ARRAY"):
                return False, None
            elif (from_type == "SELECTION_TYPE"):
                return False, None
        elif (to_type == "CURVE"):
            if (from_type == "NUMBER"):
                return False, None
            elif (from_type == "BOOL"):
                return False, None
            elif (from_type == "STRING"):
                return False, None
            elif (from_type == "VECTOR"):
                return False, None
            elif (from_type == "OBJECT"):
                return False, None
            elif (from_type == "CURVE"):
                val = data
            elif (from_type == "ARRAY"):
                return False, None
            elif (from_type == "SELECTION_TYPE"):
                return False, None
        elif (to_type == "ARRAY"):
            if (from_type == "NUMBER"):
                val = "[" + str(data) + "]"
            elif (from_type == "BOOL"):
                val = "[" + str(data) + "]"
            elif (from_type == "STRING"):
                parsed = safe_literal_eval(data, None)
                if (parsed is None):
                    return False, None
                val = str(list(parsed))
            elif (from_type == "VECTOR"):
                val = str(list(data))
            elif (from_type == "OBJECT"):
                val = "[" + repr(data) + "]"
            elif (from_type == "CURVE"):
                val = "[" + repr(data) + "]"
            elif (from_type == "ARRAY"):
                val = data
            elif (from_type == "SELECTION_TYPE"):
                val = str(list(data))
        elif (to_type == "SELECTION_TYPE"):
            if (from_type == "NUMBER"):
                return False, None
            elif (from_type == "BOOL"):
                return False, None
            elif (from_type == "STRING"):
                parsed = safe_literal_eval(data, None)
                if isinstance(parsed, (set, list, tuple)):
                    val = set(parsed)
                elif isinstance(parsed, str):
                    val = set([parsed]) if parsed in ["VERT", "EDGE", "FACE"] else set()
                else:
                    return False, None
            elif (from_type == "VECTOR"):
                val = set()
                if bool(data[0]):
                    val.add("VERT")
                if bool(data[1]):
                    val.add("EDGE")
                if bool(data[2]):
                    val.add("FACE")
            elif (from_type == "OBJECT"):
                return False, None
            elif (from_type == "CURVE"):
                return False, None
            elif (from_type == "ARRAY"): # Allows you to take in a boolean array
                data_eval = safe_parse_array(data, [])
                if (len(data_eval) < 3):
                    return False, None
                val = set()
                if bool(data_eval[0]):
                    val.add("VERT")
                if bool(data_eval[1]):
                    val.add("EDGE")
                if bool(data_eval[2]):
                    val.add("FACE")
            elif (from_type == "SELECTION_TYPE"):
                val = data
        return True, val
    except (TypeError, ValueError, IndexError, KeyError):
        return False, None

def selection_type_to_string(sel_type):
    out = []
    if "VERT" in sel_type:
        out.append("Vertex")

    if "EDGE" in sel_type:
        out.append("Edge")

    if "FACE" in sel_type:
        out.append("Face")

    return " + ".join(out)
