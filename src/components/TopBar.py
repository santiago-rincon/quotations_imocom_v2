from flet import AppBar, IconButton, Icons, FontWeight, TextStyle, ThemeMode


class TopBar(AppBar):
    def __init__(self, title: str):
        super().__init__()
        self.title = title
        self.actions = [
            IconButton(
                icon=None,
                icon_color="blue400",
                icon_size=20,
                tooltip="Cambiar apariencia",
                on_click=lambda _: self._change_appearance(),
            )
        ]
        self.title_text_style = TextStyle(
            size=24, weight=FontWeight.BOLD, color="onSurfaceVariant")
        self.bgcolor = "outlineVariant"

    def build(self):
        self._change_icon()
        return AppBar(
            title=self.title,
            actions=self.actions,
            title_text_style=self.title_text_style,
            bgcolor=self.bgcolor
        )

    def _change_appearance(self):
        current_theme = self.page.theme_mode.value

        if current_theme == "system":
            current_theme = self.page.platform_brightness.value

        if current_theme == "light":
            self.page.theme_mode = ThemeMode.DARK
            self._change_icon("dark")

        else:
            self.page.theme_mode = ThemeMode.LIGHT
            self._change_icon("light")

    def _change_icon(self, current_theme=None):
        if not current_theme:
            current_theme = self.page.theme_mode.value

        if current_theme == "system":
            current_theme = self.page.platform_brightness.value

        if current_theme == "light":
            self.actions[0].icon = Icons.NIGHTLIGHT_ROUND_OUTLINED
        else:
            self.actions[0].icon = Icons.LIGHT_MODE_OUTLINED

        self.page.update()
