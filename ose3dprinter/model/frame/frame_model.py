from FreeCAD import Placement, Vector
from ose3dprinter.part import (AngledBarFrame, AngleFrameConnector,
                                   CNCCutFrame)
from osecore.app.model import Model

from .get_face_side import get_face_side
from .get_faces_for_side import get_faces_for_side
from .get_outer_faces import get_outer_faces


class FrameModel(Model):
    """
    Encapsulates the data (i.e. topography and shape) for a Frame,
    and is separate from the "view" or GUI representation.

    See D3D Frame on the Open Source Ecology Wiki:
    https://wiki.opensourceecology.org/wiki/D3D_Frame
    """

    Type = 'OSEFrame'

    def __init__(self,
                 obj,
                 size=304.8,  # 12 inches
                 width=38.1,  # 1.5 inches
                 thickness=3.175,  # 1/8 inch
                 has_corners=False,
                 placement=Placement(),
                 origin_translation_offset=Vector()):
        super(FrameModel, self).__init__(obj)

        # Size property
        size_tooltip = 'Size or dimension of cubic frame.'
        obj.addProperty('App::PropertyLength', 'Size', 'Base', size_tooltip)
        obj.Size = size

        # Width property
        width_tooltip = 'Width of frame.'
        obj.addProperty('App::PropertyLength', 'Width', 'Base', width_tooltip)
        obj.Width = width

        # Thickness property
        thickness_tooltip = 'Thickness of frame.'
        obj.addProperty('App::PropertyLength', 'Thickness',
                        'Base', thickness_tooltip)
        obj.Thickness = thickness

        # HasCorners property
        has_corners_tooltip = 'Whether the frame has 3d printed corners or not.'
        obj.addProperty('App::PropertyBool', 'HasCorners',
                        'Base', has_corners_tooltip)
        obj.HasCorners = has_corners

    def execute(self, obj):
        """
        Called on document recompute
        """
        side = obj.Size.Value
        # Width of 12" (304.8 mm) frame is 1" (25.4 mm)
        width = obj.Width.Value
        sheet_thickness = obj.Thickness.Value

        Frame = AngledBarFrame if obj.HasCorners else CNCCutFrame

        obj.Shape = Frame.make(side, width, sheet_thickness)

    @property
    def distance_between_axis_side_mount_holes(self):
        d = AngleFrameConnector.distance_between_axis_side_mount_holes_and_frame()
        return self.Object.Size.Value + (d * 2)

    @property
    def XMin(self):
        x_min = self.Object.Shape.BoundBox.XMin
        if self.Object.HasCorners:
            return x_min + AngleFrameConnector.axis_side_mount_width
        else:
            return x_min

    @property
    def XMax(self):
        x_min = self.Object.Shape.BoundBox.XMax
        if self.Object.HasCorners:
            return x_min - AngleFrameConnector.axis_side_mount_width
        else:
            return x_min

    @property
    def YMin(self):
        y_min = self.Object.Shape.BoundBox.YMin
        if self.Object.HasCorners:
            return y_min + \
                AngleFrameConnector.calculate_y_axis_overhang_distance()
        else:
            return y_min

    @property
    def YMax(self):
        y_max = self.Object.Shape.BoundBox.YMax
        if self.Object.HasCorners:
            return y_max - \
                AngleFrameConnector.calculate_y_axis_overhang_distance()
        else:
            return y_max

    @property
    def ZMin(self):
        return self.Object.Shape.BoundBox.ZMin

    @property
    def ZMax(self):
        return self.Object.Shape.BoundBox.ZMax

    def get_face_side(self, face, axis_orientation):
        return get_face_side(self.Object, face, axis_orientation)

    def get_faces_for_side(self, side):
        return get_faces_for_side(self.Object, side)

    def get_outer_faces(self):
        return get_outer_faces(self.Object)

    def __getstate__(self):
        return self.Type

    def __setstate__(self, state):
        if state:
            self.Type = state