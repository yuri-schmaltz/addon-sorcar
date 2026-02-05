import bpy

from bpy.props import IntProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import safe_parse_array

class ScGetElement(Node, ScNode):
    bl_idname = "ScGetElement"
    bl_label = "Get Element"
    
    in_index: IntProperty(update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketArray", "Array")
        self.inputs.new("ScNodeSocketNumber", "Index").init("in_index", True)
        self.outputs.new("ScNodeSocketUniversal", "Element")
    
    def post_execute(self):
        out = {}
        arr = safe_parse_array(self.inputs["Array"].default_value, [])
        try:
            out["Element"] = repr(arr[int(self.inputs["Index"].default_value)])
        except (TypeError, ValueError, IndexError):
            out["Element"] = None
        return out
