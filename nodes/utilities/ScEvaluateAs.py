import bpy

from bpy.types import Node
from mathutils import Vector
from .._base.node_base import ScNode
from ...helper import safe_literal_eval, resolve_data_reference

class ScEvaluateAs(Node, ScNode):
    bl_idname = "ScEvaluateAs"
    bl_label = "Evaluate As"

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketUniversal", "Element")
        self.outputs.new("ScNodeSocketArray", "As Array")
        self.outputs.new("ScNodeSocketBool", "As Bool")
        self.outputs.new("ScNodeSocketCurve", "As Curve")
        self.outputs.new("ScNodeSocketNumber", "As Float")
        self.outputs.new("ScNodeSocketNumber", "As Int")
        self.outputs.new("ScNodeSocketObject", "As Object")
        self.outputs.new("ScNodeSocketString", "As String")
        self.outputs.new("ScNodeSocketVector", "As Vector")
    
    def error_condition(self):
        return (self.inputs["Element"].default_value == None)
    
    def post_execute(self):
        out = {}
        raw = self.inputs["Element"].default_value
        value = safe_literal_eval(raw, raw)
        if isinstance(value, str):
            ref = resolve_data_reference(value)
            if (ref is not None):
                value = ref
        try:
            out["As Array"] = repr(list(value))
        except (TypeError, ValueError):
            out["As Array"] = "[]"
        try:
            out["As Bool"] = bool(value)
        except (TypeError, ValueError):
            out["As Bool"] = False
        try:
            out["As Curve"] = bpy.data.objects.get(value.name)
        except AttributeError:
            out["As Curve"] = None
        try:
            out["As Float"] = float(value)
        except (TypeError, ValueError):
            out["As Float"] = 0.0
        try:
            out["As Int"] = int(value)
        except (TypeError, ValueError):
            out["As Int"] = 0
        try:
            out["As Object"] = bpy.data.objects.get(value.name)
        except AttributeError:
            out["As Object"] = None
        try:
            out["As String"] = str(value)
        except (TypeError, ValueError):
            out["As String"] = ""
        try:
            out["As Vector"] = Vector(value).to_tuple()
        except (TypeError, ValueError):
            out["As Vector"] = (0, 0, 0)
        return out
