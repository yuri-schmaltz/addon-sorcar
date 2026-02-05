import bpy
import math

from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import safe_parse_array

class ScAddArray(Node, ScNode):
    bl_idname = "ScAddArray"
    bl_label = "Add Array"

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketArray", "Array")
        self.inputs.new("ScNodeSocketArray", "Secondary Array")
        self.outputs.new("ScNodeSocketArray", "New Array")

    def post_execute(self):
        out = {}
        arr = safe_parse_array(self.inputs["Array"].default_value, [])
        arr.extend(safe_parse_array(self.inputs["Secondary Array"].default_value, []))
        out["New Array"] = repr(arr)
        return out
