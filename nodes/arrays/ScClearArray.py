import bpy
import math

from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import safe_parse_array

class ScClearArray(Node, ScNode):
    bl_idname = "ScClearArray"
    bl_label = "Clear Array"

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketArray", "Array")
        self.outputs.new("ScNodeSocketArray", "Empty Array")

    def post_execute(self):
        out = {}
        arr = safe_parse_array(self.inputs["Array"].default_value, [])
        arr.clear()
        out["Empty Array"] = repr(arr)
        return out
