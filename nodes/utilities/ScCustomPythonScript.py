import bpy
import math

from bpy.props import IntProperty, StringProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import print_log

class ScCustomPythonScript(Node, ScNode):
    bl_idname = "ScCustomPythonScript"
    bl_label = "Custom Python Script"

    prop_allow_execution: BoolProperty(
        name="Allow Execution",
        description="Run the custom Python script during node execution",
        default=False,
        update=ScNode.update_value
    )
    in_script: StringProperty(default="print('Hello')", update=ScNode.update_value)
    in_iteration: IntProperty(default=1, min=1, soft_max=50, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketUniversal", "In")
        self.inputs.new("ScNodeSocketString", "Script").init("in_script", True)
        self.inputs.new("ScNodeSocketNumber", "Repeat").init("in_iteration")
        self.outputs.new("ScNodeSocketUniversal", "Out")

    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, "prop_allow_execution", text="Allow Script Execution")
        if (not self.prop_allow_execution):
            layout.label(text="Script execution is disabled", icon='ERROR')
    
    def error_condition(self):
        return (
            (not self.prop_allow_execution)
            or
            int(self.inputs["Repeat"].default_value) < 1
        )
    
    def pre_execute(self):
        print_log(self.name, None, None, self.inputs["Script"].default_value)
    
    def functionality(self):
        _C = bpy.context
        _D = bpy.data
        _O = bpy.ops
        _S = _C.scene
        _N = self
        _NT = self.id_data
        if not hasattr(_NT, "variables"):
            _NT.variables = {}
        _VAR = _NT.variables
        _IN = self.inputs["In"].default_value
        for i in range(0, int(self.inputs["Repeat"].default_value)):
            exec(self.inputs["Script"].default_value)

    def post_execute(self):
        return {"Out": self.inputs["In"].default_value}
