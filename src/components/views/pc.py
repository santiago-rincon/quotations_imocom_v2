from flet import Container, Text


class PcView(Container):
    def __init__(self):
        super().__init__()
        self.content = Text("Pc View")

    def build(self):
        return Container(
            content=self.content
        )
