
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
    name = "MVA Points Data Input"
    description = "Retreive MVA Pseudo Points from selected DataModel in the active tab of locally running 4Cast application"
    icon = "icons/mvaPointsInput.svg"
    priority = 20
    predefinedColumns = []
    want_main_area = False

    domainVars = list(map(lambda col: ContinuousVariable.make(col), predefinedColumns))
    domainMetas = []
    predefinedDomain = Domain(domainVars, metas = domainMetas)


    class Outputs:
        data = Output("Pseudo Points", Orange.data.Table)
        predicted = Output("Target Prediction", Orange.data.Table)

    def __init__(self):
        OWWidget.__init__(self)
        RpcClient.__init__(self)
        InputMixin.__init__(self)
        gui.button(self.controlArea, self, "Update", callback=self.update)
        self.update()

    def pseudoPointsReceived(self, data):
        self.dataReceived(data)
        self.requestData("getPseudoPointsPrediction", partial(self.dataReceived, output="predicted"))

    def update(self):
        self.requestData("getPseudoPoints", self.pseudoPointsReceived)
        

if __name__ == "__main__":
    WidgetPreview(PseudoPointsInput).run()
