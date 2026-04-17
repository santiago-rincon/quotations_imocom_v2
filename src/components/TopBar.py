import flet as ft


class TopBar(ft.AppBar):
    def __init__(self, title: str):
        super().__init__()
        self.title = title
        self.actions = [
            ft.IconButton(
                icon=None,
                icon_color="blue400",
                icon_size=20,
                tooltip="Cambiar apariencia",
                on_click=lambda _: self._change_appearance(),
            )
        ]
        self.title_text_style = ft.TextStyle(
            size=24, weight=ft.FontWeight.BOLD, color="onSurfaceVariant"
        )
        self.bgcolor = "outlineVariant"

    def build(self):
        self._change_icon()
        return ft.AppBar(
            title=self.title,
            actions=self.actions,
            title_text_style=self.title_text_style,
            bgcolor=self.bgcolor,
        )

    def _change_appearance(self):
        current_theme = self.page.theme_mode.value

        if current_theme == "system":
            current_theme = self.page.platform_brightness.value

        if current_theme == "light":
            self.page.theme_mode = ft.ThemeMode.DARK
            self._change_icon("dark")

        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self._change_icon("light")

    def _change_icon(self, current_theme=None):
        if not current_theme:
            current_theme = self.page.theme_mode.value

        if current_theme == "system":
            current_theme = self.page.platform_brightness.value

        if current_theme == "light":
            self.actions[0].icon = ft.Icons.NIGHTLIGHT_ROUND_OUTLINED
        else:
            self.actions[0].icon = ft.Icons.LIGHT_MODE_OUTLINED

        self.page.update()
