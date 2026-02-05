import bpy
import math

from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import safe_parse_array

class ScReverseArray(Node, ScNode):
    bl_idname = "ScReverseArray"
    bl_label = "Reverse Array"

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketArray", "Array")
        self.outputs.new("ScNodeSocketArray", "New Array")

    def post_execute(self):
        out = {}
        arr = safe_parse_array(self.inputs["Array"].default_value, [])
        arr.reverse()
        out["New Array"] = repr(arr)
        return out
