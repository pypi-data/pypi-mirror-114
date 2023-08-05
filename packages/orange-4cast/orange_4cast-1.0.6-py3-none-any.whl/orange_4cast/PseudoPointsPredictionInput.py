
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.data import Domain, ContinuousVariable, StringVariable
from functools import partial

import math

from orange_4cast.RpcClient import RpcClient
from orange_4cast.InputMixin import InputMixin


class PseudoPointsInput(OWWidget, RpcClient, InputMixin):
    name = "MVA Points Prediction Input"
    description = "Retreive target prediction for MVA Pseudo Points from selected DataModel in the active tab of locally running 4Cast application"
    icon = "icons/mvaPointsPredictionInput.svg"
    priority = 20
    predefinedColumns = []
    want_main_area = False

    domainVars = list(map(lambda col: ContinuousVariable.make(col), predefinedColumns))
    domainMetas = []
    predefinedDomain = Domain(domainVars, metas = domainMetas)


    class Outputs:
        data = Output("Target Prediction", Orange.data.Table)

    def __init__(self):
        OWWidget.__init__(self)
        RpcClient.__init__(self)
        InputMixin.__init__(self)
        gui.button(self.controlArea, self, "Update", callback=self.update)
        self.update()


    def update(self):
        self.requestData("getPseudoPointsPrediction", self.dataReceived)
        

if __name__ == "__main__":
    WidgetPreview(PseudoPointsInput).run()
