import bpy
import base64
import pickle
import numpy

from bpy.props import EnumProperty, FloatProperty, IntProperty, BoolProperty, StringProperty
from bpy.types import Node
from .._base.node_base import ScNode
from numpy import array, uint32

class ScNumber(Node, ScNode):
    bl_idname = "ScNumber"
    bl_label = "Number"

    prop_type: EnumProperty(name="Type", items=[("FLOAT", "Float", ""), ("INT", "Integer", ""), ("ANGLE", "Angle", "")], default="FLOAT", update=ScNode.update_value)
    prop_float: FloatProperty(name="Float", update=ScNode.update_value)
    prop_int: IntProperty(name="Integer", update=ScNode.update_value)
    prop_angle: FloatProperty(name="Angle", unit="ROTATION", update=ScNode.update_value)
    prop_random_state: StringProperty()
    in_random: BoolProperty(update=ScNode.update_value)
    in_seed: IntProperty(min=0, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketBool", "Random").init("in_random", True)
        self.inputs.new("ScNodeSocketNumber", "Seed").init("in_seed")
        self.outputs.new("ScNodeSocketNumber", "Value")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if (not self.inputs["Random"].default_value):
            layout.prop(self, "prop_type", expand=True)
            if (self.prop_type == "FLOAT"):
                layout.prop(self, "prop_float")
            elif (self.prop_type == "INT"):
                layout.prop(self, "prop_int")
            elif (self.prop_type == "ANGLE"):
                layout.prop(self, "prop_angle")
    
    def error_condition(self):
        return (
            super().error_condition()
            or int(self.inputs["Seed"].default_value) < 0
        )
    
    def post_execute(self):
        out = {}
        if (self.inputs["Random"].default_value):
            rs = numpy.random.RandomState(int(self.inputs["Seed"].default_value))
            if (not self.first_time and self.prop_random_state != ""):
                try:
                    state = pickle.loads(base64.b64decode(self.prop_random_state.encode("ascii")))
                    rs.set_state(state)
                except (TypeError, ValueError, pickle.PickleError):
                    pass
            out["Value"] = rs.rand()
            self.prop_random_state = base64.b64encode(pickle.dumps(rs.get_state())).decode("ascii")
        else:
            if (self.prop_type == "FLOAT"):
                out["Value"] = self.prop_float
            elif (self.prop_type == "INT"):
                out["Value"] = self.prop_int
            elif (self.prop_type == "ANGLE"):
                out["Value"] = self.prop_angle
        return out
