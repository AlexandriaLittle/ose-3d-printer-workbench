import FreeCAD as App
from ose3dprinter.gui.part_feature import create_frame
from ose3dprinter.gui.icon import get_icon_path


class AddFrameCommand:
    """
    Command to add Frame object.
    """

    NAME = 'AddFrame'

    def Activated(self):
        document = App.ActiveDocument
        if not document:
            document = App.newDocument()
        create_frame(document, 'Frame')
        document.recompute()

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            'Pixmap': get_icon_path('Frame.svg'),
            'MenuText': 'Add Frame',
            'ToolTip': 'Add Frame'
        }