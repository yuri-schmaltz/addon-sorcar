import bpy

from bpy.props import StringProperty
from bpy.types import NodeSocket
from ._base.socket_base import ScNodeSocket
from ..nodes._base.node_base import ScNode
from ..helper import safe_parse_array

class ScNodeSocketArray(NodeSocket, ScNodeSocket):
    bl_idname = "ScNodeSocketArray"
    bl_label = "Array"
    color = (0.0, 0.0, 1.0, 1.0)

    default_value: StringProperty(default="[]")
    default_value_update: StringProperty(default="[]", update=ScNode.update_value)
    default_type: StringProperty(default="ARRAY")

    def get_label(self):
        arr = safe_parse_array(self.default_value, None)
        if (arr is None):
            return "0"
        return str(len(arr))
    
    def draw(self, context, layout, node, text):
        if (self.is_output or self.is_linked):
            layout.label(text=text + " [" + self.get_label() + "]")
        else:
            layout.label(text=text)
