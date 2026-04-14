from flet import (
    Container,
    Text,
    FontWeight,
    Column,
)


class SettingsView(Container):
    def __init__(self):
        super().__init__()
        self.text = Text("Configuración", size=20, weight=FontWeight.BOLD)
        self.content = Column(
            controls=[self.text],
            expand=True,
            spacing=20,
        )

    def build(self):
        return Container(content=self.content, expand=True)
