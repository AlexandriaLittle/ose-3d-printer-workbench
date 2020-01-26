import FreeCAD as App
import FreeCADGui as Gui


class ThreeDimensionalPrinterWorkbench(Gui.Workbench):
    """
    3D Printer Workbench
    """

    def __init__(self):
        from ose3dprinter_workbench import get_resource_path

        self.__class__.MenuText = 'OSE 3D Printer'
        self.__class__.ToolTip = \
            'A workbench for designing 3D printers by Open Source Ecology'
        self.__class__.Icon = get_resource_path('Frame.svg')

    def Initialize(self):
        """
        Executed when FreeCAD starts
        """
        from ose3dprinter_workbench import main_toolbar

        self.appendToolbar(main_toolbar.name, main_toolbar.keys)

    def Activated(self):
        """
        Executed when workbench is activated.
        """
        if not(App.ActiveDocument):
            App.newDocument()

    def Deactivated(self):
        """
        Executed when workbench is deactivated.
        """
        pass

    def GetClassName(self):
        return 'Gui::PythonWorkbench'


Gui.addWorkbench(ThreeDimensionalPrinterWorkbench())
