
class OutputMixin():

    def dataReceived(self, data):
        text = '\n'.join(data)
        self.infoa.setText(text)
        if len(data) > 0:
            self.warning(text)
        else:
            self.warning()

