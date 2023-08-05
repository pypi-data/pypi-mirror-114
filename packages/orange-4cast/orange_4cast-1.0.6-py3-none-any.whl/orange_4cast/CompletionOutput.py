
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets import gui
from Orange.data import Domain, ContinuousVariable, StringVariable

from orange_4cast.RpcClient import RpcClient
from orange_4cast.InputMixin import InputMixin
from orange_4cast.OutputMixin import OutputMixin
from orange_4cast.utils import rowToDict, tableToDictionary


class CompletionOutput(OWWidget, RpcClient, OutputMixin, InputMixin):
    name = "Completion Data Output"
    description = "Send completion data to 4Cast application"
    icon = "icons/completionOutput.svg"
    priority = 100
    want_main_area = False

    class Inputs:
        data = Input("Completion table", Orange.data.Table, default=True)


    def __init__(self):
        OWWidget.__init__(self)
        RpcClient.__init__(self)
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(box, "No data on input yet, waiting to get something.")
        self.infob = gui.widgetLabel(box, "")

    @Inputs.data
    def set_data(self, dataset):
        if dataset is not None:
            self.infoa.setText("%d instances in input data set" % len(dataset))
            self.requestData("setCompletions", self.dataReceived, tableToDictionary(dataset))
        else:
            self.infoa.setText("No data on input yet, waiting to get something.")




if __name__ == "__main__":
    WidgetPreview(CompletionInput).run()
