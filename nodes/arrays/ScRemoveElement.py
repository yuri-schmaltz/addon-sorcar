import bpy
import math

from bpy.props import IntProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import safe_parse_array

class ScRemoveElement(Node, ScNode):
    bl_idname = "ScRemoveElement"
    bl_label = "Remove Element"

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketArray", "Array")
        self.inputs.new("ScNodeSocketUniversal", "Element")
        self.outputs.new("ScNodeSocketArray", "New Array")

    def post_execute(self):
        out = {}
        arr = safe_parse_array(self.inputs["Array"].default_value, [])
        try:
            arr.remove(self.inputs["Element"].default_value)
        except ValueError:
            pass
        out["New Array"] = repr(arr)
        return out
